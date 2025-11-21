package rag.rerank;

import rag.retrieval.Hit;

import java.util.List;

public class SimpleRerankerTest {

    public static void main(String[] args) {
        SimpleReranker reranker = new SimpleReranker("config/reranker.yaml");

        Hit muHit = new Hit("mu-policy-1", "MU", "MU Makeup Exam Guideline", "Policy text with makeup exam details", 1.0);
        Hit compeHit = new Hit("compe-policy-1", "CompE", "CompE Internship Policy", "Policy text", 1.0);

        // Kaynak boost: CompE > MU
        List<Hit> reranked = reranker.rerank(List.of("policy"), List.of(muHit, compeHit), null);
        assert reranked.get(0).docId().equals("compe-policy-1") : "Source boost CompE'yi üste taşımalı";

        // Proximity bonus: technical/trip yakın duruyor, FoE öne geçmeli
        Hit proximityHit = new Hit(
                "foe-policy-2",
                "FoE",
                "FoE Technical Trip",
                "technical trip insurance forms must be filed",
                0.2
        );
        List<Hit> rerankedWithProximity = reranker.rerank(
                List.of("technical", "trip"),
                List.of(proximityHit, compeHit),
                null
        );
        assert rerankedWithProximity.get(0).docId().equals("foe-policy-2") : "Proximity bonus FoE'yi öne almalı";

        // Title boost: başlıkta 'policy' geçen doküman, eşit skor durumunda öne çıkmalı
        Hit titleHit = new Hit("title-hit", "MU", "Policy Overview", "generic text", 0.5);
        Hit plainHit = new Hit("plain-hit", "MU", "Overview", "generic text", 0.5);
        List<Hit> titleCheck = reranker.rerank(
                List.of("policy"),
                List.of(titleHit, plainHit),
                null
        );
        assert titleCheck.get(0).docId().equals("title-hit") : "Title boost 'policy' içeren başlığı öne taşımalı";

        System.out.println("SimpleRerankerTest passed");
    }
}
