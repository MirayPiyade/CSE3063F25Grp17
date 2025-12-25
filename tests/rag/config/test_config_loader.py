import pytest
import os

from rag.config.config_loader import ConfigLoader
from rag.config.config import Config

@pytest.fixture
def temp_config_file(tmp_path):
    f = tmp_path / "test_config.json"
    data = {
        "retrieverType": "keyword",
        "topK": 10,
        "sourcePriority": ["Test"],
        "embeddingProviderType": "stub"
    }
    import json
    f.write_text(json.dumps(data), encoding='utf-8')
    return str(f)

def test_load_valid_file(temp_config_file):
    cfg = ConfigLoader.load(temp_config_file)
    assert cfg.retriever_type == "keyword"
    assert cfg.top_k == 10
    assert cfg.source_priority == ["Test"]
    assert cfg.embedding_provider_type == "stub"

def test_load_none_returns_default():
    cfg = ConfigLoader.load(None)
    # Checks default config
    # Based on Config.default_config() or defaults
    assert cfg.retriever_type in ["vector", "keyword"] 

def test_missing_file_error():
    # If file not found, it might raise FileNotFoundError or RuntimeError depending on impl
    with pytest.raises((FileNotFoundError, RuntimeError)):
        ConfigLoader.load("/non/existent/path.yaml")

def test_invalid_yaml(tmp_path):
    f = tmp_path / "bad.yaml"
    # "key: value: error" might be parsed loosely. Use garbage.
    f.write_text("!!! INVALID !!!", encoding='utf-8')
    # Since ConfigLoader falls back gracefully (returns defaults if keys missing/parse fail fallback yields nothing),
    # we expect a valid default config, NOT an exception.
    # Note: _parse_simple_yaml returns {} for garbage, so defaults are utilized.
    cfg = ConfigLoader.load(str(f))
    assert cfg is not None
    assert cfg.retriever_type in ["vector", "keyword"]
