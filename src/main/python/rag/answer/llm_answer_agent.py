from typing import List, Optional
import os
from dotenv import load_dotenv
from openai import OpenAI
from rag.answer.answer_agent import AnswerAgent
from rag.answer.answer import Answer
from rag.retrieval.hit import Hit

class LLMAnswerAgent(AnswerAgent):
    def __init__(self) -> None:
        load_dotenv()
        self.openai_client = OpenAI(
            api_key=os.getenv("OPENAI_API_KEY")
        )

    def generate_answer(self, hits: List[Hit], query: str) -> Optional[Answer]:
        if not hits:
            return None
        
        # Build context from hits
        context_str = "\n\n".join([f"Source: {h.source}\nText: {h.text}" for h in hits])
        
        system_prompt = (
            "You are a helpful assistant. Answer the question using ONLY the provided context. "
            "If the information is not present in the context, state that you don't know. "
            "Keep the answer concise and strictly relevant to the question."
        )
        user_prompt = f"Context:\n{context_str}\n\nQuestion: {query}"

        try:
            response = self.openai_client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                temperature=0.0
            )
            
            answer_text = response.choices[0].message.content
            
            # Collect unique sources for citations
            citations = list(set([h.source for h in hits]))
            
            return Answer(answer_text, citations)
            
        except Exception as e:
            print(f"Error calling LLM: {e}")
            return None
