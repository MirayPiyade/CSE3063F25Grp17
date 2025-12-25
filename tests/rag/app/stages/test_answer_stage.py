import pytest
from unittest.mock import MagicMock, patch
from rag.app.stages.answer_stage import AnswerStage
from rag.app.context import Context
from rag.app.strategy_registry import StrategyRegistry
from rag.answer.answer import Answer
from rag.retrieval.hit import Hit
from rag.trace.trace_bus import TraceBus

@pytest.fixture
def mock_registry():
    return MagicMock(spec=StrategyRegistry)

@pytest.fixture
def mock_trace_bus():
    return MagicMock(spec=TraceBus)

def test_answer_stage_success(mock_registry, mock_trace_bus):
    mock_agent = MagicMock()
    mock_registry.get_answer_agent.return_value = mock_agent
    
    ans = Answer("My Answer", ["cite1"])
    mock_agent.generate_answer.return_value = ans
    
    # Mock validator to pass
    with patch("rag.app.stages.answer_stage.CitationValidator") as mock_validator_cls:
        mock_validator = mock_validator_cls.return_value
        mock_validator.validate.return_value = True
        
        stage = AnswerStage(mock_registry)
        context = Context("Q")
        context.set_hits([Hit("d1", "s1", "t", 1.0, "T", None)])
        
        stage.run(context, mock_trace_bus)
        
        assert context.get_answer() == ans
        mock_trace_bus.publish.assert_called_once()

def test_answer_stage_invalid_citations(mock_registry, mock_trace_bus):
    mock_agent = MagicMock()
    mock_registry.get_answer_agent.return_value = mock_agent
    
    ans = Answer("My Answer", ["cite1"])
    mock_agent.generate_answer.return_value = ans
    
    with patch("rag.app.stages.answer_stage.CitationValidator") as mock_validator_cls:
        mock_validator = mock_validator_cls.return_value
        mock_validator.validate.return_value = False
        
        stage = AnswerStage(mock_registry)
        context = Context("Q")
        
        stage.run(context, mock_trace_bus)
        
        assert context.get_answer() is None
        # Should log error in trace
        args, _ = mock_trace_bus.publish.call_args
        event = args[0]
        assert event.error == "Invalid citations"
