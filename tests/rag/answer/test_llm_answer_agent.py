import pytest
from unittest.mock import MagicMock, patch
from rag.answer.llm_answer_agent import LLMAnswerAgent
from rag.retrieval.hit import Hit

@pytest.fixture
def mock_openai():
    with patch("rag.answer.llm_answer_agent.OpenAI") as mock:
        yield mock

@pytest.fixture
def agent_with_mock(mock_openai):
    # Initialize agent (which triggers OpenAI init)
    return LLMAnswerAgent()

def test_init_loads_dotenv(mock_openai):
    # Just creating the agent should init OpenAI
    _ = LLMAnswerAgent()
    mock_openai.assert_called_once()

def test_generate_answer_no_hits(agent_with_mock):
    assert agent_with_mock.generate_answer([], "query") is None

def test_generate_answer_success(agent_with_mock):
    # Setup mock response
    mock_client = agent_with_mock.openai_client
    mock_response = MagicMock()
    mock_response.choices[0].message.content = "LLM Generated Answer"
    mock_client.chat.completions.create.return_value = mock_response

    hits = [
        Hit(doc_id="d1", source="s1", text="Content 1", score=1.0, title="T", embedding=None),
        Hit(doc_id="d2", source="s2", text="Content 2", score=0.9, title="T", embedding=None)
    ]
    
    ans = agent_with_mock.generate_answer(hits, "query")
    
    assert ans is not None
    assert ans.text == "LLM Generated Answer"
    # Citations should be unique sources
    assert set(ans.citations) == {"s1", "s2"}
    
    # Verify call arguments
    args, kwargs = mock_client.chat.completions.create.call_args
    assert kwargs["model"] == "gpt-4o-mini"
    messages = kwargs["messages"]
    assert len(messages) == 2
    assert "Content 1" in messages[1]["content"] # User prompt contains context

def test_generate_answer_api_error(agent_with_mock):
    mock_client = agent_with_mock.openai_client
    mock_client.chat.completions.create.side_effect = Exception("API Error")
    
    hits = [Hit(doc_id="d1", source="s1", text="C", score=1.0, title="T", embedding=None)]
    
    ans = agent_with_mock.generate_answer(hits, "query")
    
    # Should catch exception and return None
    assert ans is None
