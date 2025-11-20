package rag.trace;
import java.util.*;

public class TraceBus {
    private List<TraceSink> sinks = new ArrayList<>();

    public void addSink(TraceSink sink) { sinks.add(sink); }
    public void publish(TraceEvent ev) throws Exception {
        for (TraceSink sink : sinks) {
            try {
                sink.record(ev);
            } catch (RuntimeException ex) {
                System.err.println("Failed");;
            }
        }
    }

    public void setSinks(List<TraceSink> sinks) { this.sinks = sinks; }
    public List<TraceSink> getSinks() { return this.sinks; }

    @Override
    public String toString() {
        String trace = "";
        for (int i = 0; i < sinks.size(); i++) {
            trace += sinks.get(i);
            trace += "\n";
        }
        return trace;
    }
}