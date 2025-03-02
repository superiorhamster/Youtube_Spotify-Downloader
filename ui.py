import tkinter as tk
from tkinter import simpledialog, filedialog, messagebox
from VidDownloader import VidDownloader
from AudDownloader import YTAudDownloader, SpotAudDownloader

def show_main_menu():
    clear_window()
    tk.Button(root, text="Download Video", command=show_video_options).pack()
    tk.Button(root, text="Download Audio", command=show_audio_options).pack()

def show_video_options():
    clear_window()
    tk.Button(root, text="Download Single Video", command=download_single_video).pack()
    tk.Button(root, text="Download Playlist", command=download_playlist).pack()
    tk.Button(root, text="Download Multiple Videos", command=download_multiple_videos).pack()
    tk.Button(root, text="Back", command=show_main_menu).pack()

def show_audio_options():
    clear_window()
    tk.Button(root, text="Download from YouTube", command=lambda: download_audio(1)).pack()
    tk.Button(root, text="Download from Spotify", command=lambda: download_audio(2)).pack()
    tk.Button(root, text="Back", command=show_main_menu).pack()

def clear_window():
    for widget in root.winfo_children():
        widget.destroy()

def download_single_video():
    url = simpledialog.askstring("Input", "Enter the video URL:")
    save_path = filedialog.askdirectory(title="Select Save Folder")
    if not url or not save_path:
        messagebox.showerror("Error", "Please enter a URL and select a save path")
        return
    downloader = VidDownloader(url, save_path)
    downloader.download()
    messagebox.showinfo("Success", "Video downloaded successfully")

def download_playlist():
    url = simpledialog.askstring("Input", "Enter the playlist URL:")
    save_path = filedialog.askdirectory(title="Select Save Folder")
    if not url or not save_path:
        messagebox.showerror("Error", "Please enter a URL and select a save path")
        return
    downloader = VidDownloader(url, save_path)
    downloader.download()
    messagebox.showinfo("Success", "Playlist downloaded successfully")

def download_multiple_videos():
    urls = simpledialog.askstring("Input", "Enter the video URLs separated by commas:")
    if urls:
        urls = urls.split(',')
    save_path = filedialog.askdirectory(title="Select Save Folder")
    if not urls or not save_path:
        messagebox.showerror("Error", "Please enter URLs and select a save path")
        return
    for url in urls:
        downloader = VidDownloader(url.strip(), save_path)
        downloader.download()
    messagebox.showinfo("Success", "All videos downloaded successfully")

def download_audio(platform):
    url = simpledialog.askstring("Input", "Enter the audio URL:")
    save_path = filedialog.askdirectory(title="Select Save Folder")
    if not url or not save_path:
        messagebox.showerror("Error", "Please enter a URL and select a save path")
        return
    
    if platform == 1:
        downloader = YTAudDownloader(url, save_path)
    elif platform == 2:
        downloader = SpotAudDownloader(save_path)
        type = url.split('/')[-2]
        downloader.download(url, type)
    else:
        messagebox.showerror("Error", "Please select a valid platform")
        return
    
    downloader.download()
    messagebox.showinfo("Success", "Audio downloaded successfully")

# GUI Setup
root = tk.Tk()
root.title("Downloader UI")
root.geometry("400x400")

show_main_menu()
root.mainloop()
