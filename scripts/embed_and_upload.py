import json
import os
from dotenv import load_dotenv
from openai import OpenAI
from pymongo import MongoClient

load_dotenv()

# OpenAI
openai_client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# MongoDB
mongo = MongoClient(os.getenv("MONGODB_URI"))
db = mongo["oosdRAG_db"]
collection = db["chunks"]

# (opsiyonel) temiz başlangıç
# collection.delete_many({})

with open("data/chunks/chunks.jsonl", "r", encoding="utf-8") as f:
    for line in f:
        doc = json.loads(line)

        embedding = openai_client.embeddings.create(
            model="text-embedding-3-small",
            input=doc["text"]
        ).data[0].embedding

        doc["embedding"] = embedding
        collection.insert_one(doc)

print("✅ Embedding oluşturuldu ve MongoDB'ye yüklendi")

