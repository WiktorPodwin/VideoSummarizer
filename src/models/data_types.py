from enum import Enum


class AudioSource(str, Enum):
    """
    Enumeration of possible audio sources.

    Attributes:
        YOUTUBE: Indicates the audio was downloaded from YouTube.
        UPLOADED: Indicates the audio was manually uploaded by the user.
    """

    YOUTUBE = "YouTube"
    UPLOADED = "uploaded"
