# Use Case — Load and Index Knowledge Base  

**Scope:** MiniRAG Chatbot System  
**Level:** Subfunction (System-level use case)  
**Primary Actor:** RagOrchestrator  
**Supporting Actor:** KnowledgeBaseLoader, IndexBuilder Components  

---

### Stakeholders and Interests  

**Student:**  
- Expects accurate answers from updated sources.  

**Content Administrator:**  
- Wants newly added files (JSON/YAML) to be indexed automatically.  

**Developer / Maintainer:**  
- Needs consistent schema and robust file parsing.  

**Instructor / TA:**  
- Needs visibility into which documents were loaded and chunked.  

---

### Preconditions  
1. Knowledge base directories (CompE, FoE, MU) defined in configuration.  
2. JSON/YAML files exist in those directories.  

---

### Postconditions  
- Documents loaded and indexed per source scope.  
- Index reference stored in shared context.  
- Trace event created with doc count, chunk count, and duration.  

---

### Main Success Scenario  
1. Orchestrator calls `KnowledgeBaseLoader.loadAll(config.paths)`.  
2. Loader scans CompE, FoE, MU directories.  
3. Each file is parsed and converted to document models.  
4. Documents tagged with source scope metadata.  
5. Orchestrator calls `IndexBuilder.build(docs)`.  
6. IndexBuilder creates an inverted keyword index.  
7. Index stored in shared context.  
8. TraceBus logs total documents, chunks, and indexing time.  

---

### Extensions  

| Step | Condition | System Behavior |
|------|------------|----------------|
| 2a | Directory empty | Logs warning; continues with remaining directories. |
| 3a | Parse error | Skips faulty file, logs filename and reason. |
| 6a | Memory limit exceeded | Builds simplified index with term frequencies only. |
| 7a | Context write failure | Logs error and stops pipeline safely. |

---

### Special Requirements  
- Only local JSON/YAML files allowed.  
- Each document carries its source scope metadata.  

---

### Technology and Data Variations  
- **Baseline:** Keyword inverted index.  
- **Future:** Embedding-based (vector) retrieval index.  

---

### Frequency of Occurrence  
- Once at pipeline initialization.  
