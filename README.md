# Video to Google Slides Converter

A powerful Python application that automatically transforms videos into Google Slides presentations by intelligently extracting key frames. Perfect for creating presentations from recorded lectures, tutorials, webinars, or any video content where visual changes indicate important moments.

## Overview

This tool bridges the gap between video content and presentation formats. It analyzes videos to identify significant visual changes (like slide transitions in a recorded presentation) or extracts frames at regular intervals, then automatically creates a Google Slides presentation with these frames. This saves hours of manual screenshot work and makes it easy to repurpose video content for different audiences.

### Key Use Cases
- ** Educational Content**: Convert recorded lectures or tutorials into slide decks for students
- ** Business Presentations**: Transform webinar recordings into shareable presentations
- ** Video Documentation**: Create visual documentation from screen recordings
- ** Training Materials**: Convert training videos into reference slides
- ** Meeting Recordings**: Extract key moments from recorded meetings

##  Features

### Video Input Flexibility
- **Local Video Files**: Process videos already on your computer (MP4, MOV, AVI, etc.)
- **YouTube Downloads**: Download and process videos directly from YouTube URLs
- **Batch Processing**: Handle multiple videos in sequence

### Intelligent Frame Extraction
- **Difference-Based Detection**: Automatically captures frames when significant visual changes occur
  - Ideal for recorded presentations where slides change
  - Customizable sensitivity threshold
  - Skips redundant frames automatically
- **Interval-Based Extraction**: Captures frames at regular time intervals
  - Perfect for continuous content like tutorials
  - Configurable interval settings

### Google Integration
- **Automatic Upload**: Frames are uploaded to Google Drive
- **Slides Creation**: Automatically creates or updates Google Slides presentations
- **Batch Operations**: Efficiently handles multiple frames with rate limiting
- **Public Sharing**: Optionally makes slides publicly accessible

### Professional Features
- ** Secure Configuration**: Credentials stored in environment variables
- ** Progress Tracking**: Visual progress bars for all operations
- ** Comprehensive Logging**: Detailed logs for debugging and monitoring
- ** Modular Architecture**: Easy to extend and maintain
- ** Testable Design**: Comprehensive test suite included

## Requirements

- Python 3.8 or higher
- Google Cloud account with:
  - Google Drive API enabled
  - Google Slides API enabled
  - Service account credentials
- OpenCV (automatically installed)
- Internet connection for Google API operations

## Installation

### 1. Clone the Repository
```bash
git clone https://github.com/yourusername/video-to-slides.git
cd video-to-slides
```

### 2. Set Up Python Environment
```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# On macOS/Linux:
source venv/bin/activate
# On Windows:
venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

#### Optional: Install as Package
```bash
pip install -e .
# Now use from anywhere:
video-to-slides --help
```

### 3. Configure Google API Access

#### Create a Google Cloud Project:
1. Go to [Google Cloud Console](https://console.cloud.google.com)
2. Create a new project or select existing
3. Enable Google Drive API and Google Slides API

#### Create Service Account:
1. Go to "IAM & Admin" > "Service Accounts"
2. Create a new service account
3. Download the JSON key file
4. Save it securely (e.g., `~/.credentials/your-service-account.json`)

#### Set Up Google Drive Folder:
1. Create a folder in Google Drive for uploaded images
2. Share the folder with your service account email
3. Copy the folder ID from the URL

### 4. Configure Environment Variables
```bash
# Copy example environment file
cp .env.example .env

# Edit .env with your settings:
# - GOOGLE_SERVICE_ACCOUNT_FILE: Path to your JSON key file
# - PRESENTATION_ID: ID of target Google Slides presentation (optional)
# - UPLOAD_FOLDER_ID: Google Drive folder ID for uploads
```

## Usage

### Basic Commands

#### Extract frames from a local video:
```bash
python -m src.main --file /path/to/video.mp4 --create-frames
```

#### Process a YouTube video:
```bash
python -m src.main --url "https://youtube.com/watch?v=VIDEO_ID" --create-frames
```

#### Complete workflow (extract, upload, create slides):
```bash
python -m src.main --file video.mp4 --create-frames --upload-frames --add-slides
```

### Command Options

| Option | Description | Default |
|--------|-------------|---------|
| `--url` | YouTube video URL to download | - |
| `--file` | Path to local video file | - |
| `--mode` | Extraction mode: `diff` or `interval` | `diff` |
| `--threshold` | Sensitivity for change detection (1-100) | 30.0 |
| `--interval` | Frame interval for extraction | 30 |
| `--prefix` | Prefix for saved frame files | `frame` |
| `--create-frames` | Extract frames from video | False |
| `--upload-frames` | Upload frames to Google Drive | False |
| `--add-slides` | Add frames to Google Slides | False |
| `--presentation-id` | Override default presentation ID | From .env |

### Extraction Modes Explained

#### Difference Mode (`--mode diff`)
Best for videos with distinct visual changes:
- Recorded presentations with slide transitions
- Screen recordings with different screens
- Tutorials with clear step changes

```bash
# High sensitivity (captures more changes)
python -m src.main --file presentation.mp4 --create-frames --mode diff --threshold 15

