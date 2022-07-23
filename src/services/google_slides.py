from typing import List
import time
from googleapiclient.discovery import build
from loguru import logger
from tqdm import tqdm
from colorama import Fore, Style
from .auth_manager import AuthManager
from src.core.exceptions import GoogleAPIError

class GoogleSlidesService:
    def __init__(self):
        self.creds = AuthManager.get_credentials()
        self.service = build('slides', 'v1', credentials=self.creds)
        
    def add_slide_with_image(self, presentation_id: str, image_url: str):
        """Add a slide with an image to the presentation"""
        try:
            # Create new slide
            body = {'requests': [{'createSlide': {}}]}
            response = self.service.presentations().batchUpdate(
                presentationId=presentation_id,
                body=body
            ).execute()
            
            slide_id = response.get('replies')[0].get('createSlide').get('objectId')
            
            # Add image to slide
            slide_width_emus = 10 * 914400
            slide_height_emus = 5.625 * 914400
            
            body = {
                'requests': [{
                    'createImage': {
                        'url': image_url,
                        'elementProperties': {
                            'pageObjectId': slide_id,
                            'size': {
                                'height': {'magnitude': slide_height_emus, 'unit': 'EMU'},
                                'width': {'magnitude': slide_width_emus, 'unit': 'EMU'},
                            },
                            'transform': {
                                'scaleX': 1,
                                'scaleY': 1,
                                'translateX': 0,
                                'translateY': 0,
                                'unit': 'EMU'
                            }
                        }
                    }
                }]
            }
            
            self.service.presentations().batchUpdate(
                presentationId=presentation_id,
                body=body
            ).execute()
            
        except Exception as e:
            logger.error(f"Failed to add slide: {e}")
            raise GoogleAPIError(f"Failed to add slide: {e}")
        
    def batch_add_slides(self, presentation_id: str, image_urls: List[str], 
                        delay: float = 1.0):
        """Add multiple slides with images"""
        logger.info(f"{Fore.MAGENTA}📊 Starting to create presentation slides ({len(image_urls)} slides)")
        
        pbar = tqdm(image_urls, 
                   desc=f"{Fore.MAGENTA}🎯 Creating slides", 
                   unit="slides",
                   bar_format='{desc}: {percentage:3.0f}%|{bar}| {n_fmt}/{total_fmt} [{elapsed}<{remaining}] {postfix}')
        
        for i, url in enumerate(pbar, 1):
            try:
                self.add_slide_with_image(presentation_id, url)
                time.sleep(delay)  # Rate limiting
                
                # Update progress
                pbar.set_postfix({
                    'slide': i,
                    'status': 'created'
                })
                
            except Exception as e:
                pbar.write(f"{Fore.RED}❌ Failed to add slide {i}: {e}")
                logger.error(f"Failed to add slide {i+1}: {e}")
        
        logger.success(f"{Fore.GREEN}✅ Presentation complete: {len(image_urls)} slides added to Google Slides")

    def create_presentation(self, title: str) -> str:
        """Create a new presentation and return its ID"""
        try:
            body = {'title': title}
            presentation = self.service.presentations().create(body=body).execute()
            return presentation.get('presentationId')
        except Exception as e:
            logger.error(f"Failed to create presentation: {e}")
            raise GoogleAPIError(f"Failed to create presentation: {e}")
