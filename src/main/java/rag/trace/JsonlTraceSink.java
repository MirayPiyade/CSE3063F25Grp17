package rag.trace;

import java.io.FileWriter;
import java.io.IOException;

public class JsonlTraceSink implements TraceSink {

    private final FileWriter writer;

    public JsonlTraceSink(String path) throws IOException {
        this.writer = new FileWriter(path, true);
    }

    @Override
    public void accept(TraceEvent e) {
        try {
            String summary = e.summary == null ? "" : e.summary.replace("\"", "\\\"");
            String error = e.error == null ? "" : e.error.replace("\"", "\\\"");
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
            throw new RuntimeException(ex);
        }
    }
}
