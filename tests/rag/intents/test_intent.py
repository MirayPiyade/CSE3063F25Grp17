import pytest
from rag.intents.intent import Intent

def test_intent_mapping():
    # Verify intents exist
    assert Intent.CourseInfo
    assert Intent.Unknown
    
    assert str(Intent.CourseInfo) == "Intent.CourseInfo"
