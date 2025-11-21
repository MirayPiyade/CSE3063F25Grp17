package rag.retrieval;

import java.util.List;

public class KeywordRetrieverTest {

    public static void main(String[] args) {
        // Küçük ve deterministik bir corpus
        Document d1 = new Document("comp-doc", "CompE", "Comp Policy", "policy requirements and forms");
        Document d2 = new Document("mu-doc", "MU", "MU Policy", "policy requirements for students");
        Document d3 = new Document("compe-course", "CompE", "CSE3063", "CSE3063 AKTS bilgisi ve onkosul");

        KeywordRetriever retriever = new KeywordRetriever(2, List.of("CompE", "MU"));

        // Kaynak önceliği: d1 ve d2 aynı skorda, CompE önce gelmeli
        List<Hit> policyHits = retriever.retrieve(
                "policy requirements",
                List.of("policy"),
                List.of(d1, d2)
        );
        assert policyHits.size() == 2 : "İki hit bekleniyor";
        assert "comp-doc".equals(policyHits.get(0).docId()) : "Kaynak önceliği CompE önde olmalı";

        // topK kırpma ve docId tie-break (aynı source ve skor)
        KeywordRetriever retrieverTop1 = new KeywordRetriever(1, List.of("CompE", "MU"));
        List<Hit> top1 = retrieverTop1.retrieve(
                "policy forms",
                List.of("policy", "forms"),
                List.of(d1, d2)
        );
        assert top1.size() == 1 : "topK=1 kırpmalı";

        // Course araması: soru + terim ile en yüksek puan compe-course olmalı
        List<Hit> courseHits = retriever.retrieve(
                "CSE3063 AKTS",
                List.of("cse3063", "akts"),
                List.of(d3, d1)
        );
        assert !courseHits.isEmpty() : "Course hit bulunmalı";
        assert "compe-course".equals(courseHits.get(0).docId()) : "CSE3063 dokümanı önde olmalı";

        System.out.println("KeywordRetrieverTest passed");
    }
}
