import pytest
from unittest.mock import MagicMock
from rag.app.stages.retrieval_stage import RetrievalStage
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

def test_retrieval_run(mock_registry, mock_trace_bus):
    mock_retriever = MagicMock()
    mock_docs = [MagicMock()]
    mock_registry.get_retriever.return_value = mock_retriever
    mock_registry.get_documents.return_value = mock_docs
    
    hits = [Hit(doc_id="d1", source="s1", text="t", score=1.0, title="T", embedding=None)]
    mock_retriever.retrieve.return_value = hits
    
    stage = RetrievalStage(mock_registry)
    context = Context("Q")
    context.set_terms(["term"])
    
    stage.run(context, mock_trace_bus)
    
    assert context.get_hits() == hits
    mock_retriever.retrieve.assert_called_with("Q", ["term"], mock_docs)
    mock_trace_bus.publish.assert_called_once()
