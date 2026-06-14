<div align="center">

<h1>🎬 YouTube Subtitle Automation</h1>

<p>
  <strong>Auto-generate and burn subtitles into any video — fully from the command line.</strong><br/>
  Powered by OpenAI Whisper for speech recognition and FFmpeg for rendering.
</p>

<p>
  <img src="https://img.shields.io/badge/Python-3.12-blue?style=for-the-badge&logo=python&logoColor=white" alt="Python 3.12"/>
  <img src="https://img.shields.io/badge/OpenAI-Whisper-412991?style=for-the-badge&logo=openai&logoColor=white" alt="Whisper"/>
  <img src="https://img.shields.io/badge/FFmpeg-007808?style=for-the-badge&logo=ffmpeg&logoColor=white" alt="FFmpeg"/>
  <img src="https://img.shields.io/badge/License-MIT-green?style=for-the-badge" alt="MIT License"/>
  <img src="https://img.shields.io/badge/Languages-99+-orange?style=for-the-badge" alt="99+ Languages"/>
</p>

</div>

---

## 📽️ Demo

> Click the thumbnails below to play the videos directly on GitHub.

<table>
  <tr>
    <th align="center">⬅️ Input — No Subtitles</th>
    <th align="center">➡️ Output — Burned-in Subtitles</th>
  </tr>
  <tr>
    <td align="center">
      <a href="Input%20%26%20Output/video.mp4">
        <img src="https://img.shields.io/badge/▶%20Play-Input%20Video-555555?style=for-the-badge" alt="Play Input Video"/>
      </a>
      <br/><sub><code>Input &amp; Output/video.mp4</code></sub>
    </td>
    <td align="center">
      <a href="Input%20%26%20Output/output_video_with_subtitles.mp4">
        <img src="https://img.shields.io/badge/▶%20Play-Output%20Video-007808?style=for-the-badge" alt="Play Output Video"/>
      </a>
      <br/><sub><code>Input &amp; Output/output_video_with_subtitles.mp4</code></sub>
    </td>
  </tr>
</table>

---

## ✨ Features

| Feature | Details |
|---|---|
| 🎙️ **AI Speech-to-Text** | OpenAI Whisper — industry-leading accuracy |
| 🌍 **99 Languages** | Auto-detect or specify explicitly |
| ⚡ **5 Model Sizes** | `tiny` → `large` — trade speed for accuracy |
| 📝 **Word-chunked subtitles** | 3–5 word cards for natural readability |
| ⏱️ **Proportional timestamps** | Duration scales with word count per chunk |
| 🔥 **Burned-in subtitles** | Hardcoded into the video via FFmpeg — no external file needed |
| 🎨 **Custom styling** | Font size, color (white/yellow/cyan/green), vertical position |
| 📄 **SRT export** | Optionally keep the generated `.srt` alongside the output |
| 🎞️ **Multi-format** | mp4, avi, mov, mkv, webm, flv |
| 🆓 **MIT Licensed** | Free for personal and commercial use |

---

## 🚀 Quick Start

```bash
# Clone
git clone https://github.com/vasu356/YouTube-Subtitle-Automation.git
cd YouTube-Subtitle-Automation

# Install dependencies
pip install -r requirements.txt

# Run
python main.py -i video.mp4
```

Output: `video_subtitled.mp4` in the same directory. Done.

---

## 📋 Requirements

- **Python 3.10+**
- **FFmpeg** — must be on your system PATH

### Install FFmpeg

<details>
<summary><b>🐧 Linux</b></summary>

```bash
sudo apt-get install ffmpeg
```
</details>

<details>
<summary><b>🍎 macOS</b></summary>

```bash
brew install ffmpeg
```
</details>

<details>
<summary><b>🪟 Windows</b></summary>

