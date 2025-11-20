package rag.app;

import rag.app.stages.*;
import rag.config.Config;
import rag.trace.ConsoleTraceSink;
import rag.trace.JsonlTraceSink;
import rag.trace.TraceBus;

import java.nio.file.Files;
import java.nio.file.Path;
import java.util.List;

/**
 * RagOrchestrator is the GRASP Controller.
 * It constructs the pipeline, sets up tracing, and executes the request.
 *
 * Iteration-1 Responsibilities:
 *  - Load config values (question, log path, yaml file paths)
 *  - Build strategy registry
 *  - Build pipeline (Intent → Query → Retrieval → Rerank → Answer)
 *  - Run pipeline
 *  - Print final answer to stdout
 */
public class RagOrchestrator {

    private final Config config;

    public RagOrchestrator(Config config) {
        this.config = config;
    }

    /**
     * Execute one complete RAG pipeline run.
     */
    public void run() throws Exception {

        // -------------------------
        // 1. Create Context
        // -------------------------
        Context context = new Context(config.getQuestion());

        // -------------------------
        // 2. Setup Trace Logging
        // -------------------------
        TraceBus traceBus = new TraceBus();
        Files.createDirectories(Path.of(config.getLogDir()));
        String logFile = Path.of(
                config.getLogDir(),
                "run-" + System.currentTimeMillis() + ".jsonl"
        ).toString();
        traceBus.addSink(new ConsoleTraceSink());
        traceBus.addSink(new JsonlTraceSink(logFile));

        // -------------------------
        // 3. Build Strategy Registry
        // -------------------------
        StrategyRegistry registry = new StrategyRegistry(config);

        // -------------------------
        // 4. Define Pipeline Stages (Iteration-1)
        // -------------------------
        List<PipelineStage> stages = List.of(
                new IntentDetectionStage(registry),
                new QueryWritingStage(registry),
                new RetrievalStage(registry),
                new RerankingStage(registry),
                new AnswerStage(registry),
                new FinalizeStage(registry)
        );

        DefaultPipeline pipeline = new DefaultPipeline(stages);

        // -------------------------
        // 5. Run Pipeline
        // -------------------------
        try {
            pipeline.run(context, traceBus);
        } catch (Exception ex) {
            System.err.println("Pipeline aborted: " + ex.getMessage());
        }

        if (context.getAnswer() == null) {
            context.setAnswer(registry.getFallbackHandler().buildFallback(context));
        }

        // -------------------------
        // 6. Output Final Answer
        // -------------------------
        if (context.getAnswer() != null) {
            System.out.println(context.getAnswer().getText());
            if (context.getAnswer().getCitations() != null && !context.getAnswer().getCitations().isEmpty()) {
                System.out.println("Citations: " + String.join(", ", context.getAnswer().getCitations()));
            }
        } else {
            System.out.println("No answer was produced.");
        }
    }
}
