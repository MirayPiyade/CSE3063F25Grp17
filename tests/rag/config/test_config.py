import pytest
from rag.config.config import Config

def test_config_defaults():
    # Test default_config static method
    cfg = Config.default_config()
    assert cfg.retriever_type == "keyword"
    assert cfg.embedding_provider_type == "openai"

def test_with_overrides():
    cfg = Config.default_config()
    
    new_cfg = cfg.with_cache_disabled()
    assert new_cfg.cache_enabled is False
    assert cfg.cache_enabled is True # Immutability check
    
    new_cfg = cfg.with_question("Q")
    assert new_cfg.question == "Q"
    
    new_cfg = cfg.with_reranker_type("hybrid")
    assert new_cfg.reranker_type == "hybrid"
    
    new_cfg = cfg.with_retriever_type("keyword")
    assert new_cfg.retriever_type == "keyword"

    new_cfg = cfg.with_embedding_provider_type("stub")
    assert new_cfg.embedding_provider_type == "stub"
    
    new_cfg = cfg.with_answer_agent_type("template")
    assert new_cfg.answer_agent_type == "template"
