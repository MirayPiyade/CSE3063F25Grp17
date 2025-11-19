package rag.trace;

public interface TraceSink {
    void accept(TraceEvent event);
}
