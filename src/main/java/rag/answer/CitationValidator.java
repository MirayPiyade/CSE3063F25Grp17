package rag.answer;

import java.util.List;

public class CitationValidator {

    public boolean validate(List<String> citations) {
        if (citations == null || citations.isEmpty()) {
            return false;
        }
        return citations.stream().noneMatch(c -> c == null || c.isBlank());
    }
}