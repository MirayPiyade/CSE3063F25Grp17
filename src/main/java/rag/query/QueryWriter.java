package rag.query;

import java.util.*;
import java.util.regex.Pattern;
import java.util.regex.Matcher;

/**
 * QueryWriter class for RAG Chatbot :/ :) :(
 * 
 * This class formats and enhances user queries for better retrieval in the RAG system.
 * It rewrites queries based on provided intent to improve search accuracy and
 * ensures queries are properly formatted for the RAG pipeline.
 * 
 * Note: Intent detection should be done by IntentDetector before calling this class.
 * The orchestrator should pass both the query and the detected intent to this class.
 */
public class QueryWriter {
    
    // Pattern for extracting course codes (e.g., CSE3063, CS101)
    private static final Pattern COURSE_CODE_PATTERN = Pattern.compile(
        "\\b([A-Z]{2,4}\\s*\\d{3,4})\\b", 
        Pattern.CASE_INSENSITIVE
    );
    
    // Pattern for extracting person names (basic pattern)
    private static final Pattern PERSON_NAME_PATTERN = Pattern.compile(
        "\\b(?:Professor|Prof|Dr\\.?|Dr)\\s+([A-Z][a-z]+(?:\\s+[A-Z][a-z]+)?)\\b",
        Pattern.CASE_INSENSITIVE
    );
    
    /**
     * Default constructor for QueryWriter.
     */
    public QueryWriter() {
        // No initialization needed - intent is provided from orchestrator
    }
    
    /**
     * Writes and enhances a query for the RAG system based on provided intent.
     * The orchestrator should detect intent using IntentDetector first, then pass it here.
     * 
     * @param userQuery The original user query
     * @param intent The detected intent (should be detected by IntentDetector in orchestrator)
     * @return An enhanced query string optimized for RAG retrieval
     */
    public String writeQuery(String userQuery, Intent intent) {
        if (userQuery == null || userQuery.trim().isEmpty()) {
            return "";
        }
        
        if (intent == null) {
            intent = Intent.Unknown;
        }
        
        String enhancedQuery = enhanceQuery(userQuery, intent);
        return enhancedQuery.trim();
    }
    
    /**
     * Enhances a query based on the detected intent.
     * 
     * @param query The original query
     * @param intent The detected intent
     * @return Enhanced query string
     */
    private String enhanceQuery(String query, Intent intent) {
        String normalizedQuery = query.trim();
        
        switch (intent) {
            case Registration:
                return enhanceRegistrationQuery(normalizedQuery);
            case StaffLookup:
                return enhanceStaffLookupQuery(normalizedQuery);
            case PolicyFAQ:
                return enhancePolicyFAQQuery(normalizedQuery);
            case Course:
                return enhanceCourseQuery(normalizedQuery);
            case Unknown:
                return normalizedQuery; // Return original query if intent is unknown
            default:
                return normalizedQuery;
        }
    }
    
    /**
     * Enhances queries related to registration.
     */
    private String enhanceRegistrationQuery(String query) {
        String enhanced = query;
        
        // Extract course codes
        List<String> courseCodes = extractCourseCodes(query);
        
        // Add context keywords if not present
        if (!query.toLowerCase().contains("registration") && 
            !query.toLowerCase().contains("enroll") &&
            !query.toLowerCase().contains("register")) {
            enhanced = "registration enrollment " + enhanced;
        }
        
        // Append course codes if found
        if (!courseCodes.isEmpty()) {
            enhanced += " course code: " + String.join(" ", courseCodes);
        }
        
        // Normalize common variations
        enhanced = enhanced.replaceAll("\\b(add|enroll|sign up for)\\b", "register for")
                          .replaceAll("\\b(remove|drop|withdraw from)\\b", "unregister from")
                          .replaceAll("\\bclass\\b", "course");
        
        return enhanced;
    }
    
    /**
     * Enhances queries related to staff lookup.
     */
    private String enhanceStaffLookupQuery(String query) {
        String enhanced = query;
        
        // Extract person names
        List<String> personNames = extractPersonNames(query);
        
        // Extract course mentions for "who teaches" queries
        List<String> courseCodes = extractCourseCodes(query);
        
        // Add context if looking for contact information
        if (query.toLowerCase().matches(".*\\b(email|phone|contact|office)\\b.*")) {
            enhanced = "faculty staff contact information " + enhanced;
        }
        
        // Add context for "who teaches" queries
        if (query.toLowerCase().contains("teaches") || 
            query.toLowerCase().contains("who teaches") ||
            query.toLowerCase().contains("teaches") && !courseCodes.isEmpty()) {
            enhanced = "instructor professor teaching " + enhanced;
        }
        
        // Add person names if found
        if (!personNames.isEmpty()) {
            enhanced = String.join(" ", personNames) + " " + enhanced;
        }
        
        // Normalize variations
        enhanced = enhanced.replaceAll("\\b(prof|professor|dr|doctor)\\s+", "professor ")
                          .replaceAll("\\b(faculty|instructor|lecturer)\\b", "staff");
        
        return enhanced;
    }
    
