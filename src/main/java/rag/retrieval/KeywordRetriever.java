package rag.retrieval;

import java.util.List;

public class KeywordRetriever implements Retriever {
    @Override
    public List<Hit> retrieve(List<String> terms) {
        // TODO read index, compute TF
        return List.of();
    }
}
