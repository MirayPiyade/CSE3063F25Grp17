from typing import TextIO
from pathlib import Path
from rag.trace.trace_sink import TraceSink
from rag.trace.trace_event import TraceEvent


class JsonlTraceSink(TraceSink):
    def __init__(self, path: str) -> None:
        self.writer: TextIO = open(path, 'a', encoding='utf-8')

    def accept(self, e: TraceEvent) -> None:
        try:
            summary: str = (e.summary.replace('"', '\\"') if e.summary else "")
            error: str = (e.error.replace('"', '\\"') if e.error else "")
            json_str: str = (
                f'{{"timestamp":{e.timestamp},"stage":"{e.stage}",'
                f'"summary":"{summary}","durationMs":{e.duration_ms},'
                f'"error":"{error}"}}\n'
            )
            self.writer.write(json_str)
            self.writer.flush()
        except Exception as ex:
            raise RuntimeError(str(ex)) from ex






