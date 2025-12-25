from dataclasses import dataclass, replace
from typing import Optional, List


@dataclass(frozen=True)
class Hit:
    doc_id: str
    source: str
    title: str
    text: str
    score: float
    embedding: Optional[List[float]] = None

    def with_score(self, new_score: float) -> 'Hit':
        return replace(self, score=new_score)

    def __str__(self) -> str:
        return f"{self.doc_id}@{self.source} score={self.score}"






