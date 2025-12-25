import pytest
from unittest.mock import patch, mock_open
import json
from rag.retrieval.document_store import DocumentStore
from rag.retrieval.document import Document

@pytest.fixture
def mock_docs_file(tmp_path):
    f = tmp_path / "docs.json"
    data = [
        {"id": "1", "source": "s1", "title": "t1", "text": "content1"},
        {"id": "2", "source": "s2", "title": "t2", "text": "content2"}
    ]
    f.write_text(json.dumps(data), encoding='utf-8')
    return str(f)

def test_load_documents(mock_docs_file):
    store = DocumentStore.load(mock_docs_file)
    docs = store.get_documents()
    assert len(docs) == 2
    assert docs[0].id == "1"
    assert docs[1].text == "content2"

def test_load_invalid_json(tmp_path):
    f = tmp_path / "bad.json"
    f.write_text("{not a list}", encoding='utf-8')
    with pytest.raises(Exception):
        DocumentStore.load(str(f))

def test_load_malformed_entry(tmp_path):
    f = tmp_path / "malformed.json"
    # Missing required fields handled safely? Implementation uses .get() with defaults
    data = [{"id": "1"}] # missing source/title/text
    f.write_text(json.dumps(data), encoding='utf-8')
    
    store = DocumentStore.load(str(f))
    docs = store.get_documents()
    assert len(docs) == 1
    assert docs[0].source == "Unknown"
