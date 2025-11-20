package rag.rerank;

import rag.retrieval.Hit;
import java.util.List;

public class NoOpReranker implements Reranker {

    @Override
    public List<Hit> rerank(List<String> terms, List<Hit> hits, Object config) {
        return hits; // hiçbir şey yapmadan geri döndür
    }
}
