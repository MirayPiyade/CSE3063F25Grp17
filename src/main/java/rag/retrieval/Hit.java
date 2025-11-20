package rag.retrieval;

public record Hit(
        String docId,
        String source,
        String title,
        String text,
        double score
) {
    public Hit withScore(double newScore) {
        return new Hit(docId, source, title, text, newScore);
    }

    @Override
    public String toString() {
        return docId + "@" + source + " score=" + score;
    }
}
