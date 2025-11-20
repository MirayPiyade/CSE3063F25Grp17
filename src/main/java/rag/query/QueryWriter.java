package rag.query;

import rag.intents.Intent;
import java.util.List;

public interface QueryWriter {
    List<String> write(String question, Intent intent) throws Exception;
}
