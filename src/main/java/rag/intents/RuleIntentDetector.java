package rag.intents;

import rag.utils.JsonUtils;

import java.nio.file.Files;
import java.nio.file.Path;
import java.util.ArrayList;
import java.util.Comparator;
import java.util.List;
import java.util.Locale;
import java.util.Map;

public class RuleIntentDetector implements IntentDetector {

    private static final class Rule {
        final Intent intent;
        final int priority;
        final List<String> keywords;

        Rule(Intent intent, int priority, List<String> keywords) {
            this.intent = intent;
            this.priority = priority;
            this.keywords = keywords;
        }
    }

    private final List<Rule> rules = new ArrayList<>();

    public RuleIntentDetector(String yamlPath) throws Exception {
        String raw = Files.readString(Path.of(yamlPath));
        Map<String, Object> root = JsonUtils.expectObject(
                JsonUtils.parse(raw),
                "intents.yaml must contain a JSON object"
        );
        for (Map.Entry<String, Object> entry : root.entrySet()) {
            Intent intent = parseIntent(entry.getKey());
            Map<String, Object> spec = JsonUtils.expectObject(
                    entry.getValue(),
                    "Intent definition for " + entry.getKey() + " must be an object"
            );
            int priority = spec.containsKey("priority")
                    ? ((Number) spec.get("priority")).intValue()
                    : Integer.MAX_VALUE;
            List<Object> keywordsNode = JsonUtils.expectArray(
                    spec.get("keywords"),
                    "Intent " + entry.getKey() + " is missing keywords"
            );
            List<String> keywords = new ArrayList<>();
            for (Object keyword : keywordsNode) {
                keywords.add(keyword.toString().toLowerCase(Locale.ROOT));
            }
            rules.add(new Rule(intent, priority, keywords));
        }
        rules.sort(Comparator.comparingInt(r -> r.priority));
    }

    @Override
    public Intent detect(String q) {
        if (q == null || q.isBlank()) {
            return Intent.Unknown;
        }
        String text = q.toLowerCase(Locale.ROOT);
        Intent best = Intent.Unknown;
        int bestScore = 0;
        int bestPriority = Integer.MAX_VALUE;

        for (Rule rule : rules) {
            int matches = 0;
            for (String keyword : rule.keywords) {
                if (text.contains(keyword)) {
                    matches++;
                }
            }
            if (matches == 0) continue;
            if (matches > bestScore || (matches == bestScore && rule.priority < bestPriority)) {
                bestScore = matches;
                bestPriority = rule.priority;
                best = rule.intent;
            }
        }

        return best;
    }

    private Intent parseIntent(String value) {
        try {
            return Intent.valueOf(value);
        } catch (IllegalArgumentException ex) {
            return Intent.Unknown;
        }
    }
}
