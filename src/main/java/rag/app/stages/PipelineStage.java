package rag.app.stages;

import rag.app.Context;

public interface PipelineStage {
    void run(Context ctx);
}
