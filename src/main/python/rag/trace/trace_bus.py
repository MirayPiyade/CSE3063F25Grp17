from typing import List
from rag.trace.trace_sink import TraceSink
from rag.trace.trace_event import TraceEvent


class TraceBus:
    def __init__(self) -> None:
        self.sinks: List[TraceSink] = []

    def add_sink(self, sink: TraceSink) -> None:
        self.sinks.append(sink)

    def publish(self, e: TraceEvent) -> None:
        for sink in self.sinks:
            try:
                sink.accept(e)
            except RuntimeError as ex:
                print(f"Trace sink failed: {str(ex)}", file=__import__('sys').stderr)






