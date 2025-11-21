package rag.answer;

import rag.retrieval.Hit;

import java.util.ArrayList;
import java.util.Comparator;
import java.util.List;

public class TemplateAnswerAgent implements AnswerAgent {

    @Override
    public Answer generateAnswer(List<Hit> hits, String query) {
        if (hits == null || hits.isEmpty()) {
            return null;
        }

        String effectiveQuery = query == null ? "" : query;
        Hit bestHit = hits.get(0);
        String rawText = bestHit.text() == null ? "" : bestHit.text();

        String bestSentence = selectBestSentence(effectiveQuery, rawText);

        int start = rawText.indexOf(bestSentence);
        if (start < 0) start = 0;
        int end = Math.min(rawText.length(), start + bestSentence.length());

        String citation = buildCitation(bestHit, start, end);

        String finalSentence = bestSentence;
        if (!finalSentence.endsWith(".")) {
            finalSentence = finalSentence + ".";
        }

        String text = "Your answer: " + finalSentence + " See: " + citation;

        return new Answer(text, List.of(citation));
    }

    private String selectBestSentence(String query, String text) {
        if (text == null || text.isBlank()) {
            return "Relevant information is available but cannot be displayed.";
        }

        String regex = "(?<!\\b(Mr|Mrs|Ms|Dr|Prof|Rev|Capt|Gen|Col|Lt|Maj|St|Inc|Ltd|Corp|Co|No|Fig|vb|Av)\\.)(?<=[.!?])\\s+(?=[A-ZÇĞİÖŞÜ])";
        String[] sentences = text.split(regex);
        if (sentences.length == 0) {
            return text.trim();
        }

        String[] terms = query.toLowerCase().split("\\s+");
        List<String> options = new ArrayList<>(List.of(sentences));

        return options.stream()
                .max(Comparator.comparingInt(s -> matchCount(s, terms)))
                .orElse(sentences[0])
                .trim();
    }

    private int matchCount(String sentence, String[] terms) {
        String normalized = sentence.toLowerCase();
        int score = 0;
        for (String term : terms) {
            if (!term.isBlank() && normalized.contains(term)) {
                score++;
            }
        }
        return score;
    }

    private String buildCitation(Hit hit, int start, int end) {
        String docId = hit.docId();
        String sectionId = hit.source();
        if (sectionId == null || sectionId.isBlank()) {
            sectionId = "1";
        }
        return docId + ":" + sectionId + ":" + start + "-" + end;
    }
}
