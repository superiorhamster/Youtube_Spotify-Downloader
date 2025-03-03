import yt_dlp
import subprocess
import os

import yt_dlp
import subprocess
import os
import time
from threading import Thread

class SpotAudDownloader:
    """A class to download tracks, albums, and playlists using spotDL."""

    def __init__(self, save_path="downloads"):
        """Initialize the downloader with a save path."""
        self.save_path = os.path.abspath(save_path)  # Get absolute path
        os.makedirs(self.save_path, exist_ok=True)  # Ensure the directory exists
        self.progress = 0  # Placeholder progress for spotDL
        self.downloading = False  # Flag to track if download is in progress

    def simulate_progress(self):
        """Simulate progress for spotDL downloads."""
        self.progress = 0
        self.downloading = True
        while self.downloading and self.progress < 100:
            time.sleep(1)  # Simulate progress every second
            self.progress += 10  # Increment progress by 10% (placeholder)
        self.progress = 100  # Ensure progress reaches 100% when done

    def download(self, url, content_type):
        """Downloads content using spotDL based on the provided URL and type."""
        output_path = os.path.join(self.save_path, "{title} - {artist}.{ext}")  # spotDL uses this format
        try:
            # Start progress simulation in a separate thread
            progress_thread = Thread(target=self.simulate_progress)
            progress_thread.start()

            # Run spotDL download
            subprocess.run(f'spotdl {url} --output "{output_path}"', shell=True, check=True)
            self.downloading = False  # Stop progress simulation
            print(f"Downloaded {content_type}: {url} to {self.save_path}")
        except subprocess.CalledProcessError as e:
            self.downloading = False  # Stop progress simulation
            print(f"Failed to download {content_type}: {url}. Error: {e}")

    def get_progress(self):
        """Returns the current download progress."""
        return self.progress

    def download_track(self, url):
        """Downloads a track using spotDL."""
        self.download(url, "track")

    def download_album(self, url):
        """Downloads an album using spotDL."""
        self.download(url, "album")

    def download_playlist(self, url):
        """Downloads a playlist using spotDL."""
        self.download(url, "playlist")
        

class YTAudDownloader:
    def __init__(self, url, save_path):
        self.url = url
        self.save_path = save_path
        self.progress = 0  # Track download progress
        self.ydl_opts = {
            'format': 'bestaudio/best',  # Download best audio
            'outtmpl': f'{self.save_path}/%(title)s.mp3',
            'progress_hooks': [self.progress_hook],  # Add progress hook
        }

    def progress_hook(self, d):
        """Hook function to update progress."""
        if d['status'] == 'downloading':
            total_bytes = d.get('total_bytes') or d.get('total_bytes_estimate')
            downloaded_bytes = d['downloaded_bytes']
            if total_bytes:
                self.progress = int((downloaded_bytes / total_bytes) * 100)
                print(f"Download Progress: {self.progress}%")  # For debugging

    def get_progress(self):
        """Returns the current download progress."""
        return self.progress

    def download(self):
        with yt_dlp.YoutubeDL(self.ydl_opts) as ydl:
            ydl.download([self.url])
        print('Download Complete!')