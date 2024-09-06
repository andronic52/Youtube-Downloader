import pygame
import os
import yt_dlp
from sys import exit
import threading

pygame.init()
pygame.mixer.init()

screen = pygame.display.set_mode((700, 400))
pygame.display.set_caption('Yt Downloader')
clock = pygame.time.Clock()
slide = 1
last_hover_time = 0
hover_cooldown = 200

error_displayed = False

button_hovered = {'audio': False, 'video': False, 'both': False}

click_sound = pygame.mixer.Sound('../Youtube Downloader/Assets/Audio/interface-12-204786.mp3')
hover_sound = pygame.mixer.Sound('../Youtube Downloader/Assets/Audio/touchpad-click-158339.mp3')
downloading_sound = pygame.mixer.Sound('../Youtube Downloader/Assets/Audio/oldcomputerbootingup-16979.mp3')
success_sound = pygame.mixer.Sound('../Youtube Downloader/Assets/Audio/success-fanfare-trumpets-6185.mp3')
error_sound = pygame.mixer.Sound('../Youtube Downloader/Assets/Audio/funny-laughing-sound-effect-205565.mp3')

# URL to download
url = "https://youtu.be/pLlW1S9rw0w?si=Z_4wzgfp8wdBK6RW"  # Test URL

# Images
home = pygame.image.load('../Youtube Downloader/Assets/Images/home.png')
audio = pygame.image.load('../Youtube Downloader/Assets/Images/audio.png')
video = pygame.image.load('../Youtube Downloader/Assets/Images/video.png')
both = pygame.image.load('../Youtube Downloader/Assets/Images/both.png')
error = pygame.image.load('../Youtube Downloader/Assets/Images/Error.png')
success_img = pygame.image.load('../Youtube Downloader/Assets/Images/success.png')

# Animation frames
animation_frames = [
    pygame.image.load('../Youtube Downloader/Assets/Images/downloading 1.png'),
    pygame.image.load('../Youtube Downloader/Assets/Images/downloading 2.png'),
    pygame.image.load('../Youtube Downloader/Assets/Images/downloading 3.png'),
    pygame.image.load('../Youtube Downloader/Assets/Images/downloading 4.png')
]
current_frame = 0
last_frame_change_time = 0
frame_delay = 250  # Time delay between frames in milliseconds

# Rectangles
audio_rect = video_rect = both_rect = None

# Global variable to track download state
download_in_progress = False
download_complete = False
download_error = False
success_start_time = 0
error_start_time = 0


def progress_hook(d):
    global download_in_progress, download_complete, download_error

    if d['status'] == 'downloading':
        download_in_progress = True
        download_complete = False
        download_error = False

    elif d['status'] == 'finished':
        download_in_progress = False
        download_complete = True
        download_error = False
        global success_start_time
        success_start_time = pygame.time.get_ticks()

    elif d['status'] == 'error':
        download_in_progress = False
        download_complete = False
        download_error = True
        global error_start_time
        error_start_time = pygame.time.get_ticks()


# Function to show animation with time-based frame switching
def show_loading_animation():
    global current_frame, last_frame_change_time, frame_delay

    # Get the current time
    current_time1 = pygame.time.get_ticks()

    # Check if enough time has passed to switch to the next frame
    if current_time1 - last_frame_change_time > frame_delay:
        current_frame = (current_frame + 1) % len(animation_frames)
        last_frame_change_time = current_time1
        if frame_delay >= 10:
            frame_delay -= 2

    # Draw the current animation frame
    screen.blit(animation_frames[current_frame], (0, 0))


def start_download(ydl_opts):
    global download_in_progress, download_complete, download_error
    download_in_progress = True
    download_complete = False
    download_error = False
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
    except Exception as e:
        download_error = True
        download_in_progress = False


