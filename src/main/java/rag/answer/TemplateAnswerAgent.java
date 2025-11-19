package rag.answer;

import rag.retrieval.Hit;
import java.util.Collections;
import java.util.List;

public class TemplateAnswerAgent implements AnswerAgent {

    @Override
    public Answer generateAnswer(List<Hit> hits) {
        if (hits == null || hits.isEmpty()) {
            return new Answer(
                    "Sorry, I couldn't help you with that.",
                    Collections.emptyList()
            );
        }

        Hit best = hits.get(0);  // already reranked

        String answerText = String.format(
                "According to the information I found:\n\n%s\n\n(Source: %s)",
                best.getChunk().getText(),
                best.getChunk().getDocumentId()
        );

        List<String> citations = List.of(best.getChunk().getDocumentId());

        return new Answer(answerText, citations);
    }
}