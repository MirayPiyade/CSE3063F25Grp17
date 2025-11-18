package rag.preprocess;

import rag.retrieval.Chunk;

import java.util.ArrayList;
import java.util.List;
import java.util.UUID;

public class Chunker {
    private final int windowSize; // token count per chunk
    private final int stride;

    public Chunker(int windowSize, int stride) {
        this.windowSize = windowSize;
        this.stride = stride;
    }

    /**
     * tokens: tüm doküman tokenleri
     * returns list of Chunk-like lightweight objects (we'll construct Chunk later with docId)
     */
    public List<ChunkPieces> chunkify(List<String> tokens) {
        List<ChunkPieces> out = new ArrayList<>();
        for (int start = 0; start < tokens.size(); start += stride) {
            int end = Math.min(start + windowSize, tokens.size());
            List<String> sub = tokens.subList(start, end);
            String text = String.join(" ", sub);
            String chunkId = UUID.randomUUID().toString();
            out.add(new ChunkPieces(chunkId, text, new ArrayList<>(sub), start));
            if (end == tokens.size()) break;
        }
        return out;
    }

    public static class ChunkPieces {
        public final String chunkId;
        public final String text;
        public final List<String> tokens;
        public final int offset;

        public ChunkPieces(String chunkId, String text, List<String> tokens, int offset) {
            this.chunkId = chunkId;
            this.text = text;
            this.tokens = tokens;
            this.offset = offset;
        }
    }
}
