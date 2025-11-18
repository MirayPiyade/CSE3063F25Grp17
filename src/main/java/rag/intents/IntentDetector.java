package rag.intents;

import java.util.*;

/**
 * IntentDetector class for University RAG Chatbot
 * Analyzes user input to determine the intent behind university-related queries.
 * 
 * This class uses pattern matching and keyword analysis to classify
 * user intents into: Registration, StaffLookup, PolicyFAQ, Course, or Unknown.
 * This helps route queries to appropriate handlers in the RAG system.
 */
public class IntentDetector {
    
    // Keywords and patterns for Registration intent
    private static final Set<String> REGISTRATION_KEYWORDS = new HashSet<>(Arrays.asList(
        "register", "registration", "enroll", "enrollment", "enrol", "sign up", 
        "add course", "drop course", "withdraw", "add/drop", "course registration",
        "register for", "enroll in", "sign up for", "add class", "drop class",
        "course schedule", "registration deadline", "preregistration", "preregister",
        "waitlist", "wait list", "course capacity", "full course"
    ));
    
    // Keywords and patterns for StaffLookup intent
    private static final Set<String> STAFF_LOOKUP_KEYWORDS = new HashSet<>(Arrays.asList(
        "staff", "professor", "prof", "faculty", "instructor", "lecturer", "teacher",
        "find", "lookup", "look up", "contact", "email", "phone", "office", 
        "office hours", "office location", "department", "who teaches", 
        "who is", "faculty member", "staff member", "academic staff",
        "professor name", "instructor name", "faculty directory", "staff directory"
    ));
    
    // Keywords and patterns for PolicyFAQ intent
    private static final Set<String> POLICY_FAQ_KEYWORDS = new HashSet<>(Arrays.asList(
        "policy", "policies", "rule", "rules", "regulation", "regulations",
        "faq", "frequently asked", "question", "requirement", "requirements",
        "guideline", "guidelines", "procedure", "procedures", "process",
        "academic policy", "university policy", "student policy", "grading policy",
        "attendance policy", "exam policy", "plagiarism", "academic integrity",
        "code of conduct", "student handbook", "what is the policy", "how to"
    ));
    
    // Keywords and patterns for Course intent
    private static final Set<String> COURSE_KEYWORDS = new HashSet<>(Arrays.asList(
        "course", "courses", "class", "classes", "syllabus", "syllabi", 
        "schedule", "prerequisite", "prerequisites", "credit", "credits",
        "course code", "course number", "course description", "course content",
        "textbook", "textbooks", "required book", "course material", "course outline",
        "lecture", "lectures", "lab", "laboratory", "tutorial", "tutorials",
        "exam", "exams", "midterm", "final", "assignment", "assignments",
        "course evaluation", "course rating", "gpa", "grade", "grades"
    ));
    
    /**
     * Detects the intent from user input text.
     * Priority order: Registration > StaffLookup > PolicyFAQ > Course > Unknown
     * 
     * @param userInput The user's input text
     * @return The detected Intent
     */
    public Intent detectIntent(String userInput) {
        if (userInput == null || userInput.trim().isEmpty()) {
            return Intent.Unknown;
        }
        
        // Normalize input: convert to lowercase and trim
        String normalizedInput = userInput.toLowerCase().trim();
        
        // Check for Registration intent (highest priority)
        if (isRegistration(normalizedInput)) {
            return Intent.Registration;
        }
        
        // Check for StaffLookup intent
        if (isStaffLookup(normalizedInput)) {
            return Intent.StaffLookup;
        }
        
        // Check for PolicyFAQ intent
        if (isPolicyFAQ(normalizedInput)) {
            return Intent.PolicyFAQ;
        }
        
        // Check for Course intent
        if (isCourse(normalizedInput)) {
            return Intent.Course;
        }
        
        // If no specific intent detected, return Unknown
        return Intent.Unknown;
    }
    
