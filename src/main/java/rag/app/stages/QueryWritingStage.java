package rag.app.stages;

import rag.app.Context;
import rag.app.StrategyRegistry;
import rag.query.QueryWriter;
import rag.trace.TraceBus;
import rag.trace.TraceEvent;

import java.util.List;

public class QueryWritingStage implements PipelineStage {

    private final QueryWriter writer;

    public QueryWritingStage(StrategyRegistry registry) {
        this.writer = registry.getQueryWriter();
    }

    @Override
    public String getName() {
        return "QueryWritingStage";
    }

    @Override
    public void run(Context context, TraceBus traceBus) throws Exception {

        long start = System.currentTimeMillis();
        String error = null;
        List<String> terms = null;
        Exception failure = null;

        try {
            terms = writer.write(
                    context.getQuestion(),
                    context.getIntent()
            );
            context.setTerms(terms);

        } catch (Exception ex) {
            error = ex.getMessage();
            failure = ex;
        } finally {
            long duration = System.currentTimeMillis() - start;

            traceBus.publish(
                    new TraceEvent(
                            getName(),
                            "terms=" + terms,
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
