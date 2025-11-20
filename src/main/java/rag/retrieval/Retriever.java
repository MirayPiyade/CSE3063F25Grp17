package rag.retrieval;

import java.util.List;

public interface Retriever {
    List<Hit> retrieve(List<String> terms, KeywordIndex index);
}
