from typing import Protocol
from rag.trace.trace_event import TraceEvent


class TraceSink(Protocol):
    def accept(self, event: TraceEvent) -> None:
        ...






