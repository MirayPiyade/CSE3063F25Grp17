package rag.preprocess;

import rag.retrieval.Chunk;
import rag.retrieval.KeywordIndex;

import java.util.List;

public class IndexBuilder {

    /**
     * Adds chunks to the index
     */
    public void addChunksToIndex(KeywordIndex index, String docId, List<Chunker.ChunkPieces> pieces) {
        for (Chunker.ChunkPieces p : pieces) {
            Chunk c = new Chunk(p.chunkId, docId, p.text, p.tokens, p.offset);
            index.addChunk(c);
        }
    }
}
