package rag.rerank;

import rag.retrieval.Hit;

import java.util.List;

public class SimpleRerankerTest {

    public static void main(String[] args) {
        SimpleReranker reranker = new SimpleReranker("config/reranker.yaml");

        Hit muHit = new Hit("mu-policy-1", "MU", "MU Makeup Exam Guideline", "Policy text", 1.0);
        Hit compeHit = new Hit("compe-policy-1", "CompE", "CompE Internship Policy", "Policy text", 1.0);

        List<Hit> reranked = reranker.rerank(List.of("policy"), List.of(muHit, compeHit), null);
        assert reranked.get(0).docId().equals("compe-policy-1") : "Source boost should push CompE to the top";

        Hit lowScore = new Hit("foe-policy-2", "FoE", "FoE Technical Trip", "trip policy", 0.1);
        List<Hit> rerankedWithScores = reranker.rerank(List.of("trip"), List.of(lowScore, compeHit), null);
        assert rerankedWithScores.get(0).docId().equals("compe-policy-1") : "Title/proximity boosts should maintain consistent ordering";

        System.out.println("SimpleRerankerTest passed");
    }
}
