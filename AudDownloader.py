import yt_dlp
import subprocess
import os

class SpotAudDownloader:
    """A class to download tracks, albums, and playlists using spotDL."""
    

    def __init__(self, save_path="downloads"):
        """Initialize the downloader with a save path."""
        self.save_path = os.path.abspath(save_path)  # Get absolute path
        os.makedirs(self.save_path, exist_ok=True)  # Ensure the directory exists

    def download(self, url, content_type):
        """Downloads content using spotDL based on the provided URL and type."""
        output_path = os.path.join(self.save_path, "{title} - {artist}.{ext}")  # spotDL uses this format
        try:
            subprocess.run(f'spotdl {url} --output "{output_path}"', shell=True, check=True)
            print(f"Downloaded {content_type}: {url} to {self.save_path}")
        except subprocess.CalledProcessError as e:
            print(f"Failed to download {content_type}: {url}. Error: {e}")
    
    def print_audio_quality(self, file_path):
        """Prints the audio quality of the downloaded file."""
        try:
            result = subprocess.run(f'ffprobe -i "{file_path}" -show_entries format=bit_rate -v quiet -of csv="p=0"', 
                                   shell=True, capture_output=True, text=True, check=True)
            bit_rate = result.stdout.strip()
            print(f"Audio quality (bit rate): {bit_rate} bps")
        except subprocess.CalledProcessError as e:
            print(f"Failed to retrieve audio quality for {file_path}. Error: {e}")
    
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
        self.ydl_opts = {
            'format': 'bestaudio/best',  # Download best audio
            'outtmpl': f'{self.save_path}/%(title)s.mp3', 
            'progress_hooks': [self.progress_hook],  # Add progress hook
        }

    def progress_hook(self, d):
        if d['status'] == 'downloading':
            total_bytes = d.get('total_bytes') or d.get('total_bytes_estimate')
            downloaded_bytes = d['downloaded_bytes']
            if total_bytes:
                percent = int(downloaded_bytes / total_bytes * 100)
                print(f"Downloading: {percent}%")

    def download(self):
        with yt_dlp.YoutubeDL(self.ydl_opts) as ydl:
            ydl.download([self.url])
        print('Download Complete!')

