from typing import List, Optional
from rag.app.stages.pipeline_stage import PipelineStage
from rag.app.context import Context
from rag.app.strategy_registry import StrategyRegistry
from rag.rerank.reranker import Reranker
from rag.retrieval.hit import Hit
from rag.trace.trace_bus import TraceBus
from rag.trace.trace_event import TraceEvent
from rag.utils.timer_utils import now


class RerankingStage(PipelineStage):
    def __init__(self, registry: StrategyRegistry) -> None:
        self.reranker: Reranker = registry.get_reranker()

    def get_name(self) -> str:
        return "RerankingStage"

    def run(self, context: Context, trace_bus: TraceBus) -> None:
        start: int = now()
        error: Optional[str] = None
        reranked: Optional[List[Hit]] = None
        failure: Optional[Exception] = None

        try:
            reranked = self.reranker.rerank(
                context.get_terms() or [],
                context.get_hits() or [],
                {"query": context.get_question()}
            )
            context.set_hits(reranked)
        except Exception as ex:
            error = str(ex)
            failure = ex
        finally:
            duration: int = now() - start
            top_hit: str = str(reranked[0]) if reranked and reranked else "none"
            trace_bus.publish(
                TraceEvent(
                    self.get_name(),
                    f"top={top_hit}",
                    duration,
                    error
                )
            )

        if failure is not None:
            raise failure






