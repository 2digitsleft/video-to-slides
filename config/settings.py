import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

class Settings:
    # Paths
    BASE_DIR = Path(__file__).parent.parent
    DATA_DIR = BASE_DIR / "data"
    VIDEO_DIR = DATA_DIR / "videos"
    FRAMES_DIR = DATA_DIR / "frames"
    
    # Google API
    SERVICE_ACCOUNT_FILE = os.getenv(
        "GOOGLE_SERVICE_ACCOUNT_FILE",
        "/Users/gpruessmann/.credentials/jap2eng-da4dd7259a17.json"
    )
    PRESENTATION_ID = os.getenv(
        "PRESENTATION_ID",
        "1tT26oLVzE0oN9Ux_osft5PYUhxmEQILXvWG2WBODfas"
    )
    UPLOAD_FOLDER_ID = os.getenv(
        "UPLOAD_FOLDER_ID",
        "1rcxXPQZZ9RzRVenkREMxZRG8Q9zbOC2R"
    )
    
    # Video Processing
    DEFAULT_THRESHOLD = float(os.getenv("DEFAULT_THRESHOLD", "30.0"))
    DEFAULT_INTERVAL = int(os.getenv("DEFAULT_INTERVAL", "30"))
    
    # API Scopes
    GOOGLE_SCOPES = [
        'https://www.googleapis.com/auth/presentations',
        'https://www.googleapis.com/auth/drive',
        'https://www.googleapis.com/auth/presentations.readonly'
    ]

settings = Settings()
