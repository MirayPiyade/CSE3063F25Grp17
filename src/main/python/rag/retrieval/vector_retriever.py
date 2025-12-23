from typing import List, Optional, Dict, Any
import os
from dotenv import load_dotenv
from pymongo import MongoClient
from openai import OpenAI
from rag.retrieval.retriever import Retriever
from rag.retrieval.document import Document
from rag.retrieval.hit import Hit

class VectorRetriever(Retriever):
    def __init__(self, top_k: int) -> None:
        self.top_k = top_k
        load_dotenv()
        
        # OpenAI client
        self.openai_client = OpenAI(
            api_key=os.getenv("OPENAI_API_KEY")
        )

        # MongoDB client
        self.mongo_client = MongoClient(os.getenv("MONGODB_URI"))
        self.collection = self.mongo_client.oosdRAG_db.chunks

    def retrieve(self, question: str, terms: List[str], documents: List[Document]) -> List[Hit]:
        # 1. Generate embedding for the question
        embedding = self.openai_client.embeddings.create(
            model="text-embedding-3-small",
            input=question
        ).data[0].embedding

        # 2. MongoDB Vector Search pipeline
        pipeline = [
            {
                "$vectorSearch": {
                    "index": "vector_index",
                    "path": "embedding",
                    "queryVector": embedding,
                    "numCandidates": 100,
                    "limit": self.top_k
                }
            },
            {
                "$project": {
                    "_id": 0,
                    "source": 1,
                    "chunk_id": 1,
                    "text": 1,
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
                title="", # Title is not available in chunks
                text=r.get("text", ""),
                score=r.get("score", 0.0)
            ))
            
        return hits
