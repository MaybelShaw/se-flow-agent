from abc import ABC, abstractmethod
from typing import List
from sentence_transformers import SentenceTransformer

class EmbeddingInterface:
    @abstractmethod
    def embed_texts(
        self,
        texts: List[str],
    ) -> List[List[float]]:
        pass

class SentenceTransformerEmbedder(EmbeddingInterface):
    def __init__(self, model_name="all-MiniLM-L6-v2"):
        self.model = SentenceTransformer(model_name)

    def embed_texts(
        self,
        texts: List[str],
    ) -> List[List[float]]:
        embeddings = self.model.encode(texts, convert_to_tensor=False)
        return embeddings


if __name__ == "__main__":
    sample_texts = [
        "This is a sample sentence.",
        "Another example of text to embed."
    ]
    embedding_model = SentenceTransformerEmbedder()
    embeddings = embedding_model.embed_texts(sample_texts)
    for i, emb in enumerate(embeddings):
        print(f"Text: {sample_texts[i]}\nEmbedding: {emb}\n")
