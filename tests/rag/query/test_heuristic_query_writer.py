import json
import pytest

from rag.query.heuristic_query_writer import HeuristicQueryWriter
from rag.intents.intent import Intent

@pytest.fixture
def mock_stopwords(tmp_path):
    f = tmp_path / "stopwords.json"
    data = {
        "stopwords": ["the", "is", "a", "an"],
        "boosters": {
            "CourseInfo": ["syllabus", "grading", "curriculum"],
            "Unknown": ["general", "computer", "engineering"]
        } 
    }
    f.write_text(json.dumps(data), encoding='utf-8')
    return str(f)

def test_query_writer_basic(mock_stopwords):
    writer = HeuristicQueryWriter(mock_stopwords)
    terms = writer.write("The quick brown fox", Intent.Unknown)
    # Should remove 'the', keep others
    assert "quick" in terms
    assert "brown" in terms
    assert "fox" in terms
    assert "the" not in terms

def test_query_writer_normalization(mock_stopwords):
    writer = HeuristicQueryWriter(mock_stopwords)
    terms = writer.write("Capitals And Punctuations!", Intent.Unknown)
    assert "capitals" in terms
    assert "punctuations" in terms # assuming it strips punctuation

def test_query_writer_domain_expansion(mock_stopwords):
    writer = HeuristicQueryWriter(mock_stopwords)
    # If "course" is in query, it typically adds synonyms like "syllabus"
    # Checking implementation details...
    terms = writer.write("computer course", Intent.CourseInfo)
    assert "course" in terms
    assert "syllabus" in terms # assuming expansion logic exists for 'course'
    assert "curriculum" in terms # assuming expansion logic exists

def test_query_writer_comp_e_expansion(mock_stopwords):
    writer = HeuristicQueryWriter(mock_stopwords)
    terms = writer.write("cse", Intent.Unknown)
    assert "computer" in terms
    assert "engineering" in terms
