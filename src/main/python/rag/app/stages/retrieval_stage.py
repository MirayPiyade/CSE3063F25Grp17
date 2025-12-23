from typing import List, Optional
from rag.app.stages.pipeline_stage import PipelineStage
from rag.app.context import Context
from rag.app.strategy_registry import StrategyRegistry
from rag.retrieval.document import Document
from rag.retrieval.hit import Hit
from rag.retrieval.retriever import Retriever
from rag.trace.trace_bus import TraceBus
from rag.trace.trace_event import TraceEvent
from rag.utils.timer_utils import now


class RetrievalStage(PipelineStage):
    def __init__(self, registry: StrategyRegistry) -> None:
        self.retriever: Retriever = registry.get_retriever()
        self.documents: List[Document] = registry.get_documents()

    def get_name(self) -> str:
        return "RetrievalStage"

    def run(self, context: Context, trace_bus: TraceBus) -> None:
        start: int = now()
        error: Optional[str] = None
        hits: Optional[List[Hit]] = None
        failure: Optional[Exception] = None

        try:
            hits = self.retriever.retrieve(
                context.get_question(),
                context.get_terms() or [],
                self.documents
            )
            context.set_hits(hits)
        except Exception as ex:
            error = str(ex)
            failure = ex
        finally:
            duration: int = now() - start
            trace_bus.publish(
                TraceEvent(
                    self.get_name(),
                    f"hits={len(hits) if hits else 0}",
                    duration,
                    error
                )
            )

        if failure is not None:
            raise failure






