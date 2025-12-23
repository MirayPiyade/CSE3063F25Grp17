from typing import List, Optional
from pathlib import Path
from datetime import datetime
from rag.app.context import Context
from rag.app.strategy_registry import StrategyRegistry
from rag.app.default_pipeline import DefaultPipeline
from rag.app.stages.pipeline_stage import PipelineStage
from rag.app.stages.intent_detection_stage import IntentDetectionStage
from rag.app.stages.query_writing_stage import QueryWritingStage
from rag.app.stages.retrieval_stage import RetrievalStage
from rag.app.stages.reranking_stage import RerankingStage
from rag.app.stages.answer_stage import AnswerStage
from rag.app.stages.finalize_stage import FinalizeStage
from rag.config.config import Config
from rag.answer.answer import Answer
from rag.trace.trace_bus import TraceBus
from rag.trace.console_trace_sink import ConsoleTraceSink
from rag.trace.jsonl_trace_sink import JsonlTraceSink


class RagOrchestrator:
    def __init__(self, config: Config) -> None:
        self.config: Config = config

    def run(self) -> None:
        context: Context = Context(self.config.question or "")

        trace_bus: TraceBus = TraceBus()
        Path(self.config.log_dir).mkdir(parents=True, exist_ok=True)
        timestamp: str = datetime.now().strftime("%Y%m%d-%H%M%S")
        log_file: str = str(Path(self.config.log_dir) / f"run-{timestamp}.jsonl")
        trace_bus.add_sink(ConsoleTraceSink())
        trace_bus.add_sink(JsonlTraceSink(log_file))

        registry: StrategyRegistry = StrategyRegistry(self.config)

        stages: List[PipelineStage] = [
            IntentDetectionStage(registry),
            QueryWritingStage(registry),
            RetrievalStage(registry),
            RerankingStage(registry),
            AnswerStage(registry),
            FinalizeStage(registry)
        ]

        pipeline: DefaultPipeline = DefaultPipeline(stages)

        try:
            pipeline.run(context, trace_bus)
        except Exception as ex:
            print(f"Pipeline aborted: {str(ex)}", file=__import__('sys').stderr)

        if context.get_answer() is None:
            context.set_answer(registry.get_fallback_handler().build_fallback(context))
        answer: Optional[Answer] = context.get_answer()
        if answer is not None:
            print(answer.get_text())
            citations: Optional[List[str]] = answer.get_citations()
            if citations:
                print(f"Citations: {', '.join(citations)}")
        else:
            print("No answer was produced.")






