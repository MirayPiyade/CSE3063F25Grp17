from typing import Optional
from rag.app.stages.pipeline_stage import PipelineStage
from rag.app.context import Context
from rag.app.strategy_registry import StrategyRegistry
from rag.intents.intent import Intent
from rag.intents.intent_detector import IntentDetector
from rag.trace.trace_bus import TraceBus
from rag.trace.trace_event import TraceEvent
from rag.utils.timer_utils import now


class IntentDetectionStage(PipelineStage):
    def __init__(self, registry: StrategyRegistry) -> None:
        self.detector: IntentDetector = registry.get_intent_detector()

    def get_name(self) -> str:
        return "IntentDetectionStage"

    def run(self, context: Context, trace_bus: TraceBus) -> None:
        start: int = now()
        error: Optional[str] = None
        detected: Optional[Intent] = None
        failure: Optional[Exception] = None

        try:
            detected = self.detector.detect(context.get_question())
            context.set_intent(detected)
        except Exception as ex:
            error = str(ex)
            failure = ex
        finally:
            duration: int = now() - start
            trace_bus.publish(
                TraceEvent(
                    self.get_name(),
                    f"intent={detected}",
                    duration,
                    error
                )
            )

        if failure is not None:
            raise failure






