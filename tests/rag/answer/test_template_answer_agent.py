import pytest
from rag.answer.template_answer_agent import TemplateAnswerAgent
from rag.retrieval.hit import Hit

@pytest.fixture
def simple_hits():
    return [
        Hit(
            doc_id="doc1",
            source="source1",
            text="First sentence. Second sentence mentions keyword. Third sentence.",
            score=1.0,
            title="Title",
            embedding=None
        )
    ]

def test_generate_answer_no_hits():
    agent = TemplateAnswerAgent()
    assert agent.generate_answer([], "query") is None

def test_generate_answer_basic_extraction(simple_hits):
    agent = TemplateAnswerAgent()
    # Query matches "keyword" in second sentence
    ans = agent.generate_answer(simple_hits, "keyword")
    
    assert ans is not None
    assert "Second sentence mentions keyword." in ans.text
    assert "See: doc1:source1:" in ans.text

def test_abbreviation_handling():
    agent = TemplateAnswerAgent()
    hit = Hit(
        doc_id="d1", source="s1", score=1.0, title="T", embedding=None,
        text="Dr. Smith is here. He is nice."
    )
    
    # "Dr." should not split the sentence
    ans = agent.generate_answer([hit], "smith")
    
    # It should pick the whole first sentence including "Dr."
    assert "Dr. Smith is here." in ans.text

def test_default_sentence_no_match(simple_hits):
    agent = TemplateAnswerAgent()
    # Query matches nothing
    ans = agent.generate_answer(simple_hits, "xyz")
    
    # Should default to first sentence
    assert "First sentence." in ans.text

def test_citation_format(simple_hits):
    agent = TemplateAnswerAgent()
    ans = agent.generate_answer(simple_hits, "first")
    
    # format: Your answer: ... See: doc_id:source:start-end
    assert ans.citations[0].startswith("doc1:source1:")
