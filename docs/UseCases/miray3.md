
#   Use Case 3 — Retrieve Documents  

  Scope:   MiniRAG Chatbot System
  Level:   Subfunction (System-level)
  Primary Actor:   RagOrchestrator
  Supporting Actor:   Retriever Component

---

###   Stakeholders and Interests  

    User:  

    Wants the system to find the most relevant information sources.

    System:  

    Must locate document chunks matching the query terms from the keyword index.

    Developer:  

    Needs retrieval to be reproducible for unit testing.

    Instructor / TA:  

    Needs clear output showing top-K chunks and deterministic tie-breaking.

    Logger:  

    Records each retrieval query, top-K results, and scores.

---

###   Preconditions  

  The query term list is available in the context.
  Keyword index file is loaded.

---

###   Postconditions  

  Top-K document chunks are retrieved and sorted by score.
  Results are stored in the context.
  Trace entry created with retrieval summary.

---

###   Main Success Scenario  

1. The orchestrator calls `Retriever.retrieve(terms, index)`.
2. The   Retriever   loads the keyword index into memory.
3. Each term’s occurrences are located in the index.
4. Each chunk’s score = sum of term frequencies (TF).
5. Chunks are sorted by descending score, then by docId, then chunkId (tie-break).
6. The top K (default 10) results are stored in the context.
7. A trace log records the retrieved hits.

---

###   Extensions  

| Step | Condition             | System Behavior                               |
| ---- | --------------------- | --------------------------------------------- |
| 2a   | Index file missing    | System logs error and halts pipeline.         |
| 4a   | Query terms not found | Empty result set returned with warning.       |
| 5a   | Tie in scores         | Deterministic tie-breaking by docId, chunkId. |

---

###   Special Requirements  

  Deterministic output order.
  Configurable top-K.

---

###   Technology and Data Variations  

  Baseline: KeywordRetriever.
  Future: VectorRetriever (semantic search).

---

###   Frequency of Occurrence  

  Once per query.

---
