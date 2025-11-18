package rag.retrieval;

import java.util.List;

public interface Retriever {

    List<Hit> retrieve(String query);
}
