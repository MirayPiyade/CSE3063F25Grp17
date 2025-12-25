import pytest
from unittest.mock import MagicMock
from rag.answer.fallback_handler import FallbackHandler
from rag.app.context import Context
from rag.intents.intent import Intent

@pytest.fixture
def mock_context():
    return MagicMock(spec=Context)

def test_empty_question(mock_context):
    handler = FallbackHandler()
    mock_context.get_question.return_value = ""
    
    answer = handler.build_fallback(mock_context)
    
    assert answer.text == "I couldn't produce an answer because the question was empty."
    assert answer.citations == ["fallback:EmptyQuestion"]
    mock_context.set_fallback_reason.assert_called_with("EmptyQuestion")

def test_unknown_intent(mock_context):
    handler = FallbackHandler()
    mock_context.get_question.return_value = "Valid Question"
    mock_context.get_intent.return_value = Intent.Unknown
    
    answer = handler.build_fallback(mock_context)
    
    assert "unsure which topic" in answer.text
    assert answer.citations == ["fallback:UnknownIntent"]
    mock_context.set_fallback_reason.assert_called_with("UnknownIntent")

def test_none_intent(mock_context):
    handler = FallbackHandler()
    mock_context.get_question.return_value = "Valid Question"
    mock_context.get_intent.return_value = None
    
    answer = handler.build_fallback(mock_context)
    
    assert "unsure which topic" in answer.text
    assert answer.citations == ["fallback:UnknownIntent"]

def test_generic_fallback(mock_context):
    handler = FallbackHandler()
    mock_context.get_question.return_value = "Valid Question"
    mock_context.get_intent.return_value = Intent.CourseInfo # Valid intent
    # But if build_fallback is called, it means something else failed (caught by Orchestrator usually)
    # Wait, determine_reason logic says: if intent is valid, return "Unknown"
    
    answer = handler.build_fallback(mock_context)
    
    assert answer.text == "I could not produce an answer for this query."
    assert answer.citations == ["fallback:Unknown"]
    mock_context.set_fallback_reason.assert_called_with("Unknown")
