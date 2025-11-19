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
            String json = String.format(
                "{\"stage\":\"%s\",\"summary\":\"%s\",\"durationMs\":%d,\"error\":\"%s\"}\n",
                e.stage,
                e.summary.replace("\"", "\\\""),
                e.durationMs,
                e.error
            );

            writer.write(json);
            writer.flush();
        } catch (IOException ex) {
            throw new RuntimeException(ex);
        }
    }
}
