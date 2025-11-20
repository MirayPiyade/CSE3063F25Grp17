package rag.app.stages;

import rag.app.Context;
import rag.app.StrategyRegistry;
import rag.answer.Answer;
import rag.answer.AnswerAgent;
import rag.answer.CitationValidator;
import rag.trace.TraceBus;
import rag.trace.TraceEvent;

public class AnswerStage implements PipelineStage {

    private final AnswerAgent agent;
    private final CitationValidator validator = new CitationValidator();

    public AnswerStage(StrategyRegistry registry) {
        this.agent = registry.getAnswerAgent();
    }

    @Override
    public String getName() {
        return "AnswerStage";
    }

    @Override
    public void run(Context context, TraceBus traceBus) throws Exception {

        long start = System.currentTimeMillis();
        String error = null;
        Answer answer = null;
        Boolean citationsOK = null;
        Exception failure = null;

        try {
            answer = agent.generateAnswer(context.getHits());
            if (answer != null) {
                citationsOK = validator.validate(answer.getCitations());
                if (Boolean.TRUE.equals(citationsOK)) {
                    context.setAnswer(answer);
                } else {
                    error = "Invalid citations";
                    citationsOK = Boolean.FALSE;
                    context.setAnswer(null);
                }
            }

        } catch (Exception ex) {
            error = ex.getMessage();
            failure = ex;
        } finally {
            long duration = System.currentTimeMillis() - start;

            traceBus.publish(
                    new TraceEvent(
                            getName(),
                            "citations=" + citationsOK,
                            duration,
                            error
                    )
            );
        }

        if (failure != null) {
            throw failure;
        }
    }
}
