package rag.retrieval;

import java.util.ArrayList;
import java.util.Collections;
import java.util.Comparator;
import java.util.List;
import java.util.Locale;

public class KeywordRetriever implements Retriever {

    private final int topK;
    private final List<String> priorityOrder;

    public KeywordRetriever(int topK, List<String> priorityOrder) {
        this.topK = topK;
        this.priorityOrder = List.copyOf(priorityOrder);
    }

    @Override
    public List<Hit> retrieve(String question, List<String> terms, List<Document> documents) {
        if (documents == null || documents.isEmpty()) {
            return Collections.emptyList();
        }
        String normalizedQuestion = question == null ? "" : question.toLowerCase(Locale.ROOT).trim();
        List<String> normalizedTerms = terms == null ? List.of() : terms.stream()
                .filter(t -> t != null && !t.isBlank())
                .map(t -> t.toLowerCase(Locale.ROOT))
                .toList();

        List<Hit> hits = new ArrayList<>();

        for (Document doc : documents) {
            String text = doc.text() == null ? "" : doc.text();
            String lowerText = text.toLowerCase(Locale.ROOT);
            double score = 0;

            if (!normalizedQuestion.isBlank() && lowerText.contains(normalizedQuestion)) {
                score += 2;
            }

            for (String term : normalizedTerms) {
                if (lowerText.contains(term)) {
                    score += 1;
                }
            }

            if (score > 0) {
                hits.add(new Hit(doc.id(), doc.source(), doc.title(), text, score));
            }
        }

        hits.sort(Comparator
                .comparingDouble(Hit::score).reversed()
                .thenComparing(hit -> priorityIndex(hit.source()))
                .thenComparing(Hit::docId));

        if (hits.size() > topK) {
            return new ArrayList<>(hits.subList(0, topK));
        }
        return hits;
    }

    private int priorityIndex(String source) {
        int idx = priorityOrder.indexOf(source);
        return idx >= 0 ? idx : priorityOrder.size();
    }
}
