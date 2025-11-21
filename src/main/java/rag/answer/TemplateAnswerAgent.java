package rag.answer;

import java.util.ArrayList;
import java.util.Comparator;
import java.util.List;
import rag.retrieval.Hit;

public class TemplateAnswerAgent implements AnswerAgent {

    @Override
    public Answer generateAnswer(String query, List<Hit> hits) {
        if (hits == null || hits.isEmpty()) {
            return new Answer("No relevant information found.", List.of("fallback:NoHits"));
        }

        Hit bestHit = hits.get(0);
        String rawText = bestHit.text();

        // 1. Select the best sentence
        String bestSentence = selectBestSentence(query, rawText);

        // 2. Offset calculation
        int start = rawText.indexOf(bestSentence);
        int end = (start == -1) ? 0 : start + bestSentence.length();
        if (start == -1) start = 0;

        // 3. Create citation
        String citation = buildCitation(bestHit, start, end);

        // 4. Build final answer text
        String finalSentence = bestSentence;
        if (finalSentence.endsWith(".")) {
            finalSentence = finalSentence.substring(0, finalSentence.length() - 1);
        }

        String text = "Your answer: " + finalSentence + ". See: " + citation;

        return new Answer(text, List.of(citation));
    }

    private String selectBestSentence(String query, String text) {
            if (text == null || text.isBlank()) return "";

            String regex = "(?<!\\b(Mr|Mrs|Ms|Dr|Prof|Rev|Capt|Gen|Col|Lt|Maj|St|Inc|Ltd|Corp|Co|No|Fig|vb|Av)\\.)(?<=[.!?])\\s+(?=[A-ZÇĞİÖŞÜ])";
            
            String[] sentences = text.split(regex);

            if (sentences.length == 0) return text.trim();

            String[] terms = query.toLowerCase().split("\\s+");
            List<String> list = new ArrayList<>(List.of(sentences));

            return list.stream()
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
        
        // If sectionId is null or empty, default to "1" (security)
        if (sectionId == null || sectionId.isEmpty()) {
            sectionId = "1";
        }
        
        return docId + ":" + sectionId + ":" + start + "-" + end;
    }
}