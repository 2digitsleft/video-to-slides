from typing import List
from pathlib import Path
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
from tqdm import tqdm
from loguru import logger
from colorama import Fore, Style
from .auth_manager import AuthManager
from src.core.exceptions import GoogleAPIError

class GoogleDriveService:
    def __init__(self):
        self.creds = AuthManager.get_credentials()
        self.service = build('drive', 'v3', credentials=self.creds)
    
    def upload_images(self, image_files: List[str], folder_id: str) -> List[str]:
        """Upload images to Google Drive and return URLs"""
        file_urls = []
        
        logger.info(f"{Fore.CYAN}☁️  Starting upload to Google Drive ({len(image_files)} files)")
        
        pbar = tqdm(image_files, 
                   desc=f"{Fore.BLUE}📤 Uploading to Drive", 
                   unit="files",
                   bar_format='{desc}: {percentage:3.0f}%|{bar}| {n_fmt}/{total_fmt} [{elapsed}<{remaining}] {postfix}')
        
        for i, image_file in enumerate(pbar, 1):
            try:
                file_metadata = {
                    'name': Path(image_file).name,
                    'parents': [folder_id],
                    'mimeType': 'image/png'
                }
                
                media = MediaFileUpload(image_file, mimetype='image/png')
                file = self.service.files().create(
                    body=file_metadata,
                    media_body=media,
                    fields='id'
                ).execute()
                
                # Make file publicly accessible
                self.service.permissions().create(
                    fileId=file['id'],
                    body={'type': 'anyone', 'role': 'reader'}
                ).execute()
                
                file_urls.append(f"https://drive.google.com/file/d/{file['id']}/view")
                
                # Update progress with current file info
                pbar.set_postfix({
                    'current': Path(image_file).name,
                    'uploaded': i
                })
                
            except Exception as e:
                pbar.write(f"{Fore.RED}❌ Failed to upload {Path(image_file).name}: {e}")
                logger.error(f"Failed to upload {image_file}: {e}")
                raise GoogleAPIError(f"Upload failed: {e}")
        
        logger.success(f"{Fore.GREEN}✅ Upload complete: {len(file_urls)} files uploaded to Google Drive")
        return file_urls
    
    @staticmethod
    def get_direct_link(shareable_link: str) -> str:
        """Convert shareable link to direct link"""
        try:
            file_id = shareable_link.split('/d/')[1].split('/')[0]
            return f"https://drive.google.com/uc?export=view&id={file_id}"
        except IndexError:
            raise ValueError(f"Invalid shareable link format: {shareable_link}")
