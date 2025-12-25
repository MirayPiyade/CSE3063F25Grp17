import os
from typing import List
from dotenv import load_dotenv
from openai import OpenAI
from rag.vector.embedding_provider import EmbeddingProvider

class OpenAIEmbeddingProvider(EmbeddingProvider):
    def __init__(self) -> None:
        load_dotenv()
        self.client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

    def embed_query(self, text: str) -> List[float]:
        return self.client.embeddings.create(
            model="text-embedding-3-small",
            input=text
        ).data[0].embedding
