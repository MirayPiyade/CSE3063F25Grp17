from typing import List, Dict, Any, Set, Optional
from pathlib import Path
from rag.query.query_writer import QueryWriter
from rag.intents.intent import Intent
from rag.utils.json_utils import JsonUtils


class HeuristicQueryWriter(QueryWriter):
    def __init__(self, stopwords_path: str) -> None:
        raw: str = Path(stopwords_path).read_text(encoding='utf-8')
        root: Dict[str, Any] = JsonUtils.expect_object(
            JsonUtils.parse(raw),
            "stopwords.yaml must contain a JSON object"
        )
        self.stopwords: Set[str] = set(self._read_list(root.get("stopwords")))

        booster_map: Dict[Intent, List[str]] = {}
        booster_node: Any = root.get("boosters")
        if isinstance(booster_node, dict):
            for key, value in booster_node.items():
                key_str: str = str(key)
                intent: Intent = self._parse_intent(key_str)
                booster_map[intent] = self._read_list(value)
        self.boosters: Dict[Intent, List[str]] = booster_map

    def write(self, question: Optional[str], intent: Optional[Intent]) -> List[str]:
        if question is None:
            question = ""
        effective_intent: Intent = intent if intent is not None else Intent.Unknown

        import re
        normalized: str = re.sub(r'[^\w\s]', ' ', question.lower()).strip()
        if not normalized:
            return []

        tokens: List[str] = normalized.split()
        short_question: bool = len(tokens) <= 2
        terms: List[str] = []
        seen: Set[str] = set()

        for token in tokens:
            if not token.strip():
                continue
            if not short_question and token in self.stopwords:
                continue
            if token not in seen:
                terms.append(token)
                seen.add(token)

        if not terms and short_question:
            for token in tokens:
                if token.strip() and token not in seen:
                    terms.append(token)
                    seen.add(token)

        for booster in self.boosters.get(effective_intent, []):
            if booster not in seen:
                terms.append(booster)
                seen.add(booster)
        for booster in self.boosters.get(Intent.Unknown, []):
            if booster not in seen:
                terms.append(booster)
                seen.add(booster)

        terms.append(effective_intent.name.lower())
        return terms

    def _read_list(self, node: Any) -> List[str]:
        if isinstance(node, list):
            return [str(value).lower() for value in node]
        return []

    def _parse_intent(self, name: str) -> Intent:
        try:
            return Intent[name]
        except KeyError:
            return Intent.Unknown

