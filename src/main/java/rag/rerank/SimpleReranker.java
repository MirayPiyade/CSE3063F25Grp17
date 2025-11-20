package rag.rerank;

import rag.retrieval.Hit;
import rag.utils.JsonUtils;

import java.nio.file.Files;
import java.nio.file.Path;
import java.util.ArrayList;
import java.util.Collections;
import java.util.Comparator;
import java.util.HashMap;
import java.util.List;
import java.util.Locale;
import java.util.Map;
import java.util.stream.Collectors;

public class SimpleReranker implements Reranker {

    private final double proximityBonus;
    private final int proximityWindow;
    private final double titleBoost;
    private final Map<String, Double> sourceBoosts;

    public SimpleReranker(String configPath) {
        try {
            String raw = Files.readString(Path.of(configPath));
            Map<String, Object> root = JsonUtils.expectObject(
                    JsonUtils.parse(raw),
                    "reranker.yaml must contain a JSON object"
            );
            proximityBonus = root.containsKey("proximityBonus")
                    ? ((Number) root.get("proximityBonus")).doubleValue()
                    : 0.0;
            proximityWindow = root.containsKey("proximityWindow")
                    ? ((Number) root.get("proximityWindow")).intValue()
                    : 15;
            titleBoost = root.containsKey("titleBoost")
                    ? ((Number) root.get("titleBoost")).doubleValue()
                    : 0.0;
            Map<String, Double> boosts = new HashMap<>();
            Object boostsNode = root.get("sourceBoosts");
            if (boostsNode instanceof Map<?, ?> map) {
                for (Map.Entry<?, ?> entry : map.entrySet()) {
                    boosts.put(entry.getKey().toString(), ((Number) entry.getValue()).doubleValue());
                }
            }
            sourceBoosts = boosts;
        } catch (Exception e) {
            throw new RuntimeException("Failed to read reranker config: " + e.getMessage(), e);
        }
    }

    @Override
    public List<Hit> rerank(List<String> terms, List<Hit> hits, Object cfg) {
        if (hits == null || hits.isEmpty()) {
            return Collections.emptyList();
        }
        List<String> normalizedTerms = terms == null
                ? List.of()
                : terms.stream()
                .filter(t -> t != null && !t.isBlank())
                .map(t -> t.toLowerCase(Locale.ROOT))
                .distinct()
                .collect(Collectors.toList());

        List<Hit> reranked = new ArrayList<>();
        for (Hit hit : hits) {
            double score = hit.score();
            score += computeSourceBoost(hit);
            score += computeTitleBoost(hit.title(), normalizedTerms);
            score += computeProximityBonus(hit.text(), normalizedTerms);
            reranked.add(hit.withScore(score));
        }

        reranked.sort(Comparator
                .comparingDouble(Hit::score).reversed()
                .thenComparing(Hit::docId)
                .thenComparing(Hit::chunkId));
        return reranked;
    }

    private double computeSourceBoost(Hit hit) {
        return sourceBoosts.getOrDefault(hit.source(), 0.0);
    }

    private double computeTitleBoost(String title, List<String> terms) {
        if (title == null || title.isBlank() || terms.isEmpty()) {
            return 0.0;
        }
        String lower = title.toLowerCase(Locale.ROOT);
        for (String term : terms) {
            if (lower.contains(term)) {
                return titleBoost;
            }
        }
        return 0.0;
    }

    private double computeProximityBonus(String text, List<String> terms) {
        if (text == null || text.isBlank() || terms.size() < 2 || proximityBonus == 0.0) {
            return 0.0;
        }
        String lower = text.toLowerCase(Locale.ROOT);
        for (int i = 0; i < terms.size(); i++) {
            for (int j = i + 1; j < terms.size(); j++) {
                int posA = lower.indexOf(terms.get(i));
                int posB = lower.indexOf(terms.get(j));
                if (posA >= 0 && posB >= 0 && Math.abs(posA - posB) <= proximityWindow) {
                    return proximityBonus;
                }
            }
        }
        return 0.0;
    }
}
