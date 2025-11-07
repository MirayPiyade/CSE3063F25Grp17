#   Use Case 4 — Rerank Results  

  Scope:   MiniRAG Chatbot System
  Level:   Subfunction
  Primary Actor:   RagOrchestrator
  Supporting Actor:   Reranker Component

---

###   Stakeholders and Interests  

    User:  

    Wants the most relevant text chunks to appear first.

    System:  

    Must apply deterministic scoring bonuses.

    Developer / Maintainer:  

    Wants easily replaceable reranking strategies (e.g., NoOpReranker).

    Instructor / TA:  

    Needs reproducible scoring logic for grading and verification.

---

###   Preconditions  

  Retrieved hits are available in the context.
  Query text is known.

---

###   Postconditions  

  Hits reordered according to reranking scores.
  Updated ranking stored in context and trace log.

---

###   Main Success Scenario  

1. The orchestrator calls `Reranker.rerank(query, hits, metadata)`.
2.   Reranker   calculates each hit’s adjusted score:

     `score = tf_sum   10 + proximityBonus + titleBoost`.
3. Proximity bonus applied if two query terms are within 15 characters.
4. Title boost applied if query term appears in document title.
5. Hits sorted by new score (DESC, docId ASC, chunkId ASC).
6. Reordered results stored in context.
7. Trace event logged.

---

###   Extensions  

| Step | Condition             | System Behavior      |
| ---- | --------------------- | -------------------- |
| 3a   | No proximity detected | Proximity bonus = 0. |
| 4a   | No title info         | Title boost skipped. |
| 5a   | Tie                   | Stable sort applied. |

---

###   Special Requirements  

  Deterministic scoring and tie-breaking.
  Configurable bonuses.

---

###   Technology and Data Variations  

  Baseline: SimpleReranker.
  Future: HybridReranker (e.g., Jaccard or cosine).

---

###   Frequency of Occurrence  

  Once per query, after retrieval.

---