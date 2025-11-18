package rag.app;

import rag.answer.Answer;
import rag.intents.Intent;
import rag.retrieval.Hit;

import java.util.List;

public class Context {
    private String question;
    private Intent intent;
    private List<String> terms;
    private List<Hit> hits;
    private Answer answer;

    public Context(String question) { this.question = question; }

    public String getQuestion() { return question; }
    public void setIntent(Intent intent) { this.intent = intent; }
    public Intent getIntent() { return intent; }

    public void setTerms(List<String> terms) { this.terms = terms; }
    public List<String> getTerms() { return terms; }

    public void setHits(List<Hit> hits) { this.hits = hits; }
    public List<Hit> getHits() { return hits; }

    public void setAnswer(Answer answer) { this.answer = answer; }
    public Answer getAnswer() { return answer; }
}
