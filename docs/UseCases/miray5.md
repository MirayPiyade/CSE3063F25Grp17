

#   Use Case 5 — Generate Answer  

  Scope:   MiniRAG Chatbot System
  Level:   Subfunction
  Primary Actor:   RagOrchestrator
  Supporting Actor:   AnswerAgent Component

---

###   Stakeholders and Interests  

    User:  

    Wants a concise, readable, and trustworthy answer with proper citations.

    System:  

    Must construct an answer string using the top-ranked chunk.
    Must attach valid citation identifiers.

    Instructor / TA:  

    Requires verifiable citations and deterministic formatting.

    Developer:  

    Wants flexible templates for future answer generation methods.

    Logger:  

    Records final answer and citation IDs.

---

###   Preconditions  

  Ranked document chunks available in context.

---

###   Postconditions  

  Formatted answer with at least one citation is generated.
  Logged in the trace file and printed to stdout.

---

###   Main Success Scenario  

1. Orchestrator calls `AnswerAgent.answer(query, topHits, store)`.
2.   AnswerAgent   selects the top chunk.
3. Splits text into sentences.
4. Chooses sentence containing most query terms.
5. Constructs formatted answer:
   `"Your answer: {sentence}. See: {docId:sectionId:offsetStart–offsetEnd}"`.
6. Logs result in trace file.
7. Prints answer to CLI.

---

###   Extensions  

| Step | Condition                 | System Behavior                  |
| ---- | ------------------------- | -------------------------------- |
| 4a   | No sentence matches       | First sentence used as fallback. |
| 5a   | Missing citation metadata | Default offsets used.            |
| 6a   | Log write fails           | Warning message printed.         |

---

###   Special Requirements  

  Template-driven answer generation.
  UTF-8 text handling.
  At least one valid citation required.

---

###   Technology and Data Variations  

  Baseline: TemplateAnswerAgent.
  Future: Summarization or LLM-based agent.

---

###   Frequency of Occurrence  

  Once per pipeline execution.

