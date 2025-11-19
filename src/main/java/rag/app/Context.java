package rag.app;

import rag.intents.Intent;
import rag.retrieval.Hit;
import rag.answer.Answer;
import java.util.List;

public class Context {

    private final String question;

    private Intent intent;
    private List<String> terms;
    private List<Hit> hits;
    private Answer answer;

    public Context(String question) {
        this.question = question;
    }

    public String getQuestion() { return question; }

    public Intent getIntent() { return intent; }
    public void setIntent(Intent intent) { this.intent = intent; }

    public List<String> getTerms() { return terms; }
    public void setTerms(List<String> terms) { this.terms = terms; }

    public List<Hit> getHits() { return hits; }
    public void setHits(List<Hit> hits) { this.hits = hits; }

    public Answer getAnswer() { return answer; }
    public void setAnswer(Answer answer) { this.answer = answer; }

    public String summary() {
        return "{intent=" + intent +
                ", terms=" + terms +
                ", hits=" + (hits != null ? hits.size() : "null") +
                ", answer=" + (answer != null) +
                "}";
    }
}
