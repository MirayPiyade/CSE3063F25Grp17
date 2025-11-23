"""Answer data model."""
from dataclasses import dataclass
from typing import List


@dataclass
class Answer:
    """Generated answer with citations."""
    text: str
    citations: List[str]

