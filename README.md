# VideoSubtitler

VideoSubtitler is a Python tool that extracts audio from a video, transcribes it using the Whisper model, and burns subtitles into the video using FFmpeg. It splits text into readable chunks and distributes timestamps proportionally for a clean subtitle experience.

## Features
- Extracts audio from video files.
- Transcribes audio with Whisper AI.
- Generates SRT subtitle files with 3-4 word chunks.
- Burns subtitles into videos with customizable styling.

## Installation
1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/VideoSubtitler.git
   cd VideoSubtitler

2. Install dependencies:
    pip install -r requirements.txt

3. Install FFmpeg:
    On Windows: Use a package manager like Chocolatey (choco install ffmpeg).
    OR Else you can manually download the ffmpeg if the command does not work to download the ffmpeg and then copy paste the path directory to the environment variables.
    On macOS: brew install ffmpeg.
    On Linux: sudo apt-get install ffmpeg.

Usage
Run the main script with your video file: