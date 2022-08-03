"""Custom exceptions for the video-to-slides application"""

class VideoToSlidesException(Exception):
    """Base exception for the application"""
    pass

class VideoDownloadError(VideoToSlidesException):
    """Raised when video download fails"""
    pass

class FrameExtractionError(VideoToSlidesException):
    """Raised when frame extraction fails"""
    pass

class GoogleAPIError(VideoToSlidesException):
    """Raised when Google API operations fail"""
    pass

class AuthenticationError(GoogleAPIError):
    """Raised when authentication fails"""
    pass
