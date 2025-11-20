package rag.intents;

public interface IntentDetector {
    Intent detect(String question) throws Exception;
}
