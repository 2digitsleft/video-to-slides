import os
from pytube import YouTube
from loguru import logger
from config.settings import settings

class VideoDownloader:
    def __init__(self, download_dir=None):
        self.download_dir = download_dir or settings.VIDEO_DIR
        self.download_dir.mkdir(parents=True, exist_ok=True)
    
    def download_from_youtube(self, url: str) -> str:
        """Download video from YouTube URL"""
        try:
            yt = YouTube(url)
            stream = yt.streams.filter(
                file_extension='mp4', 
                progressive=True
            ).first()
            
            if not stream:
                raise ValueError("No suitable stream found")
            
            filepath = stream.download(
                output_path=str(self.download_dir),
                filename=f"{yt.title}.mp4"
            )
            logger.info(f"Downloaded video to {filepath}")
            return filepath
            
        except Exception as e:
            logger.error(f"Failed to download video: {e}")
            raise
