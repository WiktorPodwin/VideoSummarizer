import os
from attrs import define


@define
class BaseConfig:
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    DATA_DIR = os.path.join(BASE_DIR, "data")

    AUDIO_TRANSCRIPTION_MODEL = "openai/whisper-tiny"
