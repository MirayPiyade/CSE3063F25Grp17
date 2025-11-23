import re
from typing import List


class TextNormalizer:

    def normalize(self, text: str) -> str:
        import re
        normalized = (
            text.replace("İ", "i")
            .replace("I", "ı")
            .lower()
        )
        # Remove non-alphanumeric characters except Turkish chars and spaces
        normalized = re.sub(r"[^a-z0-9ğüşöçı ]", " ", normalized)
        # Collapse whitespace
        normalized = re.sub(r"\s+", " ", normalized)
        return normalized.strip()

    def tokenize(self, text: str) -> List[str]:
        return self.normalize(text).split()
