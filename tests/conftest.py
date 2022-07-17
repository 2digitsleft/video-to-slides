import pytest
from pathlib import Path
import tempfile
import shutil
import cv2
import numpy as np

@pytest.fixture
def temp_dir():
    """Create a temporary directory for test files"""
    temp_path = tempfile.mkdtemp()
    yield Path(temp_path)
    shutil.rmtree(temp_path)

@pytest.fixture
def sample_video(temp_dir):
    """Create a simple test video"""
    video_path = temp_dir / "test_video.mp4"
    
    # Create a simple video with 3 different colored frames
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    out = cv2.VideoWriter(str(video_path), fourcc, 1.0, (640, 480))
    
    # Red frame
    frame1 = np.zeros((480, 640, 3), dtype=np.uint8)
    frame1[:, :, 2] = 255
    
    # Green frame
    frame2 = np.zeros((480, 640, 3), dtype=np.uint8)
    frame2[:, :, 1] = 255
    
    # Blue frame
    frame3 = np.zeros((480, 640, 3), dtype=np.uint8)
    frame3[:, :, 0] = 255
    
    # Write frames multiple times to create duration
    for _ in range(10):
        out.write(frame1)
    for _ in range(10):
        out.write(frame2)
    for _ in range(10):
        out.write(frame3)
    
    out.release()
    return video_path

@pytest.fixture
def mock_credentials(monkeypatch):
    """Mock Google credentials"""
    def mock_from_service_account_file(*args, **kwargs):
        class MockCredentials:
            pass
        return MockCredentials()
    
    monkeypatch.setattr(
        "google.oauth2.service_account.Credentials.from_service_account_file",
        mock_from_service_account_file
    )
