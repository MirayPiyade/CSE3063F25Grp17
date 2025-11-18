package rag.intents;

public enum Intent {
    Registration,       // User queries about course registration, enrollment, etc.
    StaffLookup,        // User queries about finding staff, professors, faculty members
    PolicyFAQ,          // User queries about university policies, rules, FAQs
    Course,             // User queries about courses, classes, schedules, syllabi
    Unknown             // When Intent cannot be determined
}
