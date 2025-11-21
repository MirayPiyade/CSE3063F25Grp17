package rag.reranker;
import java.util.*;
import java.util.stream.Collectors;
import java.nio.file.*;
import rag.retrieval.Hit;
import rag.utils.JsonUtils;


// applies heuristic scoring based on proximity, title presence and boosting
public class SimpleReranker implements Reranker {


    private final double proximityBonus;
    private final int proximityWindow;
    private final double titleBoost;
    private final Map<String, Double> sourceBoosts;

    // load configuration parameters and parse JSON/YAML file to configPath
    public SimpleReranker(String configPath) {
        try {

            // read config file
            String raw = Files.readString(Path.of(configPath));

            // parse the raw string into map
            Map<String, Object> root = JsonUtils.expectObject(
                    JsonUtils.parse(raw),
                    "reranker.yaml must contain a JSON object"
            );


            proximityBonus = root.containsKey("proximityBonus")
                    ? ((Number) root.get("proximityBonus")).doubleValue()
                    : 0.0;
            proximityWindow = root.containsKey("proximityWindow")
                    ? ((Number) root.get("proximityWindow")).intValue()
                    : 15; // default size
            titleBoost = root.containsKey("titleBoost")
                    ? ((Number) root.get("titleBoost")).doubleValue()
                    : 0.0;

            // load optional sourceBoosts map
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

    // terms are the processed search terms from the QueryWriter
    // hits are the list of hits from the Retriever
    // rContext the central RagContext object, carries all pipeline state
    @Override
    public List<Hit> rerank(List<String> terms, List<Hit> hits, Object config) {
        if (hits == null || hits.isEmpty()) {
            return Collections.emptyList();
        }

        // normalizing terms, creating a standart for searching
        List<String> normalizedTerms = terms == null
                ? List.of()
                : terms.stream()
                .filter(t -> t != null && !t.isBlank())
                .map(t -> t.toLowerCase(Locale.ROOT))
                .distinct()
                .collect(Collectors.toList());

        // the scoring formula 
        List<Hit> reranked = new ArrayList<>();
        for (Hit hit : hits) {
            double score = hit.score(); // initial score
            score += computeSourceBoost(hit);
            score += computeTitleBoost(hit.title(), normalizedTerms);
            score += computeProximityBonus(hit.text(), normalizedTerms);
            reranked.add(hit.withScore(score));
        }

        // deterministic sorting based on new scores
        reranked.sort(Comparator
                .comparingDouble(Hit::score).reversed()
                .thenComparing(Hit::docId));
                // .thenComparing(Hit::chunkId) can be added in next iteration
        return reranked;
    }

    // calculate sourceBoost
    private double computeSourceBoost(Hit hit) {
        return sourceBoosts.getOrDefault(hit.source(), 0.0);
    }

    // calculate titleBoost
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

    // calculate proximityBonus
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