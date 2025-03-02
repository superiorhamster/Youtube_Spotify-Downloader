from VidDownloader import VidDownloader
from AudDownloader import YTAudDownloader, SpotAudDownloader
if __name__ == "__main__":
    choice = int(input("Enter 1 for downloading video, 2 for downloading audio: "))
    if choice == 1:
        vid_down = int(input("Enter 1 for downloading a single video, 2 for downloading a playlist, 3 for downloading multiple videos: "))
        save_path = "D:/YTdown"  # Or get this from the user

        if vid_down == 1:
            url = input("Enter the video URL: ")
            downloader = VidDownloader(url, save_path)
            downloader.download()
        elif vid_down == 2:
            url = input("Enter the playlist URL: ")
            downloader = VidDownloader(url, save_path)
            downloader.download()  # yt_dlp handles playlists automatically
        elif vid_down == 3:
            urls = input("Enter the video URLs separated by commas: ").split(',')
            for url in urls:
                downloader = VidDownloader(url, save_path)
                downloader.download()
        else:
            print("Invalid choice!")
    elif choice == 2:
        platform = int(input("Enter 1 for YouTube, 2 for Spotify: "))
        
        if platform == 1:  
            url = input("Enter the YouTube URL: ")
            save_path = "D:/YTdown"
            downloader = YTAudDownloader(url, save_path)
            downloader.download()
        elif platform == 2:
            url = input("Enter the Spotify URL: ")
            save_path = "D:/YTdown"
            downloader = SpotAudDownloader(save_path)
            type = url.split('/')[-2]
            print(type)
            downloader.download(url, type)
    else:
        print("Invalid choice!")