from typing import List, Optional
from rag.retrieval.retriever import Retriever
from rag.retrieval.document import Document
from rag.retrieval.hit import Hit


class KeywordRetriever(Retriever):
    def __init__(self, top_k: int, priority_order: List[str]) -> None:
        self.top_k: int = top_k
        self.priority_order: List[str] = list(priority_order)

    def retrieve(self, question: Optional[str], terms: Optional[List[str]], documents: List[Document]) -> List[Hit]:
        if not documents:
            return []
        normalized_question: str = (question.lower().strip() if question else "")
        normalized_terms: List[str] = []
        if terms:
            normalized_terms = [t.lower() for t in terms if t and t.strip()]

        hits: List[Hit] = []

        for doc in documents:
            text: str = doc.text if doc.text else ""
            lower_text: str = text.lower()
            score: float = 0.0

            if normalized_question and normalized_question in lower_text:
                score += 2.0

            for term in normalized_terms:
                if term in lower_text:
                    score += 1.0

            if score > 0:
                hits.append(Hit(doc.id, doc.source, doc.title, text, score))

        hits.sort(key=lambda h: (
            -h.score,
            self._priority_index(h.source),
            h.doc_id
        ))

        if len(hits) > self.top_k:
            return hits[:self.top_k]
        return hits

    def _priority_index(self, source: str) -> int:
        try:
            idx: int = self.priority_order.index(source)
            return idx
        except ValueError:
            return len(self.priority_order)






