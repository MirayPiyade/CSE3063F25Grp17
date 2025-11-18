## Elif'inkini çarpıp detaylandırdım 

##   Use Case 1 —  Detect intent

  Scope:   MiniRAG Chatbot System
  Level:   Subfunction (System-level use case)
  Primary Actor:   RagOrchestrator (System Controller)
  Supporting Actor:   IntentDetector Component

---

###   Stakeholders and Interests  

    User (Student):  

    Wants the chatbot to correctly understand what type of question is being asked (e.g., course details, staff info, or policy).
    Expects fast and accurate responses without having to manually specify the topic.

    System (MiniRAG Pipeline):  

    Must determine the correct intent category so the next components (QueryWriter, Retriever) can process correctly.
    Requires deterministic behavior — same question and config should always produce the same intent.

    Instructor / TA:  

    Needs clear traceability between this use case, its UML artifacts (SSD, DCD), and the implemented code.
    Expects observable and testable system behavior that can be validated through logs.

    Developer / Maintainer:  

    Wants an easy way to update or extend intent rules (by editing YAML/JSON files, not code).
    Needs modularity to replace rule-based detection with an ML-based classifier later, without modifying orchestrator logic (OCP compliance).

    Logger / Trace System:  

    Records every input, detected intent, processing time, and outcome in JSONL format.
    Provides transparency for debugging and grading reproducibility.

    Future ML Extension (Optional):  

    Will depend on a consistent interface (`IntentDetector` Strategy pattern) for later iterations where an ML model may classify intents probabilistically.

---

###   Preconditions  

  The system is running in CLI mode.
  Configuration file (`config.yaml` or `.json`) is loaded successfully.
  Intent rules and keyword sets are available and valid.
  The user’s question text has been received by the orchestrator.

---

###   Postconditions (Success Guarantees)  

  The question is assigned to one of the intent categories: `CourseInfo`, `StaffLookup`, `PolicyFAQ`, or `Unknown`.
  The selected intent is stored in the shared   Context Object   for the next pipeline stage (`QueryWriter`).
  A   TraceEvent   entry is created with the detected intent and processing time.

---

###   Main Success Scenario  

1. The user enters a question through the CLI interface.
2. The   RagOrchestrator   reads the question and initializes the pipeline context.
3. The orchestrator calls `IntentDetector.detect(question)` using the strategy defined in the config (e.g., `RuleIntentDetector`).
4. The   IntentDetector   loads its keyword rules and intent priorities from the YAML/JSON configuration file.
5. The system normalizes the question text (e.g., lowercasing, trimming).
6. The   IntentDetector   compares the question terms with each intent’s keyword list.
7. The system applies the configured priority list if multiple intents match.
8. The system assigns the most appropriate intent (e.g., `CourseInfo`).
9. The detected intent is stored in the shared   Context Object  .
10. The   TraceBus   publishes an event recording input, intent, and processing metadata to the JSONL trace log.
11. The orchestrator proceeds to the next pipeline stage (`QueryWriter`).

---

###   Extensions (Alternative Scenarios)  

| Step | Condition                             | System Behavior                                                            |
| ---- | ------------------------------------- | -------------------------------------------------------------------------- |
| 2a   | The input question is empty           | The system prompts the user to enter a valid question and logs a warning.  |
| 3a   | Configuration file missing or invalid | The system aborts the run, logs the error, and exits with a failure code.  |
| 6a   | Multiple intents match                | The system applies priority rules and selects the highest-priority intent. |
| 6b   | No keywords match                     | The system assigns `Intent = Unknown` and continues the pipeline.          |
| 10a  | TraceBus write fails                  | The system logs a warning and retries once before continuing.              |

---

###   Special Requirements  

  Intent keyword rules must be loaded from external YAML/JSON configuration files.
  System behavior must be   deterministic  : identical inputs always yield identical intents.
  All text inputs are normalized (lowercased, UTF-8 encoded, punctuation stripped if configured).
  Trace logging must include stage name, intent, and execution time.

---

###   Technology and Data Variations  

    Baseline (Iteration 1):   Rule-based detection using keyword matching and fixed priorities.
    Future Iterations (Iteration 2+):   Optionally extend to ML-based intent classification or hybrid models.
    Configuration:   Strategy implementation specified in the config file (e.g., `detector: RuleIntentDetector`).

---

###   Frequency of Occurrence  

  Once per user query (each run of the pipeline).

---

###   Validation / Test Scenarios  

  Question contains overlapping keywords → system should return intent based on priority list.
  Question with no match → `Intent = Unknown` logged correctly.
  Empty input → validation error message printed.
  Corrupted configuration → system aborts gracefully.

---

###   Open Issues  

  Should future iterations support multi-intent detection (e.g., “Which courses does Dr. Ganiz teach and what are the prerequisites?”)?
  Should the system ask clarification questions if confidence in intent is low?
  How should language-specific stemming and stopword handling affect intent classification?

---
