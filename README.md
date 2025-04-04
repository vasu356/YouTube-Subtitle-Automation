# YouTube-Subtitle-Automation

YouTube-Subtitle-Automation is a Python tool that extracts audio from a video, transcribes it using the Whisper model, and burns subtitles into the video using FFmpeg. It splits text into readable chunks and distributes timestamps proportionally for a clean subtitle experience.

## Features
- Extracts audio from video files.
- Transcribes audio with Whisper AI.
- Generates SRT subtitle files with 3-4 word chunks.
- Burns subtitles into videos with customizable().

## Installation

1. **Clone the repository**:
   ```bash
   git clone https://github.com/vasu356/YouTube-Subtitle-Automation.git
   cd YouTube-Subtitle-Automation
   ```

2. **Install Python dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Install FFmpeg**:
   - **Windows**:
     - Use a package manager like Chocolatey: `choco install ffmpeg`.
     - Alternatively, download FFmpeg manually from [ffmpeg.org](https://ffmpeg.org/download.html), extract it, and add the `bin` directory to your system’s PATH environment variable.
   - **macOS**:
     - Install via Homebrew: `brew install ffmpeg`.
   - **Linux**:
     - Install via apt: `sudo apt-get install ffmpeg`.

## Usage
Run the main script with your video file:
```bash
python main.py
```
- **Input**: `video.mp4`
- **Output**: `output_video_with_subtitles.mp4`

## Requirements
See `requirements.txt` for Python dependencies.

## License
MIT License - see `LICENSE` for details.

## Contributing
Feel free to submit issues or pull requests!
