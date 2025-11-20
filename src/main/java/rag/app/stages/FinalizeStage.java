package rag.app.stages;

import rag.answer.Answer;
import rag.answer.FallbackHandler;
import rag.app.Context;
import rag.app.StrategyRegistry;
import rag.trace.TraceBus;
import rag.trace.TraceEvent;

public class FinalizeStage implements PipelineStage {

    private final FallbackHandler fallbackHandler;

    public FinalizeStage(StrategyRegistry registry) {
        this.fallbackHandler = registry.getFallbackHandler();
    }

    @Override
    public String getName() {
        return "FinalizeStage";
    }

    @Override
    public void run(Context context, TraceBus traceBus) throws Exception {
        long start = System.currentTimeMillis();
        String error = null;
        boolean usedFallback = false;
        Exception failure = null;

        try {
            Answer answer = context.getAnswer();
            if (answer == null || answer.getText() == null || answer.getText().isBlank()) {
                Answer fallback = fallbackHandler.buildFallback(context);
                context.setAnswer(fallback);
                usedFallback = true;
            } else {
                context.setFallbackReason("AnswerReady");
            }
        } catch (Exception ex) {
            error = ex.getMessage();
            failure = ex;
        } finally {
            long duration = System.currentTimeMillis() - start;
            traceBus.publish(new TraceEvent(
                    getName(),
                    usedFallback ? "fallback=" + context.getFallbackReason() : "answer-ready",
                    duration,
                    error
            ));
        }

        if (failure != null) {
            throw failure;
        }
    }
}
