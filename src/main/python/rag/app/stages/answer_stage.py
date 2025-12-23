from typing import Optional
from rag.app.stages.pipeline_stage import PipelineStage
from rag.app.context import Context
from rag.app.strategy_registry import StrategyRegistry
from rag.answer.answer import Answer
from rag.answer.answer_agent import AnswerAgent
from rag.answer.citation_validator import CitationValidator
from rag.trace.trace_bus import TraceBus
from rag.trace.trace_event import TraceEvent
from rag.utils.timer_utils import now


class AnswerStage(PipelineStage):
    def __init__(self, registry: StrategyRegistry) -> None:
        self.agent: AnswerAgent = registry.get_answer_agent()
        self.validator: CitationValidator = CitationValidator()

    def get_name(self) -> str:
        return "AnswerStage"

    def run(self, context: Context, trace_bus: TraceBus) -> None:
        start: int = now()
        error: Optional[str] = None
        answer: Optional[Answer] = None
        citations_ok: Optional[bool] = None
        failure: Optional[Exception] = None

        try:
            answer = self.agent.generate_answer(
                context.get_hits() or [],
                context.get_question()
            )
            if answer is not None:
                citations_ok = self.validator.validate(answer.get_citations())
                if citations_ok:
                    context.set_answer(answer)
                else:
                    error = "Invalid citations"
                    citations_ok = False
                    context.set_answer(None)
        except Exception as ex:
            error = str(ex)
            failure = ex
        finally:
            duration: int = now() - start
            trace_bus.publish(
                TraceEvent(
                    self.get_name(),
                    f"citations={citations_ok}",
                    duration,
                    error
                )
            )

        if failure is not None:
            raise failure






