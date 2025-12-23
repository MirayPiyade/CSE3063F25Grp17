from typing import List
import re


class TextNormalizer:
    def normalize(self, text: str) -> str:
        normalized: str = (
            text.replace("İ", "i")
            .replace("I", "ı")
            .lower()
        )
        normalized = re.sub(r'[^a-z0-9ğüşöçıİ ]', ' ', normalized)
        normalized = re.sub(r'\s+', ' ', normalized)
        return normalized.strip()

    def tokenize(self, text: str) -> List[str]:
        return self.normalize(text).split()

