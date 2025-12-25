import pytest
from rag.utils.json_utils import JsonUtils

def test_parse_simple_types():
    assert JsonUtils.parse("true") is True
    assert JsonUtils.parse("false") is False
    assert JsonUtils.parse("null") is None
    assert JsonUtils.parse("123") == 123
    assert JsonUtils.parse("12.34") == 12.34
    assert JsonUtils.parse('"hello"') == "hello"

def test_parse_object():
    json_str = '{"key": "value", "num": 1}'
    obj = JsonUtils.parse(json_str)
    assert obj == {"key": "value", "num": 1}

def test_parse_array():
    json_str = '[1, "two", true]'
    arr = JsonUtils.parse(json_str)
    assert arr == [1, "two", True]

def test_parse_nested():
    json_str = '{"a": [1, 2], "b": {"c": "d"}}'
    obj = JsonUtils.parse(json_str)
    assert obj["a"] == [1, 2]
    assert obj["b"]["c"] == "d"

def test_expect_methods():
    obj = {"k": "v"}
    assert JsonUtils.expect_object(obj, "err") == obj
    
    with pytest.raises(ValueError):
        JsonUtils.expect_object([], "err")
        
    assert JsonUtils.expect_string("s", "err") == "s"
    with pytest.raises(ValueError):
        JsonUtils.expect_string(1, "err")

def test_parse_errors():
    with pytest.raises(ValueError):
        JsonUtils.parse("{") # Incomplete
    
    with pytest.raises(ValueError):
        JsonUtils.parse('{"key": }') # Missing value
        
    with pytest.raises(ValueError):
        JsonUtils.parse(None)

def test_escape_sequences():
    s = r'"line\nbreak"'
    assert JsonUtils.parse(s) == "line\nbreak"
