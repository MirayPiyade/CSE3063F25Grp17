import pytest
from rag.app.default_pipeline import DefaultPipeline
from rag.app.stages.pipeline_stage import PipelineStage
from unittest.mock import MagicMock

def test_create_pipeline_structure():
    mock_stage = MagicMock(spec=PipelineStage)
    pipeline = DefaultPipeline([mock_stage])
    
    assert isinstance(pipeline.stages, list)
    assert len(pipeline.stages) == 1
    assert pipeline.stages[0] == mock_stage
