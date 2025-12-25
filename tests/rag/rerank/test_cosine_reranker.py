import pytest
from unittest.mock import MagicMock
from rag.rerank.cosine_reranker import CosineReranker
from rag.retrieval.hit import Hit
# Assuming EmbeddingProvider is in vector module
from rag.vector.embedding_provider import EmbeddingProvider

def test_cosine_reranker():
    # Mock embedding provider
    mock_provider = MagicMock()
    # Query vector: [1, 0]
    mock_provider.embed_query.return_value = [1.0, 0.0]
    
    reranker = CosineReranker(mock_provider)
    
    # Hit 1: aligned with query [1, 0]
    h1 = Hit("d1", "s", "t", "text", 0.0, [1.0, 0.0])
    # Hit 2: orthogonal [0, 1]
    h2 = Hit("d2", "s", "t", "text", 0.0, [0.0, 1.0])
    # Hit 3: no embedding (should be penalized or ignored/kept at 0?)
    h3 = Hit("d3", "s", "t", "text", 0.0, None)
    
    hits = [h2, h3, h1]
    
    reranked = reranker.rerank([], hits, {"query": "test"})
    
    # h1 cosine similarity should be 1.0
    # h2 cosine similarity should be 0.0
    # h3 ? Impl detail: probably -1 or 0 if None
    
    assert reranked[0].doc_id == "d1"
    assert reranked[0].score > 0.9
    
    # Confirm h1 is top
    mock_provider.embed_query.assert_any_call("test")

def test_cosine_missing_query():
    reranker = CosineReranker(MagicMock())
    hits = [Hit("d1", "s", "t", "text", 1.0, None)]
    
    # If query missing in context, what happens?
    # Logically returns original hits
    reranked = reranker.rerank([], hits, {})
    assert len(reranked) == 1
    assert reranked[0].doc_id == "d1"
    # Wait, need to check implementation if it raises or catches
    pass
