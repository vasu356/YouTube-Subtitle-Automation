from extract_and_transcribe_audio import extract_and_transcribe_audio
from add_subtitles_to_video import add_subtitles_to_video
import os

if __name__ == "__main__":
    videopath = "video.mp4"
    audio_path = "audio.wav"
    outputpath = "output_video_with_subtitles.mp4"

    # Extract audio and transcribe
    segments = extract_and_transcribe_audio(videopath, audio_path)
    print("Transcription Segments:")
    for segment in segments:
        print(f"Text: {segment['text']}, Start: {segment['start']}, End: {segment['end']}")

    # Add subtitles to video using FFmpeg
    add_subtitles_to_video(videopath, segments, outputpath)

    # Clean up temporary audio file
    os.remove(audio_path)