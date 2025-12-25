import pytest
from unittest.mock import MagicMock
from rag.app.stages.finalize_stage import FinalizeStage
from rag.app.context import Context
from rag.app.strategy_registry import StrategyRegistry
from rag.answer.answer import Answer
from rag.trace.trace_bus import TraceBus

@pytest.fixture
def mock_registry():
    return MagicMock(spec=StrategyRegistry)

@pytest.fixture
def mock_trace_bus():
    return MagicMock(spec=TraceBus)

def test_finalize_answer_ready(mock_registry, mock_trace_bus):
    mock_handler = MagicMock()
    mock_registry.get_fallback_handler.return_value = mock_handler
    
    stage = FinalizeStage(mock_registry)
    context = Context("Q")
    context.set_answer(Answer("Valid", []))
    
    stage.run(context, mock_trace_bus)
    
    assert context.get_fallback_reason() == "AnswerReady"
    mock_handler.build_fallback.assert_not_called()

def test_finalize_needs_fallback(mock_registry, mock_trace_bus):
    mock_handler = MagicMock()
    mock_registry.get_fallback_handler.return_value = mock_handler
    fallback_ans = Answer("Fallback", [])
    mock_handler.build_fallback.return_value = fallback_ans
    
    stage = FinalizeStage(mock_registry)
    context = Context("Q")
    # No answer set
    
    stage.run(context, mock_trace_bus)
    
    assert context.get_answer() == fallback_ans
    mock_handler.build_fallback.assert_called_with(context)
