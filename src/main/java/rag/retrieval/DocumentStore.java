package rag.retrieval;

import rag.utils.JsonUtils;

import java.nio.file.Files;
import java.nio.file.Path;
import java.util.ArrayList;
import java.util.List;
import java.util.Map;

public class DocumentStore {

    private final List<Document> documents;

    private DocumentStore(List<Document> documents) {
        this.documents = documents;
    }

    public static DocumentStore load(String path) throws Exception {
        String raw = Files.readString(Path.of(path));
        List<Object> nodes = JsonUtils.expectArray(JsonUtils.parse(raw), "docs.json must be an array");
        List<Document> docs = new ArrayList<>();
        for (Object node : nodes) {
            Map<String, Object> obj = JsonUtils.expectObject(node, "Document entry must be an object");
            String id = obj.get("id").toString();
            String source = obj.getOrDefault("source", "Unknown").toString();
            String title = obj.getOrDefault("title", id).toString();
            String text = obj.getOrDefault("text", "").toString();
            docs.add(new Document(id, source, title, text));
        }
        return new DocumentStore(docs);
    }

    public List<Document> getDocuments() {
        return documents;
    }
}
