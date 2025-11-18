package rag.intents;

import rag.app.StrategyRegistry;

public class __register__ {
    static {
        StrategyRegistry.register("intent.rule", RuleIntentDetector.class);
    }
}
