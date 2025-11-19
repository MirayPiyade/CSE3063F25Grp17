package rag.retrieval;

import java.util.*;

public class KeywordRetriever implements Retriever {

    private final int topK;

    public KeywordRetriever(int topK) {
        this.topK = topK;
    }

    @Override
    public List<Hit> retrieve(List<String> queryTerms, KeywordIndex index) {

        Map<String, Integer> scoreMap = new HashMap<>();

        for (String term : queryTerms) {
            for (KeywordIndex.Posting p : index.get(term)) {

                String key = p.docId + "::" + p.chunkId;
                scoreMap.merge(key, p.tf, Integer::sum);
            }
        }

        List<Hit> hits = new ArrayList<>();
        for (Map.Entry<String, Integer> e : scoreMap.entrySet()) {
            String[] parts = e.getKey().split("::");
            hits.add(new Hit(parts[0], parts[1], e.getValue()));
        }

        Collections.sort(hits); // deterministic

        if (hits.size() > topK) {
            return hits.subList(0, topK);
        }
        return hits;
    }
}
