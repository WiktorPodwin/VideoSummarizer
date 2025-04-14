from transformers import WhisperProcessor, WhisperForConditionalGeneration
import numpy as np


class AudioTranscription:
    """
    Class for transcribing text from an audio file using a pretrained speech-to_text model.
    """

    def __init__(self, model: str) -> None:
        """
        Args:
            model (str): The name or path of a pretrained speech-to-text model.
        """
        self.processor = WhisperProcessor.from_pretrained(model)
        self.model = WhisperForConditionalGeneration.from_pretrained(model)

    def text_transcription(self, audio: np.ndarray, sampling_rate: int | float) -> str:
        """
        Transcribes text from an audio time series.

        Args:
            audio (np.ndarray): The audio waveform.
            sampling_rate (int | float): The sampling rate of the audio.

        Returns:
            str: The transcribed text.
        """
        inputs = self.processor(audio, sampling_rate=sampling_rate, return_tensors="pt")
        predicted_ids = self.model.generate(inputs["input_features"])
        return self.processor.batch_decode(predicted_ids, skip_special_tokens=True)[0]
