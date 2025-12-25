import pytest
from rag.app.rag_cli import extract_arg

def test_extract_arg_found():
    args = ["--key", "value", "--other"]
    assert extract_arg(args, "--key") == "value"

def test_extract_arg_not_found():
    args = ["--key", "value"]
    assert extract_arg(args, "--missing") is None

def test_extract_arg_no_value():
    args = ["--key"]
    # If key is last, it returns None or crashes? Code check: i+1 < len(args)
    assert extract_arg(args, "--key") is None

def test_extract_arg_none_args():
    # Code check: if args is None return None
    assert extract_arg(None, "--key") is None
