package rag.app.stages;

import rag.app.Context;
import rag.trace.TraceBus;

public interface PipelineStage {

    // Her stage’in adı: Trace logları için zorunlu.
    String getName();

    // Stage’in gerçek işi burada yapılır.
    // Context: pipeline state
    // TraceBus: log sistemi
    void run(Context context, TraceBus traceBus) throws Exception;
}
