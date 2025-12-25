import pytest
from rag.rerank.noop_reranker import NoOpReranker
from rag.retrieval.hit import Hit

def test_noop_rerank():
    reranker = NoOpReranker()
    hits = [Hit("d1", "s1", "t", 1.0, "T", None)]
    
    # Needs args: terms, hits, context
    result = reranker.rerank([], hits, {})
    
    # Should return same hits, potentially same order
    assert result == hits
    assert result is hits # Check if it returns exact same list object if implementation does so
    # If not exact object, distinct check:
    assert len(result) == 1
    assert result[0].doc_id == "d1"
