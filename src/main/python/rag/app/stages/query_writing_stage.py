from typing import List, Optional
from rag.app.stages.pipeline_stage import PipelineStage
from rag.app.context import Context
from rag.app.strategy_registry import StrategyRegistry
from rag.query.query_writer import QueryWriter
from rag.trace.trace_bus import TraceBus
from rag.trace.trace_event import TraceEvent
from rag.utils.timer_utils import now


class QueryWritingStage(PipelineStage):
    def __init__(self, registry: StrategyRegistry) -> None:
        self.writer: QueryWriter = registry.get_query_writer()

    def get_name(self) -> str:
        return "QueryWritingStage"

    def run(self, context: Context, trace_bus: TraceBus) -> None:
        start: int = now()
        error: Optional[str] = None
        terms: Optional[List[str]] = None
        failure: Optional[Exception] = None

        try:
            terms = self.writer.write(
                context.get_question(),
                context.get_intent()
            )
            context.set_terms(terms)
        except Exception as ex:
            error = str(ex)
            failure = ex
        finally:
            duration: int = now() - start
            trace_bus.publish(
                TraceEvent(
                    self.get_name(),
                    f"terms={terms}",
                    duration,
                    error
                )
            )

        if failure is not None:
            raise failure






