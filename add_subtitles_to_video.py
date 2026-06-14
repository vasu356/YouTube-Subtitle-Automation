"""
Subtitle generation and FFmpeg video rendering module.

Converts Whisper transcription segments into an SRT file (with configurable
word-chunking and proportional timestamps), then burns the subtitles into
the video using FFmpeg's libass subtitle renderer.
"""

import os
import ffmpeg
from split_into_chunks import split_into_chunks
from distribute_timestamps import distribute_timestamps


# Map friendly color names to ASS hex color codes (BGR order, no alpha)
FONT_COLOR_MAP = {
    "white":  "&H00FFFFFF",
    "yellow": "&H0000FFFF",
    "cyan":   "&H00FFFF00",
    "green":  "&H0000FF00",
}


def format_timestamp(seconds: float) -> str:
    """
    Convert a float number of seconds into SRT timestamp format.

    Args:
        seconds: Time in seconds (e.g. 73.45).

    Returns:
        SRT-formatted timestamp string, e.g. '00:01:13,450'.
    """
    hours   = int(seconds // 3600)
    minutes = int((seconds % 3600) // 60)
    secs    = int(seconds % 60)
    millis  = int((seconds % 1) * 1000)
    return f"{hours:02d}:{minutes:02d}:{secs:02d},{millis:03d}"


def create_srt_file(
    segments: list[dict],
    srt_path: str,
    max_words: int = 4,
) -> None:
    """
    Generate an SRT subtitle file from Whisper transcription segments.

    Each Whisper segment is split into smaller readable chunks of at most
    `max_words` words. Timestamps for each chunk are distributed
    proportionally based on word count within the parent segment.

    Args:
        segments:  List of Whisper segment dicts with 'text', 'start', 'end'.
        srt_path:  File path to write the .srt file.
        max_words: Maximum number of words per subtitle card. (default: 4)
    """
    srt_lines = []
    subtitle_index = 1

    for segment in segments:
        text = segment["text"].strip()
        if not text:
            continue

        chunks = split_into_chunks(text, max_words=max_words)
        chunk_timestamps = distribute_timestamps(segment, chunks)

        for chunk_segment in chunk_timestamps:
            start_ts = format_timestamp(chunk_segment["start"])
            end_ts   = format_timestamp(chunk_segment["end"])
            chunk_text = chunk_segment["text"]

            srt_lines.append(f"{subtitle_index}")
            srt_lines.append(f"{start_ts} --> {end_ts}")
            srt_lines.append(chunk_text)
            srt_lines.append("")  # blank line between entries
            subtitle_index += 1

    with open(srt_path, "w", encoding="utf-8") as f:
        f.write("\n".join(srt_lines))


def add_subtitles_to_video(
    videopath: str,
    segments: list[dict],
    outputpath: str,
    max_words: int = 4,
    font_size: int = 15,
    font_color: str = "white",
    margin_bottom: int = 50,
    keep_srt: bool = False,
) -> str | None:
    """
    Burn subtitles into a video file using FFmpeg's subtitle filter.

    Generates a temporary SRT file from the transcription segments, passes
    it to FFmpeg via the `subtitles` video filter (ASS style), and writes
    the output video. The SRT is deleted unless `keep_srt=True`.

    Args:
        videopath:     Path to the source video file.
        segments:      Whisper transcription segments (from extract_and_transcribe_audio).
        outputpath:    Path to write the final video with burned-in subtitles.
        max_words:     Maximum words per subtitle chunk. (default: 4)
        font_size:     ASS font size for subtitle text. (default: 15)
        font_color:    Subtitle color — 'white', 'yellow', 'cyan', or 'green'. (default: white)
        margin_bottom: Vertical margin from the bottom of the frame in pixels. (default: 50)
        keep_srt:      If True, the .srt file is not deleted after rendering. (default: False)

    Returns:
        The path to the .srt file if `keep_srt=True`, else None.

    Raises:
        ffmpeg.Error: If FFmpeg encounters an error during video processing.
        ValueError:   If an unsupported font_color is provided.
    """
    if font_color not in FONT_COLOR_MAP:
        raise ValueError(
            f"Unsupported font_color '{font_color}'. "
            f"Choose from: {', '.join(FONT_COLOR_MAP.keys())}"
        )

    # Place the SRT next to the output file
    srt_path = os.path.splitext(outputpath)[0] + ".srt"
    create_srt_file(segments, srt_path, max_words=max_words)

    color_code = FONT_COLOR_MAP[font_color]

    style = (
        f"FontName=Arial,"
        f"FontSize={font_size},"
        f"PrimaryColour={color_code},"
        f"OutlineColour=&H00000000,"
        f"Outline=1,"
        f"Alignment=2,"
        f"MarginV={margin_bottom}"
    )

    # Escape colons and backslashes in the SRT path for FFmpeg's filter syntax
    escaped_srt = srt_path.replace("\\", "/").replace(":", "\\:")

    try:
        stream = ffmpeg.input(videopath)
        stream = ffmpeg.output(
            stream,
            outputpath,
            vf=f"subtitles={escaped_srt}:force_style='{style}'",
            vcodec="libx264",
            acodec="copy",   # Audio is copied without re-encoding (lossless, fast)
            f="mp4",
        )
        ffmpeg.run(stream, overwrite_output=True, quiet=True)

    except ffmpeg.Error as e:
        stderr = e.stderr.decode() if e.stderr else "No stderr available."
        print(f"[ERROR] FFmpeg failed:\n{stderr}")
        raise

    finally:
        # Always clean up the SRT unless the user explicitly wants to keep it
        if not keep_srt and os.path.exists(srt_path):
            os.remove(srt_path)

    return srt_path if keep_srt else None
