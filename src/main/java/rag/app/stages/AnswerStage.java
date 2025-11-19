package rag.app.stages;

import java.util.List;
import rag.answer.Answer;
import rag.answer.AnswerAgent;
import rag.answer.TemplateAnswerAgent;
import rag.app.Context;
import rag.retrieval.ChunkStore;
import rag.retrieval.Hit;

public class AnswerStage implements PipelineStage {

    private final AnswerAgent answerAgent;

    public AnswerStage(ChunkStore chunkStore) {
        this.answerAgent = new TemplateAnswerAgent(chunkStore);
    }

    @Override
    public void run(Context ctx) {

        List<Hit> hits = ctx.getHits();

        if (hits == null || hits.isEmpty()) {
            ctx.setAnswer(new Answer(
                    "Sorry, I couldn't help you with that.",
                    List.of()
            ));
            return;
        }

        Answer finalAnswer = answerAgent.generateAnswer(hits);

        ctx.setAnswer(finalAnswer);
    }
}
