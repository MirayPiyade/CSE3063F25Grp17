import pytest
from unittest.mock import MagicMock
from rag.retrieval.vector_retriever import VectorRetriever
from rag.retrieval.document import Document
from rag.retrieval.hit import Hit
# Assuming interfaces are available
from rag.vector.vector_index import VectorIndex
from rag.vector.embedding_provider import EmbeddingProvider

def test_vector_retriever_flow():
    mock_provider = MagicMock(spec=EmbeddingProvider)
    mock_index = MagicMock(spec=VectorIndex)
    
    mock_provider.embed_query.return_value = [0.1, 0.2]
    expected_hits = [Hit("1", "s", "t", "txt", 0.9)]
    mock_index.search.return_value = expected_hits
    
    retriever = VectorRetriever(top_k=3, embedding_provider=mock_provider, vector_index=mock_index)
    
    hits = retriever.retrieve("query", [], []) # docs arg ignored by VectorRetriever usually? 
    # Logic check: VectorRetriever.retrieve signature takes documents, but implementation ignores them 
    # because it searches the index.
    
    assert hits == expected_hits
    mock_provider.embed_query.assert_called_with("query")
    mock_index.search.assert_called_with([0.1, 0.2], 3)
