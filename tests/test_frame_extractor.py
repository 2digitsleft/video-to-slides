import pytest
from pathlib import Path
from src.core.frame_extractor import (
    DifferenceFrameExtractor, 
    IntervalFrameExtractor,
    FrameExtractorFactory
)

class TestDifferenceFrameExtractor:
    def test_extract_frames_detects_changes(self, sample_video, temp_dir):
        extractor = DifferenceFrameExtractor(output_dir=temp_dir)
        frames = extractor.extract(
            str(sample_video), 
            threshold=50.0,  # Lower threshold to detect color changes
            interval=1,
            prefix="test"
        )
        
        # Should detect at least 3 frames (one for each color)
        assert len(frames) >= 3
        
        # Check that files exist
        for frame_path in frames:
            assert Path(frame_path).exists()
            assert frame_path.endswith('.png')
    
    def test_threshold_affects_detection(self, sample_video, temp_dir):
        extractor = DifferenceFrameExtractor(output_dir=temp_dir)
        
        # High threshold = fewer frames
        frames_high = extractor.extract(
            str(sample_video), 
            threshold=200.0,
            interval=1
        )
        
        # Low threshold = more frames
        frames_low = extractor.extract(
            str(sample_video),
            threshold=10.0,
            interval=1
        )
        
        assert len(frames_low) > len(frames_high)

class TestIntervalFrameExtractor:
    def test_extract_at_intervals(self, sample_video, temp_dir):
        extractor = IntervalFrameExtractor(output_dir=temp_dir)
        frames = extractor.extract(
            str(sample_video),
            interval=10,
            prefix="interval"
        )
        
        # 30 total frames, interval of 10 = 3 frames
        assert len(frames) == 3
        
        # Check file naming
        for i, frame_path in enumerate(frames, 1):
            assert f"interval_{i}.png" in frame_path

class TestFrameExtractorFactory:
    def test_create_diff_extractor(self):
        extractor = FrameExtractorFactory.create('diff')
        assert isinstance(extractor, DifferenceFrameExtractor)
    
    def test_create_interval_extractor(self):
        extractor = FrameExtractorFactory.create('interval')
        assert isinstance(extractor, IntervalFrameExtractor)
    
    def test_invalid_mode_raises_error(self):
        with pytest.raises(ValueError):
            FrameExtractorFactory.create('invalid_mode')
