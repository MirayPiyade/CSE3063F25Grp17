from typing import Protocol, List
from rag.retrieval.hit import Hit
from rag.retrieval.document import Document


class Retriever(Protocol):
    def retrieve(self, question: str, terms: List[str], documents: List[Document]) -> List[Hit]:
        ...






