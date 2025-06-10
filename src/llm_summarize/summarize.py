from transformers import T5Tokenizer, T5ForConditionalGeneration, pipeline
import torch

class TextSummarizer:
    """
    Class for summarizing long text using a pretrained T5-based model.
    Automatically splits the input into manageable chunks if it's longer than the model's token limit.
    """

    def __init__(self, model_name: str = "MBZUAI/LaMini-Flan-T5-248M") -> None:
        """
        Initializes the summarization model and tokenizer.

        Args:
            model_name (str): Name or path of the pretrained summarization model.
        """

        self.tokenizer = T5Tokenizer.from_pretrained(model_name)
        self.model = T5ForConditionalGeneration.from_pretrained(
            model_name,
            device_map="auto",
            torch_dtype=torch.float32,
            offload_folder="./offload",
        )
        self.summarizer = pipeline(
            "summarization",
            model=self.model,
            tokenizer=self.tokenizer,
            max_length=500,
            min_length=50,
        )
        self.max_chunk_tokens = 500

    def summarize(self, text: str) -> str:
        """
        Summarizes the input text. If the text is longer than the model's max token limit,
        it is split into smaller chunks, each summarized independently.

        Args:
            text (str): The text to be summarized.

        Returns:
            str: A concatenated summary of all text chunks.
        """
        # Tokenize and split into chunks
        input_tokens = self.tokenizer.encode(text, return_tensors="pt", truncation=False)[0]
        chunks = []

        for i in range(0, len(input_tokens), self.max_chunk_tokens):
            chunk_tokens = input_tokens[i:i + self.max_chunk_tokens]
            chunk_text = self.tokenizer.decode(chunk_tokens, skip_special_tokens=True)
            chunks.append(chunk_text)

        # Summarize each chunk
        summaries = []
        for chunk in chunks:
            result = self.summarizer(chunk)
            summaries.append(result[0]["summary_text"])

        return "\n\n".join(summaries)

# # Funkcja do streszczenia tekstu
# def llm_summarize_text(input_text: str):
#     summarizer = pipeline(
#         "summarization",
#         model=base_model,
#         tokenizer=tokenizer,
#         max_length=500,
#         min_length=50,
#     )
#     result = summarizer(input_text)
#     return result[0]["summary_text"]