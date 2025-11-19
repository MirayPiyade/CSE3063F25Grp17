package rag.retrieval;

import java.util.List;

public class Chunk {

    private final String docId;
    private final String sectionId;
    private final String chunkId;
    private final String text;
    private final List<String> tokens;
    private final int startOffset;
    private final int endOffset;

    public Chunk(String docId, String sectionId, String chunkId, String text,
                 List<String> tokens, int startOffset, int endOffset) {
        this.docId = docId;
        this.sectionId = sectionId;
        this.chunkId = chunkId;
        this.text = text;
        this.tokens = tokens;
        this.startOffset = startOffset;
        this.endOffset = endOffset;
    }

    public String getDocId() { return docId; }
    public String getChunkId() { return chunkId; }
    public String getText() { return text; }
    public List<String> getTokens() { return tokens; }
    public int getStartOffset() { return startOffset; }
    public int getEndOffset() { return endOffset; }
}
