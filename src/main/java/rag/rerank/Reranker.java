package rag.reranker;
import java.util.*;
import rag.retrieval.Hit;

// Strategy pattern for RAG pipeline, reranks retrieved hits regarding to query

public interface Reranker {
    // query is the original text query like proximityBonus or titleBoost. it is required to calculate heuristic points
    // hits is the list that first scoring (tf-sum) found by retriever
    // rContext is the  object that holds all the state coming from preceding stages of the pipeline managed by RagOrchestrator (e.g. Query's final terms)
    public List<Hit> rerank(List<String> terms, List<Hit> hits, Object config);
}