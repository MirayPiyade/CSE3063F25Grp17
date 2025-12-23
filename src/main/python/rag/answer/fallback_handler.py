from typing import List, Optional
from rag.answer.answer import Answer
from rag.app.context import Context
from rag.intents.intent import Intent


class FallbackHandler:
    def build_fallback(self, context: Context) -> Answer:
        reason: str = self._determine_reason(context)
        context.set_fallback_reason(reason)
        message: str = self._get_message(reason)
        return Answer(message, [f"fallback:{reason}"])

    def _determine_reason(self, context: Context) -> str:
        if not context.get_question() or not context.get_question().strip():
            return "EmptyQuestion"
        intent: Optional[Intent] = context.get_intent()
        if intent is None or intent == Intent.Unknown:
            return "UnknownIntent"
        return "Unknown"

    def _get_message(self, reason: str) -> str:
        if reason == "EmptyQuestion":
            return "I couldn't produce an answer because the question was empty."
        elif reason == "UnknownIntent":
            return "I am unsure which topic you are asking about. Please rephrase the question."
        else:
            return "I could not produce an answer for this query."

