package rag.preprocess;

import rag.retrieval.Chunk;
import rag.retrieval.ChunkStore;

import java.util.List;

public class ChunkStoreBuilder {

    private final ChunkStore store;

    public ChunkStoreBuilder(ChunkStore store) {
        this.store = store;
    }

    /**
     * Takes already created chunk pieces and pushes them into ChunkStore.
     * (Iteration 1: keeps them in memory)
     */
    public void addChunks(List<Chunk> chunks) {
        for (Chunk c : chunks) {
            store.put(c);
        }
    }

    public ChunkStore getStore() {
        return store;
    }
}
