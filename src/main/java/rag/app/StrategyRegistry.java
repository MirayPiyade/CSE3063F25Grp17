package rag.app;

import rag.answer.AnswerAgent;
import rag.answer.FallbackHandler;
import rag.answer.TemplateAnswerAgent;
import rag.answer._register_;
import rag.config.Config;
import rag.intents.IntentDetector;
import rag.intents.RuleIntentDetector;
import rag.query.HeuristicQueryWriter;
import rag.query.QueryWriter;
import rag.rerank.Reranker;
import rag.rerank.SimpleReranker;
import rag.retrieval.Document;
import rag.retrieval.DocumentStore;
import rag.retrieval.KeywordRetriever;
import rag.retrieval.Retriever;

import java.util.List;

/**
 * StrategyRegistry:
 *  - Creates strategy objects (IntentDetector, QueryWriter, Retriever, Reranker, AnswerAgent)
 *  - Loads necessary data files (intents.yaml, stopwords.yaml, keyword index, etc.)
 *  - Provides these objects to pipeline stages
 *
 * Fully aligned with Iteration-1 architecture.
 * All pipeline stages call this registry to get the correct strategy.
 */
public class StrategyRegistry {

    private final Config config;

    private List<Document> documents;
    private IntentDetector intentDetector;
    private QueryWriter queryWriter;
    private Retriever retriever;
    private Reranker reranker;
    private AnswerAgent answerAgent;
    private FallbackHandler fallbackHandler;

    public StrategyRegistry(Config config) {
        this.config = config;
    }

    // -------------------------------
    // Intent Detector Strategy
    // -------------------------------
    public IntentDetector getIntentDetector() {
        if (intentDetector == null) {
            try {
                intentDetector = new RuleIntentDetector(config.getIntentsPath());
            } catch (Exception e) {
                throw new RuntimeException("Failed to load intents.yaml: " + e.getMessage(), e);
            }
        }
        return intentDetector;
    }


    // -------------------------------
    // Query Writer Strategy
    // -------------------------------
    public QueryWriter getQueryWriter() {
        if (queryWriter == null) {
            try {
                queryWriter = new HeuristicQueryWriter(config.getStopwordsPath());
            } catch (Exception e) {
                throw new RuntimeException("Failed to load stopwords.yaml: " + e.getMessage(), e);
            }
        }
        return queryWriter;
    }


    // -------------------------------
    // Retriever Strategy
    // -------------------------------
    public Retriever getRetriever() {
        if (retriever == null) {
            retriever = new KeywordRetriever(config.getTopK(), config.getSourcePriority());
        }
        return retriever;
    }

    public List<Document> getDocuments() {
        if (documents == null) {
            try {
                documents = DocumentStore.load(config.getDocsPath()).getDocuments();
            } catch (Exception e) {
                throw new RuntimeException("Failed to load docs.json: " + e.getMessage(), e);
            }
        }
        return documents;
    }


    // -------------------------------
    // Reranker Strategy
    // -------------------------------
    public Reranker getReranker() {
        if (reranker == null) {
            reranker = new SimpleReranker(config.getRerankerPath());
        }
        return reranker;
    }

    // -------------------------------
    // AnswerAgent Strategy
    // -------------------------------
    public AnswerAgent getAnswerAgent() {

        // teammate's registry integration
        if (answerAgent == null) {
            AnswerAgent agent = _register_.get("template");

            if (agent == null) {
                // fallback if teammate forgets to register
                answerAgent = new TemplateAnswerAgent();
            } else {
                answerAgent = agent;
            }
        }

        return answerAgent;
    }

    public FallbackHandler getFallbackHandler() {
        if (fallbackHandler == null) {
            fallbackHandler = new FallbackHandler();
        }
        return fallbackHandler;
    }
}
