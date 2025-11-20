package rag.answer;

import java.util.HashMap;
import java.util.Map;

public class _register_ {

    private static final Map<String, AnswerAgent> agents = new HashMap<>();

    static {
        agents.put("template", new TemplateAnswerAgent());
    }

    public static AnswerAgent get(String name) {
        return agents.get(name);
    }
}
