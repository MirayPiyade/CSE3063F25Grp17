package rag.reranker;
import java.util.*;
import rag.retrieval.Hit;

public class NoOpReranker implements Reranker {
    
    // return wihtout doing any operation
    @Override
    public List<Hit> rerank(List<String> terms, List<Hit> hits, Object config) {
        return hits;
    }
}
