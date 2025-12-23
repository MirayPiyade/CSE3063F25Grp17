from typing import List, Dict, Any, Optional
from pathlib import Path
from rag.rerank.reranker import Reranker
from rag.retrieval.hit import Hit
from rag.utils.json_utils import JsonUtils


class SimpleReranker(Reranker):
    def __init__(self, config_path: str) -> None:
        try:
            raw: str = Path(config_path).read_text(encoding='utf-8')
            root: Dict[str, Any] = JsonUtils.expect_object(
                JsonUtils.parse(raw),
                "reranker.yaml must contain a JSON object"
            )
            self.proximity_bonus: float = float(root.get("proximityBonus", 0.0))
            self.proximity_window: int = int(root.get("proximityWindow", 15))
            self.title_boost: float = float(root.get("titleBoost", 0.0))
            boosts: Dict[str, float] = {}
            boosts_node: Any = root.get("sourceBoosts")
            if isinstance(boosts_node, dict):
                for key, value in boosts_node.items():
                    key_str: str = str(key)
                    boosts[key_str] = float(value)
            self.source_boosts: Dict[str, float] = boosts
        except Exception as e:
            raise RuntimeError(f"Failed to read reranker config: {str(e)}") from e

    def rerank(self, terms: Optional[List[str]], hits: List[Hit], cfg: Any) -> List[Hit]:
        if not hits:
            return []
        normalized_terms: List[str] = []
        if terms:
            normalized_terms = list(dict.fromkeys([t.lower() for t in terms if t and t.strip()]))

        reranked: List[Hit] = []
        for hit in hits:
            score: float = hit.score
            score += self._compute_source_boost(hit)
            score += self._compute_title_boost(hit.title, normalized_terms)
            score += self._compute_proximity_bonus(hit.text, normalized_terms)
            reranked.append(hit.with_score(score))

        reranked.sort(key=lambda h: (-h.score, h.doc_id))
        return reranked

    def _compute_source_boost(self, hit: Hit) -> float:
        return self.source_boosts.get(hit.source, 0.0)

    def _compute_title_boost(self, title: Optional[str], terms: List[str]) -> float:
        if not title or not title.strip() or not terms:
            return 0.0
        lower: str = title.lower()
        for term in terms:
            if term in lower:
                return self.title_boost
        return 0.0

    def _compute_proximity_bonus(self, text: Optional[str], terms: List[str]) -> float:
        if not text or not text.strip() or len(terms) < 2 or self.proximity_bonus == 0.0:
            return 0.0
        lower: str = text.lower()
        for i in range(len(terms)):
            for j in range(i + 1, len(terms)):
                pos_a: int = lower.find(terms[i])
                pos_b: int = lower.find(terms[j])
                if pos_a >= 0 and pos_b >= 0 and abs(pos_a - pos_b) <= self.proximity_window:
                    return self.proximity_bonus
        return 0.0






