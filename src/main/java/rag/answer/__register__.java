package rag.answer;

import rag.app.StrategyRegistry;

public class __register__ {
    static {
        StrategyRegistry.register("answer.template", TemplateAnswerAgent.class);
    }
}
