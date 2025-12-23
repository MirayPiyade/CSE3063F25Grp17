from dataclasses import dataclass


@dataclass(frozen=True)
class Document:
    id: str
    source: str
    title: str
    text: str






