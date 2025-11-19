package rag.app.stages;

import rag.app.Context;
import rag.trace.TraceBus;
import rag.trace.TraceEvent;
import rag.answer.Answer;
import rag.answer.AnswerAgent;
import rag.answer._register_;
import rag.answer.CitationValidator;

public class AnswerStage implements PipelineStage {

    private final AnswerAgent agent;
    private final CitationValidator validator = new CitationValidator();

    public AnswerStage() {
        // teammate's registry (works correctly)
        this.agent = _register_.get("template");
    }

    @Override
    public String getName() {
        return "AnswerStage";
    }

    @Override
    public void run(Context context, TraceBus traceBus) throws Exception {

        long start = System.currentTimeMillis();

        // teammate’s logic
        var hits = context.getHits();
        Answer answer = agent.generateAnswer(hits);

        boolean citationsOK = validator.validate(answer.getCitations());
        context.setAnswer(answer);

        long duration = System.currentTimeMillis() - start;

        // Correct TraceEvent call
        traceBus.publish(
            new TraceEvent(
                getName(),                 // stage
                "citations=" + citationsOK, // summary
                duration,                   // duration in ms
                null                        // no error
            )
        );
    }
}
