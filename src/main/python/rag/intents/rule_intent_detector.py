from typing import List, Dict, Any, Optional
from dataclasses import dataclass
from pathlib import Path
from rag.intents.intent import Intent
from rag.intents.intent_detector import IntentDetector
from rag.utils.json_utils import JsonUtils


@dataclass
class Rule:
    intent: Intent
    priority: int
    keywords: List[str]


class RuleIntentDetector(IntentDetector):
    def __init__(self, yaml_path: str) -> None:
        self.rules: List[Rule] = []
        raw: str = Path(yaml_path).read_text(encoding='utf-8')
        root: Dict[str, Any] = JsonUtils.expect_object(
            JsonUtils.parse(raw),
            "intents.yaml must contain a JSON object"
        )
        for key, value in root.items():
            key_str: str = str(key)
            intent: Intent = self._parse_intent(key_str)
            spec: Dict[str, Any] = JsonUtils.expect_object(
                value,
                f"Intent definition for {key_str} must be an object"
            )
            priority: int = int(spec.get("priority", float('inf')))
            keywords_node: List[Any] = JsonUtils.expect_array(
                spec.get("keywords"),
                f"Intent {key_str} is missing keywords"
            )
            keywords: List[str] = [str(kw).lower() for kw in keywords_node]
            self.rules.append(Rule(intent, priority, keywords))
        self.rules.sort(key=lambda r: r.priority)

    def detect(self, q: Optional[str]) -> Intent:
        if q is None or not q.strip():
            return Intent.Unknown
        text: str = q.lower()
        best: Intent = Intent.Unknown
        best_score: int = 0
        best_priority: int = float('inf')

        for rule in self.rules:
            matches: int = 0
            for keyword in rule.keywords:
                if keyword in text:
                    matches += 1
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






