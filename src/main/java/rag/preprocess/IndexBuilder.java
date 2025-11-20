package rag.preprocess;

import rag.retrieval.KeywordIndex;

import java.util.List;

public class IndexBuilder {

    public void addChunksToIndex(KeywordIndex index, String docId, List<Chunker.ChunkPieces> pieces) {
        addChunksToIndex(index, docId, "Unknown", docId, pieces);
    }

    public void addChunksToIndex(KeywordIndex index, String docId, String source, String title,
                                 List<Chunker.ChunkPieces> pieces) {
        index.addPieces(docId, source, title, pieces);
    }
}
