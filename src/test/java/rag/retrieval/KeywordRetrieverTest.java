package rag.retrieval;

import java.util.List;

public class KeywordRetrieverTest {

    public static void main(String[] args) throws Exception {
        DocumentStore store = DocumentStore.load("data/docs.json");
        KeywordRetriever retriever = new KeywordRetriever(5, List.of("CompE", "FoE", "MU"));

        List<Hit> hits = retriever.retrieve(
                "CSE3063 dersinin akts degeri nedir?",
                List.of("cse3063", "akts", "courseinfo"),
                store.getDocuments()
        );

        assert !hits.isEmpty() : "Expected at least one hit";
        assert "compe-course-1".equals(hits.get(0).docId()) : "CompE course should rank first";

        List<Hit> policyHits = retriever.retrieve(
                "Mazeret sinavi policy",
                List.of("policy", "sinavi"),
                store.getDocuments()
        );
        assert policyHits.stream().anyMatch(hit -> hit.docId().equals("mu-policy-1")) : "MU policy document should be found";

        System.out.println("KeywordRetrieverTest passed");
    }
}
