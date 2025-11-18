package rag.app;

import rag.app.stages.PipelineStage;

public class RagOrchestrator {
    private PipelineStage[] stages;

    public RagOrchestrator(PipelineStage[] stages) {
        this.stages = stages;
    }

    public rag.answer.Answer run(String question) {
        Context ctx = new Context(question);
        for (PipelineStage stage : stages)
            stage.run(ctx);
        return ctx.getAnswer();
    }
}
