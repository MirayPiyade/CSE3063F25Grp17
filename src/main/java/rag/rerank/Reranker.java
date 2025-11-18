package rag.rerank;

import rag.retrieval.Hit;

import java.util.List;

public interface Reranker {
    List<Hit> rerank(List<Hit> hits);
}
