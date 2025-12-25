import pytest
from rag.retrieval.keyword_retriever import KeywordRetriever
from rag.retrieval.document import Document

def test_keyword_retrieval_scoring():
    retriever = KeywordRetriever(top_k=2, priority_order=["s1", "s2"])
    
    doc1 = Document("1", "s1", "t1", "The quick brown fox")
    doc2 = Document("2", "s2", "t2", "lazy dog")
    doc3 = Document("3", "s3", "t3", "random text")
    
    docs = [doc1, doc2, doc3]
    
    # Question matches doc1 (2.0 points), Term "lazy" matches doc2 (1.0 point)
    hits = retriever.retrieve("quick", ["lazy"], docs)
    
    assert len(hits) == 2
    assert hits[0].doc_id == "1"
    assert hits[0].score >= 2.0
    assert hits[1].doc_id == "2"
    assert hits[1].score >= 1.0

def test_keyword_retrieval_priority_sorting():
    retriever = KeywordRetriever(top_k=5, priority_order=["high", "low"])
    
    # Both have same score (term match)
    doc1 = Document("1", "low", "t1", "apple")
    doc2 = Document("2", "high", "t2", "apple")
    
    hits = retriever.retrieve("", ["apple"], [doc1, doc2])
    
    # doc2 should come first because 'high' is earlier in priority_order
    assert hits[0].doc_id == "2"
    assert hits[1].doc_id == "1"

def test_keyword_retrieval_empty_docs():
    retriever = KeywordRetriever(top_k=5, priority_order=[])
    hits = retriever.retrieve("q", [], [])
    assert len(hits) == 0
