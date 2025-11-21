package rag.answer;

import rag.app.Context;
import rag.intents.Intent;

import java.util.List;

public class FallbackHandler {

    public Answer buildFallback(Context context) {
        String reason = determineReason(context);
        context.setFallbackReason(reason);
        String message = switch (reason) {
            case "EmptyQuestion" -> "I couldn't produce an answer because the question was empty.";
            case "UnknownIntent" -> "I am unsure which topic you are asking about. Please rephrase the question.";
            default -> "I could not produce an answer for this query.";
        };
        return new Answer(message, List.of("fallback:" + reason));
    }

    private String determineReason(Context context) {
        if (context.getQuestion() == null || context.getQuestion().isBlank()) {
            return "EmptyQuestion";
        }
        Intent intent = context.getIntent();
        if (intent == null || intent == Intent.Unknown) {
            return "UnknownIntent";
        }

        return "Unknown";
    }
}
