import pytest
from unittest.mock import MagicMock
from rag.app.stages.reranking_stage import RerankingStage
from rag.app.context import Context
from rag.app.strategy_registry import StrategyRegistry
from rag.retrieval.hit import Hit
from rag.trace.trace_bus import TraceBus

@pytest.fixture
def mock_registry():
    return MagicMock(spec=StrategyRegistry)

@pytest.fixture
def mock_trace_bus():
    return MagicMock(spec=TraceBus)

def test_reranking_run(mock_registry, mock_trace_bus):
    mock_reranker = MagicMock()
    mock_registry.get_reranker.return_value = mock_reranker
    
    hits_in = [Hit("d1", "s1", "t", 0.5, "T", None)]
    hits_out = [Hit("d1", "s1", "t", 0.9, "T", None)]
    
    mock_reranker.rerank.return_value = hits_out
    
    stage = RerankingStage(mock_registry)
    context = Context("Q")
    context.set_hits(hits_in)
    context.set_terms(["t"])
    
    stage.run(context, mock_trace_bus)
    
    assert context.get_hits() == hits_out
    mock_reranker.rerank.assert_called_with(["t"], hits_in, {"query": "Q"})
    mock_trace_bus.publish.assert_called_once()
