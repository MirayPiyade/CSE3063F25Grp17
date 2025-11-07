# Use Case — Enforce Hierarchical Retrieval Priority  

**Scope:** MiniRAG Chatbot System  
**Level:** Subfunction (System-level use case)  
**Primary Actor:** RagOrchestrator  
**Supporting Actor:** HierarchicalRetriever Component  

---

### Stakeholders and Interests  

**Student:**  
- Expects answers to come from the most relevant (CompE first) sources.  

**University / Department:**  
- Prefers departmental documents to override generic university policies.  

**Developer / Maintainer:**  
- Needs configurable, rule-based retrieval order.  

**Instructor / TA:**  
- Requires trace logs showing source-level retrieval order and hit counts.  

---

### Preconditions  
1. Index sets for CompE, FoE, and MU are available.  
2. Query and detected intent ready.  

---

### Postconditions  
- Retrieval executed in the priority order CompE → FoE → MU.  
- Results merged respecting score and priority.  
- Trace event recorded for each retrieval stage.  

---

### Main Success Scenario  
1. Orchestrator calls `HierarchicalRetriever.search(query, indexSets)`.  
2. Retriever loads priority order from config (default CompE > FoE > MU).  
3. Searches CompE index.  
4. If enough results, stops and returns.  
5. Otherwise searches FoE index, merges results.  
6. If still insufficient, searches MU index.  
7. Final results merged and sorted by score and priority.  
8. TraceBus logs hit count, latency, and sources.  

---

### Extensions  

| Step | Condition | System Behavior |
|------|------------|----------------|
| 3a | CompE index missing | Starts from FoE index, logs warning. |
| 5a | FoE has strong results | Still prioritizes CompE results in tie-breaking. |
| 7a | Equal scores | Uses deterministic order CompE > FoE > MU. |

---

### Special Requirements  
- Priority rule strictly follows CompE → FoE → MU order.  
- Deterministic merging and tie-breaking.  

---

### Technology and Data Variations  
- **Baseline:** Term frequency + fixed weights.  
- **Future:** Weighted hybrid scoring by source importance.  

---

### Frequency of Occurrence  
- Once per query in UC-1: Find Answer to Query.  
