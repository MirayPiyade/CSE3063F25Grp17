from abc import ABC, abstractmethod

from rag.intents.intent import Intent


class IntentDetector(ABC):

    @abstractmethod
    def detect(self, question: str) -> Intent:
        pass

