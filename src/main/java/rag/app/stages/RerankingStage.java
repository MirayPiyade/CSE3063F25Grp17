package rag.app.stages;

import rag.app.Context;
import rag.app.StrategyRegistry;
import rag.rerank.Reranker;
import rag.retrieval.Hit;
import rag.trace.TraceBus;
import rag.trace.TraceEvent;

import java.util.List;

public class RerankingStage implements PipelineStage {

    private final Reranker reranker;

    public RerankingStage(StrategyRegistry registry) {
        this.reranker = registry.getReranker();
    }

    @Override
    public String getName() {
        return "RerankingStage";
    }

    @Override
    public void run(Context context, TraceBus traceBus) throws Exception {

        long start = System.currentTimeMillis();
        String error = null;
        List<Hit> reranked = null;
        Exception failure = null;

        try {
            reranked = reranker.rerank(
                    context.getTerms(),
                    context.getHits(),
                    null
            );
            context.setHits(reranked);

        } catch (Exception ex) {
            error = ex.getMessage();
            failure = ex;
        } finally {
            long duration = System.currentTimeMillis() - start;

            traceBus.publish(
                    new TraceEvent(
                            getName(),
                            "top=" + (reranked != null && !reranked.isEmpty()
                                    ? reranked.get(0)
                                    : "none"),
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
