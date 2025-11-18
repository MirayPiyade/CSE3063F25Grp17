package rag.retrieval;

import rag.preprocess.TextNormalizer;

import java.util.*;
import java.util.stream.Collectors;

/**
 * Simple keyword retriever:
 * - tokenize query
 * - for each token get posting lists and sum term frequencies as score
 */
public class KeywordRetriever implements Retriever {

    private final KeywordIndex index;
    private final TextNormalizer normalizer;

    public KeywordRetriever(KeywordIndex index) {
        this.index = index;
        this.normalizer = new TextNormalizer();
    }

    @Override
    public List<Hit> retrieve(String query) {
        List<String> terms = normalizer.tokenize(query);
        Map<String, Double> scores = new HashMap<>();

        for (String term : terms) {
            Map<String,Integer> posting = index.getPosting(term);
            for (Map.Entry<String,Integer> e : posting.entrySet()) {
                scores.put(e.getKey(), scores.getOrDefault(e.getKey(), 0.0) + e.getValue());
            }
        }

        // convert to Hits
        List<Hit> hits = scores.entrySet().stream()
                .map(en -> new Hit(index.getChunk(en.getKey()), en.getValue()))
                .sorted()
                .collect(Collectors.toList());

        // set ranks
        for (int i = 0; i < hits.size(); i++) hits.get(i).setRank(i+1);
        return hits;
    }
}

