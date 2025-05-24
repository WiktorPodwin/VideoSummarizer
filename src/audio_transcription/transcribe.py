from transformers import WhisperProcessor, WhisperForConditionalGeneration
import numpy as np
import torch


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

    def text_transcription(
        self, audio: np.ndarray, sampling_rate: int | float, chunk_length_s: int = 25
    ) -> str:
        """
        Transcribes text from an audio time series.

        Args:
            audio (np.ndarray): The audio waveform.
            sampling_rate (int | float): The sampling rate of the audio.
            chunk_length_s (int): The length of each audio chunk in seconds. Default is 25 seconds.

        Returns:
            str: The transcribed text.
        """
        chunk_size = int(sampling_rate * chunk_length_s)
        chunks = [audio[i : i + chunk_size] for i in range(0, len(audio), chunk_size)]

        min_valid_chunk = int(sampling_rate * 5)
        if len(chunks) > 1 and len(chunks[-1]) < min_valid_chunk:
            shortage = min_valid_chunk - len(chunks[-1])
            borrow = min(shortage, len(chunks[-2]) // 2)

            chunks[-2] = chunks[-2][:-borrow]
            chunks[-1] = np.concatenate((chunks[-2][-borrow:], chunks[-1]))

        full_transcription = []
        for chunk in chunks:
            inputs = self.processor(
                chunk, sampling_rate=sampling_rate, return_tensors="pt", language="en"
            )

            if "attention_mask" not in inputs:
                inputs["attention_mask"] = torch.ones_like(
                    inputs["input_features"], dtype=torch.long
                )

            with torch.no_grad():
                predicted_ids = self.model.generate(
                    inputs["input_features"], attention_mask=inputs["attention_mask"]
                )
                transcription = self.processor.batch_decode(
                    predicted_ids, skip_special_tokens=True
                )[0]
                full_transcription.append(transcription)

        return " ".join(full_transcription)
