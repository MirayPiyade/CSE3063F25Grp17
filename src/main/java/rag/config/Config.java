package rag.config;

import java.util.List;

public class Config {

    private final String question;
    private final String logDir;
    private final String intentsPath;
    private final String stopwordsPath;
    private final String docsPath;
    private final String rerankerPath;
    private final int topK;
    private final List<String> sourcePriority;

    private Config(
            String question,
            String logDir,
            String intentsPath,
            String stopwordsPath,
            String docsPath,
            String rerankerPath,
            int topK,
            List<String> sourcePriority
    ) {
        this.question = question;
        this.logDir = logDir;
        this.intentsPath = intentsPath;
        this.stopwordsPath = stopwordsPath;
        this.docsPath = docsPath;
        this.rerankerPath = rerankerPath;
        this.topK = topK;
        this.sourcePriority = List.copyOf(sourcePriority);
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

    public String getDocsPath() {
        return docsPath;
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
                docsPath,
                rerankerPath,
                topK,
                sourcePriority
        );
    }

    public static Config defaultConfig() {
        return new Config(
                null,
                "logs",
                "config/intents.yaml",
                "config/stopwords.yaml",
                "data/docs.json",
                "config/reranker.yaml",
                5,
                List.of("CompE", "FoE", "MU")
        );
    }
}
