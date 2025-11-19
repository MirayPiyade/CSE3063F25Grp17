package rag.answer;

import java.util.HashMap;
import java.util.Map;

public class _register_ {

    private static final Map<String, AnswerAgent> AGENTS = new HashMap<>();

    static {
        AGENTS.put("template", new TemplateAnswerAgent());
    }

    public static AnswerAgent get(String name) {
        return AGENTS.getOrDefault(name, new TemplateAnswerAgent());
    }
}