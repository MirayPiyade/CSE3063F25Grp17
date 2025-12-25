import pytest
from rag.vector.stub_vector_index import StubVectorIndex
from rag.retrieval.document import Document
from rag.vector.stub_embedding_provider import StubEmbeddingProvider

@pytest.fixture
def mock_embedding_provider():
    return StubEmbeddingProvider()

def test_stub_index_flow(mock_embedding_provider):
    doc = Document("1", "S", "T", "content")
    index = StubVectorIndex([doc], mock_embedding_provider)
    # Just ensure no error
    assert index is not None

def test_stub_vector_index_search():
    provider = StubEmbeddingProvider()
    
    doc1 = Document("1", "S", "T", "target query")
    doc2 = Document("2", "S", "T", "irrelevant")
    
    # Pass LIST of Document objects, not path string
    index = StubVectorIndex([doc1, doc2], provider)
    
    query_vec = provider.embed_query("target")
    hits = index.search(query_vec, top_k=1)
    
    assert len(hits) == 1
    assert hits[0].doc_id == "1"
    assert hits[0].score > 0
