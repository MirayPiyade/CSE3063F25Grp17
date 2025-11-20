package rag.retrieval;

import java.util.ArrayList;
import java.util.Collections;
import java.util.Comparator;
import java.util.HashMap;
import java.util.List;
import java.util.Map;

public class KeywordRetriever implements Retriever {

    private final int topK;
    private final List<String> priorityOrder;

    public KeywordRetriever(int topK, List<String> priorityOrder) {
        this.topK = topK;
        this.priorityOrder = List.copyOf(priorityOrder);
    }

    @Override
    public List<Hit> retrieve(List<String> terms, KeywordIndex index) {
        if (terms == null || terms.isEmpty()) {
            return Collections.emptyList();
        }

        Map<String, ScoreCard> scores = new HashMap<>();

        for (String term : terms) {
            if (term == null || term.isBlank()) continue;
            List<KeywordIndex.Entry> entries = index.lookup(term);
            for (KeywordIndex.Entry entry : entries) {
                Chunk chunk = index.getChunk(entry.getChunkId());
                if (chunk == null) continue;
                ScoreCard card = scores.computeIfAbsent(entry.getChunkId(), id -> new ScoreCard(chunk));
                card.score += entry.getFrequency();
            }
        }

        if (scores.isEmpty()) {
            return Collections.emptyList();
        }

        List<Hit> hits = new ArrayList<>();
        for (ScoreCard card : scores.values()) {
            Chunk chunk = card.chunk;
            hits.add(new Hit(
                    chunk.getChunkId(),
                    chunk.getDocId(),
                    chunk.getSource(),
                    chunk.getTitle(),
                    chunk.getText(),
                    card.score
            ));
        }

        Comparator<Hit> comparator = Comparator
                .comparingDouble(Hit::score).reversed()
                .thenComparing(this::priorityIndex)
                .thenComparing(Hit::docId)
                .thenComparing(Hit::chunkId);

        Map<String, List<Hit>> grouped = new HashMap<>();
        for (Hit hit : hits) {
            grouped.computeIfAbsent(hit.source(), s -> new ArrayList<>()).add(hit);
        }
        for (List<Hit> group : grouped.values()) {
            group.sort(comparator);
        }

        List<Hit> ordered = new ArrayList<>();

        for (String source : priorityOrder) {
            List<Hit> group = grouped.get(source);
            if (group == null) continue;
            for (Hit hit : group) {
                ordered.add(hit);
                if (ordered.size() >= topK) {
                    return ordered;
                }
            }
        }

        List<String> remaining = new ArrayList<>(grouped.keySet());
        remaining.removeAll(priorityOrder);
        Collections.sort(remaining);
        for (String source : remaining) {
            List<Hit> group = grouped.get(source);
            for (Hit hit : group) {
                ordered.add(hit);
                if (ordered.size() >= topK) {
                    return ordered;
                }
            }
        }

        return ordered;
    }

    private int priorityIndex(Hit hit) {
        int idx = priorityOrder.indexOf(hit.source());
        return idx >= 0 ? idx : priorityOrder.size();
    }

    private static final class ScoreCard {
        private final Chunk chunk;
        private double score;

        private ScoreCard(Chunk chunk) {
            this.chunk = chunk;
            this.score = 0;
        }
    }
}
