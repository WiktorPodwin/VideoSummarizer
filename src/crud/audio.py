from sqlmodel import Session, select

from src.models import Audio

from uuid import UUID
from typing import List


def create_audio(session: Session, audio: Audio) -> Audio:
    """
    Creates a new record in the Audio table.

    Args:
        session (Session): An active database session.
        audio (Audio): An Audio object to be inserted into Audio table.

    Returns:
        Audio: The ingested Audio object.
    """
    session.add(audio)
    session.commit()
    session.refresh(audio)
    return audio


def get_audio(session: Session, id: UUID) -> Audio:
    """
    Retrieves a record from the Audio table by its ID.

    Args:
        session (Session): An active database session.
        id (UUID): An unique identifier of the audio.

    Returns:
        Audio: A corresponding Audio object, if found.
    """
    return session.get(Audio, id)


def get_all_audio(session: Session) -> List[Audio]:
    """
    Retrieves all records from the Audio table.

    Args:
        session (Session): An active database session.

    Returns:
        List[Audio]: A list of all Audio objects in the table.
    """
    statement = select(Audio)
    return session.exec(statement).all()


def update_audio(
    session: Session, id: UUID, transcription: str = None, summary: str = None
) -> Audio | None:
    """
    Updates an existing audio record from the Audio table.

    Args:
        session (Session): An active database session.
        id (UUID): An unique identifier of the audio.
        transcription (str): Transcribed text from the audio.
        summary (str): Summary of the transcribed audio.

    Returns:
        Audio | None: The Audio object if found and updated, else None.
    """
    audio = session.get(Audio, id)
    if transcription is None and summary is None:
        raise ValueError(
            "You have to provide either transcription or summary parameters or both."
        )
    if not audio:
        return None

    if transcription:
        audio.transcription = transcription
    if summary:
        audio.summary = summary

    session.commit()
    session.refresh(audio)
    return audio


def delete_audio(session: Session, id: UUID) -> bool:
    """
    Deletes a record from the Audio table.

    Args:
        session (Session): An active database session.
        id (UUID): An unique identifier of the audio.

    Returns:
        bool: True if the record was deleted, False if not found.
    """
    audio = session.get(Audio, id)
    if not audio:
        return False
    session.delete(audio)
    session.commit()
    return True
