import json
from pathlib import Path
from typing import Dict, List, Set

from rag.intents.intent import Intent
from rag.query.query_writer import QueryWriter


class HeuristicQueryWriter(QueryWriter):

    def __init__(self, stopwords_path: str):
        self.stopwords: Set[str] = set()
        self.boosters: Dict[Intent, List[str]] = {}
        self._load_config(stopwords_path)

    def _load_config(self, stopwords_path: str) -> None:
        path = Path(stopwords_path)
        raw = path.read_text(encoding='utf-8')
        
        try:
            root = json.loads(raw)
        except json.JSONDecodeError:
            root = self._parse_simple_yaml(raw)

        self.stopwords = set(
            str(w).lower() for w in root.get("stopwords", [])
        )

        booster_node = root.get("boosters")
        if isinstance(booster_node, dict):
            for key, value in booster_node.items():
                intent = self._parse_intent(key)
                self.boosters[intent] = [
                    str(v).lower() for v in value
                ] if isinstance(value, list) else []

    def _parse_simple_yaml(self, raw: str) -> dict:
        result = {}
        for line in raw.splitlines():
            trimmed = line.strip()
            if not trimmed or trimmed.startswith("#"):
                continue
            idx = trimmed.find(":")
            if idx < 0:
                continue
            key = trimmed[:idx].strip()
            value_part = trimmed[idx + 1:].strip()
            try:
                value = json.loads(value_part)
            except json.JSONDecodeError:
                value = value_part
            result[key] = value
        return result

    def write(self, question: str, intent: Intent) -> List[str]:
        if question is None:
            question = ""
        effective_intent = intent if intent is not None else Intent.Unknown

        # Remove non-alphanumeric characters except spaces
        normalized = "".join(c if c.isalnum() or c.isspace() else " " for c in question.lower())
        # Collapse multiple spaces
        normalized = " ".join(normalized.split())
        normalized = normalized.strip()
        if not normalized:
            return []

        tokens = normalized.split()
        short_question = len(tokens) <= 2
        terms = []

        for token in tokens:
            if not token.strip():
                continue
            if not short_question and token in self.stopwords:
                continue
            if token not in terms:
                terms.append(token)

        if not terms and short_question:
            for token in tokens:
                if token.strip() and token not in terms:
                    terms.append(token)

        # Add boosters
        for booster in self.boosters.get(effective_intent, []):
            if booster not in terms:
                terms.append(booster)
        for booster in self.boosters.get(Intent.Unknown, []):
            if booster not in terms:
                terms.append(booster)

        # Add intent name
        intent_name = effective_intent.name.lower()
        if intent_name not in terms:
            terms.append(intent_name)

        return terms

    def _parse_intent(self, name: str) -> Intent:
        """Parse intent enum from string."""
        try:
            return Intent[name]
        except KeyError:
            return Intent.Unknown

