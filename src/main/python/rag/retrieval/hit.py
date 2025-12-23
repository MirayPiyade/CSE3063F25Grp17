from dataclasses import dataclass, replace


@dataclass(frozen=True)
class Hit:
    doc_id: str
    source: str
    title: str
    text: str
    score: float

    def with_score(self, new_score: float) -> 'Hit':
        return replace(self, score=new_score)

    def __str__(self) -> str:
        return f"{self.doc_id}@{self.source} score={self.score}"






