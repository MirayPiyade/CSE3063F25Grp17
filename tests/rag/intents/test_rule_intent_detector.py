import json
import pytest

from rag.intents.rule_intent_detector import RuleIntentDetector
from rag.intents.intent import Intent

@pytest.fixture
def mock_intents_file(tmp_path):
    f = tmp_path / "intents.json"
    data = {
        "CourseInfo": {
            "keywords": ["course", "syllabus"],
            "regex": ".*course.*"
        },
        "FeeInfo": { # If FeeInfo not in Intent Enum, parser returns Unknown
            "keywords": ["fee", "tuition"]
        }
    }
    f.write_text(json.dumps(data), encoding='utf-8')
    return str(f)

def test_detector_init(mock_intents_file):
    detector = RuleIntentDetector(mock_intents_file)
    assert detector is not None

def test_detect_by_keyword(mock_intents_file):
    detector = RuleIntentDetector(mock_intents_file)
    # "tuition" is in FeeInfo keywords
    intent = detector.detect("What is the tuition?")
    assert intent == Intent.FeeInfo

def test_detect_by_regex(mock_intents_file):
    detector = RuleIntentDetector(mock_intents_file)
    # "course" is in regex
    intent = detector.detect("Show me the course details")
    assert intent == Intent.CourseInfo

def test_detect_by_keyword(mock_intents_file):
    detector = RuleIntentDetector(mock_intents_file)
    assert detector.detect("I need course syllabus") == Intent.CourseInfo
    assert detector.detect("unknown keywords") == Intent.Unknown
    assert detector.detect("CoUrSe") == Intent.CourseInfo
