package rag.app.stages;

import rag.app.Context;
import rag.trace.TraceBus;
import rag.trace.TraceEvent;
import rag.query.QueryWriter;
import rag.app.StrategyRegistry;

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

        // 🔥 ÇÖZÜM: writer.write(...) değerini List<String> olarak CAST ediyoruz
        @SuppressWarnings("unchecked")
        List<String> terms = (List<String>) writer.write(
                context.getQuestion(),
                context.getIntent()
        );

        context.setTerms(terms);

        long duration = System.currentTimeMillis() - start;

        traceBus.publish(new TraceEvent(
            getName(),
            "terms=" + terms,
            duration,
            null
        ));
    }
}
