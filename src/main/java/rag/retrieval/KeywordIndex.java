package rag.retrieval;

import rag.preprocess.Chunker;
import rag.utils.JsonUtils;

import java.nio.file.Files;
import java.nio.file.Path;
import java.util.ArrayList;
import java.util.Collections;
import java.util.HashMap;
import java.util.List;
import java.util.Map;

public class KeywordIndex {

    private final Map<String, Map<String, Entry>> index = new HashMap<>();
    private final ChunkStore chunkStore = new ChunkStore();

    public static class Entry {
        private final String chunkId;
        private int frequency;

        public Entry(String chunkId) {
            this.chunkId = chunkId;
            this.frequency = 0;
        }

        public void increment() {
            frequency++;
        }

        public String getChunkId() {
            return chunkId;
        }

        public int getFrequency() {
            return frequency;
        }
    }

    public void addChunk(Chunk chunk) {
        chunkStore.put(chunk);
        for (String token : chunk.getTokens()) {
            addToken(token, chunk.getChunkId());
        }
    }

    private void addToken(String token, String chunkId) {
        if (token == null || token.isBlank()) return;
        String normalized = token.toLowerCase();
        Map<String, Entry> postings = index.computeIfAbsent(normalized, k -> new HashMap<>());
        Entry entry = postings.computeIfAbsent(chunkId, Entry::new);
        entry.increment();
    }

    public List<Entry> lookup(String token) {
        if (token == null) {
            return Collections.emptyList();
        }
        Map<String, Entry> postings = index.get(token.toLowerCase());
        if (postings == null) {
            return Collections.emptyList();
        }
        return new ArrayList<>(postings.values());
    }

    public Chunk getChunk(String chunkId) {
        return chunkStore.get(chunkId);
    }

    public static KeywordIndex load(String path) throws Exception {
        String raw = Files.readString(Path.of(path));
        List<Object> nodes = JsonUtils.expectArray(JsonUtils.parse(raw), "keyword_index.json must be an array");
        KeywordIndex keywordIndex = new KeywordIndex();
        for (Object node : nodes) {
            Map<String, Object> obj = JsonUtils.expectObject(node, "Chunk entry must be an object");
            String chunkId = obj.get("chunkId").toString();
            String docId = obj.get("docId").toString();
            String source = obj.getOrDefault("source", "Unknown").toString();
            String title = obj.getOrDefault("title", docId).toString();
            String text = obj.get("text").toString();
            int start = ((Number) obj.getOrDefault("startOffset", 0)).intValue();
            int end = ((Number) obj.getOrDefault("endOffset", start)).intValue();
            List<Object> tokensNode = JsonUtils.expectArray(obj.get("tokens"), "Chunk tokens array missing");
            List<String> tokens = new ArrayList<>();
            for (Object t : tokensNode) {
                tokens.add(t.toString());
            }
            Chunk chunk = new Chunk(docId, chunkId, text, tokens, start, end, source, title);
            keywordIndex.addChunk(chunk);
        }
        return keywordIndex;
    }

    // Helper used by preprocess.IndexBuilder when chunk metadata already provided.
    public void addPieces(String docId, String source, String title, List<Chunker.ChunkPieces> pieces) {
        for (Chunker.ChunkPieces piece : pieces) {
            Chunk chunk = new Chunk(docId, piece.chunkId, piece.text, piece.tokens, piece.offset,
                    piece.offset + piece.tokens.size(), source, title);
            addChunk(chunk);
        }
    }
}
