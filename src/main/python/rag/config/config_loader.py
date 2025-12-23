from typing import Dict, Any, List, Optional
from pathlib import Path
from rag.config.config import Config
from rag.utils.json_utils import JsonUtils


class ConfigLoader:
    @staticmethod
    def load(path: Optional[str]) -> Config:
        defaults: Config = Config.default_config()
        if path is None or not path.strip():
            return defaults
        try:
            raw: str = Path(path).read_text(encoding='utf-8')
            root: Dict[str, Any] = ConfigLoader._parse_config(raw, path)

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
                source_priority=source_priority
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






