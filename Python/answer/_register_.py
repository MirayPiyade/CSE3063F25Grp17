from typing import Dict

from rag.answer.answer_agent import AnswerAgent
from rag.answer.template_answer_agent import TemplateAnswerAgent


class _register_:

    _agents: Dict[str, AnswerAgent] = {
        "template": TemplateAnswerAgent(),
    }

    @staticmethod
    def get(name: str) -> AnswerAgent:
        return _register_._agents.get(name)


