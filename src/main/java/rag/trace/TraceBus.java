package rag.trace;
import java.util.*;


public class TraceBus {

    private List<TraceSink> sinks = new ArrayList<>();

    // register a new TraceSink (Observer) to receive trace events
    public void addSink(TraceSink sink) { sinks.add(sink); }
    public void publish(TraceEvent ev) throws Exception {
        for (TraceSink sink : sinks) {
            try {
                sink.record(ev);
            } catch (RuntimeException ex) {
                // print the error message
                System.err.printf(
                    "Error recording event in sink %s: %s%n", 
                    sink.getClass().getSimpleName(), 
                    ex.getMessage()
                );
            }
        }
    }

    // Optionally provides read-only access to the list of sinks for monitoring/debugging.
    public List<TraceSink> getSinks() { return this.sinks; }
}