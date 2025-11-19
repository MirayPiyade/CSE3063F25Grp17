package rag.preprocess;

import java.util.Arrays;
import java.util.List;

public class TextNormalizer {

    public String normalize(String text) {
        return text
                .replace("İ", "i").replace("I", "ı")
                .toLowerCase()
                .replaceAll("[^a-z0-9ğüşöçı ]", " ")
                .replaceAll("\\s+", " ")
                .trim();
    }

    public List<String> tokenize(String text) {
        return Arrays.asList(normalize(text).split(" "));
    }
}
