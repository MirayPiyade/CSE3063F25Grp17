package rag.retrieval;

import java.util.HashMap;
import java.util.Map;

public class ChunkStore {

    private final Map<String, Chunk> chunks = new HashMap<>();

    public void put(Chunk chunk) {
        chunks.put(chunk.getChunkId(), chunk);
    }

    public Chunk get(String chunkId) {
        return chunks.get(chunkId);
    }

    public boolean contains(String chunkId) {
        return chunks.containsKey(chunkId);
    }
}
