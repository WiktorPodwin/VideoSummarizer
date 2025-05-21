from sqlmodel import Field, SQLModel
from uuid import uuid4, UUID

from .data_types import AudioSource


class Audio(SQLModel, table=True):
    """
    Represents audio data and its extracted informations.

    Attributes:
        id (UUID): A unique identifier.
        title (str): The title of the audio.
        audio_source (VideoSource): Indicates whether the audio is uploaded or sourced from YouTube.
        audio_url (str): The URL of the audio, if sourced from YouTube.
        transcribed_text (str): The transcribed text from the audio.
        summary (str): A summary of the transcribed text.
    """

    __table_args__ = {"extend_existing": True}

    id: UUID = Field(primary_key=True, default_factory=uuid4)
    title: str
    audio_source: AudioSource
    audio_url: str | None = None
    transcription: str | None = None
    summary: str | None = None
