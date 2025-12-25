import sys
import os
import pytest

# Add src/main/python to sys.path so tests can import 'rag'
# This ensures that 'import rag.answer...' works within tests
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src/main/python')))

@pytest.fixture
def mock_docs_path(tmp_path):
    d = tmp_path / "data"
    d.mkdir()
    f = d / "docs.json"
    f.write_text('[{"id": "doc1", "text": "test content", "source": "test", "title": "Test Doc"}]', encoding='utf-8')
    return str(f)
