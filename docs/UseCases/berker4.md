# Use Case — Handle Out-of-Scope or Ambiguous Queries  

**Scope:** MiniRAG Chatbot System  
**Level:** Subfunction (System-level use case)  
**Primary Actor:** RagOrchestrator  
**Supporting Actor:** FallbackHandler Component  

---

### Stakeholders and Interests  

**Student:**  
- Wants honest, clear feedback when the system cannot answer.  

**University / Department:**  
- Avoids misinformation and hallucinated responses.  

**Developer / Maintainer:**  
- Needs configurable fallback messages and thresholds.  

**Instructor / TA:**  
- Requires trace logs for out-of-scope or low-confidence cases.  

---

### Preconditions  
- Retrieval and/or generation completed but:  
  - No relevant hits found, **or**  
  - Intent = Unknown, **or**  
  - Generated answer confidence is too low.  

---

### Postconditions  
- User receives a fallback message (e.g., “I couldn’t find information about that topic.”).  
- Trace event recorded with reason code (`OutOfScope`, `NoHits`, `LowConfidence`).  

---

### Main Success Scenario  
1. Orchestrator reviews retrieval and generation outputs.  
2. Checks if criteria for fallback apply.  
3. If yes, calls `FallbackHandler.handle(context)`.  
4. Handler selects appropriate message template.  
5. Constructs fallback answer.  
6. Writes message to context.  
7. TraceBus logs fallback type and reason.  

---

### Extensions  

| Step | Condition | System Behavior |
|------|------------|----------------|
| 2a | Query too short | Prompts for clarification instead. |
| 4a | No template found | Uses default “information not found” message. |
| 7a | Trace write fails | Prints warning but continues normally. |

---

### Special Requirements  
- Fallback messages must never contain fabricated data.  
- Each fallback event must include a clear reason code.  

---

### Technology and Data Variations  
- **Baseline:** Static string templates.  
- **Future:** Contextual guidance or web link recommendations.  

---

### Frequency of Occurrence  
- 0 or 1 time per query (only when errors or uncertainty occur).  
