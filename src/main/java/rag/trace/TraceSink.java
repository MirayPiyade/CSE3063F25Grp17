package rag.trace;

// TraceSink defines for all concrete logging
public interface TraceSink {
    void record(TraceEvent event);
}
