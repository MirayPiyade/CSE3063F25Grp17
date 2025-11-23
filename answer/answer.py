from dataclasses import dataclass
from typing import List

@dataclass
class Answer:
    text: str
    citations: List[str]


