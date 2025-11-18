package rag.retrieval;

import rag.app.StrategyRegistry;

public class _register_ {
    static {
        try {
            StrategyRegistry.registerRetriever("keyword", KeywordRetriever.class);
            // eğer StrategyRegistry tek register method kullanıyorsa onu kullan
        } catch (Throwable t) {
            // static initializer must not blow up; log or ignore
            System.err.println("Warning: could not register KeywordRetriever: " + t.getMessage());
        }
    }
}
