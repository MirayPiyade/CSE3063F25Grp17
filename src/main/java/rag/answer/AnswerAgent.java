package rag.answer;

import java.util.List;
import rag.retrieval.Hit;

public interface AnswerAgent {
    Answer generateAnswer(String query, List<Hit> hits);
}
