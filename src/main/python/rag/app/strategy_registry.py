from typing import List, Optional
from rag.config.config import Config
from rag.intents.intent_detector import IntentDetector
from rag.intents.rule_intent_detector import RuleIntentDetector
from rag.query.query_writer import QueryWriter
from rag.query.heuristic_query_writer import HeuristicQueryWriter
from rag.rerank.reranker import Reranker
from rag.rerank.simple_reranker import SimpleReranker
from rag.rerank.cosine_reranker import CosineReranker
from rag.rerank.hybrid_reranker import HybridReranker
from rag.rerank.noop_reranker import NoOpReranker
from rag.vector.embedding_provider import EmbeddingProvider
from rag.vector.stub_embedding_provider import StubEmbeddingProvider
from rag.vector.openai_embedding_provider import OpenAIEmbeddingProvider
from rag.vector.vector_index import VectorIndex
from rag.vector.stub_vector_index import StubVectorIndex
from rag.vector.mongo_vector_index import MongoVectorIndex
from rag.retrieval.retriever import Retriever
from rag.retrieval.keyword_retriever import KeywordRetriever
from rag.retrieval.document import Document
from rag.retrieval.document_store import DocumentStore
from rag.answer.answer_agent import AnswerAgent
from rag.answer.template_answer_agent import TemplateAnswerAgent
from rag.answer.fallback_handler import FallbackHandler
from rag.answer._register_ import _register_
from rag.retrieval.vector_retriever import VectorRetriever
from rag.answer.llm_answer_agent import LLMAnswerAgent


class StrategyRegistry:
    def __init__(self, config: Config) -> None:
        self.config: Config = config
        self._documents: Optional[List[Document]] = None
        self._intent_detector: Optional[IntentDetector] = None
        self._query_writer: Optional[QueryWriter] = None
        self._retriever: Optional[Retriever] = None
        self._reranker: Optional[Reranker] = None
        self._answer_agent: Optional[AnswerAgent] = None
        self._embedding_provider: Optional[EmbeddingProvider] = None
        self._vector_index: Optional[VectorIndex] = None
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
        elif retriever_type == "vector":
            self._retriever = VectorRetriever(
                top_k=self.config.top_k,
                embedding_provider=self.get_embedding_provider(),
                vector_index=self.get_vector_index()
            )
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
        elif reranker_type == "cosine":
            self._reranker = CosineReranker(self.get_embedding_provider())
        elif reranker_type == "hybrid":
            self._reranker = HybridReranker(self.config.reranker_path, self.get_embedding_provider())
        else:
            raise ValueError(f"Unsupported reranker type: {self.config.reranker_type}")
        return self._reranker

    def get_answer_agent(self) -> AnswerAgent:
        if self._answer_agent is None:
            agent_type = self.config.answer_agent_type.lower()
            
            if agent_type == "llm":
                self._answer_agent = LLMAnswerAgent()
            else:
                agent: Optional[AnswerAgent] = _register_.get("template")
                if agent is None:
                    self._answer_agent = TemplateAnswerAgent()
                else:
                    self._answer_agent = agent
        return self._answer_agent

    def get_embedding_provider(self) -> EmbeddingProvider:
        if self._embedding_provider is not None:
            return self._embedding_provider
        
        provider_type = (self.config.embedding_provider_type.lower() 
                         if hasattr(self.config, "embedding_provider_type") else "openai")
        
        if provider_type == "stub":
            self._embedding_provider = StubEmbeddingProvider()
        elif provider_type == "openai":
            self._embedding_provider = OpenAIEmbeddingProvider()
        else:
             # Fallback or error
             raise ValueError(f"Unsupported embedding provider: {provider_type}")
        return self._embedding_provider

    def get_vector_index(self) -> VectorIndex:
        if self._vector_index is not None:
            return self._vector_index
        
        index_type = (self.config.vector_index_type.lower()
                      if hasattr(self.config, "vector_index_type") else "mongo")

        if index_type == "stub":
            self._vector_index = StubVectorIndex(self.get_documents(), self.get_embedding_provider())
        elif index_type == "mongo":
            self._vector_index = MongoVectorIndex()
        else:
            raise ValueError(f"Unsupported vector index: {index_type}")
        return self._vector_index

    def get_fallback_handler(self) -> FallbackHandler:
        if self._fallback_handler is None:
            self._fallback_handler = FallbackHandler()
        return self._fallback_handler