# Low sensitivity (captures only major changes)
python -m src.main --file presentation.mp4 --create-frames --mode diff --threshold 50
```

#### Interval Mode (`--mode interval`)
Best for continuous content:
- Live demonstrations
- Continuous lectures
- Time-lapse videos

```bash
# Capture every 30 frames (approximately 1 second at 30fps)
python -m src.main --file tutorial.mp4 --create-frames --mode interval --interval 30

# Capture every 150 frames (approximately 5 seconds at 30fps)
python -m src.main --file tutorial.mp4 --create-frames --mode interval --interval 150
```

### Real-World Examples

#### Convert a recorded Zoom presentation:
```bash
python -m src.main \
    --file "zoom_recording.mp4" \
    --create-frames \
    --upload-frames \
    --add-slides \
    --mode diff \
    --threshold 25 \
    --prefix "zoom_meeting_2024"
```

#### Create slides from a tutorial video:
```bash
python -m src.main \
    --url "https://youtube.com/watch?v=dQw4w9WgXcQ" \
    --create-frames \
    --upload-frames \
    --add-slides \
    --mode interval \
    --interval 300 \
    --prefix "tutorial"
```

#### Process multiple local videos:
```bash
for video in videos/*.mp4; do
    python -m src.main \
        --file "$video" \
        --create-frames \
        --upload-frames \
        --add-slides \
        --prefix "$(basename $video .mp4)"
done
```

## Project Structure

```
video-to-slides/
├── config/              # Configuration management
│   └── settings.py      # Centralized settings
├── src/
│   ├── core/           # Core business logic
│   │   ├── video_downloader.py    # YouTube download
│   │   └── frame_extractor.py     # Frame extraction algorithms
│   ├── services/       # External service integrations
│   │   ├── google_drive.py        # Drive upload functionality
│   │   └── google_slides.py       # Slides management
│   └── utils/          # Utility functions
├── data/               # Data directories
│   ├── videos/         # Downloaded/source videos
│   └── frames/         # Extracted frames
└── tests/              # Test suite
```

## Advanced Configuration

### Custom Frame Output Directory
```python
# In your .env file
FRAMES_DIR=/custom/path/to/frames
```

### Adjust Logging Level
```python
# In your .env file
LOG_LEVEL=DEBUG  # Options: DEBUG, INFO, WARNING, ERROR
```

### Rate Limiting for Google APIs
Modify delay between API calls in the code:
```python
# In src/services/google_slides.py
slides_service.batch_add_slides(presentation_id, urls, delay=2.0)  # 2 second delay
```

## Development

### Running Tests
```bash
# Run all tests
pytest

# Run with coverage report
pytest --cov=src --cov-report=html

# Run specific test file
pytest tests/test_frame_extractor.py
```

### Installing in Development Mode
```bash
pip install -e .

# Now you can use the command globally:
video-to-slides --help
```

### Code Style
The project follows PEP 8 guidelines. To check code style:
```bash
pip install flake8
flake8 src/
```

## Troubleshooting

### Common Issues

#### "No frames extracted"
- Check video format compatibility
- Adjust threshold for difference mode
- Verify video file isn't corrupted

#### "Google API errors"
- Verify service account has necessary permissions
- Check API quotas in Google Cloud Console
- Ensure credentials file path is correct

#### "Import errors"
- Ensure all dependencies are installed: `pip install -r requirements.txt`
- Check Python version compatibility (3.8+)

### Debug Mode
Enable detailed logging:
```bash
LOG_LEVEL=DEBUG python -m src.main --file video.mp4 --create-frames
```

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- **OpenCV**: For powerful video processing capabilities
- **PyTube**: For reliable YouTube video downloads
- **Google APIs**: For seamless cloud integration
- **Click**: For elegant command-line interface
- **Loguru**: For beautiful logging

## Contact

For questions, suggestions, or issues:
- Create an issue on GitHub

---

Made with ❤️ by the 2digits - Video-to-Slides team