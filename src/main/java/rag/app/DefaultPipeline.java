package rag.app;

import rag.app.stages.PipelineStage;
import rag.trace.TraceBus;
import rag.trace.TraceEvent;
import java.util.List;

public class DefaultPipeline {

    private final List<PipelineStage> stages;

    public DefaultPipeline(List<PipelineStage> stages) {
        this.stages = stages;
    }

    public void run(Context context, TraceBus traceBus) throws Exception {

        for (PipelineStage stage : stages) {

            long start = System.currentTimeMillis();
            String error = null;

            try {
                stage.run(context, traceBus);
            } catch (Exception ex) {
                error = ex.getMessage();
            }

            long duration = System.currentTimeMillis() - start;

            traceBus.publish(
                new TraceEvent(
                    stage.getName(),
                    context.summary(),
                    duration,
                    error
                )
            );
        }
    }
}
