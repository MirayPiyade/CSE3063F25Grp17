package rag.rerank;

import rag.app.StrategyRegistry;

public class __register__ {
    static {
        StrategyRegistry.register("rerank.simple", SimpleReranker.class);
        StrategyRegistry.register("rerank.noop", NoOpReranker.class);
    }
}
