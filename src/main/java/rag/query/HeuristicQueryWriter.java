package rag.query;

import rag.intents.Intent;
import rag.utils.JsonUtils;

import java.nio.file.Files;
import java.nio.file.Path;
import java.util.ArrayList;
import java.util.LinkedHashSet;
import java.util.List;
import java.util.Locale;
import java.util.Map;
import java.util.Set;

public class HeuristicQueryWriter implements QueryWriter {

    private final Set<String> stopwords;
    private final Map<Intent, List<String>> boosters;

    public HeuristicQueryWriter(String stopwordsPath) throws Exception {
        String raw = Files.readString(Path.of(stopwordsPath));
        Map<String, Object> root = JsonUtils.expectObject(
                JsonUtils.parse(raw),
                "stopwords.yaml must contain a JSON object"
        );
        stopwords = Set.copyOf(readList(root.get("stopwords")));

        Map<Intent, List<String>> boosterMap = new java.util.EnumMap<>(Intent.class);
        Object boosterNode = root.get("boosters");
        if (boosterNode instanceof Map<?, ?> map) {
            for (Map.Entry<?, ?> entry : map.entrySet()) {
                Intent intent = parseIntent(entry.getKey().toString());
                boosterMap.put(intent, readList(entry.getValue()));
            }
        }
        boosters = boosterMap;
    }

    @Override
    public List<String> write(String question, Intent intent) {
        if (question == null) question = "";
        Intent effectiveIntent = intent == null ? Intent.Unknown : intent;

        String normalized = question
                .toLowerCase(Locale.ROOT)
                .replaceAll("[^\\p{L}\\p{Nd} ]", " ")
                .trim();
        if (normalized.isEmpty()) {
            return List.of();
        }

        String[] tokens = normalized.split("\\s+");
        boolean shortQuestion = tokens.length <= 2;
        LinkedHashSet<String> terms = new LinkedHashSet<>();

        for (String token : tokens) {
            if (token.isBlank()) continue;
            if (!shortQuestion && stopwords.contains(token)) continue;
            terms.add(token);
        }

        if (terms.isEmpty() && shortQuestion) {
            for (String token : tokens) {
                if (!token.isBlank()) {
                    terms.add(token);
                }
            }
        }

        boosters.getOrDefault(effectiveIntent, List.of())
                .forEach(terms::add);
        boosters.getOrDefault(Intent.Unknown, List.of())
                .forEach(terms::add);

        terms.add(effectiveIntent.name().toLowerCase(Locale.ROOT));
        return new ArrayList<>(terms);
    }

    @SuppressWarnings("unchecked")
    private List<String> readList(Object node) {
        if (node instanceof List<?> list) {
            List<String> values = new ArrayList<>();
            for (Object value : list) {
                values.add(value.toString().toLowerCase(Locale.ROOT));
            }
            return values;
        }
        return List.of();
    }

    private Intent parseIntent(String name) {
        try {
            return Intent.valueOf(name);
        } catch (IllegalArgumentException ex) {
            return Intent.Unknown;
        }
    }
}
