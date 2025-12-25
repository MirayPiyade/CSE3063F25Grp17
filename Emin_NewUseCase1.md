## New Use Case 1 — Academic Planning Support

### Primary Actor
User (Student)

### Goal
Obtain comprehensive course information for academic planning, including required courses by semester, core curriculum requirements, and course listings for registration planning.

### Preconditions
• The system is running and accessible through the CLI.
• Curriculum and course documents have been indexed and are available in the document store.
• Course information includes semester assignment and requirement status.

### Postconditions
• The user receives a structured list of courses relevant to their planning query.
• Course information is displayed with supporting citations.

### Trigger
The user enters an academic planning question (e.g., "What courses are required in the first semester?" or "Zorunlu dersler nelerdir?").

### Main Success Scenario
1. The user enters an academic planning question.
2. The system detects the user's intent as "Course Information Query."
3. The system extracts keywords from the question related to semester, course requirements, and curriculum structure.
4. The retrieval module searches the knowledge base for course and curriculum documents.
5. The system ranks the retrieved results based on relevance, prioritizing semester and requirement matches.
6. The answer generator summarizes the relevant course information and constructs a structured response.
7. The system displays the course information and the supporting citation.

### Extensions / Alternative Flows

E1. No Relevant Document Found:

4a. The system cannot find courses matching the specified criteria (e.g., no courses in the requested semester).

4b. The fallback stage returns a response and system terminates.

E2. Ambiguous Results:

5a. Multiple courses or semesters match the query with similar relevance scores.

5b. The system returns the most relevant results and indicates the scope of the response.

E3. Multiple Department Curricula Available:

4a. Multiple curriculum sources (CompE, FoE, MU) contain matching courses.

4b. The system prioritizes results based on source priority configuration.

4c. The system may indicate the source of each course recommendation.

### Special Requirements
• The system must respond within a reasonable time (< 5 seconds).
• Information must include citations to ensure reliability.
• The system must support queries about different semesters (first, second, etc.).
• Course requirements (mandatory, elective, core) should be clearly indicated in responses.
