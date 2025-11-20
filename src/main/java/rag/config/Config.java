package rag.config;

import rag.utils.JsonUtils;

import java.nio.file.Files;
import java.nio.file.Path;
import java.util.ArrayList;
import java.util.List;
import java.util.Map;

public class Config {

    private final String question;
    private final String logDir;
    private final String intentsPath;
    private final String stopwordsPath;
    private final String keywordIndexPath;
    private final String rerankerPath;
    private final int topK;
    private final List<String> sourcePriority;

    private Config(
            String question,
            String logDir,
            String intentsPath,
            String stopwordsPath,
            String keywordIndexPath,
            String rerankerPath,
            int topK,
            List<String> sourcePriority
    ) {
        this.question = question;
        this.logDir = logDir;
        this.intentsPath = intentsPath;
        this.stopwordsPath = stopwordsPath;
        this.keywordIndexPath = keywordIndexPath;
        this.rerankerPath = rerankerPath;
        this.topK = topK;
        this.sourcePriority = List.copyOf(sourcePriority);
    }

    public static Config load(String path) throws Exception {
        String raw = Files.readString(Path.of(path));
        Map<String, Object> root = JsonUtils.expectObject(
                JsonUtils.parse(raw),
                "Config file must contain a JSON object"
        );

        String question = root.containsKey("question")
                ? root.get("question").toString()
                : null;
        String logDir = requireString(root, "logsDir");
        String intents = requireString(root, "intentsPath");
        String stopwords = requireString(root, "stopwordsPath");
        String index = requireString(root, "keywordIndexPath");
        String reranker = requireString(root, "rerankerPath");

        int topK = root.containsKey("topK")
                ? ((Number) root.get("topK")).intValue()
                : 5;
        if (topK <= 0) topK = 5;

        List<String> priority = new ArrayList<>();
        Object priorityNode = root.get("sourcePriority");
        if (priorityNode instanceof List<?> list && !list.isEmpty()) {
            for (Object entry : list) {
                priority.add(entry.toString());
            }
        } else {
            priority.add("CompE");
            priority.add("FoE");
            priority.add("MU");
        }

        return new Config(
                question,
                logDir,
                intents,
                stopwords,
                index,
                reranker,
                topK,
                priority
        );
    }

    private static String requireString(Map<String, Object> root, String key) {
        Object value = root.get(key);
        if (value == null) {
            throw new IllegalArgumentException("Missing config value: " + key);
        }
        return value.toString();
    }

    public String getQuestion() {
        return question;
    }

    public String getLogDir() {
        return logDir;
    }

    public String getIntentsPath() {
        return intentsPath;
    }

    public String getStopwordsPath() {
        return stopwordsPath;
    }

    public String getKeywordIndexPath() {
        return keywordIndexPath;
    }

    public String getRerankerPath() {
        return rerankerPath;
    }

    public int getTopK() {
        return topK;
    }

    public List<String> getSourcePriority() {
        return sourcePriority;
    }

    public Config withQuestion(String newQuestion) {
        return new Config(
                newQuestion,
                logDir,
                intentsPath,
                stopwordsPath,
                keywordIndexPath,
                rerankerPath,
                topK,
                sourcePriority
        );
    }
}
