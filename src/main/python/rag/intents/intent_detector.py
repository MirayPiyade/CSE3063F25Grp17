from typing import Protocol
from rag.intents.intent import Intent


class IntentDetector(Protocol):
    def detect(self, question: str) -> Intent:
        ...






