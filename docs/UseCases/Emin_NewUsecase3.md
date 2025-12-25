## New Use Case 3 — Credit Calculation and Tracking

### Primary Actor
User (Student)

### Goal
Obtain information about credit requirements for graduation, understand total AKTS credit requirements, and receive guidance on credit distribution across the curriculum. The system helps students understand credit-related policies and requirements.

### Preconditions
• The system is running and accessible through the CLI.
• Curriculum documents and course credit information have been indexed and are available in the document store.
• Course documents include AKTS credit values.
• Graduation requirement documents are available in the knowledge base.

### Postconditions
• The user receives information about credit requirements and course credit values.
• Credit-related information is displayed with supporting citations.

### Trigger
The user enters a question about credit requirements or course credits (e.g., "How many AKTS credits do I need to graduate?" or "CSE3063 kaç kredi?").

### Main Success Scenario
1. The user enters a question about credit requirements or course credit values.
2. The system detects the user's intent as "Course Information Query" or "Policy Query" depending on the question type.
3. The system extracts keywords from the question related to credits (AKTS, credit, kredi) and graduation requirements or course codes.
4. The retrieval module searches the knowledge base for curriculum, course, and policy documents containing credit information.
5. The system ranks the retrieved results based on relevance, prioritizing documents containing specific credit values or requirement details.
6. The answer generator extracts credit information and formats it clearly.
7. The system displays the credit information and the supporting citation.

### Extensions / Alternative Flows

E1. No Relevant Document Found:

4a. The system cannot find credit information for the requested course or requirement.

4b. The fallback stage returns a response and system terminates.

E2. Ambiguous Results:

5a. Multiple documents contain credit information with conflicting or different values.

5b. The system returns the most relevant result based on source priority and context.

E3. General Credit Requirement Query:

4a. The question asks about total graduation credits without specifying a course.

4b. The system retrieves curriculum or graduation requirement documents and returns total credit requirements if available.

E4. Specific Course Credit Query:

3a. The question asks about credits for a specific course (e.g., "CSE3063 kaç kredi?").

3b. The system extracts the course code and searches course documents specifically.

3c. The system returns the AKTS credit value for the specified course.

### Special Requirements
• The system must respond within a reasonable time (< 5 seconds).
• Information must include citations to ensure reliability.
• Credit values (AKTS) must be accurately extracted from course documents.
• The system must handle both Turkish ("kredi", "AKTS") and English ("credit", "AKTS") terminology.
