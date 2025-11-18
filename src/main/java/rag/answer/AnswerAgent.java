package rag.answer;

import rag.retrieval.Hit;
import java.util.List;

public interface AnswerAgent {
    Answer answer(List<Hit> hits);
}
