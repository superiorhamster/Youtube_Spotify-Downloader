import yt_dlp

class VidDownloader:
    def __init__(self, url, save_path):
        self.url = url
        self.save_path = save_path
        self.progress = 0  # Track download progress
        self.ydl_opts = {
            'format': 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best',  # Download best mp4, then best overall
            'outtmpl': f'{self.save_path}/%(title)s.%(ext)s',  # Save with original title
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