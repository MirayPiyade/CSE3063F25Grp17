import json
from dataclasses import dataclass
from pathlib import Path
from typing import List

from rag.intents.intent import Intent
from rag.intents.intent_detector import IntentDetector


@dataclass
class Rule:
    intent: Intent
    priority: int
    keywords: List[str]


class RuleIntentDetector(IntentDetector):

    def __init__(self, yaml_path: str):
        self.rules: List[Rule] = []
        self._load_rules(yaml_path)

    def _load_rules(self, yaml_path: str) -> None:
        path = Path(yaml_path)
        raw = path.read_text(encoding='utf-8')
        
        try:
            root = json.loads(raw)
        except json.JSONDecodeError:
            root = self._parse_simple_yaml(raw)

        for key, value in root.items():
            intent = self._parse_intent(key)
            spec = value if isinstance(value, dict) else {}
            priority = spec.get("priority", float('inf'))
            if not isinstance(priority, (int, float)):
                priority = float('inf')
            keywords_node = spec.get("keywords", [])
            keywords = [str(k).lower() for k in keywords_node]
            self.rules.append(Rule(intent, int(priority) if priority != float('inf') else priority, keywords))

        self.rules.sort(key=lambda r: r.priority)

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

    def detect(self, question: str) -> Intent:
        if not question or not question.strip():
            return Intent.Unknown

        text = question.lower()
        best = Intent.Unknown
        best_score = 0
        best_priority = float('inf')

        for rule in self.rules:
            matches = sum(1 for keyword in rule.keywords if keyword in text)
            if matches == 0:
                continue
            if matches > best_score or (matches == best_score and rule.priority < best_priority):
                best_score = matches
                best_priority = rule.priority
                best = rule.intent

        return best

    def _parse_intent(self, value: str) -> Intent:
        try:
            return Intent[value]
        except KeyError:
            return Intent.Unknown

