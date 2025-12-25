import pytest
from rag.answer.citation_validator import CitationValidator

def test_validate_valid_citations():
    validator = CitationValidator()
    citations = ["doc1", "doc2"]
    assert validator.validate(citations) is True

def test_validate_empty_list():
    validator = CitationValidator()
    assert validator.validate([]) is False

def test_validate_none():
    validator = CitationValidator()
    assert validator.validate(None) is False

def test_validate_list_with_none():
    validator = CitationValidator()
    citations = ["doc1", None] # type: ignore
    # The code uses 'c is not None' check, so this should return False
    assert validator.validate(citations) is False

def test_validate_list_with_empty_string():
    validator = CitationValidator()
    citations = ["doc1", ""]
    # The code uses 'c.strip()' check, so empty string is falsy -> return False
    assert validator.validate(citations) is False
