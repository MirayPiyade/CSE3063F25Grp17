package rag.trace;

import java.io.*;

// concrete implementation of TraceSink that writes events to a JSON Lines format
public class JsonlTraceSink implements TraceSink {

    private final FileWriter writer;

    public JsonlTraceSink(String path) throws IOException {
        this.writer = new FileWriter(path, true);
    }

    @Override
    public void record(TraceEvent e) throws RuntimeException {
        try {

            // manual escaping
            String summary = e.summary == null ? "" : e.summary.replace("\"", "\\\"");
            String error = e.error == null ? "" : e.error.replace("\"", "\\\"");

            // generate a JSON file
            String json = String.format(
                "{\"timestamp\":%d,\"stage\":\"%s\",\"summary\":\"%s\",\"durationMs\":%d,\"error\":\"%s\"}\n",
                e.timestamp,
                e.stage,
                summary,
                e.durationMs,
                error
            );

            writer.write(json);
            writer.flush();
        } catch (IOException ex) {
            // log the error
            System.err.println("failed regarding to I/O while writing to JsonlTraceSink" + ex.getMessage());
        }
    }
}