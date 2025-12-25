import pytest
from unittest.mock import MagicMock
from rag.app.stages.query_writing_stage import QueryWritingStage
from rag.app.context import Context
from rag.app.strategy_registry import StrategyRegistry
from rag.intents.intent import Intent
from rag.trace.trace_bus import TraceBus

@pytest.fixture
def mock_registry():
    return MagicMock(spec=StrategyRegistry)

@pytest.fixture
def mock_trace_bus():
    return MagicMock(spec=TraceBus)

def test_query_writing_run(mock_registry, mock_trace_bus):
    mock_writer = MagicMock()
    mock_registry.get_query_writer.return_value = mock_writer
    mock_writer.write.return_value = ["term1", "term2"]
    
    stage = QueryWritingStage(mock_registry)
    context = Context("Q")
    context.set_intent(Intent.CourseInfo)
    
    stage.run(context, mock_trace_bus)
    
    assert context.get_terms() == ["term1", "term2"]
    mock_writer.write.assert_called_with("Q", Intent.CourseInfo)
    mock_trace_bus.publish.assert_called_once()
