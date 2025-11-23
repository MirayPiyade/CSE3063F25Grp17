from abc import ABC, abstractmethod
from typing import List

from rag.intents.intent import Intent


class QueryWriter(ABC):


    @abstractmethod
    def write(self, question: str, intent: Intent) -> List[str]:
        pass
