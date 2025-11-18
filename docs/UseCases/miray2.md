#   Use Case 2 — Write Query  

  Scope:   MiniRAG Chatbot System
  Level:   Subfunction (System-level)
  Primary Actor:   RagOrchestrator (System Controller)
  Supporting Actor:   QueryWriter Component

---

###   Stakeholders and Interests  

    User (Student):  

    Wants the system to understand their question and extract the important search terms automatically.
    Expects relevant documents to be retrieved even if question phrasing varies.

    System (MiniRAG Pipeline):  

    Must generate effective query terms based on detected intent.
    Needs to handle stopwords, duplicates, and stemming consistently.

    Developer / Maintainer:  

    Requires the query generation process to be configurable and testable (e.g., stopword list, boosters).
    Wants flexible strategy substitution for different query writing techniques.

    Instructor / TA:  

    Needs traceability of query output and correctness validation for grading.

    Trace System:  

    Logs the generated query terms and their derivation from input.

---

###   Preconditions  

  Detected intent is available in the context.
  Stopword and booster lists are loaded from the configuration file.

---

###   Postconditions (Success Guarantees)  

  A list of processed query terms is stored in the shared context.
  A `TraceEvent` is recorded with original question, intent, and generated query terms.

---

###   Main Success Scenario  

1. The orchestrator calls `QueryWriter.write(question, intent)`.
2. The   QueryWriter   loads configuration values such as stopword list and booster terms.
3. The system normalizes the question (lowercasing, removing punctuation).
4. Stopwords are removed.
5. Duplicate terms are filtered, preserving order.
6. Intent-specific booster words are added (e.g., “advisor” for StaffLookup).
7. The resulting query term list is stored in the context.
8. The system emits a `TraceEvent` summarizing the query generation step.

---

###   Extensions (Alternative Scenarios)  

| Step | Condition                         | System Behavior                                                  |
| ---- | --------------------------------- | ---------------------------------------------------------------- |
| 2a   | Missing or invalid config file    | System loads default stopword and booster lists.                 |
| 3a   | Question is too short (1–2 words) | System uses the full question as the query without modification. |
| 5a   | Query list empty                  | System logs a warning and continues with an empty query set.     |

---

###   Special Requirements  

  Deterministic ordering of terms.
  Configuration-driven stopword and booster management.
  UTF-8 normalization.

---

###   Technology and Data Variations  

  Baseline: HeuristicQueryWriter (rule-based).
  Future: LLM-assisted or embedding-based query writing.

---

###   Frequency of Occurrence  

  Once per question, following intent detection.

---

###   Open Issues  

  Should phrase-based queries (n-grams) be supported in later versions?
  Should query length be limited for efficiency?

