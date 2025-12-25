from typing import Protocol, List

class EmbeddingProvider(Protocol):
    def embed_query(self, text: str) -> List[float]:
        """Generates an embedding vector for the given query text."""
        ...
