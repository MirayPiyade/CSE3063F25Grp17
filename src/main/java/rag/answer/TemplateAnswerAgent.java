package rag.answer;

import rag.retrieval.Hit;

import java.util.List;

public class TemplateAnswerAgent implements AnswerAgent {

    @Override
    public Answer generateAnswer(List<Hit> hits) {
        if (hits == null || hits.isEmpty()) {
            return null;
        }

        Hit best = hits.get(0);
        String sentence = selectSentence(best.text());
        String text = "Your answer: " + sentence +
                " Source: " + best.title() + " (" + best.docId() + ")";

        return new Answer(text, List.of(best.chunkId()));
    }

    private String selectSentence(String text) {
        if (text == null || text.isBlank()) {
            return "Relevant information is available but cannot be displayed.";
        }
        String[] sentences = text.split("(?<=[.!?])\\s+");
        return sentences.length > 0 ? sentences[0].trim() : text.trim();
    }
}
