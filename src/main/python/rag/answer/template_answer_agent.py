from typing import List, Optional
import re
from rag.answer.answer_agent import AnswerAgent
from rag.answer.answer import Answer
from rag.retrieval.hit import Hit


class TemplateAnswerAgent(AnswerAgent):
    def generate_answer(self, hits: Optional[List[Hit]], query: Optional[str]) -> Optional[Answer]:
        if not hits:
            return None

        effective_query: str = query if query else ""
        best_hit: Hit = hits[0]
        raw_text: str = best_hit.text if best_hit.text else ""

        best_sentence: str = self._select_best_sentence(effective_query, raw_text)

        start: int = raw_text.find(best_sentence)
        if start < 0:
            start = 0
        end: int = min(len(raw_text), start + len(best_sentence))

        citation: str = self._build_citation(best_hit, start, end)

        final_sentence: str = best_sentence
        if not final_sentence.endswith('.'):
            final_sentence = final_sentence + "."

        text: str = f"Your answer: {final_sentence} See: {citation}"

        return Answer(text, [citation])

    def _select_best_sentence(self, query: str, text: Optional[str]) -> str:
        if not text or not text.strip():
            return "Relevant information is available but cannot be displayed."

        abbreviations: List[str] = ['Mr', 'Mrs', 'Ms', 'Dr', 'Prof', 'Rev', 'Capt', 'Gen', 'Col', 'Lt', 'Maj', 'St', 'Inc', 'Ltd', 'Corp', 'Co', 'No', 'Fig', 'vb', 'Av']
        temp_text: str = text
        for abbr in abbreviations:
            temp_text = temp_text.replace(f'{abbr}.', f'{abbr}__ABBR__')
        
        regex: str = r'(?<=[.!?])\s+(?=[A-ZÇĞİÖŞÜ])'
        sentences: List[str] = re.split(regex, temp_text)
        
        sentences = [s.replace('__ABBR__', '.') for s in sentences]
        
        if not sentences:
            return text.strip()

        terms: List[str] = query.lower().split()
        options: List[str] = list(sentences)

        return max(options, key=lambda s: self._match_count(s, terms), default=sentences[0]).strip()

    def _match_count(self, sentence: str, terms: List[str]) -> int:
        normalized: str = sentence.lower()
        score: int = 0
        for term in terms:
            if term.strip() and term in normalized:
                score += 1
        return score

    def _build_citation(self, hit: Hit, start: int, end: int) -> str:
        doc_id: str = hit.doc_id
        section_id: str = hit.source
        if not section_id or not section_id.strip():
            section_id = "1"
        return f"{doc_id}:{section_id}:{start}-{end}"

