#!/bin/bash

# Quick start script for video-to-slides

echo "Video to Slides - Quick Start"
echo "============================"
echo ""

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
echo "Activating virtual environment..."
source venv/bin/activate

# Install dependencies
echo "Installing dependencies..."
pip install -r requirements.txt

echo ""
echo "Setup complete! Here are some example commands:"
echo ""
echo "1. Extract frames from a local video:"
echo "   python -m src.main --file video.mp4 --create-frames"
echo ""
echo "2. Download from YouTube and create slides:"
echo "   python -m src.main --url 'https://youtube.com/watch?v=...' --create-frames --upload-frames --add-slides"
echo ""
echo "3. Your previous command format:"
echo "   python -m src.main --mode interval --threshold 30 --interval 30 --create-frames --upload-frames --add-slides --prefix 'coba_' --file video.mp4"
echo ""
echo "Run 'python -m src.main --help' for all options"
