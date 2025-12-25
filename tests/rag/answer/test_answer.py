import pytest
from rag.answer.answer import Answer

def test_answer_creation():
    ans = Answer(text="Test Answer", citations=["source1", "source2"])
    assert ans.text == "Test Answer"
    assert ans.citations == ["source1", "source2"]

def test_answer_getters():
    ans = Answer(text="Hello", citations=["cite1"])
    assert ans.get_text() == "Hello"
    assert ans.get_citations() == ["cite1"]

def test_answer_immutability():
    ans = Answer(text="Immutable", citations=[])
    with pytest.raises(Exception):
        ans.text = "Changed"
