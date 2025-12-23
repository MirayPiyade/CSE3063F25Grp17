from typing import Protocol
from rag.app.context import Context
from rag.trace.trace_bus import TraceBus


class PipelineStage(Protocol):
    def get_name(self) -> str:
        ...

    def run(self, context: Context, trace_bus: TraceBus) -> None:
        ...






