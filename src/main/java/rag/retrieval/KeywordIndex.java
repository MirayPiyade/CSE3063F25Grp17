package rag.retrieval;

import java.util.*;
import java.util.concurrent.ConcurrentHashMap;

/**
 * A very small inverted index mapping token -> list of chunkIds + freq
 */
public class KeywordIndex {

    // token -> map(chunkId -> termFreq)
    private final Map<String, Map<String, Integer>> index = new ConcurrentHashMap<>();
    // chunkId -> Chunk (holds docId and text)
    private final Map<String, Chunk> chunkMap = new ConcurrentHashMap<>();

    public void addChunk(Chunk chunk) {
        chunkMap.put(chunk.getChunkId(), chunk);
        for (String t : chunk.getTokens()) {
            index.computeIfAbsent(t, k -> new HashMap<>());
            Map<String, Integer> posting = index.get(t);
            posting.put(chunk.getChunkId(), posting.getOrDefault(chunk.getChunkId(), 0) + 1);
        }
    }

    public List<String> lookup(String term) {
        Map<String, Integer> posting = index.get(term);
        if (posting == null) return Collections.emptyList();
        return new ArrayList<>(posting.keySet());
    }

    public Map<String, Integer> getPosting(String term) {
        return index.getOrDefault(term, Collections.emptyMap());
    }

    public Chunk getChunk(String chunkId) {
        return chunkMap.get(chunkId);
    }

    public Collection<Chunk> getAllChunks() { return chunkMap.values(); }

    public int docFrequency(String term) {
        Map<String,Integer> p = index.get(term);
        return p == null ? 0 : p.size();
    }

    public int totalChunks() { return chunkMap.size(); }
}
