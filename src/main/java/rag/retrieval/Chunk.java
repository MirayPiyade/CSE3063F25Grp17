package rag.retrieval;

import java.util.List;

public class Chunk {

    private final String docId;
    private final String chunkId;
    private final String text;
    private final List<String> tokens;
    private final int startOffset;
    private final int endOffset;
    private final String source;
    private final String title;

    public Chunk(String docId, String chunkId, String text,
                 List<String> tokens, int startOffset, int endOffset,
                 String source, String title) {
        this.docId = docId;
        this.chunkId = chunkId;
        this.text = text;
        this.tokens = tokens;
        this.startOffset = startOffset;
        this.endOffset = endOffset;
        this.source = source;
        this.title = title;
    }

    public String getDocId() { return docId; }
    public String getChunkId() { return chunkId; }
    public String getText() { return text; }
    public List<String> getTokens() { return tokens; }
    public int getStartOffset() { return startOffset; }
    public int getEndOffset() { return endOffset; }
    public String getSource() { return source; }
    public String getTitle() { return title; }
}
