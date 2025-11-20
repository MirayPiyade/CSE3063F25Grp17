package rag.retrieval;

import java.util.List;

public interface Retriever {
    List<Hit> retrieve(String question, List<String> terms, List<Document> documents);
}
