package rag.query;

import rag.app.StrategyRegistry;

public class __register__ {
    static {
        StrategyRegistry.register("query.heuristic", HeuristicQueryWriter.class);
    }
}
