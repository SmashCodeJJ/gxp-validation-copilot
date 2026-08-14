from collections.abc import Sequence

from sentence_transformers import SentenceTransformer


class EmbeddingService:
    def __init__(
        self,
        model_name: str,
    ) -> None:
        self.model_name = model_name

        self.model = SentenceTransformer(
            model_name
        )

    def embed_text(
        self,
        text: str,
    ) -> list[float]:

        cleaned_text = text.strip()

        if not cleaned_text:
            raise ValueError(
                "Text cannot be empty."
            )

        embedding = self.model.encode(
            cleaned_text,
            normalize_embeddings=True,
        )

        return embedding.tolist()

    def embed_texts(
        self,
        texts: Sequence[str],
    ) -> list[list[float]]:

        cleaned_texts = [
            text.strip()
            for text in texts
        ]

        if not cleaned_texts:
            return []

        if any(
            not text
            for text in cleaned_texts
        ):
            raise ValueError(
                "Embedding input cannot contain empty text."
            )

        embeddings = self.model.encode(
            cleaned_texts,
            normalize_embeddings=True,
        )

        return embeddings.tolist()