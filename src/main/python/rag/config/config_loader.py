from typing import Dict, Any, List, Optional
from pathlib import Path
from rag.config.config import Config
from rag.utils.json_utils import JsonUtils


class ConfigLoader:
    @staticmethod
    def load(path: Optional[str]) -> Config:
        defaults: Config = Config.default_config()
        
        # If no path provided, try default locations
        if path is None or not path.strip():
            if Path("config/config.yaml").exists():
                path = "config/config.yaml"
            elif Path("config.yaml").exists():
                path = "config.yaml"
            else:
                return defaults

        p = Path(path)
        if not p.exists():
            # If plain filename provided, check in config/ directory
            # strict check: properly check if it's not already pointing to config dir
            if not str(p).startswith("config/") and \
               not str(p).startswith("config\\") and \
               (Path("config") / p).exists():
                p = Path("config") / p

        try:
            raw: str = p.read_text(encoding='utf-8')
            root: Dict[str, Any] = ConfigLoader._parse_config(raw, str(p))

            question: Optional[str] = JsonUtils.expect_string(
                root.get("question", defaults.question),
                "question must be a string"
            )
            log_dir: str = JsonUtils.expect_string(
                root.get("logDir", defaults.log_dir),
                "logDir must be a string"
            )
            intents_path: str = JsonUtils.expect_string(
                root.get("intentsPath", defaults.intents_path),
                "intentsPath must be a string"
            )
            stopwords_path: str = JsonUtils.expect_string(
                root.get("stopwordsPath", defaults.stopwords_path),
                "stopwordsPath must be a string"
            )
            docs_path: str = JsonUtils.expect_string(
                root.get("docsPath", defaults.docs_path),
                "docsPath must be a string"
            )

            reranker_type: str = JsonUtils.expect_string(
                root.get("rerankerType", defaults.reranker_type),
                "rerankerType must be a string"
            )
            reranker_path: str = JsonUtils.expect_string(
                root.get("rerankerPath", defaults.reranker_path),
                "rerankerPath must be a string"
            )

            retriever_type: str = JsonUtils.expect_string(
                root.get("retrieverType", defaults.retriever_type),
                "retrieverType must be a string"
            )
            top_k: int = int(JsonUtils.expect_number(
                root.get("topK", defaults.top_k),
                "topK must be numeric"
            ))

            source_priority: List[str] = list(defaults.source_priority)
            src_node: Any = root.get("sourcePriority")
            if src_node is not None:
                arr: List[Any] = JsonUtils.expect_array(
                    src_node,
                    "sourcePriority must be an array"
                )
                source_priority.clear()
                for o in arr:
                    source_priority.append(str(o))

            answer_agent_type: str = JsonUtils.expect_string(
                root.get("answerAgentType", defaults.answer_agent_type),
                "answerAgentType must be a string"
            )

            embedding_provider_type: str = JsonUtils.expect_string(
                root.get("embeddingProviderType", defaults.embedding_provider_type),
                "embeddingProviderType must be a string"
            )

            vector_index_type: str = JsonUtils.expect_string(
                root.get("vectorIndexType", defaults.vector_index_type),
                "vectorIndexType must be a string"
            )

            cache_enabled: bool = bool(root.get("cacheEnabled", defaults.cache_enabled))

            return Config(
                question=question,
                log_dir=log_dir,
                intents_path=intents_path,
                stopwords_path=stopwords_path,
                docs_path=docs_path,
                reranker_type=reranker_type,
                reranker_path=reranker_path,
                retriever_type=retriever_type,
                top_k=top_k,
                source_priority=source_priority,
                answer_agent_type=answer_agent_type,
                embedding_provider_type=embedding_provider_type,
                vector_index_type=vector_index_type,
                cache_enabled=cache_enabled
            )
        except Exception as e:
            raise RuntimeError(f"Failed to load config from {path}: {str(e)}") from e

    @staticmethod
    def _parse_config(raw: str, path: str) -> Dict[str, Any]:
        try:
            return JsonUtils.expect_object(
                JsonUtils.parse(raw),
                "config file must be an object"
            )
        except Exception as json_ex:
            lower: str = path.lower()
            if lower.endswith((".yaml", ".yml")):
                return ConfigLoader._parse_simple_yaml(raw)
            raise json_ex

    @staticmethod
    def _parse_simple_yaml(raw: str) -> Dict[str, Any]:
        map_obj: Dict[str, Any] = {}
        lines: List[str] = raw.splitlines()
        for line in lines:
            trimmed: str = line.strip()
            if not trimmed or trimmed.startswith('#'):
                continue
            idx: int = trimmed.find(':')
            if idx < 0:
                continue
            key: str = trimmed[:idx].strip()
            value_part: str = trimmed[idx + 1:].strip()
            value: Any = ConfigLoader._parse_value(value_part)
            map_obj[key] = value
        return map_obj

    @staticmethod
    def _parse_value(raw: str) -> Any:
        if not raw:
            return ""
        if raw.startswith('[') and raw.endswith(']'):
            inner: str = raw[1:-1].strip()
            if not inner:
                return []
            parts: List[str] = inner.split(',')
            values: List[Any] = []
            for part in parts:
                values.append(ConfigLoader._parse_value(part.strip()))
            return values
        if (raw.startswith('"') and raw.endswith('"')) or (raw.startswith("'") and raw.endswith("'")):
            return raw[1:-1]
        try:
            if '.' in raw:
                return float(raw)
            return int(raw)
        except ValueError:
            pass
        return raw






