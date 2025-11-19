package rag.retrieval;

import java.util.*;

public class KeywordIndex {

    public static class Posting {
        public final String docId;
        public final String chunkId;
        public final int tf;

        public Posting(String docId, String chunkId, int tf) {
            this.docId = docId;
            this.chunkId = chunkId;
            this.tf = tf;
        }
    }

    private final Map<String, List<Posting>> index = new HashMap<>();

    public void add(String token, String docId, String chunkId, int tf) {
        index.computeIfAbsent(token, k -> new ArrayList<>())
             .add(new Posting(docId, chunkId, tf));
    }

    public List<Posting> get(String token) {
        return index.getOrDefault(token, Collections.emptyList());
    }
}
