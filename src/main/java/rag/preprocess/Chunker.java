package rag.preprocess;

import java.util.ArrayList;
import java.util.List;

public class Chunker {

    private final int chunkSize;
    private final int overlap;

    public static class ChunkPieces {
        public String chunkId;
        public String sectionId;
        public String text;
        public List<String> tokens;
        public int offset;
    }

    public Chunker(int chunkSize, int overlap) {
        this.chunkSize = chunkSize;
        this.overlap = overlap;
    }

    public List<ChunkPieces> chunkify(List<String> tokens) {
        List<ChunkPieces> pieces = new ArrayList<>();

        int id = 0;
        for (int i = 0; i < tokens.size(); i += (chunkSize - overlap)) {
            int end = Math.min(i + chunkSize, tokens.size());

            ChunkPieces p = new ChunkPieces();
            p.chunkId = "chunk_" + id++;
            p.sectionId = sectionId;
            //p.tokens = tokens.subList(i, end);
            p.tokens = new ArrayList<>(tokens.subList(i, end));
            p.text = String.join(" ", p.tokens);
            p.offset = i;

            pieces.add(p);

            if (end == tokens.size()) break;
        }

        return pieces;
    }
}