    /**
     * Enhances queries related to policies and FAQs.
     */
    private String enhancePolicyFAQQuery(String query) {
        String enhanced = query;
        
        // Add university context
        if (!query.toLowerCase().contains("policy") && 
            !query.toLowerCase().contains("rule") &&
            !query.toLowerCase().contains("regulation")) {
            enhanced = "university policy " + enhanced;
        }
        
        // Add FAQ context if asking a question
        if (query.contains("?") || query.toLowerCase().startsWith("what") ||
            query.toLowerCase().startsWith("how") || query.toLowerCase().startsWith("why")) {
            enhanced = "frequently asked question FAQ " + enhanced;
        }
        
        // Normalize policy-related terms
        enhanced = enhanced.replaceAll("\\b(rule|rules|regulation|regulations)\\b", "policy policies")
                          .replaceAll("\\b(requirement|requirements)\\b", "requirement requirement");
        
        return enhanced;
    }
    
    /**
     * Enhances queries related to courses.
     */
    private String enhanceCourseQuery(String query) {
        String enhanced = query;
        
        // Extract course codes
        List<String> courseCodes = extractCourseCodes(query);
        
        // Add course context if not present
        if (!query.toLowerCase().contains("course") && 
            !query.toLowerCase().contains("class")) {
            enhanced = "course " + enhanced;
        }
        
        // Append course codes if found
        if (!courseCodes.isEmpty()) {
            enhanced += " course code: " + String.join(" ", courseCodes);
        }
        
        // Enhance syllabus queries
        if (query.toLowerCase().contains("syllabus") || 
            query.toLowerCase().contains("syllabi")) {
            enhanced = "course syllabus content outline " + enhanced;
        }
        
        // Enhance prerequisite queries
        if (query.toLowerCase().contains("prerequisite") || 
            query.toLowerCase().contains("prereq")) {
            enhanced = "course prerequisite requirement " + enhanced;
        }
        
        // Enhance schedule queries
        if (query.toLowerCase().contains("schedule") || 
            query.toLowerCase().contains("time") ||
            query.toLowerCase().contains("when")) {
            enhanced = "course schedule time " + enhanced;
        }
        
        // Normalize variations
        enhanced = enhanced.replaceAll("\\bclass\\b", "course")
                          .replaceAll("\\b(prereq|pre req|prerequisite)\\b", "prerequisite");
        
        return enhanced;
    }
    
    /**
     * Extracts course codes from a query (e.g., CSE3063, CS101).
     * 
     * @param query The query string
     * @return List of extracted course codes
     */
    private List<String> extractCourseCodes(String query) {
        List<String> courseCodes = new ArrayList<>();
        Matcher matcher = COURSE_CODE_PATTERN.matcher(query);
        
        while (matcher.find()) {
            String code = matcher.group(1).replaceAll("\\s+", "").toUpperCase();
            if (!courseCodes.contains(code)) {
                courseCodes.add(code);
            }
        }
        
        return courseCodes;
    }
    
    /**
     * Extracts person names from a query (e.g., Professor Smith, Dr. Johnson).
     * 
     * @param query The query string
     * @return List of extracted person names
     */
    private List<String> extractPersonNames(String query) {
        List<String> names = new ArrayList<>();
        Matcher matcher = PERSON_NAME_PATTERN.matcher(query);
        
        while (matcher.find()) {
            String name = matcher.group(1);
            if (!names.contains(name)) {
                names.add(name);
            }
        }
        
        return names;
    }
    
    /**
     * Gets metadata about the query including intent, entities, and confidence.
     * The intent and confidence should be provided by the orchestrator.
     * 
     * @param userQuery The original user query
     * @param intent The detected intent (from IntentDetector)
     * @param confidence The confidence score (from IntentDetector)
     * @return QueryMetadata object containing query information
     */
    public QueryMetadata getQueryMetadata(String userQuery, Intent intent, double confidence) {
        if (userQuery == null || userQuery.trim().isEmpty()) {
            return new QueryMetadata("", Intent.Unknown, 0.0, 
                                   new ArrayList<>(), new ArrayList<>());
        }
        
        if (intent == null) {
            intent = Intent.Unknown;
        }
        
        List<String> courseCodes = extractCourseCodes(userQuery);
        List<String> personNames = extractPersonNames(userQuery);
        
        return new QueryMetadata(userQuery, intent, confidence, courseCodes, personNames);
    }
    
    /**
     * Formats a query for logging or display purposes.
     * 
     * @param originalQuery The original query
     * @param enhancedQuery The enhanced query
     * @param intent The detected intent
     * @return Formatted string
     */
    public String formatQueryForLogging(String originalQuery, String enhancedQuery, Intent intent) {
        return String.format(
            "[Intent: %s] Original: \"%s\" | Enhanced: \"%s\"",
            intent, originalQuery, enhancedQuery
        );
    }
    
    /**
     * Inner class to hold query metadata.
     */
    public static class QueryMetadata {
        private String originalQuery;
        private Intent intent;
        private double confidence;
        private List<String> courseCodes;
        private List<String> personNames;
        
        public QueryMetadata(String originalQuery, Intent intent, double confidence,
                           List<String> courseCodes, List<String> personNames) {
            this.originalQuery = originalQuery;
            this.intent = intent;
            this.confidence = confidence;
            this.courseCodes = new ArrayList<>(courseCodes);
            this.personNames = new ArrayList<>(personNames);
        }
        
        public String getOriginalQuery() { return originalQuery; }
        public Intent getIntent() { return intent; }
        public double getConfidence() { return confidence; }
        public List<String> getCourseCodes() { return new ArrayList<>(courseCodes); }
        public List<String> getPersonNames() { return new ArrayList<>(personNames); }
        
        @Override
        public String toString() {
            return String.format(
                "QueryMetadata{query='%s', intent=%s, confidence=%.2f, courseCodes=%s, personNames=%s}",
                originalQuery, intent, confidence, courseCodes, personNames
            );
        }
    }   
}

