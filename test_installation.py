#!/usr/bin/env python
"""
Test script to verify the installation and imports
"""

import sys
import os

# Add the project root to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def test_imports():
    """Test if all modules can be imported"""
    print("Testing imports...")
    
    try:
        from config.settings import settings
        print("✓ Config module imported successfully")
        print(f"  - Video directory: {settings.VIDEO_DIR}")
        print(f"  - Frames directory: {settings.FRAMES_DIR}")
    except Exception as e:
        print(f"✗ Config import failed: {e}")
    
    try:
        from src.core.video_downloader import VideoDownloader
        print("✓ VideoDownloader imported successfully")
    except Exception as e:
        print(f"✗ VideoDownloader import failed: {e}")
    
    try:
        from src.core.frame_extractor import FrameExtractorFactory
        print("✓ FrameExtractor imported successfully")
    except Exception as e:
        print(f"✗ FrameExtractor import failed: {e}")
    
    try:
        from src.services.google_drive import GoogleDriveService
        print("✓ GoogleDriveService imported successfully")
    except Exception as e:
        print(f"✗ GoogleDriveService import failed: {e}")
    
    try:
        from src.services.google_slides import GoogleSlidesService
        print("✓ GoogleSlidesService imported successfully")
    except Exception as e:
        print(f"✗ GoogleSlidesService import failed: {e}")
    
    print("\nChecking credentials file...")
    creds_file = "/Users/gpruessmann/.credentials/jap2eng-da4dd7259a17.json"
    if os.path.exists(creds_file):
        print(f"✓ Credentials file found: {creds_file}")
    else:
        print(f"✗ Credentials file not found: {creds_file}")
        print("  Please ensure your Google service account JSON file is in the correct location")

if __name__ == "__main__":
    test_imports()
