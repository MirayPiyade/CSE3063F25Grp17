from typing import Protocol, List, Any
from rag.retrieval.hit import Hit


class Reranker(Protocol):
    def rerank(self, terms: List[str], hits: List[Hit], config: Any) -> List[Hit]:
        ...






