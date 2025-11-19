package rag.trace;

public class TraceEvent {

    public final String stage;
    public final String summary;
    public final long durationMs;
    public final String error;

    public TraceEvent(String stage, String summary, long durationMs, String error) {
        this.stage = stage;
        this.summary = summary;
        this.durationMs = durationMs;
        this.error = error;
    }
}
