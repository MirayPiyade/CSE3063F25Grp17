# Requirement Analysis Document (RAD) - RAG Chatbot
# 1. Introduction
The system's purpose is to answer user queries based on a local knowledge base, with a specific focus on Marmara University information.
The system will prioritize information retrieval in the following order:
1.	Computer Engineering (CompE) Department documents.
2.	Faculty of Engineering (FoE) documents.
3.	General Marmara University (MU) policies and regulations.
The system will not have a GUI or a database, relying solely on local JSON or YAML files for its knowledge base.

# 2. Actors
- Student: The primary user seeking information from the chatbot. (This can be any user, such as a student, faculty member, or staff).
- Content Administrator: A user (likely a student or department admin) responsible for updating, adding, or deleting the local knowledge base files (JSON/YAML) that the chatbot uses.

# 3. Use Case Diagram (Context)
This diagram shows the main user-goal use cases.

    | (Student) | ------> | [UC-1: Find Answer to Query] |
   
            |
            | (System Boundary: RAG Chatbot)
            V
                                                              
    | [UC-2: Manage Knowledge Base] |    <----     | (Content Admin) |
        
# 4. Use Case Specifications
## UC-1: Find Answer to Query
### Use Case Name: Find Answer to Query
-	Scope: RAG Chatbot System
-	Level: User-goal (This is an "Elementary Business Process").
  ### Actors:
-	Primary: Student
### Stakeholders and Interests:
-	Student: Wants a fast, accurate, and relevant answer to their question.
-	University/Department: Wants to provide information efficiently and reduce repetitive inquiries.
###	Preconditions:
1.	The RAG chatbot application is running.
2.	The knowledge base files (e.g., compe.json, foe.json, university.json) exist, are accessible, and are populated with data.
### Postconditions (Success Guarantee):
- The system provides the Student with a synthesized answer and its sources, or a message indicating the information could not be found.
### Main Success Scenario :
1.	The Student starts the application (e.g., runs the console command).
2.	The System loads and indexes the knowledge base files from the local directory.
3.	The System prompts the Student for a query.
4.	The Student submits a query (e.g., "What are the prerequisite courses for CSE 3063?").
5.	The System analyzes the query.
6.	The System searches the knowledge base using the specified retrieval hierarchy:
- a. It searches the "Computer Engineering" (CompE) document store.
- b. If relevant information is not found (or below a confidence threshold), it expands the search to the "Faculty of Engineering" (FoE) document store.
- c. If relevant information is still not found, it expands the search to the "University Policies" (MU) document store.
7.	The System retrieves the most relevant text chunk(s) from the documents (the "Retrieval" step).
8.	The System passes the original query and the retrieved text chunk(s) to the generation component (the "Generation" step).
9.	The System generates a concise, natural language answer based only on the retrieved context.
10.	The System presents the generated answer and the source(s).
### Extensions (Alternate Scenarios):
- a. No relevant documents found.
- If, after searching all hierarchical stores, no relevant document chunks are found, the system skips to step 10.
- System presents a message: "I could not find any relevant information about your query in the available documents."
- b. Generation component fails or produces a low-quality answer.
- System presents a message: "I found relevant information but could not generate a summary. Please check this source: [Retrieved text chunk and source]."
### Special Requirements:
- SR-1: All knowledge base data must be loaded from local JSON or YAML files.
- SR-2: The retrieval search must follow the CompE -> FoE -> MU hierarchy.
- SR-3: The system must be a console-based application (No GUI).
- SR-4: Traceability: All classes and methods implementing this use case (e.g., QueryHandler, HierarchicalRetriever, AnswerGenerator) must be traceable to these steps.
# UC-2: Manage Knowledge Base
### Use Case Name: Manage Knowledge Base
### Scope: RAG Chatbot System (from the perspective of its data source).
### Level: User-goal (EBP).
###	Actors:
-	Primary: Content Administrator
###	Stakeholders and Interests:
-Content Administrator: Wants a simple, defined process to update the chatbot's knowledge to keep it accurate.
-	Student: (Indirect) Benefits from accurate and up-to-date information.
###	Preconditions:
1.	The Content Administrator has the new/updated information (e.g., a downloaded text page).
2.	The Content Administrator has write-access to the knowledge base file directory.
###	Postconditions (Success Guarantee):
- The specified knowledge base file (e.g., compe.json) is created, updated, or deleted on the file system.
### Main Success Scenario (Updating a Document):
1.	The Content Administrator obtains new information (e.g., "New internship policy").
2.	The Administrator manually converts this information into the required, structured JSON or YAML format.
3.	The Administrator opens the corresponding local file (e.g., compe.json).
4.	The Administrator adds the new JSON/YAML object to the file and saves it.
5.	The next time the RAG Chatbot (UC-1) is run, it will automatically load this new information.
### Special Requirements:
-	SR-1: The data structure (schema) for the JSON/YAML files must be clearly defined and documented.
