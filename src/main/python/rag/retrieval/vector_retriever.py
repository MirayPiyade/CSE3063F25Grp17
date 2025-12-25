from typing import List
from rag.retrieval.retriever import Retriever
from rag.retrieval.document import Document
from rag.retrieval.hit import Hit
from rag.vector.embedding_provider import EmbeddingProvider
from rag.vector.vector_index import VectorIndex

class VectorRetriever(Retriever):
    def __init__(self, top_k: int, embedding_provider: EmbeddingProvider, vector_index: VectorIndex) -> None:
        self.top_k = top_k
        self.embedding_provider = embedding_provider
        self.vector_index = vector_index

    def retrieve(self, question: str, terms: List[str], documents: List[Document]) -> List[Hit]:
        # 1. Generate embedding
        embedding = self.embedding_provider.embed_query(question)

        # 2. Search index
        hits = self.vector_index.search(embedding, self.top_k)
        
        return hits
