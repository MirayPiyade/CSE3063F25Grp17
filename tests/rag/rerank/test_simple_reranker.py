import json
import pytest

from rag.rerank.simple_reranker import SimpleReranker
from rag.retrieval.hit import Hit

@pytest.fixture
def mock_reranker_config(tmp_path):
    f = tmp_path / "reranker.json"
    data = {
        "sourceBoosts": {
            "source1": 2.0,
            "source2": 0.5
        }
    }
    f.write_text(json.dumps(data), encoding='utf-8')
    return str(f)

def test_simple_reranker_boost(mock_reranker_config):
    reranker = SimpleReranker(mock_reranker_config)
    
    h1 = Hit("d1", "source1", "t1", "text", 1.0, None)
    h2 = Hit("d2", "source2", "t2", "text", 1.0, None)
    h3 = Hit("d3", "unknown", "t3", "text", 1.0, None)
    
    hits = [h2, h3, h1] # unsorted input
    
    # Context usually contains 'query'
    reranked = reranker.rerank([], hits, {})
    
    # h1 (source1) gets 2.0 * 1.0 = 2.0
    # h2 (source2) gets 0.5 * 1.0 = 0.5
    # h3 (unknown) gets 1.0 * 1.0 = 1.0 (assuming default of 1.0 if not listed)
    
    assert reranked[0].doc_id == "d1"
    assert reranked[1].doc_id == "d2"
    assert reranked[2].doc_id == "d3"
    
    assert reranked[0].score == 3.0
    assert reranked[2].score == 1.0
    assert reranked[1].score == 1.5

def test_simple_reranker_load_error():
    with pytest.raises(Exception):
        SimpleReranker("/non/existent/path.yaml")
