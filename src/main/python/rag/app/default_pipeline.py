from typing import List, Optional
from rag.app.context import Context
from rag.app.stages.pipeline_stage import PipelineStage
from rag.trace.trace_bus import TraceBus
from rag.trace.trace_event import TraceEvent
from rag.utils.timer_utils import now


class DefaultPipeline:
    def __init__(self, stages: List[PipelineStage]) -> None:
        self.stages: List[PipelineStage] = stages

    def run(self, context: Context, trace_bus: TraceBus) -> None:
        for stage in self.stages:
            start: int = now()
            error: Optional[str] = None
            failure: Optional[Exception] = None

            try:
                stage.run(context, trace_bus)
            except Exception as ex:
                error = str(ex)
                failure = ex
            finally:
                duration: int = now() - start
                trace_bus.publish(
                    TraceEvent(
                        stage.get_name(),
                        context.summary(),
                        duration,
                        error
                    )
                )

            if failure is not None:
                raise failure

