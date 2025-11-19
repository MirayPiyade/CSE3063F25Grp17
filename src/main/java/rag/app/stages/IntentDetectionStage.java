package rag.app.stages;

import rag.app.Context;
import rag.trace.TraceBus;
import rag.trace.TraceEvent;
import rag.intents.Intent;
import rag.intents.IntentDetector;
import rag.app.StrategyRegistry;

public class IntentDetectionStage implements PipelineStage {

    private final IntentDetector detector;

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

        Intent intent = detector.detect(context.getQuestion());
        context.setIntent(intent);

        long duration = System.currentTimeMillis() - start;

        traceBus.publish(new TraceEvent(
                getName(),
                "intent=" + intent,
                duration,
                null
        ));
    }
}
