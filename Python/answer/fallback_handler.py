"""Fallback handler for when answer generation fails."""
from typing import List

from rag.answer.answer import Answer
from rag.app.context import Context
from rag.intents.intent import Intent


class FallbackHandler:
    """Handles fallback answers when generation fails."""

    def build_fallback(self, context: Context) -> Answer:
        """Build fallback answer based on context."""
        reason = self._determine_reason(context)
        context.fallback_reason = reason

        messages = {
            "EmptyQuestion": "I couldn't produce an answer because the question was empty.",
            "UnknownIntent": "I am unsure which topic you are asking about. Please rephrase the question.",
        }
        message = messages.get(reason, "I could not produce an answer for this query.")

        return Answer(text=message, citations=[f"fallback:{reason}"])

    def _determine_reason(self, context: Context) -> str:
        """Determine fallback reason."""
        if not context.question or not context.question.strip():
            return "EmptyQuestion"
        if context.intent is None or context.intent == Intent.Unknown:
            return "UnknownIntent"
        return "Unknown"

