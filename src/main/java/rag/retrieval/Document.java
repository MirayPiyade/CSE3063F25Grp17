package rag.retrieval;

public class Document {
    private final String docId;
    private final String title;
    private final String sourcePath;

    public Document(String docId, String title, String sourcePath) {
        this.docId = docId;
        this.title = title;
        this.sourcePath = sourcePath;
    }

    public String getDocId() { return docId; }
    public String getTitle() { return title; }
    public String getSourcePath() { return sourcePath; }
}
