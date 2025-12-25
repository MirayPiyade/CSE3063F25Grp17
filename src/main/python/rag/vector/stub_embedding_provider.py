from typing import List
from rag.vector.embedding_provider import EmbeddingProvider

class StubEmbeddingProvider(EmbeddingProvider):
    def embed_query(self, text: str) -> List[float]:
        # Simple deterministic hashing (Hash Trick)
        # Allows "apple ok" and "apple" to have some overlap, unlike random.
        dim = 1536
        vector = [0.0] * dim
        
        words = text.lower().split()
        if not words:
            return vector
            
        for word in words:
            # Hash word to an index 0..1535
            h = hash(word) % dim
            vector[h] += 1.0
            
        # Normalize
        magnitude = sum(x*x for x in vector) ** 0.5
        if magnitude > 0:
            vector = [x / magnitude for x in vector]
            
        return vector
