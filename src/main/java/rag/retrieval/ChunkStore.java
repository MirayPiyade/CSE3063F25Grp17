package rag.retrieval;

import java.util.Collection;
import java.util.concurrent.ConcurrentHashMap;

/**
 * In-memory chunk store for iteration1. Later can serialize to disk.
 */
public class ChunkStore {
    private final ConcurrentHashMap<String, Chunk> store = new ConcurrentHashMap<>();

    public void put(Chunk c) { store.put(c.getChunkId(), c); }
    public Chunk get(String chunkId) { return store.get(chunkId); }
    public Collection<Chunk> allChunks() { return store.values(); }
    public boolean contains(String chunkId) { return store.containsKey(chunkId); }
}

