"""
Audio extraction and Whisper transcription module.

Extracts audio from a video file, resamples it to 16 kHz mono
(as required by Whisper), and returns timestamped transcription segments.
"""

import numpy as np
from moviepy.editor import VideoFileClip
from scipy.io import wavfile
from scipy.signal import resample
import whisper


def extract_and_transcribe_audio(
    videopath: str,
    audio_path: str,
    model_size: str = "base",
    language: str | None = None,
) -> list[dict]:
    """
    Extract audio from a video file and transcribe it using OpenAI Whisper.

    Args:
        videopath:   Path to the source video file.
        audio_path:  Temporary path to write the extracted WAV audio.
        model_size:  Whisper model size — 'tiny', 'base', 'small', 'medium', or 'large'.
                     Larger models are more accurate but require more memory and time.
        language:    BCP-47 language code (e.g. 'en', 'hi', 'es'). Pass None to
                     let Whisper auto-detect the language from the audio.

    Returns:
        A list of segment dicts, each containing:
            - 'text'  (str)   : Transcribed text for this segment.
            - 'start' (float) : Start time in seconds.
            - 'end'   (float) : End time in seconds.

    Raises:
        ValueError: If the audio data type from the WAV file is not supported.
        FileNotFoundError: If the video file does not exist (propagated from moviepy).
    """
    # --- Step 1: Extract audio from video ---
    video = VideoFileClip(videopath)
    video.audio.write_audiofile(audio_path, logger=None)
    video.close()

    # --- Step 2: Read and normalize the WAV file ---
    sample_rate, audio_data = wavfile.read(audio_path)

    # Normalize to float32 in [-1.0, 1.0] — Whisper requires float32 audio
    if audio_data.dtype == np.int16:
        audio_data = audio_data.astype(np.float32) / 32768.0
    elif audio_data.dtype == np.int32:
        audio_data = audio_data.astype(np.float32) / 2147483648.0
    elif audio_data.dtype == np.float32:
        pass  # Already in the correct format
    else:
        raise ValueError(
            f"Unsupported audio dtype: {audio_data.dtype}. "
            "Expected int16, int32, or float32."
        )

    # --- Step 3: Convert stereo → mono (take left channel) ---
    if audio_data.ndim > 1:
        audio_data = audio_data[:, 0]

    # --- Step 4: Resample to 16 kHz (Whisper's required sample rate) ---
    if sample_rate != 16000:
        new_length = int(len(audio_data) * (16000 / sample_rate))
        audio_data = resample(audio_data, new_length)

    # --- Step 5: Load Whisper model and transcribe ---
    print(f"      Loading Whisper '{model_size}' model...")
    model = whisper.load_model(model_size)

    transcribe_kwargs = {"word_timestamps": False}
    if language:
        transcribe_kwargs["language"] = language

    result = model.transcribe(audio_data, **transcribe_kwargs)

    detected = result.get("language", "unknown")
    if not language:
        print(f"      Auto-detected language: {detected}")

    return result["segments"]
