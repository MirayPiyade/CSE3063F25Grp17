from typing import Protocol, List
from rag.retrieval.hit import Hit

class VectorIndex(Protocol):
    def search(self, query_vector: List[float], top_k: int) -> List[Hit]:
        """Searches the index for the nearest neighbors to the query vector."""
        ...
