import pytest
from rag.retrieval.hit import Hit

def test_hit_creation():
    hit = Hit("doc1", "source1", "Title", "Text", 1.0)
    assert hit.doc_id == "doc1"
    assert hit.score == 1.0
    assert str(hit) == "doc1@source1 score=1.0"

def test_hit_with_score():
    hit = Hit("doc1", "source1", "Title", "Text", 1.0)
    new_hit = hit.with_score(2.0)
    
    assert hit.score == 1.0  # Original unchanged (frozen)
    assert new_hit.score == 2.0
    assert new_hit.doc_id == hit.doc_id
