import re
from typing import List

from rag.answer.answer import Answer
from rag.answer.answer_agent import AnswerAgent
from rag.retrieval.hit import Hit


class TemplateAnswerAgent(AnswerAgent):

    def generate_answer(self, hits: List[Hit], query: str) -> Answer:
        if not hits:
            return None

        effective_query = query or ""
        best_hit = hits[0]
        raw_text = best_hit.text or ""

        best_sentence = self._select_best_sentence(effective_query, raw_text)

        start = raw_text.find(best_sentence)
        if start < 0:
            start = 0
        end = min(len(raw_text), start + len(best_sentence))

        citation = self._build_citation(best_hit, start, end)

        final_sentence = best_sentence
        if not final_sentence.endswith("."):
            final_sentence = final_sentence + "."

        text = f"Your answer: {final_sentence} See: {citation}"

        return Answer(text=text, citations=[citation])

    def _select_best_sentence(self, query: str, text: str) -> str:
        if not text or not text.strip():
            return "Relevant information is available but cannot be displayed."

        # Sentence splitting regex (handles common abbreviations)
        sentence_pattern = (
            r"(?<!\b(Mr|Mrs|Ms|Dr|Prof|Rev|Capt|Gen|Col|Lt|Maj|St|Inc|Ltd|Corp|Co|No|Fig|vb|Av)\.)"
            r"(?<=[.!?])\s+(?=[A-ZÇĞİÖŞÜ])"
        )
        sentences = re.split(sentence_pattern, text)
        sentences = [s.strip() for s in sentences if s.strip()]

        if not sentences:
            return text.strip()

        terms = query.lower().split()
        best_sentence = max(
            sentences,
            key=lambda s: self._match_count(s, terms),
            default=sentences[0]
        )

        return best_sentence.strip()

    def _match_count(self, sentence: str, terms: List[str]) -> int:
        normalized = sentence.lower()
        return sum(1 for term in terms if term and term in normalized)

    def _build_citation(self, hit: Hit, start: int, end: int) -> str:
        doc_id = hit.doc_id
        section_id = hit.source or "1"
        return f"{doc_id}:{section_id}:{start}-{end}"


