from typing import List, Dict, Any, Optional
from pathlib import Path
from rag.rerank.reranker import Reranker
from rag.rerank.cosine_reranker import CosineReranker
from rag.retrieval.hit import Hit
from rag.utils.json_utils import JsonUtils
from rag.vector.embedding_provider import EmbeddingProvider
from rag.rerank.reranker import Reranker

class HybridReranker(Reranker):
    def __init__(self, config_path: str, embedding_provider: EmbeddingProvider) -> None:
        self.cosine_reranker = CosineReranker(embedding_provider)
        try:
            raw: str = Path(config_path).read_text(encoding='utf-8')
            # Simple YAML parser (since we can't use complex libs and JsonUtils is for JSON)
            root: Dict[str, Any] = {}
            for line in raw.splitlines():
                if ":" in line and not line.strip().startswith("#"):
                    key, val = line.split(":", 1)
                    root[key.strip()] = float(val.strip())
            
            self.alpha: float = float(root.get("alpha", 0.5))
            self.beta: float = float(root.get("beta", 0.5))
        except Exception as e:
            raise RuntimeError(f"Failed to read hybrid reranker config: {str(e)}") from e

    def rerank(self, terms: List[str], hits: List[Hit], config: Any) -> List[Hit]:
        if not hits:
            return []

        # 1. Get Vector Scores (Cosine Similarity)
        # We invoke cosine reranker but we need to map results back to original hits to preserve data
        vector_hits = self.cosine_reranker.rerank(terms, hits, config)
        
        # Create a map for O(1) lookup
        vector_scores = {h.doc_id: h.score for h in vector_hits}
        
        # 2. Compute Hybrid Score
        hybrid_hits: List[Hit] = []
        for hit in hits:
            # Original score comes from the retriever (keyword or vector)
            original_score = hit.score
            
            # Vector score calculated freshly by CosineReranker
            vec_score = vector_scores.get(hit.doc_id, 0.0)
            
            # Formula: final = alpha * vector + beta * original
            # Note: We assume original_score might need normalization in a real system, 
            # but per requirements we just combine them.
            final_score = (self.alpha * vec_score) + (self.beta * original_score)
            
            hybrid_hits.append(hit.with_score(final_score))

        # Deterministic sort
        hybrid_hits.sort(key=lambda h: (-h.score, h.doc_id))
        return hybrid_hits
