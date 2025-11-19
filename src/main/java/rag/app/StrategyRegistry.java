package rag.app;

import rag.intents.*;
import rag.query.*;
import rag.retrieval.*;
import rag.rerank.*;

public class StrategyRegistry {

    public IntentDetector getIntentDetector() {
        return new RuleIntentDetector();
    }

    public QueryWriter getQueryWriter() {
        return new HeuristicQueryWriter();
    }

    public Retriever getRetriever() {
        return new KeywordRetriever();
    }

    public Reranker getReranker() {
        return new SimpleReranker();
    }

    public KeywordIndex getIndex() {
        return KeywordIndex.load("data/keyword_index.json");
    }
}
