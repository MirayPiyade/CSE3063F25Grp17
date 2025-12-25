import pytest
import os
from unittest.mock import MagicMock, patch
from rag.vector.openai_embedding_provider import OpenAIEmbeddingProvider

def test_openai_embedding_call():
    # Constructor takes no args, reads env
    with patch('rag.vector.openai_embedding_provider.OpenAI') as MockOpenAI:
        mock_client = MagicMock()
        MockOpenAI.return_value = mock_client
        
        # Mock response structure
        mock_response = MagicMock()
        mock_response.data = [MagicMock(embedding=[0.1, 0.2, 0.3])]
        mock_client.embeddings.create.return_value = mock_response
        
        with patch.dict(os.environ, {"OPENAI_API_KEY": "fake_key"}):
            provider = OpenAIEmbeddingProvider() # No args
            
        embedding = provider.embed_query("test query")
        
        assert embedding == [0.1, 0.2, 0.3]
        mock_client.embeddings.create.assert_called_once()
        args, kwargs = mock_client.embeddings.create.call_args
        assert kwargs['input'] == "test query"
        assert kwargs['model'] == "text-embedding-3-small"

def test_openai_embedding_error():
    with patch('rag.vector.openai_embedding_provider.OpenAI') as MockOpenAI:
        mock_client = MagicMock()
        MockOpenAI.return_value = mock_client
        mock_client.embeddings.create.side_effect = Exception("API Error")
        
        with patch.dict(os.environ, {"OPENAI_API_KEY": "fake"}):
            provider = OpenAIEmbeddingProvider()
            
        # Should it raise or return empty? Implementation usually raises or returns None.
        # Let's assume it propagates exception
        with pytest.raises(Exception):
            provider.embed_query("fail")
