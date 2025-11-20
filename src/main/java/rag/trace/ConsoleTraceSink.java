package rag.trace;

public class ConsoleTraceSink implements TraceSink {

    @Override
    public void accept(TraceEvent event) {
        System.out.println("[TRACE] "
                + event.stage
                + " | summary=" + event.summary
                + " | duration=" + event.durationMs
                + "ms | error=" + (event.error == null ? "-" : event.error));
    }
}
