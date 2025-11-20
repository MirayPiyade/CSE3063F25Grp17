package rag.answer;

import rag.retrieval.Hit;
import java.util.List;

public interface AnswerAgent {
    Answer generateAnswer(List<Hit> hits);
}
