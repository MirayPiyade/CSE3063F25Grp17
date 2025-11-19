package rag.answer;

import java.util.List;
import rag.retrieval.Hit;

public interface AnswerAgent {
    Answer generateAnswer(List<Hit> hits);
}