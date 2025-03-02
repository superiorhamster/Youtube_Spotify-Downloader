import tkinter as tk
from tkinter import simpledialog, filedialog, messagebox
from VidDownloader import VidDownloader
from AudDownloader import YTAudDownloader, SpotAudDownloader
import threading

# Global variables
DEFAULT_SAVE_PATH = None
AUTO_SAVE_TO_DEFAULT = False  # Default to manual save path selection

def show_main_menu():
    clear_window()
    tk.Button(root, text="Download Video", command=show_video_options).pack()
    tk.Button(root, text="Download Audio", command=show_audio_options).pack()
    tk.Button(root, text="Set Default Save Path", command=set_default_save_path).pack()
    tk.Button(root, text="Toggle Auto-Save to Default", command=toggle_auto_save).pack()
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

def toggle_auto_save():
    global AUTO_SAVE_TO_DEFAULT
    AUTO_SAVE_TO_DEFAULT = not AUTO_SAVE_TO_DEFAULT
    status = "enabled" if AUTO_SAVE_TO_DEFAULT else "disabled"
    messagebox.showinfo("Auto-Save", f"Auto-save to default path is now {status}.")

def get_save_path():
    """Returns the default save path if auto-save is enabled, otherwise prompts the user to select one."""
    global DEFAULT_SAVE_PATH, AUTO_SAVE_TO_DEFAULT
    if AUTO_SAVE_TO_DEFAULT and DEFAULT_SAVE_PATH:
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
        if downloader.is_playlist:
            progress_label.config(text=f"Queue ({downloader.current_video_index + 1}/{downloader.total_videos}): {progress}%")
        else:
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

def choose_resolution(url, save_path):
    """Let the user choose the resolution for the video."""
    downloader = VidDownloader(url, save_path)
    resolutions = downloader.get_available_resolutions()

    if not resolutions:
        messagebox.showerror("Error", "No resolutions found for this video.")
        return None

    # Filter resolutions higher than 720p
    high_resolutions = [r for r in resolutions if r > 720]
    if not high_resolutions:
        # If no high resolutions, default to max
        return 'max'

    # Create a dialog to choose resolution
    resolution_window = tk.Toplevel(root)
    resolution_window.title("Choose Resolution")
    resolution_window.geometry("300x150")

    tk.Label(resolution_window, text="Choose a resolution:").pack(pady=10)

    selected_resolution = tk.StringVar(value='720p')  # Default to 720p

    # Add buttons for 720p, 1080p, and max resolution
    tk.Radiobutton(resolution_window, text="720p", variable=selected_resolution, value='720p').pack()
    if 1080 in resolutions:
        tk.Radiobutton(resolution_window, text="1080p", variable=selected_resolution, value='1080p').pack()
    tk.Radiobutton(resolution_window, text="Max Resolution", variable=selected_resolution, value='max').pack()

    def on_ok():
        resolution_window.destroy()

    tk.Button(resolution_window, text="OK", command=on_ok).pack(pady=10)
    resolution_window.wait_window()  # Wait for the user to make a choice

    return selected_resolution.get()

def download_single_video():
    url = simpledialog.askstring("Input", "Enter the video URL:")
    if not url:
        messagebox.showerror("Error", "Please enter a URL.")
        return

    save_path = get_save_path()
    if not save_path:
        return

    # Let the user choose the resolution
    resolution = choose_resolution(url, save_path)
    if not resolution:
        return

    downloader = VidDownloader(url, save_path, resolution)
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

    downloader = VidDownloader(url, save_path)  # Set is_playlist to True
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
        # Let the user choose the resolution for each video
        resolution = choose_resolution(url.strip(), save_path)
        if not resolution:
            continue

        downloader = VidDownloader(url.strip(), save_path, resolution)
        show_progress_window(downloader, "Video")

        # Run the download in a separate thread
        threading.Thread(target=download_in_thread, args=(downloader, "Video")).start()

# GUI Setup
root = tk.Tk()
root.title("Downloader UI")
root.geometry("480x320")

show_main_menu()
root.mainloop()