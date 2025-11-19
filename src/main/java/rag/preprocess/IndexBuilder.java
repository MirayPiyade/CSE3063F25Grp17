package rag.preprocess;

import rag.retrieval.KeywordIndex;

import java.util.List;

public class IndexBuilder {

    public void addChunksToIndex(KeywordIndex index, String docId, List<Chunker.ChunkPieces> pieces) {

        for (Chunker.ChunkPieces p : pieces) {
            for (String token : p.tokens) {
                index.add(token, docId, p.chunkId);
            }
        }
    }
}
