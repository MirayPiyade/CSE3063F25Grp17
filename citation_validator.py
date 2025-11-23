"""Citation validator."""
from typing import List


class CitationValidator:
    """Validates answer citations."""

    def validate(self, citations: List[str]) -> bool:
        """Validate that citations are non-empty."""
        if not citations:
            return False
        return all(c and c.strip() for c in citations)