    /**
     * Checks if the input is related to Registration.
     */
    private boolean isRegistration(String input) {
        // Check for multi-word registration phrases first (more specific)
        for (String keyword : REGISTRATION_KEYWORDS) {
            if (input.contains(keyword)) {
                return true;
            }
        }
        
        // Check individual words
        String[] words = input.split("\\s+");
        for (String word : words) {
            word = word.replaceAll("[^a-zA-Z]", "");
            if (REGISTRATION_KEYWORDS.contains(word)) {
                return true;
            }
        }
        
        return false;
    }
    
    /**
     * Checks if the input is related to StaffLookup.
     */
    private boolean isStaffLookup(String input) {
        // Check for multi-word staff lookup phrases first
        for (String keyword : STAFF_LOOKUP_KEYWORDS) {
            if (input.contains(keyword)) {
                return true;
            }
        }
        
        // Check individual words
        String[] words = input.split("\\s+");
        for (String word : words) {
            word = word.replaceAll("[^a-zA-Z]", "");
            if (STAFF_LOOKUP_KEYWORDS.contains(word)) {
                return true;
            }
        }
        
        return false;
    }
    
    /**
     * Checks if the input is related to PolicyFAQ.
     */
    private boolean isPolicyFAQ(String input) {
        // Check for multi-word policy/FAQ phrases first
        for (String keyword : POLICY_FAQ_KEYWORDS) {
            if (input.contains(keyword)) {
                return true;
            }
        }
        
        // Check individual words
        String[] words = input.split("\\s+");
        for (String word : words) {
            word = word.replaceAll("[^a-zA-Z]", "");
            if (POLICY_FAQ_KEYWORDS.contains(word)) {
                return true;
            }
        }
        
        return false;
    }
    
    /**
     * Checks if the input is related to Course.
     */
    private boolean isCourse(String input) {
        // Check for multi-word course phrases first
        for (String keyword : COURSE_KEYWORDS) {
            if (input.contains(keyword)) {
                return true;
            }
        }
        
        // Check individual words
        String[] words = input.split("\\s+");
        for (String word : words) {
            word = word.replaceAll("[^a-zA-Z]", "");
            if (COURSE_KEYWORDS.contains(word)) {
                return true;
            }
        }
        
        return false;
    }
    
    /**
     * Gets confidence score for the detected intent (0.0 to 1.0).
     * Higher score means more confident detection.
     * 
     * @param userInput The user's input text
     * @param detectedIntent The detected intent
     * @return Confidence score between 0.0 and 1.0
     */
    public double getConfidence(String userInput, Intent detectedIntent) {
        if (userInput == null || userInput.trim().isEmpty()) {
            return 0.0;
        }
        
        String normalizedInput = userInput.toLowerCase().trim();
        int matches = 0;
        int totalWords = normalizedInput.split("\\s+").length;
        
        switch (detectedIntent) {
            case Registration:
                for (String keyword : REGISTRATION_KEYWORDS) {
                    if (normalizedInput.contains(keyword)) {
                        matches++;
                    }
                }
                break;
            case StaffLookup:
                for (String keyword : STAFF_LOOKUP_KEYWORDS) {
                    if (normalizedInput.contains(keyword)) {
                        matches++;
                    }
                }
                break;
            case PolicyFAQ:
                for (String keyword : POLICY_FAQ_KEYWORDS) {
                    if (normalizedInput.contains(keyword)) {
                        matches++;
                    }
                }
                break;
            case Course:
                for (String keyword : COURSE_KEYWORDS) {
                    if (normalizedInput.contains(keyword)) {
                        matches++;
                    }
                }
                break;
            case Unknown:
                return 0.1; // Low confidence for unknown intents
        }
        
        // Calculate confidence based on matches
        // More matches = higher confidence
        double confidence = Math.min(1.0, (double) matches / Math.max(1, totalWords / 3));
        return Math.max(0.3, confidence); // Minimum confidence of 0.3 for detected intents
    }
    
