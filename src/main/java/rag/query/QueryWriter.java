package rag.query;

import java.util.List;

public interface QueryWriter {
    List<String> write(String question);
}
