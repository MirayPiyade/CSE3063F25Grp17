package rag.retrieval;

public class Hit implements Comparable<Hit> {
    public int docId;
    public int chunkId;
    public int score;
    private final Chunk chunk;
    private int rank = -1;

    public Hit(Chunk chunk, double score) {
        this.chunk = chunk;
        this.score = score;
    }

    public Chunk getChunk() { return chunk; }
    public double getScore() { return score; }
    public int getRank() { return rank; }
    public void setRank(int rank) { this.rank = rank; }

    @Override
    public int compareTo(Hit other) {
        return Double.compare(other.score, this.score); // descending
    }
}
