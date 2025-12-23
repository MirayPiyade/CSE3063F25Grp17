from typing import List, Optional
from dataclasses import dataclass


@dataclass(frozen=True)
class Answer:
    text: str
    citations: List[str]

    def get_text(self) -> str:
        return self.text

    def get_citations(self) -> List[str]:
        return self.citations






