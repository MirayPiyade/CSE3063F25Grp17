package rag.app.stages;

import rag.app.Context;
import rag.app.StrategyRegistry;
import rag.intents.Intent;
import rag.intents.IntentDetector;
import rag.trace.TraceBus;
import rag.trace.TraceEvent;

public class IntentDetectionStage implements PipelineStage {

    private final IntentDetector detector;

    // StrategyRegistry DI (dependency injection)
    public IntentDetectionStage(StrategyRegistry registry) {
        this.detector = registry.getIntentDetector();
    }

    @Override
    public String getName() {
        return "IntentDetectionStage";
    }

    @Override
    public void run(Context context, TraceBus traceBus) throws Exception {

        long start = System.currentTimeMillis();
        String error = null;
        Intent detected = null;
        Exception failure = null;

        try {
            detected = detector.detect(context.getQuestion());
            context.setIntent(detected);
        } catch (Exception ex) {
            error = ex.getMessage();
            failure = ex;
        } finally {
            long duration = System.currentTimeMillis() - start;
            traceBus.publish(
                    new TraceEvent(
                            getName(),
                            "intent=" + detected,
                            duration,
                            error
                    )
            );
        }

        if (failure != null) {
            throw failure;
        }
    }
}
