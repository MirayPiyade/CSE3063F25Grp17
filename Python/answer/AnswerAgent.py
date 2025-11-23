"""Answer agent interface."""
from abc import ABC, abstractmethod
from typing import List

from rag.answer.answer import Answer
from rag.retrieval.hit import Hit


class AnswerAgent(ABC):
    """Interface for answer generation."""

    @abstractmethod
    def generate_answer(self, hits: List[Hit], query: str) -> Answer:
        """Generate answer from retrieved hits."""
        pass

