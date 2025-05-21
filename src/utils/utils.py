import os

from pydub import AudioSegment


def convert_to_wav(input_path: str) -> str:
    wav_output = os.path.splitext(input_path)[0] + ".wav"
    audio = AudioSegment.from_file(input_path)
    audio = audio.set_frame_rate(16000).set_channels(1)
    audio.export(wav_output, format="wav")
    return wav_output
