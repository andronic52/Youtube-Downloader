import tkinter as tk
from tkinter import ttk, messagebox
import yt_dlp
import os


class DownloadApp:
    def __init__(self, root):
        self.root = root
        self.root.title("YouTube Downloader")
        self.root.geometry("1000x400")  # Set the window size to 600x400 pixels

        # Create a black background Canvas
        self.canvas = tk.Canvas(root)
        self.canvas.pack(fill="both", expand=True)

        # Style for rounded buttons
        style = ttk.Style()
        style.configure("TButton", background="black", foreground="black", font=("Arial", 12), padding=10)
        style.map("TButton", background=[('active', 'blue')])

        # Create and place the choice selection widgets with fixed selection behavior
        self.choice_var = tk.StringVar(value="both")
        self.audio_rb = tk.Radiobutton(self.canvas, text="Audio Only", variable=self.choice_var, value="audio",
                                       bg="grey", fg="white", indicatoron=False, selectcolor="blue", padx=20, pady=10)
        self.video_rb = tk.Radiobutton(self.canvas, text="Video Only", variable=self.choice_var, value="video",
                                       bg="grey", fg="white", indicatoron=False, selectcolor="blue", padx=20, pady=10)
        self.both_rb = tk.Radiobutton(self.canvas, text="Audio and Video", variable=self.choice_var, value="both",
                                      bg="grey", fg="white", indicatoron=False, selectcolor="blue", padx=20, pady=10)

        # Keep the options fixed when selected
        self.audio_rb.pack(pady=5)
        self.video_rb.pack(pady=5)
        self.both_rb.pack(pady=5)

        # Create and place the URL entry widget (small size, about 300px wide)
        self.url_label = tk.Label(self.canvas, text="Enter YouTube URL:", bg="white", fg="black")
        self.url_label.pack(pady=5)

        # Create a smaller entry field (width=40 approximately matches 300px)
        self.url_entry = ttk.Entry(self.canvas, width=40, font=("Arial", 12))
        self.url_entry.pack(pady=5)

        # Create and place the Send button (rounded blue button)
        self.send_button = ttk.Button(self.canvas, text="Send", style="TButton", command=self.process_download)
        self.send_button.pack(pady=10)

    def process_download(self):
        choice = self.choice_var.get()
        url = self.url_entry.get().strip()

        if not url:
            messagebox.showwarning("Input Error", "Please enter a URL.")
            return

        if choice == 'audio':
            ydl_opts = {
                'outtmpl': os.path.join(os.path.expanduser("~"), "Downloads", '%(title)s.%(ext)s'),
                'format': 'bestaudio/best',
                'postprocessors': [{
                    'key': 'FFmpegExtractAudio',
                    'preferredcodec': 'mp3',
                    'preferredquality': '192',
                }],
                'ffmpeg_location': r'C:\Users\andro\Downloads\ffmpeg-master-latest-win64-gpl\ffmpeg-master-latest-win64-gpl\bin',
            }
        elif choice == 'video':
            ydl_opts = {
                'outtmpl': os.path.join(os.path.expanduser("~"), "Downloads", '%(title)s.%(ext)s'),
                'format': 'bestvideo[height<=720]',
                'merge_output_format': 'mp4',
                'postprocessors': [{
                    'key': 'FFmpegVideoConvertor',
                    'preferedformat': 'mp4',
                }],
                'ffmpeg_location': r'C:\Users\andro\Downloads\ffmpeg-master-latest-win64-gpl\ffmpeg-master-latest-win64-gpl\bin',
            }
        elif choice == 'both':
            ydl_opts = {
                'outtmpl': os.path.join(os.path.expanduser("~"), "Downloads", '%(title)s.%(ext)s'),
                'format': 'bestvideo[height<=720]+bestaudio/best',
                'merge_output_format': 'mp4',
                'postprocessors': [{
                    'key': 'FFmpegVideoConvertor',
                    'preferedformat': 'mp4',
                }],
                'ffmpeg_location': r'C:\Users\andro\Downloads\ffmpeg-master-latest-win64-gpl\ffmpeg-master-latest-win64-gpl\bin',
            }
        else:
            messagebox.showerror("Invalid Choice",
                                 "Invalid choice. Please select 'Audio Only', 'Video Only', or 'Audio and Video'.")
            return

        # Download the video or audio based on the user's choice
        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download([url])
            messagebox.showinfo("Success", "Download completed successfully.")
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {str(e)}")


if __name__ == "__main__":
    root = tk.Tk()
    app = DownloadApp(root)
    root.mainloop()
