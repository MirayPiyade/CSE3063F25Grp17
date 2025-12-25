import pytest
from rag.app.policy_router import PolicyRouter

def test_list_policies():
    router = PolicyRouter()
    policies = router.list_policies()
    assert len(policies) > 0
    # Check for default policy
    assert any(p.name == "default" for p in policies)

def test_get_config_path_valid():
    router = PolicyRouter()
    path = router.get_config_path("default")
    assert path is not None
    assert "config.yaml" in path

def test_get_config_path_invalid():
    router = PolicyRouter()
    path = router.get_config_path("non_existent_policy")
    assert path is None
