package rag.trace;

public class ConsoleTraceSink implements TraceSink {

    // prints the trace record of the event in the console
    @Override
    public void record(TraceEvent event) {
        String output = String.format(
            "| %s | %dms | %s | %s",
            event.stage,
            event.durationMs,
            event.summary,
            event.error != null ? "[HATA: " + event.error + "]" : ""
        );
        System.out.println(output);
    }
}