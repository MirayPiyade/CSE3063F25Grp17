import pytest

from rag.vector.stub_embedding_provider import StubEmbeddingProvider

def test_stub_embedding_deterministic():
    provider = StubEmbeddingProvider()
    e1 = provider.embed_query("hello")
    e2 = provider.embed_query("hello")
    assert e1 == e2

def test_stub_embedding_dimension():
    provider = StubEmbeddingProvider()
    e1 = provider.embed_query("test")
    # Implementation might produce 1536 dims or similar
    assert len(e1) > 0
    assert all(isinstance(x, float) for x in e1)

def test_stub_embedding_similarity():
    # Since it uses hashing, "apple" and "apple" are identical (dist=0, sim=1)
    # "apple" and "orange" should be different
    provider = StubEmbeddingProvider()
    v1 = provider.embed_query("apple")
    v2 = provider.embed_query("orange")
    assert v1 != v2
