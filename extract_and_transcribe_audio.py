from moviepy.editor import VideoFileClip
from scipy.io import wavfile
import numpy as np
from scipy.signal import resample
import whisper

def extract_and_transcribe_audio(videopath, audio_path):
    """
    Extract audio from video and transcribe it with timestamps using Whisper.
    """
    video = VideoFileClip(videopath)
    video.audio.write_audiofile(audio_path)

    sample_rate, audio_data = wavfile.read(audio_path)

    if audio_data.dtype == np.int16:
        audio_data = audio_data.astype(np.float32) / 32768.0
    elif audio_data.dtype == np.int32:
        audio_data = audio_data.astype(np.float32) / 2147483648.0
    elif audio_data.dtype == np.float32:
        pass
    else:
        raise ValueError("Unsupported audio data type")

    if len(audio_data.shape) > 1:
        audio_data = audio_data[:, 0]

    if sample_rate != 16000:
        new_length = int(len(audio_data) * (16000 / sample_rate))
        audio_data_resampled = resample(audio_data, new_length)
    else:
        audio_data_resampled = audio_data

    model = whisper.load_model("base")
    result = model.transcribe(audio_data_resampled, word_timestamps=False)
    return result["segments"]