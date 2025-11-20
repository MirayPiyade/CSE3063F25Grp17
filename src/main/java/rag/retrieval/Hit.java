package rag.retrieval;

public record Hit(
        String chunkId,
        String docId,
        String source,
        String title,
        String text,
        double score
) {
    public Hit withScore(double newScore) {
        return new Hit(chunkId, docId, source, title, text, newScore);
    }

    @Override
    public String toString() {
        return chunkId + "@" + source + " score=" + score;
    }
}
