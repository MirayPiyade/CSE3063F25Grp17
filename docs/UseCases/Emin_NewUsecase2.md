## New Use Case 2 — Prerequisite Chain Analysis

### Primary Actor
User (Student)

### Goal
Determine whether a student is eligible to take a specific course by analyzing prerequisite requirements and course dependencies. The system should identify prerequisite courses and help students understand the course dependency chain.

### Preconditions
• The system is running and accessible through the CLI.
• Course documents include prerequisite information (course codes and requirements).
• Prerequisite relationships are documented in the knowledge base.

### Postconditions
• The user receives information about course prerequisites.
• Prerequisite course codes and requirements are clearly displayed with citations.

### Trigger
The user enters a question about course prerequisites or eligibility (e.g., "Can I take CSE3063?" or "CSE3063 onkosul nedir?").

### Main Success Scenario
1. The user enters a question about course prerequisites or eligibility.
2. The system detects the user's intent as "Course Information Query."
3. The system extracts keywords from the question, including the course code and prerequisite-related terms.
4. The retrieval module searches the knowledge base for the course document and prerequisite information.
5. The system ranks the retrieved results based on relevance, prioritizing documents containing both the course code and prerequisite details.
6. The answer generator extracts prerequisite information and formats it clearly.
7. The system displays the prerequisite requirements and the supporting citation.

### Extensions / Alternative Flows

E1. No Relevant Document Found:

4a. The system cannot find a matching document for the requested course or prerequisite information.

4b. The fallback stage returns a response and system terminates.

E2. Ambiguous Results:

5a. Multiple courses match the query, or the course code is partially specified.

5b. The system returns the most probable match based on course code similarity and context.

E3. Course Code Missing or Partial:

3a. The question does not contain a clear course code (e.g., "What are the prerequisites?").

3b. The system attempts to retrieve prerequisite information from context or returns a general message requesting a course code.

E4. Alternative Prerequisites (Instructor Approval):

5a. The prerequisite includes alternative conditions (e.g., "CSE2045 or instructor approval").

5b. The system includes all alternative prerequisites in the response.

### Special Requirements
• The system must respond within a reasonable time (< 5 seconds).
• Information must include citations to ensure reliability.
• Course codes should be recognized even when written in lowercase or with variations (e.g., "cse3063", "CSE 3063").
• Prerequisite course codes must be accurately extracted and displayed.
