package rag.rerank;

import rag.retrieval.Hit;

import java.util.List;

public class SimpleReranker implements Reranker {
    @Override
    public List<Hit> rerank(List<Hit> hits) {
        // TODO apply scoring rules
        return hits;
    }
}
