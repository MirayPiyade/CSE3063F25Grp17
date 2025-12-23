from typing import List, Optional
from rag.config.config import Config
from rag.intents.intent_detector import IntentDetector
from rag.intents.rule_intent_detector import RuleIntentDetector
from rag.query.query_writer import QueryWriter
from rag.query.heuristic_query_writer import HeuristicQueryWriter
from rag.rerank.reranker import Reranker
from rag.rerank.simple_reranker import SimpleReranker
from rag.rerank.noop_reranker import NoOpReranker
from rag.retrieval.retriever import Retriever
from rag.retrieval.keyword_retriever import KeywordRetriever
from rag.retrieval.document import Document
from rag.retrieval.document_store import DocumentStore
from rag.answer.answer_agent import AnswerAgent
from rag.answer.template_answer_agent import TemplateAnswerAgent
from rag.answer.fallback_handler import FallbackHandler
from rag.answer._register_ import _register_


class StrategyRegistry:
    def __init__(self, config: Config) -> None:
        self.config: Config = config
        self._documents: Optional[List[Document]] = None
        self._intent_detector: Optional[IntentDetector] = None
        self._query_writer: Optional[QueryWriter] = None
        self._retriever: Optional[Retriever] = None
        self._reranker: Optional[Reranker] = None
        self._answer_agent: Optional[AnswerAgent] = None
        self._fallback_handler: Optional[FallbackHandler] = None

    def get_intent_detector(self) -> IntentDetector:
        if self._intent_detector is None:
            try:
                self._intent_detector = RuleIntentDetector(self.config.intents_path)
            except Exception as e:
                raise RuntimeError(f"Failed to load intents.yaml: {str(e)}") from e
        return self._intent_detector

    def get_query_writer(self) -> QueryWriter:
        if self._query_writer is None:
            try:
                self._query_writer = HeuristicQueryWriter(self.config.stopwords_path)
            except Exception as e:
                raise RuntimeError(f"Failed to load stopwords.yaml: {str(e)}") from e
        return self._query_writer

    def get_retriever(self) -> Retriever:
        if self._retriever is not None:
            return self._retriever

        retriever_type: str = (self.config.retriever_type.lower()
                               if self.config.retriever_type else "keyword")
        if retriever_type == "keyword":
            self._retriever = KeywordRetriever(self.config.top_k, self.config.source_priority)
        else:
            raise ValueError(f"Unsupported retriever type: {self.config.retriever_type}")
        return self._retriever

    def get_documents(self) -> List[Document]:
        if self._documents is None:
            try:
                self._documents = DocumentStore.load(self.config.docs_path).get_documents()
            except Exception as e:
                raise RuntimeError(f"Failed to load docs.json: {str(e)}") from e
        return self._documents

    def get_reranker(self) -> Reranker:
        if self._reranker is not None:
            return self._reranker

        reranker_type: str = (self.config.reranker_type.lower()
                             if self.config.reranker_type else "simple")
        if reranker_type == "noop":
            self._reranker = NoOpReranker()
        elif reranker_type == "simple":
            self._reranker = SimpleReranker(self.config.reranker_path)
        else:
            raise ValueError(f"Unsupported reranker type: {self.config.reranker_type}")
        return self._reranker

    def get_answer_agent(self) -> AnswerAgent:
        if self._answer_agent is None:
            agent: Optional[AnswerAgent] = _register_.get("template")
            if agent is None:
                self._answer_agent = TemplateAnswerAgent()
            else:
                self._answer_agent = agent
        return self._answer_agent

    def get_fallback_handler(self) -> FallbackHandler:
        if self._fallback_handler is None:
            self._fallback_handler = FallbackHandler()
        return self._fallback_handler






