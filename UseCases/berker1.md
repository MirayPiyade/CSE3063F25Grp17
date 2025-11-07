# Use Case — Load and Validate Configuration  

**Scope:** MiniRAG Chatbot System  
**Level:** Subfunction (System-level use case)  
**Primary Actor:** RagOrchestrator (System Controller)  
**Supporting Actor:** ConfigLoader Component  

---

### Stakeholders and Interests  

**Student / User:**  
- Expects deterministic system behavior across runs.  
- Wants predictable responses based on configuration.  

**Developer / Maintainer:**  
- Wants all parameters (paths, top-K values, thresholds, strategies) to be externalized in YAML/JSON.  
- Needs validation and graceful error handling for invalid configuration.  

**Instructor / TA:**  
- Needs configuration traceability for grading and experiment reproducibility.  

**Logger / Trace System:**  
- Logs configuration file name, version, and key parameters for each run.  

---

### Preconditions  
1. CLI mode is active.  
2. Configuration file path is known or defaulted.  

---

### Postconditions (Success Guarantees)  
- A validated configuration object is loaded and stored in the shared context.  
- A trace event is generated summarizing config version and load time.  

---

### Main Success Scenario  
1. Student runs `python main.py --config config.yaml`.  
2. **RagOrchestrator** calls `ConfigLoader.load(configPath)`.  
3. **ConfigLoader** locates and parses the YAML/JSON file.  
4. Schema validation checks mandatory fields.  
5. Default values are assigned where missing.  
6. The configuration object is stored in context.  
7. **TraceBus** publishes an event with configuration summary.  
8. Orchestrator proceeds to the next stage (IntentDetector).  

---

### Extensions  

| Step | Condition | System Behavior |
|------|------------|----------------|
| 3a | Config file missing | System logs error and aborts run. |
| 3b | Parse error | Logs “Invalid configuration format.” and exits. |
| 4a | Required field missing | Validation fails and pipeline stops safely. |
| 7a | TraceBus write fails | Warning logged; pipeline continues. |

---

### Special Requirements  
- Config schema must be documented.  
- Deterministic behavior for identical inputs.  
- Config path and file name must be logged.  

---

### Technology and Data Variations  
- **Baseline:** YAML-based configuration.  
- **Future:** Environment variable overrides or multiple layered configs.  

---

### Frequency of Occurrence  
- Once per pipeline run.  
