package rag.intents;

public class RuleIntentDetectorTest {

    public static void main(String[] args) throws Exception {
        RuleIntentDetector detector = new RuleIntentDetector("config/intents.yaml");

        assert detector.detect("CSE3063 dersinin akts bilgisi") == Intent.CourseInfo : "Expected CourseInfo intent";
        assert detector.detect("Danisman ofis bilgilerini verebilir misin?") == Intent.StaffLookup : "Expected StaffLookup intent";
        assert detector.detect("Staj yonergesi ve policy detaylari nedir?") == Intent.Policy : "Expected Policy intent";
        assert detector.detect("Merhaba nasilsin?") == Intent.Unknown : "Expected Unknown intent";

        System.out.println("RuleIntentDetectorTest passed");
    }
}
