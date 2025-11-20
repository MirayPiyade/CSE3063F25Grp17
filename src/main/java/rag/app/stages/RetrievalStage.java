package rag.app.stages;

import rag.app.Context;
import rag.app.StrategyRegistry;
import rag.retrieval.Document;
import rag.retrieval.Hit;
import rag.retrieval.Retriever;
import rag.trace.TraceBus;
import rag.trace.TraceEvent;

import java.util.List;

public class RetrievalStage implements PipelineStage {

    private final Retriever retriever;
    private final java.util.List<Document> documents;

    public RetrievalStage(StrategyRegistry registry) {
        this.retriever = registry.getRetriever();
        this.documents = registry.getDocuments();
    }

    @Override
    public String getName() {
        return "RetrievalStage";
    }

    @Override
    public void run(Context context, TraceBus traceBus) throws Exception {

        long start = System.currentTimeMillis();
        String error = null;
        List<Hit> hits = null;
        Exception failure = null;

        try {
            hits = retriever.retrieve(
                    context.getQuestion(),
                    context.getTerms(),
                    documents
            );
            context.setHits(hits);

        } catch (Exception ex) {
            error = ex.getMessage();
            failure = ex;
        } finally {
            long duration = System.currentTimeMillis() - start;

            traceBus.publish(
                    new TraceEvent(
                            getName(),
                            "hits=" + (hits != null ? hits.size() : 0),
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
