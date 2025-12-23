from typing import Protocol, Optional, List
from rag.answer.answer import Answer
from rag.retrieval.hit import Hit


class AnswerAgent(Protocol):
    def generate_answer(self, hits: List[Hit], query: str) -> Optional[Answer]:
        ...






