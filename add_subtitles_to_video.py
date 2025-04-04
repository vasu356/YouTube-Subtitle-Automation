import os
from split_into_chunks import split_into_chunks
from distribute_timestamps import distribute_timestamps
import ffmpeg

def format_timestamp(seconds):
    """Convert seconds to SRT timestamp format (HH:MM:SS,MMM)."""
    hours = int(seconds // 3600)
    minutes = int((seconds % 3600) // 60)
    secs = int(seconds % 60)
    millis = int((seconds % 1) * 1000)
    return f"{hours:02d}:{minutes:02d}:{secs:02d},{millis:03d}"

def create_srt_file(segments, srt_path):
    """Generate an SRT file from transcription segments."""
    srt_content = ""
    subtitle_index = 1

    for segment in segments:
        text = segment["text"].strip()
        if text:
            chunks = split_into_chunks(text, max_words=4)
            chunk_timestamps = distribute_timestamps(segment, chunks)

            for chunk_segment in chunk_timestamps:
                start_time = chunk_segment["start"]
                end_time = chunk_segment["end"]
                chunk_text = chunk_segment["text"]

                srt_content += f"{subtitle_index}\n"
                srt_content += f"{format_timestamp(start_time)} --> {format_timestamp(end_time)}\n"
                srt_content += f"{chunk_text}\n\n"
                subtitle_index += 1

    with open(srt_path, "w", encoding="utf-8") as f:
        f.write(srt_content)

def add_subtitles_to_video(videopath, segments, outputpath):
    """Add subtitles to video using FFmpeg with adjusted position."""
    srt_path = "subtitles.srt"
    
    # Generate SRT file
    create_srt_file(segments, srt_path)

    try:
        # Use FFmpeg to burn subtitles into the video
        stream = ffmpeg.input(videopath)
        stream = ffmpeg.output(
            stream,
            outputpath,
            vf=(f"subtitles={srt_path}:force_style='FontName=Arial,FontSize=15,"
                f"PrimaryColour=&H00FFFFFF,OutlineColour=&H00000000,Outline=1,"
                f"Alignment=2,MarginV=50'"),  # Added MarginV for vertical positioning
            vcodec="libx264",
            acodec="copy",  # Copy audio without re-encoding
            f="mp4"
        )
        ffmpeg.run(stream, overwrite_output=True)
    except ffmpeg.Error as e:
        print(f"An error occurred: {e.stderr.decode()}")
        raise
    finally:
        # Clean up SRT file
        if os.path.exists(srt_path):
            os.remove(srt_path)