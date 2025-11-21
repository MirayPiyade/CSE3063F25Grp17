package rag.config;

import java.util.List;

public class Config {

    private final String question;
    private final String logDir;
    private final String intentsPath;
    private final String stopwordsPath;
    private final String docsPath;
    private final String rerankerType;
    private final String rerankerPath;
    private final String retrieverType;
    private final int topK;
    private final List<String> sourcePriority;

    public Config(
            String question,
            String logDir,
            String intentsPath,
            String stopwordsPath,
            String docsPath,
            String rerankerType,
            String rerankerPath,
            String retrieverType,
            int topK,
            List<String> sourcePriority
    ) {
        this.question = question;
        this.logDir = logDir;
        this.intentsPath = intentsPath;
        this.stopwordsPath = stopwordsPath;
        this.docsPath = docsPath;
        this.rerankerType = rerankerType;
        this.rerankerPath = rerankerPath;
        this.retrieverType = retrieverType;
        this.topK = topK;
        this.sourcePriority = List.copyOf(sourcePriority);
    }

    public String getQuestion() { return question; }
    public String getLogDir() { return logDir; }
    public String getIntentsPath() { return intentsPath; }
    public String getStopwordsPath() { return stopwordsPath; }
    public String getDocsPath() { return docsPath; }
    public String getRerankerType() { return rerankerType; }
    public String getRerankerPath() { return rerankerPath; }
    public String getRetrieverType() { return retrieverType; }
    public int getTopK() { return topK; }
    public List<String> getSourcePriority() { return sourcePriority; }

    public Config withQuestion(String newQuestion) {
        return new Config(
                newQuestion,
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
    }

    public Config withRerankerType(String newType) {
        return new Config(
                question,
                logDir,
                intentsPath,
                stopwordsPath,
                docsPath,
                newType,
                rerankerPath,
                retrieverType,
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
                "simple",
                "config/reranker.yaml",
                "keyword",
                5,
                List.of("CompE", "FoE", "MU")
        );
    }
}
