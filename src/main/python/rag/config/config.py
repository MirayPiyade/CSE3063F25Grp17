from typing import List, Optional
from dataclasses import dataclass, replace


@dataclass(frozen=True)
class Config:
    question: Optional[str]
    log_dir: str
    intents_path: str
    stopwords_path: str
    docs_path: str
    reranker_type: str
    reranker_path: str
    retriever_type: str
    top_k: int
    source_priority: List[str]
    answer_agent_type: str

    def with_question(self, new_question: str) -> 'Config':
        return replace(self, question=new_question)

    def with_reranker_type(self, new_type: str) -> 'Config':
        return replace(self, reranker_type=new_type)

    @staticmethod
    def default_config() -> 'Config':
        return Config(
            question=None,
            log_dir="logs",
            intents_path="config/intents.yaml",
            stopwords_path="config/stopwords.yaml",
            docs_path="data/docs.json",
            reranker_type="simple",
            reranker_path="config/reranker.yaml",
            retriever_type="keyword",
            top_k=5,
            source_priority=["CompE", "FoE", "MU"],
            answer_agent_type="template"
        )






