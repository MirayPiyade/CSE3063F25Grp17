package rag.trace;

import java.util.ArrayList;
import java.util.List;

public class TraceBus {
    private List<TraceSink> sinks = new ArrayList<>();

    public void addSink(TraceSink sink) { sinks.add(sink); }

    public void publish(TraceEvent ev) {
        for (TraceSink s : sinks) s.record(ev);
    }
}
