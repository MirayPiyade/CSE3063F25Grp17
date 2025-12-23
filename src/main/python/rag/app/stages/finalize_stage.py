from typing import Optional
from rag.app.stages.pipeline_stage import PipelineStage
from rag.answer.answer import Answer
from rag.answer.fallback_handler import FallbackHandler
from rag.app.context import Context
from rag.app.strategy_registry import StrategyRegistry
from rag.trace.trace_bus import TraceBus
from rag.trace.trace_event import TraceEvent
from rag.utils.timer_utils import now


class FinalizeStage(PipelineStage):
    def __init__(self, registry: StrategyRegistry) -> None:
        self.fallback_handler: FallbackHandler = registry.get_fallback_handler()

    def get_name(self) -> str:
        return "FinalizeStage"

    def run(self, context: Context, trace_bus: TraceBus) -> None:
        start: int = now()
        error: Optional[str] = None
        used_fallback: bool = False
        failure: Optional[Exception] = None

        try:
            answer: Optional[Answer] = context.get_answer()
            if answer is None or not answer.get_text() or not answer.get_text().strip():
                fallback: Answer = self.fallback_handler.build_fallback(context)
                context.set_answer(fallback)
                used_fallback = True
            else:
                context.set_fallback_reason("AnswerReady")
        except Exception as ex:
            error = str(ex)
            failure = ex
        finally:
            duration: int = now() - start
            summary: str = (
                f"fallback={context.get_fallback_reason()}"
                if used_fallback
                else "answer-ready"
            )
            trace_bus.publish(
                TraceEvent(
                    self.get_name(),
                    summary,
                    duration,
                    error
                )
            )

        if failure is not None:
            raise failure






