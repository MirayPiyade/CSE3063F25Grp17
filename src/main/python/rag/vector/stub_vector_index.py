from typing import List, Dict, Tuple, Any
import math
from rag.vector.vector_index import VectorIndex
from rag.retrieval.hit import Hit
from rag.retrieval.document import Document
from rag.vector.embedding_provider import EmbeddingProvider

class StubVectorIndex(VectorIndex):
    def __init__(self, documents: List[Document], embedding_provider: EmbeddingProvider) -> None:
        self.items: List[Dict[str, Any]] = []
        
        # Build index in memory
        for doc in documents:
            embedding = embedding_provider.embed_query(doc.text)
            self.items.append({
                "doc": doc,
                "embedding": embedding
            })

    def search(self, query_vector: List[float], top_k: int) -> List[Hit]:
        scored: List[Tuple[float, Dict]] = []
        
        for item in self.items:
            doc_vec = item["embedding"]
            score = self._cosine_similarity(query_vector, doc_vec)
            scored.append((score, item))
            
        # Sort by score desc
        scored.sort(key=lambda x: x[0], reverse=True)
        
        hits: List[Hit] = []
        for score, item in scored[:top_k]:
            doc = item["doc"]
            hits.append(Hit(
                doc_id=doc.id,
                source=doc.source,
                title=doc.title,
                text=doc.text,
                score=score,
                embedding=item["embedding"]
            ))
            
        return hits

    def _cosine_similarity(self, vec1: List[float], vec2: List[float]) -> float:
        dot_product = sum(a * b for a, b in zip(vec1, vec2))
        norm_a = sum(a * a for a in vec1) ** 0.5
        norm_b = sum(b * b for b in vec2) ** 0.5
        if norm_a == 0 or norm_b == 0:
            return 0.0
        return dot_product / (norm_a * norm_b)
