import click
from pathlib import Path
from loguru import logger
from colorama import Fore, Style, init
from config.settings import settings
from src.core.video_downloader import VideoDownloader
from src.core.frame_extractor import FrameExtractorFactory
from src.services.google_drive import GoogleDriveService
from src.services.google_slides import GoogleSlidesService
from src.utils.file_handler import find_images_in_directory
from src.utils.logger import setup_logger
from tqdm import tqdm

# Initialize colorama for cross-platform colored output
init(autoreset=True)

@click.command()
@click.option('--url', help='YouTube video URL')
@click.option('--file', type=click.Path(exists=True), help='Local video file')
@click.option('--mode', type=click.Choice(['diff', 'interval']), default='diff')
@click.option('--threshold', type=float, default=settings.DEFAULT_THRESHOLD)
@click.option('--interval', type=int, default=settings.DEFAULT_INTERVAL)
@click.option('--prefix', default='frame', help='Frame filename prefix')
@click.option('--create-frames', is_flag=True, help='Extract frames from video')
@click.option('--upload-frames', is_flag=True, help='Upload frames to Drive')
@click.option('--add-slides', is_flag=True, help='Add to Slides presentation')
@click.option('--presentation-id', help='Override default presentation ID')
def main(url, file, mode, threshold, interval, prefix, create_frames, 
         upload_frames, add_slides, presentation_id):
    """Convert video to Google Slides presentation"""
    
    # Setup logger
    setup_logger()
    
    logger.info(f"{Fore.CYAN}Video-to-Slides Converter Starting...")
    logger.info(f"{Fore.CYAN}{'=' * 50}")
    
    # Determine video source
    if url:
        logger.info(f"{Fore.YELLOW}Downloading video from YouTube: {url}")
        downloader = VideoDownloader()
        video_path = downloader.download_from_youtube(url)
        logger.success(f"{Fore.GREEN}Video downloaded successfully")
    elif file:
        video_path = file
        logger.info(f"{Fore.BLUE}Using local video file: {file}")
    else:
        logger.error(f"{Fore.RED}Error: Please provide either --url or --file")
        return
    
    logger.info(f"{Fore.MAGENTA}Configuration:")
    logger.info(f"{Fore.MAGENTA}   • Mode: {mode}")
    logger.info(f"{Fore.MAGENTA}   • Threshold: {threshold}" + (" (diff mode)" if mode == 'diff' else ""))
    logger.info(f"{Fore.MAGENTA}   • Interval: {interval} frames")
    logger.info(f"{Fore.MAGENTA}   • Prefix: '{prefix}'")
    logger.info(f"{Fore.MAGENTA}   • Steps: {'✓' if create_frames else '✗'} Extract frames, {'✓' if upload_frames else '✗'} Upload, {'✓' if add_slides else '✗'} Create slides")
    logger.info(f"{Fore.CYAN}{'=' * 50}")
    
    # Extract frames
    if create_frames:
        logger.info("")
        logger.info(f"{Fore.GREEN}🔧 STEP 1/3: Frame Extraction")
        logger.info(f"{Fore.GREEN}{'-' * 30}")
        extractor = FrameExtractorFactory.create(mode)
        kwargs = {'prefix': prefix, 'interval': interval}
        if mode == 'diff':
            kwargs['threshold'] = threshold
            
        frame_paths = extractor.extract(video_path, **kwargs)
    
    # Upload and create slides
    if upload_frames or add_slides:
        # Find existing frames if not just created
        if not create_frames:
            logger.info("")
            logger.info(f"{Fore.YELLOW}Finding existing frames...")
            frame_paths = find_images_in_directory(
                settings.FRAMES_DIR, 
                f"{prefix}_*.png"
            )
            frame_paths = [str(p) for p in frame_paths]
            logger.info(f"{Fore.YELLOW}Found {len(frame_paths)} existing frames with prefix '{prefix}'")
        
        if not frame_paths:
            logger.error(f"{Fore.RED}Error: No frames found to upload")
            return
        
        # Upload to Drive
        if upload_frames or add_slides:
            logger.info("")
            logger.info(f"{Fore.BLUE}STEP 2/3: Google Drive Upload")
            logger.info(f"{Fore.BLUE}{'-' * 30}")
            drive_service = GoogleDriveService()
            urls = drive_service.upload_images(frame_paths, settings.UPLOAD_FOLDER_ID)
        
        # Add to Slides
        if add_slides:
            logger.info("")
            logger.info(f"{Fore.MAGENTA}STEP 3/3: Google Slides Creation")
            logger.info(f"{Fore.MAGENTA}{'-' * 30}")
            slides_service = GoogleSlidesService()
            target_id = presentation_id or settings.PRESENTATION_ID
            
            logger.info(f"{Fore.CYAN}Converting {len(urls)} shareable links to direct links...")
            direct_urls = [drive_service.get_direct_link(url) for url in urls]
            logger.success(f"{Fore.GREEN}Links converted successfully")
            
            slides_service.batch_add_slides(target_id, direct_urls)
    
    logger.info(f"{Fore.CYAN}{'=' * 50}")
    logger.success(f"{Fore.GREEN}🎉 PROCESS COMPLETE!")
    if create_frames:
        logger.success(f"{Fore.GREEN}   Extracted {len(frame_paths)} frames")
    if upload_frames or add_slides:
        logger.success(f"{Fore.GREEN}   Uploaded {len(frame_paths)} files to Google Drive")
    if add_slides:
        logger.success(f"{Fore.GREEN}   Created {len(frame_paths)} slides in presentation")
        logger.info(f"{Fore.CYAN}   Presentation ID: {target_id}")
    logger.info(f"{Fore.CYAN}{'=' * 50}")

if __name__ == '__main__':
    main()
