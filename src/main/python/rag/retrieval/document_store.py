from typing import List, Dict, Any
from pathlib import Path
from rag.retrieval.document import Document
from rag.utils.json_utils import JsonUtils


class DocumentStore:
    def __init__(self, documents: List[Document]) -> None:
        self.documents: List[Document] = documents

    @staticmethod
    def load(path: str) -> 'DocumentStore':
        raw: str = Path(path).read_text(encoding='utf-8')
        nodes: List[Any] = JsonUtils.expect_array(
            JsonUtils.parse(raw),
            "docs.json must be an array"
        )
        docs: List[Document] = []
        for node in nodes:
            obj: Dict[str, Any] = JsonUtils.expect_object(
                node,
                "Document entry must be an object"
            )
            doc_id: str = str(obj.get("id", ""))
            source: str = str(obj.get("source", "Unknown"))
            title: str = str(obj.get("title", doc_id))
            text: str = str(obj.get("text", ""))
            docs.append(Document(doc_id, source, title, text))
        return DocumentStore(docs)

    def get_documents(self) -> List[Document]:
        return self.documents






