package rag.answer;

import rag.retrieval.Hit;
import java.util.List;

public class TemplateAnswerAgent implements AnswerAgent {
    @Override
    public Answer answer(List<Hit> hits) {
        // TODO pick best sentence
        return new Answer("TODO answer");
    }
}
