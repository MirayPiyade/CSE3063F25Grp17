from typing import List, Optional
from rag.intents.intent import Intent
from rag.retrieval.hit import Hit
from rag.answer.answer import Answer


class Context:
    def __init__(self, question: str) -> None:
        self._question: str = question
        self._intent: Optional[Intent] = None
        self._terms: Optional[List[str]] = None
        self._hits: Optional[List[Hit]] = None
        self._answer: Optional[Answer] = None
        self._fallback_reason: Optional[str] = None

    def get_question(self) -> str:
        return self._question

    def get_intent(self) -> Optional[Intent]:
        return self._intent

    def set_intent(self, intent: Intent) -> None:
        self._intent = intent

    def get_terms(self) -> Optional[List[str]]:
        return self._terms

    def set_terms(self, terms: List[str]) -> None:
        self._terms = terms

    def get_hits(self) -> Optional[List[Hit]]:
        return self._hits

    def set_hits(self, hits: List[Hit]) -> None:
        self._hits = hits

    def get_answer(self) -> Optional[Answer]:
        return self._answer

    def set_answer(self, answer: Optional[Answer]) -> None:
        self._answer = answer

    def get_fallback_reason(self) -> Optional[str]:
        return self._fallback_reason

    def set_fallback_reason(self, fallback_reason: str) -> None:
        self._fallback_reason = fallback_reason

    def summary(self) -> str:
        hits_size: str = str(len(self._hits)) if self._hits else "null"
        answer_present: str = str(self._answer is not None)
        return (
            f"{{intent={self._intent}, terms={self._terms}, "
            f"hits={hits_size}, answer={answer_present}, "
            f"fallback={self._fallback_reason}}}"
        )






