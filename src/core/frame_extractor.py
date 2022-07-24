from abc import ABC, abstractmethod
import cv2
import numpy as np
from pathlib import Path
from typing import List
from loguru import logger
from tqdm import tqdm
from colorama import Fore, Style
from config.settings import settings

class FrameExtractor(ABC):
    def __init__(self, output_dir=None):
        self.output_dir = Path(output_dir or settings.FRAMES_DIR)
        self.output_dir.mkdir(parents=True, exist_ok=True)
    
    @abstractmethod
    def extract(self, video_path: str, **kwargs) -> List[str]:
        """Extract frames from video and return list of saved frame paths"""
        pass

class DifferenceFrameExtractor(FrameExtractor):
    """Extract frames based on visual differences"""
    
    def extract(self, video_path: str, threshold: float = 30.0, 
                interval: int = 30, prefix: str = "frame") -> List[str]:
        cap = cv2.VideoCapture(video_path)
        last_frame = None
        frame_index = 0
        saved_frame_count = 0
        saved_paths = []
        
        # Get video info for progress tracking
        total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
        fps = cap.get(cv2.CAP_PROP_FPS)
        duration = total_frames / fps if fps > 0 else 0
        
        video_name = Path(video_path).stem
        logger.info(f"{Fore.CYAN}🎬 Starting frame extraction from '{video_name}'")
        logger.info(f"{Fore.BLUE}📊 Video info: {total_frames:,} frames, {duration:.1f}s duration, {fps:.1f} FPS")
        logger.info(f"{Fore.YELLOW}⚙️  Mode: Difference detection (threshold: {threshold}, interval: {interval} frames)")
        
        # Calculate expected iterations for progress bar
        expected_iterations = total_frames // interval
        pbar = tqdm(total=expected_iterations, 
                   desc=f"{Fore.MAGENTA}🔍 Analyzing frames", 
                   unit="frames",
                   bar_format='{desc}: {percentage:3.0f}%|{bar}| {n_fmt}/{total_fmt} [{elapsed}<{remaining}] {postfix}')
        
        try:
            while cap.isOpened():
                ret, frame = cap.read()
                if not ret:
                    break
                
                should_save = False
                
                if last_frame is not None:
                    gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
                    frame_diff = cv2.absdiff(last_frame, gray_frame)
                    mean_diff = frame_diff.mean()
                    should_save = mean_diff > threshold
                    last_frame = gray_frame
                else:
                    last_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
                    should_save = True
                
                if should_save:
                    saved_frame_count += 1
                    filename = self.output_dir / f"{prefix}_{saved_frame_count}.png"
                    cv2.imwrite(str(filename), frame)
                    saved_paths.append(str(filename))
                
                frame_index += interval
                cap.set(cv2.CAP_PROP_POS_FRAMES, frame_index)
                
                # Update progress
                pbar.update(1)
                pbar.set_postfix({
                    'saved': saved_frame_count,
                    'current_time': f"{frame_index/fps:.1f}s" if fps > 0 else "N/A"
                })
                
        finally:
            pbar.close()
            cap.release()
            
        logger.success(f"{Fore.GREEN}✅ Frame extraction complete: {len(saved_paths)} frames saved")
        return saved_paths

class IntervalFrameExtractor(FrameExtractor):
    """Extract frames at regular intervals"""
    
    def extract(self, video_path: str, interval: int = 30, 
                prefix: str = "frame") -> List[str]:
        cap = cv2.VideoCapture(video_path)
        frame_index = 0
        saved_frame_count = 0
        saved_paths = []
        
        # Get video info for progress tracking
        total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
        fps = cap.get(cv2.CAP_PROP_FPS)
        duration = total_frames / fps if fps > 0 else 0
        expected_saves = total_frames // interval
        
        video_name = Path(video_path).stem
        logger.info(f"{Fore.CYAN}🎬 Starting frame extraction from '{video_name}'")
        logger.info(f"{Fore.BLUE}📊 Video info: {total_frames:,} frames, {duration:.1f}s duration, {fps:.1f} FPS")
        logger.info(f"{Fore.YELLOW}⚙️  Mode: Interval extraction (every {interval} frames, ~{expected_saves} frames expected)")
        
        pbar = tqdm(total=total_frames, 
                   desc=f"{Fore.GREEN}📹 Processing video", 
                   unit="frames",
                   bar_format='{desc}: {percentage:3.0f}%|{bar}| {n_fmt}/{total_fmt} [{elapsed}<{remaining}] {postfix}')
        
        try:
            while cap.isOpened():
                ret, frame = cap.read()
                if not ret:
                    break
                
                if frame_index % interval == 0:
                    saved_frame_count += 1
                    filename = self.output_dir / f"{prefix}_{saved_frame_count}.png"
                    cv2.imwrite(str(filename), frame)
                    saved_paths.append(str(filename))
                
                frame_index += 1
                
                # Update progress
                pbar.update(1)
                pbar.set_postfix({
                    'saved': saved_frame_count,
                    'current_time': f"{frame_index/fps:.1f}s" if fps > 0 else "N/A"
                })
                
        finally:
            pbar.close()
            cap.release()
            
        logger.success(f"{Fore.GREEN}✅ Frame extraction complete: {len(saved_paths)} frames saved")
        return saved_paths

class FrameExtractorFactory:
    @staticmethod
    def create(mode: str) -> FrameExtractor:
        extractors = {
            'diff': DifferenceFrameExtractor,
            'interval': IntervalFrameExtractor
        }
        
        extractor_class = extractors.get(mode)
        if not extractor_class:
            raise ValueError(f"Unknown extraction mode: {mode}")
            
        return extractor_class()
