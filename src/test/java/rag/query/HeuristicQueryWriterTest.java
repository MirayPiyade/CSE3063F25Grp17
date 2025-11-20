package rag.query;

import rag.intents.Intent;

import java.util.List;

public class HeuristicQueryWriterTest {

    public static void main(String[] args) throws Exception {
        HeuristicQueryWriter writer = new HeuristicQueryWriter("config/stopwords.yaml");

        List<String> courseTerms = writer.write("CSE3063 dersinin AKTS degeri nedir?", Intent.CourseInfo);
        assert courseTerms.contains("cse3063");
        assert !courseTerms.contains("nedir") : "Stopwords should be removed";
        assert courseTerms.contains("course") : "CourseInfo boosters should be appended";
        assert courseTerms.contains("bilgi") : "Unknown boosters should be appended";
        assert courseTerms.get(courseTerms.size() - 1).equals("courseinfo") : "Intent name should be appended";

        List<String> shortQuestionTerms = writer.write("ve nedir", Intent.Unknown);
        assert shortQuestionTerms.contains("ve") : "Short questions retain stopwords";

        System.out.println("HeuristicQueryWriterTest passed");
    }
}
