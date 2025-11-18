package rag.retrieval;

import rag.app.StrategyRegistry;

public class __register__ {
    static {
        StrategyRegistry.register("retriever.keyword", KeywordRetriever.class);
    }
}
