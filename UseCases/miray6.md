

#   Use Case 6 — Log and Trace Run  

  Scope:   MiniRAG Chatbot System
  Level:   Subfunction
  Primary Actor:   RagOrchestrator
  Supporting Actor:   TraceBus / JsonlTraceSink

---

###   Stakeholders and Interests  

    Instructor / TA:  

    Needs complete traceability for each stage.

    Developer:  

    Requires logs for debugging and performance testing.

    System:  

    Ensures every stage emits standardized `TraceEvent` data.

    Logger (TraceBus):  

    Must collect and persist events reliably.

---

###   Preconditions  

  Log directory exists.
  TraceBus subscribers registered.

---

###   Postconditions  

  JSONL log file created with all events.

---

###   Main Success Scenario  

1. Each pipeline stage publishes `{stage, inputs, outputs, timingMs}`.
2. TraceBus receives event and forwards it to JsonlTraceSink.
3. JsonlTraceSink writes one JSON object per line.
4. Log file saved under `/logs/run-<timestamp>.jsonl`.

---

###   Extensions  

| Step | Condition               | System Behavior                 |
| ---- | ----------------------- | ------------------------------- |
| 3a   | Write permission denied | Logs redirected to stdout.      |
| 4a   | Disk full               | Old logs deleted to free space. |

---

###   Special Requirements  

  Observer pattern must be used.
  Log files must be timestamped.
  Each stage emits consistent schema.

---

###   Frequency of Occurrence  

  Once per pipeline execution (multiple events per run).