```bash
choco install ffmpeg
```
Or download from [ffmpeg.org](https://ffmpeg.org/download.html), extract, and add `bin/` to your system PATH.
</details>

---

## 🛠️ Installation

```bash
# 1. Clone the repo
git clone https://github.com/vasu356/YouTube-Subtitle-Automation.git
cd YouTube-Subtitle-Automation

# 2. (Optional) Create a virtual environment
python -m venv .venv
source .venv/bin/activate      # Linux / macOS
.venv\Scripts\activate         # Windows

# 3. Install Python dependencies
pip install -r requirements.txt
```

---

## 💻 Usage

### Minimal — auto-detect language, default settings

```bash
python main.py -i video.mp4
```

---

### Specify output path

```bash
python main.py -i video.mp4 -o subtitled_output.mp4
```

---

### Use a more accurate Whisper model

```bash
python main.py -i video.mp4 --model medium
```

---

### Set language explicitly (faster + more accurate than auto-detect)

```bash
python main.py -i video.mp4 --language en   # English
python main.py -i video.mp4 --language hi   # Hindi
python main.py -i video.mp4 --language es   # Spanish
python main.py -i video.mp4 --language fr   # French
```

---

### Customize subtitle appearance

```bash
python main.py -i video.mp4 \
  --font-size 18        \
  --font-color yellow   \
  --margin-bottom 60    \
  --words 5
```

---

### Export the SRT file alongside the video

```bash
python main.py -i video.mp4 --keep-srt
```

---

### Full options reference

```
python main.py --help

options:
  -i,  --input          Path to input video file            [required]
  -o,  --output         Path for output video               [default: <input>_subtitled.mp4]
       --model          Whisper model size                  [default: base]
                          tiny | base | small | medium | large
       --language       Language code (e.g. en, hi, es)    [default: auto-detect]
       --words          Max words per subtitle chunk        [default: 4]
       --font-size      Subtitle font size                  [default: 15]
       --font-color     Text color                          [default: white]
                          white | yellow | cyan | green
       --margin-bottom  Bottom margin in pixels             [default: 50]
       --keep-srt       Keep .srt file alongside output     [flag]
```

---

## 🤖 Whisper Model Reference

| Model | Parameters | Relative Speed | VRAM | Best For |
|-------|-----------|----------------|------|----------|
| `tiny` | 39 M | ~32× | ~1 GB | Quick previews, constrained machines |
| `base` | 74 M | ~16× | ~1 GB | **Default** — good balance of speed & accuracy |
| `small` | 244 M | ~6× | ~2 GB | Better accuracy, still CPU-friendly |
| `medium` | 769 M | ~2× | ~5 GB | High accuracy, recommended with GPU |
| `large` | 1550 M | 1× | ~10 GB | Best accuracy — GPU required |

> GPU (CUDA) is used automatically if available, significantly improving speed for `medium` and `large`.

---

## 🌍 Supported Languages

Whisper supports **99 languages**. Common codes:

| Language | Code | Language | Code | Language | Code |
|----------|------|----------|------|----------|------|
| English | `en` | Hindi | `hi` | Arabic | `ar` |
| Spanish | `es` | Bengali | `bn` | Portuguese | `pt` |
| French | `fr` | Russian | `ru` | Urdu | `ur` |
| German | `de` | Japanese | `ja` | Korean | `ko` |
| Chinese | `zh` | Italian | `it` | Dutch | `nl` |

Full list → [OpenAI Whisper supported languages](https://github.com/openai/whisper#available-models-and-languages)

---

## ⚙️ How It Works

```
┌─────────────────────────────────────────────────────────┐
│                     Input Video                         │
└────────────────────────┬────────────────────────────────┘
                         │
                         ▼
          ┌──────────────────────────┐
          │  Extract Audio (moviepy) │  →  temp .wav file
          └──────────────┬───────────┘
                         │
                         ▼
          ┌──────────────────────────────────────┐
          │  Normalize + Resample to 16 kHz       │
          │  (scipy — Whisper requirement)        │
          └──────────────┬───────────────────────┘
                         │
                         ▼
          ┌──────────────────────────────────────┐
          │  Transcribe with OpenAI Whisper      │  →  segments [{text, start, end}]
          └──────────────┬───────────────────────┘
                         │
                         ▼
          ┌──────────────────────────────────────┐
          │  Split each segment into N-word      │
          │  chunks  (split_into_chunks)         │
          └──────────────┬───────────────────────┘
                         │
                         ▼
          ┌──────────────────────────────────────┐
          │  Distribute timestamps proportionally│
          │  by word count (distribute_timestamps│
          └──────────────┬───────────────────────┘
                         │
                         ▼
          ┌──────────────────────────────────────┐
          │  Generate .srt file                  │
          │  (create_srt_file)                   │
          └──────────────┬───────────────────────┘
                         │
                         ▼
          ┌──────────────────────────────────────┐
          │  Burn subtitles with FFmpeg           │  →  Output Video 🎬
          │  (libx264 + libass subtitle filter)  │
          └──────────────────────────────────────┘
```

---

## 📁 Project Structure

```
YouTube-Subtitle-Automation/
│
├── main.py                          # CLI entry point (argparse)
├── extract_and_transcribe_audio.py  # Audio extraction + Whisper transcription
├── add_subtitles_to_video.py        # SRT generation + FFmpeg video rendering
├── split_into_chunks.py             # Word-chunk splitting utility
├── distribute_timestamps.py         # Proportional timestamp distribution
│
├── requirements.txt                 # Python dependencies
├── LICENSE                          # MIT License
│
└── Input & Output/
    ├── video.mp4                    # Sample input (no subtitles)
    └── output_video_with_subtitles.mp4  # Sample output (burned-in subtitles)
```

---

## 📦 Dependencies

| Package | Purpose |
|---|---|
| `openai-whisper` | Speech-to-text transcription |
| `moviepy` | Audio extraction from video |
| `scipy` | Audio resampling to 16 kHz |
| `numpy` | Audio array normalization |
| `ffmpeg-python` | Python bindings for FFmpeg |
| `ffmpeg` *(system)* | Video encoding and subtitle rendering |

---

## 📄 License

This project is licensed under the **MIT License** — see [LICENSE](./LICENSE) for details.

© 2025 [Vasu Agrawal](https://github.com/vasu356)

---

## 🤝 Contributing

Contributions, issues, and feature requests are welcome!

1. Fork the repository
2. Create your branch: `git checkout -b feature/your-feature`
3. Commit your changes: `git commit -m 'Add your feature'`
4. Push to the branch: `git push origin feature/your-feature`
5. Open a Pull Request

---

<div align="center">
  <sub>Built with ❤️ by <a href="https://github.com/vasu356">Vasu Agrawal</a></sub>
</div>
