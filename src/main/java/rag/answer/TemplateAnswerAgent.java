package rag.answer;

import rag.retrieval.Chunk;
import rag.retrieval.ChunkStore;
import rag.retrieval.Hit;

import java.util.Collections;
import java.util.List;

public class TemplateAnswerAgent implements AnswerAgent {

    private final ChunkStore chunkStore;

    public TemplateAnswerAgent(ChunkStore chunkStore) {
        this.chunkStore = chunkStore;
    }

    @Override
    public Answer generateAnswer(List<Hit> hits) {

        if (hits == null || hits.isEmpty()) {
            return new Answer(
                    "Sorry, I couldn't help you with that.",
                    Collections.emptyList()
            );
        }

        Hit best = hits.get(0);

        Chunk chunk = chunkStore.get(best.chunkId);

        if (chunk == null) {
            return new Answer(
                    "Sorry, I couldn't find the chunk related to this result.",
                    Collections.emptyList()
            );
        }

        String answerText = String.format(
                "According to the information I found:\n\n%s\n\n(Source: %s)",
                chunk.getText(),
                chunk.getDocId()
        );

        List<String> citations = List.of(chunk.getDocId());

        return new Answer(answerText, citations);
    }
}
