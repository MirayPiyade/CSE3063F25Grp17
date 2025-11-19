package rag.app;

import rag.app.stages.*;
import rag.trace.*;

import java.util.List;

public class RagOrchestrator {

    private final StrategyRegistry registry = new StrategyRegistry();

    public void run(String question) throws Exception {

        Context ctx = new Context(question);

        TraceBus bus = new TraceBus();
        bus.addSink(new JsonlTraceSink("logs/run.jsonl"));

        var pipeline = new DefaultPipeline(List.of(
                new IntentDetectionStage(registry),
                new QueryWritingStage(registry),
                new RetrievalStage(registry),
                new RerankingStage(registry),
                new AnswerStage() // teammate
        ));

        pipeline.run(ctx, bus);

        System.out.println(ctx.getAnswer().getText());
    }
}
