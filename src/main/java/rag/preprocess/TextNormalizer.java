package rag.preprocess;

import java.text.Normalizer;
import java.util.Arrays;
import java.util.List;
import java.util.stream.Collectors;

public class TextNormalizer {

    // basit tokenization: kelimeleri al (letters+digits)
    public List<String> tokenize(String text) {
        String cleaned = normalize(text);
        String[] toks = cleaned.split("\\W+");
        return Arrays.stream(toks)
                .filter(t -> !t.isEmpty())
                .map(String::toLowerCase)
                .collect(Collectors.toList());
    }

    public String normalize(String text) {
        if (text == null) return "";
        // Unicode normalize + remove control chars
        String n = Normalizer.normalize(text, Normalizer.Form.NFKC);
        n = n.replaceAll("\\p{Cntrl}", " ");
        n = n.replaceAll("\\s+", " ");
        return n.trim();
    }
}
