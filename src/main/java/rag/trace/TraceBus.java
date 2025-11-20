package rag.trace;

import java.util.ArrayList;
import java.util.List;

public class TraceBus {

    private final List<TraceSink> sinks = new ArrayList<>();

    public void addSink(TraceSink sink) {
        sinks.add(sink);
    }

    public void publish(TraceEvent e) {
        for (TraceSink sink : sinks) {
            try {
                sink.accept(e);
            } catch (RuntimeException ex) {
                System.err.println("Trace sink failed: " + ex.getMessage());
            }
        }
    }
}
