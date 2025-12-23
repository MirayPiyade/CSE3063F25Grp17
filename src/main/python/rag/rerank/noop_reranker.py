from typing import List, Any
from rag.rerank.reranker import Reranker
from rag.retrieval.hit import Hit


class NoOpReranker(Reranker):
    def rerank(self, terms: List[str], hits: List[Hit], config: Any) -> List[Hit]:
        return hits






