import os
import re
from pathlib import Path
from typing import List
from loguru import logger

def find_images_in_directory(directory: Path, pattern: str = "*.png") -> List[Path]:
    """Find all images matching pattern in directory"""
    if not directory.exists():
        logger.warning(f"Directory {directory} does not exist")
        return []
    
    images = list(directory.glob(pattern))
    
    # Sort by numeric suffix if present
    def get_number(filepath):
        match = re.search(r'_(\d+)\.\w+$', str(filepath))
        return int(match.group(1)) if match else 0
    
    return sorted(images, key=get_number)

def ensure_directory_exists(directory: Path) -> None:
    """Ensure directory exists, create if necessary"""
    directory.mkdir(parents=True, exist_ok=True)

def clean_filename(filename: str) -> str:
    """Clean filename to be filesystem-safe"""
    # Remove invalid characters
    filename = re.sub(r'[<>:"/\\|?*]', '', filename)
    # Replace spaces with underscores
    filename = filename.replace(' ', '_')
    # Limit length
    name, ext = os.path.splitext(filename)
    if len(name) > 200:
        name = name[:200]
    return name + ext

def get_file_size_mb(filepath: Path) -> float:
    """Get file size in megabytes"""
    if filepath.exists():
        return filepath.stat().st_size / (1024 * 1024)
    return 0.0
