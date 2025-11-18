Use Case 1 — Detect Intent

Use Case Name: Detect Intent
Scope: MiniRAG Chatbot System
Level: User-goal

Actors:

Primary Actor: User

Secondary Actor: IntentDetector component

Stakeholders and Interests:

User: Wants the system to correctly understand the question topic.

System: Needs to determine the correct intent to route the request properly.

Preconditions:

The system is running.

The user has entered a question in the command-line interface.

Postconditions (Success Guarantees):

The question is assigned to a specific intent category (e.g., CourseInfo, StaffLookup, PolicyFAQ, Unknown).

The selected intent is stored in the shared context for the next pipeline stage.

Main Success Scenario

The user enters a question.

The system reads the question text.

The system compares the question words with predefined intent keyword sets.

The system selects the most appropriate intent based on keyword matches and priority rules.

The system saves the detected intent to the context object.

The system proceeds to the next stage (Write Query).

Extensions (Alternative Scenarios)
Step	Condition	System Behavior
2a	The input question is empty	The system prompts the user to enter a valid question.
4a	Multiple intents match	The system selects the highest priority intent (based on configuration rules).
4b	No keywords match	The system assigns Intent = Unknown, but continues the pipeline.
Special Requirements

Keyword rules must be loaded from a configuration file (YAML or JSON).

Behavior must be deterministic (same input → same output every time).

Technology and Data Variations

Baseline implementation uses rule-based keyword matching.

Additional strategies (e.g., ML-based intent classifier) may be added in later iterations.

Frequency of Occurrence

Once per user question.

Miscellaneous

Test cases must include conflicting-intent keywords, empty input checks, and Unknown intent behavior.