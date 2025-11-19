package rag.retrieval;

public class Hit implements Comparable<Hit> {

    public final String docId;
    public final String chunkId;
    public final int score;

    public Hit(String docId, String chunkId, int score) {
        this.docId = docId;
        this.chunkId = chunkId;
        this.score = score;
    }

    @Override
    public int compareTo(Hit other) {
        // DESC score
        if (this.score != other.score)
            return Integer.compare(other.score, this.score);

        // ASC docId
        int d = this.docId.compareTo(other.docId);
        if (d != 0) return d;

        // ASC chunkId
        return this.chunkId.compareTo(other.chunkId);
    }
}
