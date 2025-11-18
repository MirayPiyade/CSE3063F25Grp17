package rag.retrieval;

import java.util.List;

public class Chunk {
    private final String chunkId;
    private final String docId;
    private final String text;
    private final List<String> tokens;
    private final int offset;

    public Chunk(String chunkId, String docId, String text, List<String> tokens, int offset) {
        this.chunkId = chunkId;
        this.docId = docId;
        this.text = text;
        this.tokens = tokens;
        this.offset = offset;
    }

    public String getChunkId() { return chunkId; }
    public String getDocId() { return docId; }
    public String getText() { return text; }
    public List<String> getTokens() { return tokens; }
    public int getOffset() { return offset; }
}
