package rag.app;

import rag.app.stages.*;

public class DefaultPipeline {

    public static PipelineStage[] build() {
        return new PipelineStage[] {
                new IntentDetectionStage(),
                new QueryWritingStage(),
                new RetrievalStage(),
                new RerankingStage(),
                new AnswerStage()
        };
    }
}
