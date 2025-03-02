import tkinter as tk
from tkinter import simpledialog, filedialog, messagebox
from VidDownloader import VidDownloader
from AudDownloader import YTAudDownloader, SpotAudDownloader
import threading

# Global variable to store the default save path
DEFAULT_SAVE_PATH = None

def show_main_menu():
    clear_window()
    tk.Button(root, text="Download Video", command=show_video_options).pack()
    tk.Button(root, text="Download Audio", command=show_audio_options).pack()
    tk.Button(root, text="Set Default Save Path", command=set_default_save_path).pack()
    tk.Button(root, text="Exit", command=root.quit).pack()

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

def set_default_save_path():
    global DEFAULT_SAVE_PATH
    DEFAULT_SAVE_PATH = filedialog.askdirectory(title="Select Default Save Folder")
    if DEFAULT_SAVE_PATH:
        messagebox.showinfo("Success", f"Default save path set to: {DEFAULT_SAVE_PATH}")
    else:
        messagebox.showerror("Error", "No folder selected. Default save path not updated.")

def get_save_path():
    """Returns the default save path if set, otherwise prompts the user to select one."""
    global DEFAULT_SAVE_PATH
    if DEFAULT_SAVE_PATH:
        return DEFAULT_SAVE_PATH
    else:
        save_path = filedialog.askdirectory(title="Select Save Folder")
        if save_path:
            return save_path
        else:
            messagebox.showerror("Error", "No save path selected. Operation cancelled.")
            return None

def show_progress_window(downloader, content_type):
    """Creates a new window to show download progress."""
    progress_window = tk.Toplevel(root)
    progress_window.title(f"Downloading {content_type}")
    progress_window.geometry("300x100")

    progress_label = tk.Label(progress_window, text="Download Progress: 0%")
    progress_label.pack(pady=20)

    def update_progress():
        """Updates the progress label with the current download progress."""
        progress = downloader.get_progress()
        progress_label.config(text=f"Download Progress: {progress}%")
        if progress < 100:
            progress_window.after(1000, update_progress)  # Update every 1 second
        else:
            progress_window.destroy()  # Close the progress window when done
            messagebox.showinfo("Success", f"{content_type} downloaded successfully")

    # Start updating the progress
    progress_window.after(1000, update_progress)

def download_in_thread(downloader, content_type):
    """Runs the download process in a separate thread."""
    try:
        downloader.download()
    except Exception as e:
        messagebox.showerror("Error", f"Failed to download {content_type}: {e}")

def download_single_video():
    url = simpledialog.askstring("Input", "Enter the video URL:")
    if not url:
        messagebox.showerror("Error", "Please enter a URL.")
        return

    save_path = get_save_path()
    if not save_path:
        return

    downloader = VidDownloader(url, save_path)
    show_progress_window(downloader, "Video")

    # Run the download in a separate thread
    threading.Thread(target=download_in_thread, args=(downloader, "Video")).start()

def download_playlist():
    url = simpledialog.askstring("Input", "Enter the playlist URL:")
    if not url:
        messagebox.showerror("Error", "Please enter a URL.")
        return

    save_path = get_save_path()
    if not save_path:
        return

    downloader = VidDownloader(url, save_path)
    show_progress_window(downloader, "Playlist")

    # Run the download in a separate thread
    threading.Thread(target=download_in_thread, args=(downloader, "Playlist")).start()

def download_multiple_videos():
    urls = simpledialog.askstring("Input", "Enter the video URLs separated by commas:")
    if not urls:
        messagebox.showerror("Error", "Please enter URLs.")
        return
    urls = urls.split(',')

    save_path = get_save_path()
    if not save_path:
        return

    for url in urls:
        downloader = VidDownloader(url.strip(), save_path)
        show_progress_window(downloader, "Video")

        # Run the download in a separate thread
        threading.Thread(target=download_in_thread, args=(downloader, "Video")).start()

def download_audio(platform):
    url = simpledialog.askstring("Input", "Enter the audio URL:")
    if not url:
        messagebox.showerror("Error", "Please enter a URL.")
        return

    save_path = get_save_path()
    if not save_path:
        return

    if platform == 1:
        downloader = YTAudDownloader(url, save_path)
        content_type = "YouTube Audio"
    elif platform == 2:
        downloader = SpotAudDownloader(save_path)
        type = url.split('/')[-2]
        if type == "track":
            downloader.download_track(url)
            content_type = "Spotify Track"
        elif type == "album":
            downloader.download_album(url)
            content_type = "Spotify Album"
        elif type == "playlist":
            downloader.download_playlist(url)
            content_type = "Spotify Playlist"
        else:
            messagebox.showerror("Error", "Invalid Spotify URL type")
            return
    else:
        messagebox.showerror("Error", "Please select a valid platform")
        return

    show_progress_window(downloader, content_type)

    # Run the download in a separate thread
    threading.Thread(target=download_in_thread, args=(downloader, content_type)).start()

# GUI Setup
root = tk.Tk()
root.title("Downloader UI")
root.geometry("480x320")

show_main_menu()
root.mainloop()