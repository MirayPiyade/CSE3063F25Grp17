# CSE3063F25Grp17 – Iteration 1 (Java)

Minimal, deterministic, keyword-based RAG pipeline in Java for Iteration 1. No embeddings, no vector index, no chunk builder; loads a simple JSON corpus and performs substring retrieval with config-driven strategies.

## Architecture highlights
- **GRASP Controller**: `RagOrchestrator` drives the sequential pipeline.
- **Template Method**: `DefaultPipeline` runs ordered stages (intent → query → retrieve → rerank → answer → finalize).
- **Strategy**: IntentDetector, QueryWriter, Retriever, Reranker, AnswerAgent are swappable via config/CLI (`--reranker`).
- **Observer**: `TraceBus` publishes to `JsonlTraceSink` (logs/run-*.jsonl) and console.
- **SOLID**: SRP per stage, DIP/OCP via interfaces + `StrategyRegistry`, low coupling/high cohesion in stage responsibilities.
- **RAG shape (minimal)**: Deterministic question → intent → keyword query → substring retrieval → heuristic rerank → templated answer with citation; all local files, no external APIs.

## Setup and build
```bash
rm -rf out
mkdir -p out/classes out/test
javac -d out/classes $(find src/main/java -name "*.java")
echo "Main-Class: rag.app.RagCli" > out/manifest.mf
jar cfm rag.jar out/manifest.mf -C out/classes .
# optional: compile tests
javac -d out/test -cp rag.jar $(find src/test/java -name '*.java')
```

## Run CLI
- Default (simple reranker from config):  
  `java -jar rag.jar --config config/config.yaml --q "CSE3063 dersinin akts değeri nedir?"`
- Override reranker from terminal (no code change):  
  - Simple: `java -jar rag.jar --config config/config.yaml --reranker simple --q "policy nedir?"`  
  - NoOp: `java -jar rag.jar --config config/config.yaml --reranker noop --q "policy nedir?"`
- If `--q` is omitted, CLI prompts; if `question` exists in config, it is used.

## Config files
- `config/config.yaml` (or JSON): logDir, paths, `rerankerType` (`simple`/`noop`), `retrieverType` (`keyword`), `topK`, `sourcePriority`.  
- `config/intents.yaml`: intent keywords + priority (RuleIntentDetector).  
- `config/stopwords.yaml`: stopwords + boosters (Unknown boosters disabled to avoid random hits).  
- `config/reranker.yaml`: scoring weights for SimpleReranker.

## Tests (enable assertions with -ea)
```bash
java -ea -cp rag.jar:out/test rag.intents.RuleIntentDetectorTest
java -ea -cp rag.jar:out/test rag.retrieval.KeywordRetrieverTest
java -ea -cp rag.jar:out/test rag.rerank.SimpleRerankerTest
```

## Pipeline data flow
1) Load config → Context(question)  
2) Intent detection (RuleIntentDetector)  
3) Query writing (HeuristicQueryWriter)  
4) Retrieval (KeywordRetriever over data/docs.json)  
5) Rerank (Simple or NoOp via config/CLI)  
6) Answer (TemplateAnswerAgent selects best-matching sentence, builds citation)  
7) Finalize (FallbackHandler if needed)  
8) Trace events recorded to logs/.

