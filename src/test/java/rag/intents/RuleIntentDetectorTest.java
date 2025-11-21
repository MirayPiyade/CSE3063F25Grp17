package rag.intents;

public class RuleIntentDetectorTest {

    public static void main(String[] args) throws Exception {
        RuleIntentDetector detector = new RuleIntentDetector("config/intents.yaml");

        // Basit eşleşmeler
        assert detector.detect("CSE3063 dersinin akts bilgisi") == Intent.CourseInfo : "CourseInfo intent beklenirdi";
        assert detector.detect("Danisman ofis bilgilerini verebilir misin?") == Intent.StaffLookup : "StaffLookup intent beklenirdi";
        assert detector.detect("Staj yonergesi ve policy detaylari nedir?") == Intent.Policy : "Policy intent beklenirdi";

        // Öncelik testi: hem course hem staff anahtar kelimeleri var, priority listesinde CourseInfo önce gelmeli
        assert detector.detect("akts ve ofis bilgisi") == Intent.CourseInfo : "Öncelik CourseInfo olmalı";

        // Boş/gürültülü giriş Unknown olmalı
        assert detector.detect("   ") == Intent.Unknown : "Boş soru Unknown dönmeli";
        assert detector.detect("Merhaba nasilsin?") == Intent.Unknown : "Eşleşme yoksa Unknown";

        System.out.println("RuleIntentDetectorTest passed");
    }
}