# Main loop
while True:
    key = pygame.key.get_pressed()
    mouse = pygame.mouse.get_pos()
    current_time = pygame.time.get_ticks()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

        # Background
        screen.blit(home, (0, 0))

        # Rectangles for buttons
        if audio_rect is None:
            audio_rect = pygame.Rect(230, 115, 240, 65)
        if video_rect is None:
            video_rect = pygame.Rect(230, 197, 240, 65)
        if both_rect is None:
            both_rect = pygame.Rect(230, 280, 240, 65)

        # Button hover
        if audio_rect.collidepoint(mouse):
            if not button_hovered['audio'] and current_time - last_hover_time > hover_cooldown:
                hover_sound.play()
                last_hover_time = current_time
                button_hovered['audio'] = True
            screen.blit(audio, (0, 0))
        else:
            button_hovered['audio'] = False

        if video_rect.collidepoint(mouse):
            if not button_hovered['video'] and current_time - last_hover_time > hover_cooldown:
                hover_sound.play()
                last_hover_time = current_time
                button_hovered['video'] = True
            screen.blit(video, (0, 0))
        else:
            button_hovered['video'] = False

        if both_rect.collidepoint(mouse):
            if not button_hovered['both'] and current_time - last_hover_time > hover_cooldown:
                hover_sound.play()
                last_hover_time = current_time
                button_hovered['both'] = True
            screen.blit(both, (0, 0))
        else:
            button_hovered['both'] = False

        # Start download when button clicked
        if audio_rect.collidepoint(mouse) and event.type == pygame.MOUSEBUTTONDOWN:
            if current_time - last_hover_time > hover_cooldown:
                click_sound.play()
                last_hover_time = current_time
            slide = 2
            ydl_opts = {
                'outtmpl': os.path.join(os.path.expanduser("~"), "Downloads", '%(title)s.%(ext)s'),
                'format': 'bestaudio/best',
                'postprocessors': [{
                    'key': 'FFmpegExtractAudio',
                    'preferredcodec': 'mp3',
                    'preferredquality': '192',
                }],
                'ffmpeg_location': r'C:\Users\andro\Downloads\ffmpeg-master-latest-win64-gpl\ffmpeg-master-latest-win64-gpl\bin',
                'progress_hooks': [progress_hook]  # Attach progress hook
            }
            threading.Thread(target=start_download, args=(ydl_opts,)).start()

        if video_rect.collidepoint(mouse) and event.type == pygame.MOUSEBUTTONDOWN:
            slide = 2
            if current_time - last_hover_time > hover_cooldown:
                click_sound.play()
                last_hover_time = current_time
            ydl_opts = {
                'outtmpl': os.path.join(os.path.expanduser("~"), "Downloads", '%(title)s.%(ext)s'),
                'format': 'bestvideo[height<=720]',
                'merge_output_format': 'mp4',
                'postprocessors': [{
                    'key': 'FFmpegVideoConvertor',
                    'preferedformat': 'mp4',
                }],
                'ffmpeg_location': r'C:\Users\andro\Downloads\ffmpeg-master-latest-win64-gpl\ffmpeg-master-latest-win64-gpl\bin',
                'progress_hooks': [progress_hook]  # Attach progress hook
            }
            threading.Thread(target=start_download, args=(ydl_opts,)).start()

        if both_rect.collidepoint(mouse) and event.type == pygame.MOUSEBUTTONDOWN:
            slide = 2
            if current_time - last_hover_time > hover_cooldown:
                click_sound.play()
                last_hover_time = current_time
            ydl_opts = {
                'outtmpl': os.path.join(os.path.expanduser("~"), "Downloads", '%(title)s.%(ext)s'),
                'format': 'bestvideo[height<=720]+bestaudio/best',
                'merge_output_format': 'mp4',
                'postprocessors': [{
                    'key': 'FFmpegVideoConvertor',
                    'preferedformat': 'mp4',
                }],
                'ffmpeg_location': r'C:\Users\andro\Downloads\ffmpeg-master-latest-win64-gpl\ffmpeg-master-latest-win64-gpl\bin',
                'progress_hooks': [progress_hook]  # Attach progress hook
            }
            threading.Thread(target=start_download, args=(ydl_opts,)).start()

    # Show animation if download is in progress
    if slide == 2:
        downloading_sound.play()
        show_loading_animation()

        if download_complete:
            downloading_sound.stop()
            success_sound.play()
            screen.blit(success_img, (0, 0))  # Show success image
            if current_time - success_start_time > 3000:
                pygame.quit()
                exit()

        if download_error:
            downloading_sound.stop()
            error_sound.play()
            screen.blit(error, (0, 0))  # Show error image
            if not error_displayed:
                error_displayed = True
                error_start_time = current_time
            if current_time - error_start_time > 5200:
                pygame.quit()
                exit()

    pygame.display.update()
    clock.tick(60)

