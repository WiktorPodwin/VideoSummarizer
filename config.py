import os
from attrs import define


@define
class BaseConfig:
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))

    AUDIO_TRANSCRIPTION_MODEL = "openai/whisper-tiny"
