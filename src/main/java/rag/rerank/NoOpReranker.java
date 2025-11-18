package rag.rerank;

import rag.retrieval.Hit;

import java.util.List;

public class NoOpReranker implements Reranker {
    @Override
    public List<Hit> rerank(List<Hit> hits) {
        return hits; // no sorting
    }
}
