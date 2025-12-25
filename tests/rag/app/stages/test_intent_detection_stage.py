import pytest
from unittest.mock import MagicMock
from rag.app.stages.intent_detection_stage import IntentDetectionStage
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

def test_intent_detection_run(mock_registry, mock_trace_bus):
    # Setup mocks
    mock_detector = MagicMock()
    mock_registry.get_intent_detector.return_value = mock_detector
    mock_detector.detect.return_value = Intent.CourseInfo
    
    stage = IntentDetectionStage(mock_registry)
    context = Context(question="Test Q")
    
    stage.run(context, mock_trace_bus)
    
    assert context.get_intent() == Intent.CourseInfo
    mock_trace_bus.publish.assert_called_once()
    mock_detector.detect.assert_called_with("Test Q")

def test_intent_detection_exception(mock_registry, mock_trace_bus):
    mock_detector = MagicMock()
    mock_registry.get_intent_detector.return_value = mock_detector
    mock_detector.detect.side_effect = Exception("Detection Error")
    
    stage = IntentDetectionStage(mock_registry)
    context = Context("Q")
    
    with pytest.raises(Exception):
        stage.run(context, mock_trace_bus)
    
    # Trace bus should still publish failure event
    mock_trace_bus.publish.assert_called_once()
