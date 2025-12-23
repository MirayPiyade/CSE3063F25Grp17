from typing import List, Optional


class CitationValidator:
    def validate(self, citations: Optional[List[str]]) -> bool:
        if not citations:
            return False
        return all(c is not None and c.strip() for c in citations)






