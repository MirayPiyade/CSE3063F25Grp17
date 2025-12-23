from rag.trace.trace_sink import TraceSink
from rag.trace.trace_event import TraceEvent


class ConsoleTraceSink(TraceSink):
    def accept(self, event: TraceEvent) -> None:
        error_str: str = event.error if event.error else "-"
        print(f"[TRACE] {event.stage} | summary={event.summary} | duration={event.duration_ms}ms | error={error_str}")






