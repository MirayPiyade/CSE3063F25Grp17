import os
from dotenv import load_dotenv
from pymongo import MongoClient
from openai import OpenAI

load_dotenv()


# OpenAI client
openai_client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY")
)

# MongoDB
mongo_client = MongoClient(os.getenv("MONGODB_URI"))
collection = mongo_client.oosdRAG_db.chunks

def semantic_search(question: str, top_k: int = 5):
    # 1. Soru embedding
    embedding = openai_client.embeddings.create(
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
                "limit": top_k
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

    return list(collection.aggregate(pipeline))

if __name__ == "__main__":
    results = semantic_search("Staj süresi kaç gündür?")

    for r in results:
        print("SOURCE:", r["source"])
        print("SCORE:", r["score"])
        print("TEXT:", r["text"][:300])
        print("-" * 40)

if __name__ == "__main__":
    print("Vector search script started ✅")

    query = "inkilap dersi konuları nelerdir?"
    results = semantic_search(query)

    print(f"Toplam sonuç: {len(results)}\n")

    for r in results:
        print("SOURCE:", r["source"])
        print("SCORE:", r["score"])
        print("TEXT:", r["text"][:300])
        print("-" * 40)
