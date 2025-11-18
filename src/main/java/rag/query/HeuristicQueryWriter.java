package rag.query;

import java.util.List;

public class HeuristicQueryWriter implements QueryWriter {
    @Override
    public List<String> write(String question) {
        // TODO tokenization + stopwords removal
        return List.of();
    }
}
