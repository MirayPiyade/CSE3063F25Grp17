package rag.app.stages;

import rag.app.Context;
import rag.trace.TraceBus;
import rag.trace.TraceEvent;
import rag.retrieval.Retriever;
import rag.retrieval.KeywordIndex;
import rag.app.StrategyRegistry;

public class RetrievalStage implements PipelineStage {

    private final Retriever retriever;
    private final KeywordIndex index;

    public RetrievalStage(StrategyRegistry registry) {
        this.retriever = registry.getRetriever();
        this.index = registry.getIndex();
    }

    @Override
    public String getName() {
        return "RetrievalStage";
    }

    @Override
    public void run(Context context, TraceBus traceBus) throws Exception {

        long start = System.currentTimeMillis();

        var hits = retriever.retrieve(context.getTerms(), index);
        context.setHits(hits);

        long duration = System.currentTimeMillis() - start;

        traceBus.publish(new TraceEvent(
            getName(),
            "hits=" + hits.size(),
            duration,
            null
        ));
    }
}
