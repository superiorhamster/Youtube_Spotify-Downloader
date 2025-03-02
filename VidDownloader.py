import yt_dlp

class VidDownloader:
    def __init__(self, url, save_path, resolution=None):
        self.url = url
        self.save_path = save_path
        self.resolution = resolution
        self.progress = 0
        self.current_video_index = 0
        self.total_videos = 1  # Default to 1 for single video
        self.is_playlist = self._is_playlist(url)  # Check if the URL is a playlist
        if self.is_playlist:
            self.total_videos = self._get_playlist_video_count(url)
        self.ydl_opts = {
            'format': 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best',
            'outtmpl': f'{self.save_path}/%(title)s.mp4',
            'progress_hooks': [self.progress_hook],
        }
        self.current_video_progress = 0  # Track progress for the current video (video + audio)

    def _is_playlist(self, url):
        """Check if the URL is a playlist."""
        with yt_dlp.YoutubeDL() as ydl:
            info = ydl.extract_info(url, download=False)
            return 'entries' in info

    def _get_playlist_video_count(self, url):
        """Get the number of videos in the playlist, excluding unavailable videos."""
        with yt_dlp.YoutubeDL() as ydl:
            info = ydl.extract_info(url, download=False)
            if 'entries' in info:
                # Filter out unavailable videos
                available_videos = [entry for entry in info['entries'] if entry is not None]
                return len(available_videos)
            return 1

    def progress_hook(self, d):
        """Hook function to update progress."""
        if d['status'] == 'downloading':
            total_bytes = d.get('total_bytes') or d.get('total_bytes_estimate')
            downloaded_bytes = d['downloaded_bytes']
            if total_bytes:
                # Calculate progress for the current video (video + audio)
                self.current_video_progress = int((downloaded_bytes / total_bytes) * 100)
                # Calculate overall progress for the entire playlist
                overall_progress = (self.current_video_index * 100 + self.current_video_progress) / self.total_videos
                self.progress = int(overall_progress)
                print(f"Queue ({float((self.current_video_index + 1)/2)}/{self.total_videos}): {self.current_video_progress}%")
        elif d['status'] == 'finished':
            # Only increment the index when both video and audio are fully downloaded
            if self.current_video_progress >= 100:
                self.current_video_index += 1
                self.current_video_progress = 0  # Reset progress for the next video

    def get_progress(self):
        """Returns the current download progress."""
        return self.progress

    def get_available_resolutions(self):
        """Fetch available resolutions for the video."""
        with yt_dlp.YoutubeDL() as ydl:
            info = ydl.extract_info(self.url, download=False)
            formats = info.get('formats', [])
            resolutions = set()
            for f in formats:
                if f.get('height'):
                    resolutions.add(f['height'])
            return sorted(resolutions, reverse=True)

    def download(self):
        """Download the video with the selected resolution."""
        if self.resolution:
            if self.resolution == '720p':
                self.ydl_opts['format'] = 'bestvideo[height<=720]+bestaudio/best[height<=720]'
            elif self.resolution == '1080p':
                self.ydl_opts['format'] = 'bestvideo[height<=1080]+bestaudio/best[height<=1080]'
            elif self.resolution == 'max':
                self.ydl_opts['format'] = 'bestvideo+bestaudio/best'
        else:
            self.ydl_opts['format'] = 'bestvideo+bestaudio/best'  # Default to max resolution

        with yt_dlp.YoutubeDL(self.ydl_opts) as ydl:
            ydl.download([self.url])
        print('Download Complete!')