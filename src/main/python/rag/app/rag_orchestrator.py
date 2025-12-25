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
from rag.cache.query_cache import QueryCache
from rag.answer.answer import Answer
from rag.trace.trace_bus import TraceBus
from rag.trace.console_trace_sink import ConsoleTraceSink
from rag.trace.jsonl_trace_sink import JsonlTraceSink
from rich.console import Console
from rich.markdown import Markdown
from rich.panel import Panel
from rich.text import Text


class RagOrchestrator:
    def __init__(self, config: Config) -> None:
        self.config: Config = config

    def run(self) -> None:
        self.run_with_context()

    def run_with_context(self) -> Context:
        cache = QueryCache() 
        question = self.config.question or ""
        
        context: Context = Context(question)

        # 0. Check Cache
        if self.config.cache_enabled:
            cached = cache.get(question, self.config)
            if cached:
                # Print cached answer directly
                console = Console()
                console.print(Panel(Markdown(cached.get_text()), title="[bold magenta]Cached Answer[/bold magenta]", border_style="magenta"))
                citations = cached.get_citations()
                if citations:
                    citation_text = ", ".join(citations)
                    console.print(Panel(Text(citation_text, style="italic #C8A2C8"), title="[bold #C8A2C8]Citations[/bold #C8A2C8]", border_style="#C8A2C8"))
                
                # Hydrate context from cache for evaluator
                # (Evaluator needs context state, even if cached)
                # But wait, if cached, we don't have Hits!
                # Evaluator Hit Rate requires Hits.
                # If cached, we skip retrieval -> Hit Rate is undefined or requires Stored Hits?
                # For Evaluation, we usually want to BYPASS cache to test Retrieval.
                # So let's disable cache if we want to measure retrieval.
                # Assuming evaluator config will disable cache.
                return context

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
        
        # Save to Cache
        # Save to Cache
        if answer is not None and self.config.cache_enabled:
             cache.put(question, self.config, answer)
        
        console = Console()
        if answer is not None:
            console.print(Panel(Markdown(answer.get_text()), title="[bold magenta]Answer[/bold magenta]", border_style="magenta"))
            citations: Optional[List[str]] = answer.get_citations()
            if citations:
                citation_text = ", ".join(citations)
                console.print(Panel(Text(citation_text, style="italic #C8A2C8"), title="[bold #C8A2C8]Citations[/bold #C8A2C8]", border_style="#C8A2C8"))
        else:
            console.print(Panel("[bold red]No answer was produced.[/bold red]", title="Error", border_style="red"))
            
        return context






