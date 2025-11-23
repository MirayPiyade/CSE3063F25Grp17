package rag.answer;

import java.util.List;

public record Answer(String text, List<String> citations) {
    public String getText() { return text; }
    public List<String> getCitations() { return citations; }
}
