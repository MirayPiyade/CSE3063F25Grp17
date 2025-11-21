package rag.config;

import rag.utils.JsonUtils;

import java.nio.file.Files;
import java.nio.file.Path;
import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;
import java.util.Map;

/**
 * ConfigLoader reads a JSON/YAML-lite file and builds a Config instance.
 * The file is expected to contain simple key-value pairs; missing entries fall back to defaults.
 */
public final class ConfigLoader {

    private ConfigLoader() {}

    public static Config load(String path) {
        Config defaults = Config.defaultConfig();
        if (path == null || path.isBlank()) {
            return defaults;
        }
        try {
            String raw = Files.readString(Path.of(path));
            Map<String, Object> root = parseConfig(raw, path);

            String question = JsonUtils.expectString(root.getOrDefault("question", defaults.getQuestion()), "question must be a string");
            String logDir = JsonUtils.expectString(root.getOrDefault("logDir", defaults.getLogDir()), "logDir must be a string");
            String intentsPath = JsonUtils.expectString(root.getOrDefault("intentsPath", defaults.getIntentsPath()), "intentsPath must be a string");
            String stopwordsPath = JsonUtils.expectString(root.getOrDefault("stopwordsPath", defaults.getStopwordsPath()), "stopwordsPath must be a string");
            String docsPath = JsonUtils.expectString(root.getOrDefault("docsPath", defaults.getDocsPath()), "docsPath must be a string");

            // Reranker strategy and config path
            String rerankerType = JsonUtils.expectString(root.getOrDefault("rerankerType", defaults.getRerankerType()), "rerankerType must be a string");
            String rerankerPath = JsonUtils.expectString(root.getOrDefault("rerankerPath", defaults.getRerankerPath()), "rerankerPath must be a string");

            // Retriever strategy setup (currently only keyword)
            String retrieverType = JsonUtils.expectString(root.getOrDefault("retrieverType", defaults.getRetrieverType()), "retrieverType must be a string");
            int topK = (int) JsonUtils.expectNumber(root.getOrDefault("topK", defaults.getTopK()), "topK must be numeric");

            List<String> sourcePriority = new ArrayList<>(defaults.getSourcePriority());
            Object srcNode = root.get("sourcePriority");
            if (srcNode != null) {
                List<Object> arr = JsonUtils.expectArray(srcNode, "sourcePriority must be an array");
                sourcePriority.clear();
                for (Object o : arr) {
                    sourcePriority.add(o.toString());
                }
            }

            return new Config(
                    question,
                    logDir,
                    intentsPath,
                    stopwordsPath,
                    docsPath,
                    rerankerType,
                    rerankerPath,
                    retrieverType,
                    topK,
                    sourcePriority
            );
        } catch (Exception e) {
            throw new RuntimeException("Failed to load config from " + path + ": " + e.getMessage(), e);
        }
    }

    private static Map<String, Object> parseConfig(String raw, String path) {
        try {
            return JsonUtils.expectObject(JsonUtils.parse(raw), "config file must be an object");
        } catch (Exception jsonEx) {
            String lower = path.toLowerCase();
            if (lower.endsWith(".yaml") || lower.endsWith(".yml")) {
                return parseSimpleYaml(raw);
            }
            throw jsonEx;
        }
    }

    /**
     * Minimal YAML parser: supports top-level key: value with optional inline arrays.
     * Intended only for our config needs (no nesting).
     */
    private static Map<String, Object> parseSimpleYaml(String raw) {
        Map<String, Object> map = new HashMap<>();
        String[] lines = raw.split("\\r?\\n");
        for (String line : lines) {
            String trimmed = line.trim();
            if (trimmed.isEmpty() || trimmed.startsWith("#")) {
                continue;
            }
            int idx = trimmed.indexOf(':');
            if (idx < 0) {
                continue;
            }
            String key = trimmed.substring(0, idx).trim();
            String valuePart = trimmed.substring(idx + 1).trim();
            Object value = parseValue(valuePart);
            map.put(key, value);
        }
        return map;
    }

    private static Object parseValue(String raw) {
        if (raw.isEmpty()) return "";
        if (raw.startsWith("[") && raw.endsWith("]")) {
            String inner = raw.substring(1, raw.length() - 1).trim();
            if (inner.isEmpty()) return List.of();
            String[] parts = inner.split(",");
            List<Object> values = new ArrayList<>();
            for (String part : parts) {
                values.add(parseValue(part.trim()));
            }
            return values;
        }
        if ((raw.startsWith("\"") && raw.endsWith("\"")) || (raw.startsWith("'") && raw.endsWith("'"))) {
            return raw.substring(1, raw.length() - 1);
        }
        // number?
        try {
            if (raw.contains(".")) {
                return Double.parseDouble(raw);
            }
            return Integer.parseInt(raw);
        } catch (NumberFormatException ignored) {
            // plain string
        }
        return raw;
    }
}
