package rag.trace;

public class ConsoleTraceSink implements TraceSink {
    @Override
    public void record(TraceEvent event) {
        System.out.println("[TRACE] " + event.stage);
    }
}
