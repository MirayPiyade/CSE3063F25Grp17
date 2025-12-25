from typing import List, Optional, Any
import math
from rag.rerank.reranker import Reranker
from rag.retrieval.hit import Hit
from rag.vector.embedding_provider import EmbeddingProvider

class CosineReranker(Reranker):
    def __init__(self, embedding_provider: EmbeddingProvider) -> None:
        self.embedding_provider = embedding_provider

    def rerank(self, terms: List[str], hits: List[Hit], config: Any) -> List[Hit]:
        if not hits:
            return []
        
        # Extract query from config (passed as dict)
        query = config.get("query", "") if isinstance(config, dict) else ""
        if not query:
            return hits
        
        # Generate query embedding
        query_embedding = self.embedding_provider.embed_query(query)

        reranked: List[Hit] = []
        for hit in hits:
            # If no embedding, generate on-the-fly
            doc_embedding = hit.embedding
            if not doc_embedding:
                try:
                    # Note: This might be slow for large top_k
                    doc_embedding = self.embedding_provider.embed_query(hit.text)
                except Exception:
                    # Fallback if embedding fails
                    reranked.append(hit.with_score(0.0))
                    continue
            
            score = self._cosine_similarity(query_embedding, doc_embedding)
            # Update hit with new score (and optionally embedding, but Hit is frozen/immutable so we just return new Hit with score)
            # We don't necessarily need to persist the embedding back to the hit for this scope, just the score.
            reranked.append(hit.with_score(score))

        # Deterministic sort: score desc, doc_id asc
        reranked.sort(key=lambda h: (-h.score, h.doc_id))
        return reranked

    def _cosine_similarity(self, vec_a: List[float], vec_b: List[float]) -> float:
        if len(vec_a) != len(vec_b):
            return 0.0
        
        dot_product = sum(a * b for a, b in zip(vec_a, vec_b))
        magnitude_a = math.sqrt(sum(a * a for a in vec_a))
        magnitude_b = math.sqrt(sum(b * b for b in vec_b))
        
        if magnitude_a == 0 or magnitude_b == 0:
            return 0.0
            
        return dot_product / (magnitude_a * magnitude_b)
