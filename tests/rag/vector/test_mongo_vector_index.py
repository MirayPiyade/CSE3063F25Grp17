import pytest
import os
from unittest.mock import MagicMock, patch
from rag.vector.mongo_vector_index import MongoVectorIndex
from rag.retrieval.hit import Hit

def test_mongo_search():
    with patch('rag.vector.mongo_vector_index.MongoClient') as MockClient:
        mock_db = MagicMock()
        mock_coll = MagicMock()
        MockClient.return_value.__getitem__.return_value = mock_db
        mock_db.__getitem__.return_value = mock_coll
        
        # Mock aggregation pipeline result
        mock_coll.aggregate.return_value = [
            {
                "doc_id": "1",
                "source": "S",
                "title": "T",
                "text": "content",
                "score": 0.95,
                "embedding": [0.1]
            }
        ]
        
        # Constructor signature is (collection_name="...", index_name="...")
        # URI is loaded from env.
        with patch.dict(os.environ, {"MONGODB_URI": "mongodb://mock"}):
            index = MongoVectorIndex("db.col", "idx")
        hits = index.search([0.1], top_k=5)
        
        assert len(hits) == 1
        assert hits[0].doc_id == "S_0"
        assert hits[0].score == 0.95
        
        # Verify pipeline structure
        mock_coll.aggregate.assert_called_once()
        pipeline = mock_coll.aggregate.call_args[0][0]
        assert pipeline[0]['$vectorSearch']['limit'] == 5
        assert pipeline[0]['$vectorSearch']['queryVector'] == [0.1]

def test_mongo_search_empty():
    with patch('rag.vector.mongo_vector_index.MongoClient') as MockClient:
        MockClient.return_value.__getitem__.return_value.__getitem__.return_value.aggregate.return_value = []
        with patch.dict(os.environ, {"MONGODB_URI": "mongodb://mock"}):
            index = MongoVectorIndex("db.col", "idx")
        hits = index.search([0.1], 1)
        assert len(hits) == 0
