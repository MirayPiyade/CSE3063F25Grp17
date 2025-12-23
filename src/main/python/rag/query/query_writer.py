from typing import Protocol, List
from rag.intents.intent import Intent


class QueryWriter(Protocol):
    def write(self, question: str, intent: Intent) -> List[str]:
        ...






