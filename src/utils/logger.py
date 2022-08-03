import sys
from loguru import logger
from colorama import init
from config.settings import settings

# Initialize colorama
init(autoreset=True)

def setup_logger():
    """Configure logger for the application"""
    logger.remove()  # Remove default handler
    
    # Console logging with colorama support
    logger.add(
        sys.stderr,
        format="<green>{time:HH:mm:ss}</green> | <level>{level: <8}</level> | {message}",
        level=settings.LOG_LEVEL if hasattr(settings, 'LOG_LEVEL') else "INFO",
        colorize=True,
        enqueue=True,  # Make it thread-safe
        catch=True     # Catch exceptions
    )
    
    # File logging (without colors)
    logger.add(
        "logs/video-to-slides.log",
        rotation="10 MB",
        retention="7 days",
        level="DEBUG",
        format="{time:YYYY-MM-DD HH:mm:ss} | {level: <8} | {name}:{function}:{line} - {message}",
        enqueue=True
    )
    
    return logger

# Set up logger when module is imported
setup_logger()
