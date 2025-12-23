from typing import Optional
from dataclasses import dataclass
from rag.utils.timer_utils import now


@dataclass
class TraceEvent:
    stage: str
    summary: str
    duration_ms: int
    error: Optional[str]
    timestamp: int

    def __init__(self, stage: str, summary: str, duration_ms: int, error: Optional[str]) -> None:
        self.stage = stage
        self.summary = summary
        self.duration_ms = duration_ms
        self.error = error
        self.timestamp = now()






