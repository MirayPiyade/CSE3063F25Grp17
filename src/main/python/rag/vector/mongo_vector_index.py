import os
from typing import List
from dotenv import load_dotenv
from pymongo import MongoClient
from rag.vector.vector_index import VectorIndex
from rag.retrieval.hit import Hit

class MongoVectorIndex(VectorIndex):
    def __init__(self, collection_name: str = "oosdRAG_db.chunks", index_name: str = "vector_index") -> None:
        load_dotenv()
        self.client = MongoClient(os.getenv("MONGODB_URI"))
        # Parse db and collection from string "db.collection"
        if "." in collection_name:
            db_name, coll_name = collection_name.split(".", 1)
            self.collection = self.client[db_name][coll_name]
        else:
            # Fallback default
            self.collection = self.client["oosdRAG_db"][collection_name]
            
        self.index_name = index_name

    def search(self, query_vector: List[float], top_k: int) -> List[Hit]:
        pipeline = [
            {
                "$vectorSearch": {
                    "index": self.index_name,
                    "path": "embedding",
                    "queryVector": query_vector,
                    "numCandidates": 100,
                    "limit": top_k
                }
            },
            {
                "$project": {
                    "_id": 0,
                    "source": 1,
                    "chunk_id": 1,
                    "text": 1,
                    "embedding": 1,
                    "score": {"$meta": "vectorSearchScore"}
                }
            }
        ]

        results = list(self.collection.aggregate(pipeline))
        
        hits: List[Hit] = []
        for r in results:
            doc_id = f"{r.get('source', 'unknown')}_{r.get('chunk_id', '0')}"
            hits.append(Hit(
                doc_id=doc_id,
                source=r.get("source", "unknown"),
                title="", 
                text=r.get("text", ""),
                score=r.get("score", 0.0),
                embedding=r.get("embedding")
            ))
            
        return hits
