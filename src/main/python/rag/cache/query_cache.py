import json
from pathlib import Path
from typing import Optional, Dict, Any
from rag.config.config import Config
from rag.answer.answer import Answer

class QueryCache:
    def __init__(self, cache_file: str = ".cache/query_cache.json") -> None:
        self.cache_file = Path(cache_file)
        self._cache: Dict[str, Any] = {}
        self._load()

    def _load(self) -> None:
        if self.cache_file.exists():
            try:
                self._cache = json.loads(self.cache_file.read_text(encoding='utf-8'))
            except Exception:
                self._cache = {}
        else:
            self._cache = {}

    def _save(self) -> None:
        self.cache_file.parent.mkdir(parents=True, exist_ok=True)
        self.cache_file.write_text(json.dumps(self._cache, indent=2, ensure_ascii=False), encoding='utf-8')

    def _generate_key(self, query: str, config: Config) -> str:
        # Signature: retriever|reranker|answer_agent|embedding_provider
        # We need to access these from config.
        retriever = getattr(config, "retriever_type", "keyword")
        reranker = getattr(config, "reranker_type", "simple")
        answer_agent = getattr(config, "answer_agent_type", "template")
        # vector_index and embedding_provider are also critical for "stub" vs "real" distinction
        embedding = getattr(config, "embedding_provider_type", "openai")
        vector_index = getattr(config, "vector_index_type", "mongo")
        
        signature = f"{retriever}|{reranker}|{answer_agent}|{embedding}|{vector_index}"
        normalized_query = query.strip().lower()
        return f"{normalized_query}::{signature}"

    def get(self, query: str, config: Config) -> Optional[Answer]:
        key = self._generate_key(query, config)
        data = self._cache.get(key)
        if data:
            return Answer(
                text=data.get("text", ""),
                citations=data.get("citations", [])
            )
        return None

    def put(self, query: str, config: Config, answer: Answer) -> None:
        key = self._generate_key(query, config)
        self._cache[key] = {
            "text": answer.text,
            "citations": answer.citations
        }
        self._save()
