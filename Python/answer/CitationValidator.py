from typing import List

class CitationValidator:

    def validate(self, citations: List[str]) -> bool:
        if not citations:
            return False
        return all(c and c.strip() for c in citations)


