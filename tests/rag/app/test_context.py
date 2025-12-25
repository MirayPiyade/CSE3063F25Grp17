import pytest
from rag.app.context import Context
from rag.intents.intent import Intent
from rag.answer.answer import Answer
from rag.retrieval.hit import Hit

def test_context_initialization():
    ctx = Context(question="Test Q")
    assert ctx.get_intent() is None
    assert ctx.get_terms() is None
    assert ctx.get_hits() is None

def test_intent_management():
    ctx = Context("Q")
    assert ctx.get_intent() is None
    ctx.set_intent(Intent.CourseInfo)
    assert ctx.get_intent() == Intent.CourseInfo

def test_answers():
    ctx = Context("Q")
    ans = Answer("A", [])
    ctx.set_answer(ans)
    assert ctx.get_answer() == ans

def test_hits_management():
    ctx = Context("Q")
    hit = Hit("doc1", "source1", "text", 1.0, "title", None)
    ctx.set_hits([hit])
    assert len(ctx.get_hits()) == 1
    assert ctx.get_hits()[0] == hit
