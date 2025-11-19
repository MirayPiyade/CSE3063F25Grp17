package rag.preprocess;

import rag.retrieval.Chunk;
import rag.retrieval.ChunkStore;

import java.util.List;

public class ChunkStoreBuilder {

    private final ChunkStore store;

    public ChunkStoreBuilder(ChunkStore store) {
        this.store = store;
    }

    /*public void addChunks(List<Chunk> chunks) {
        for (Chunk c : chunks) store.put(c);
    }*/
   public void addChunks(List<Chunker.ChunkPieces> pieces, String docId) {
        
        for (Chunker.ChunkPieces p : pieces) {
            // DÜZELTME 3: "ChunkPieces" nesnesini "Chunk" nesnesine dönüştürüyoruz
            Chunk chunk = new Chunk(
                docId,           // Main'den gelen ID
                p.sectionId,     // Chunker'dan gelen Section ID
                p.chunkId,       // Chunker'dan gelen Chunk ID
                p.text,
                p.tokens,
                p.offset,
                p.offset + p.tokens.size()
            );
            
            store.put(chunk);
        }
    }

    public ChunkStore getStore() {
        return store;
    }
}
