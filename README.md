# RAG Project (CSE3063F25Grp17)

This project implements a Retrieval-Augmented Generation (RAG) system for university course information (Computer Engineering, Marmara University).
## 🚀 Setup

### 1. Initialize Virtual Environment
It is recommended to use a virtual environment.

```bash
# Create venv (if not exists)
python3 -m venv .venv

# Activate venv (macOS/Linux)
source .venv/bin/activate

# Activate venv (Windows)
.venv\Scripts\activate
```

### 2. Install Dependencies
Install the required Python packages.

```bash
pip install -r requirements.txt
# If you encounter issues with 'rich', explicitly install it:
pip install rich
```

### 3. Environment Variables
Ensure you have a `.env` file in the root directory if you plan to use OpenAI or other API-based services.
```
OPENAI_API_KEY=sk-...
```

---

## 🏃 Usage

You can run the application using either the `rag.py` script or the module directly.

```bash
# Run with default settings (Interactive Mode)
python rag.py
# OR
python -m rag
```

### CLI Arguments & Commands

You can override almost any configuration from the terminal.

| Argument | Description | Example |
| :--- | :--- | :--- |
| `--q` | Provide a query directly (skips interactive prompt) | `--q "What is CompE?"` |
| `--mode` | fast-switch between predefined modes | `--mode keyword-simple` |
| `--config` | Use a specific configuration file | `--config config/custom.yaml` |
| `--batch` | path to a JSON file for batch processing | `--batch data/eval_questions.json` |
| `--no-cache` | **Disable caching** for this run | `--no-cache` |

#### Overriding Components (Dynamic Configuration)
You can change specific components of the pipeline without editing the config file:

*   **`--retriever`**: `vector`, `keyword`
*   **`--reranker`**: `simple`, `cosine`, `hybrid`, `none`
*   **`--embedding`**: `openai`, `stub`
*   **`--agent`**: `llm`, `template`

**Examples:**

1.  **Run with Vector Search + LLM (Default):**
    ```bash
    python rag.py
    ```

2.  **Force Keyword Search + Stub Embedding:**
    ```bash
    python rag.py --retriever keyword --embedding stub
    ```

3.  **Run a specific question without cache:**
    ```bash
    python rag.py --q "Yaz okulu ücretleri?" --no-cache
    ```

---

## ⚙️ Configuration

The main configuration is located at `config/config.yaml`.

### Common Config Options

```yaml
# Paths
docsPath: data/docs.json           # Source documents
stopwordsPath: config/stopwords.yaml
intentsPath: config/intents.yaml

# Pipeline Components
retrieverType: vector              # Options: vector, keyword
rerankerType: simple               # Options: simple, cosine, hybrid, none
embeddingProviderType: openai      # Options: openai, stub
vectorIndexType: mongo             # Options: mongo, stub
answerAgentType: llm               # Options: llm, template

# Reranker Specific
rerankerPath: config/reranker.yaml # Path for simple/hybrid reranker weights

# Search Settings
topK: 5                            # Number of documents to retrieve
sourcePriority: [CompE, FoE, MU]   # Priority boost for sources
```

### Predefined Configurations
*   `config/config.yaml`: **Vector + LLM** (Default)
*   `config/keyword_simple_config.yaml`: **Keyword + Simple Rerank**
*   `config/vector_stub_config.yaml`: **Stub/Offline Test Mode**

---

## 📂 Project Structure

*   `src/main/python/rag/`: Python main source code
*   `config/`: Configuration files (YAML)
*   `data/`: Data files (docs, chunks, raw texts)
*   `logs/`: Application logs

---

## 🧪 Testing

Bu projede unit testler `pytest` kullanılarak yazılmıştır. Testler `tests/` klasörü altında, kaynak kod yapısını (mirror) takip edecek şekilde organize edilmiştir.

### Testleri Çalıştırma

Tüm testleri çalıştırmak için proje kök dizininde şu komutu çalıştırın:

```bash
# Önerilen yöntem (Import hatalarını önler)
python3 -m pytest

# Alternatif yöntem (Eğer path ayarlarınız doğruysa)
pytest
```

**Not:** `python3 -m pytest` komutu, çalışma dizinini `sys.path`'e eklediği için import sorunlarını (ModuleNotFoundError) önlemede daha güvenlidir.

Belirli bir modülün testlerini çalıştırmak için:

```bash
# Sadece vector modülü testleri
pytest tests/rag/vector

# Sadece config modülü testleri
pytest tests/rag/config
```

### Test Kapsamı

Proje aşağıdaki modüller için kapsamlı unit testlere sahiptir:
- **rag/app**: Pipeline, Orchestrator, Context, Stages
- **rag/answer**: Answer Agents, Validators
- **rag/config**: Config loading ve parsing
- **rag/cache**: Cache mekanizması
- **rag/intents**: Rule-based intent detection
- **rag/query**: Query rewriting
- **rag/rerank**: Tüm reranker stratejileri (Simple, Cosine, Hybrid)
- **rag/retrieval**: Keyword ve Vector retrieval
- **rag/vector**: Embedding providerlar ve Vector indexler
- **rag/utils**: Yardımcı araçlar

---

## 📊 Değerlendirme (Evaluation)

RAG sisteminin başarımını ölçmek için `evaluate.py` scripti kullanılır. Bu script, belirlenen soru-cevap setleri üzerinden doğruluk (hit rate) ve cevap kalitesi (answer match rate) ölçümlerini yapar.

### Kullanım

```bash
# Tüm modları karşılaştırmalı olarak değerlendirmek için:
python evaluate.py --mode all

# Belirli bir modu test etmek için (örn: vector-llm):
python evaluate.py --mode vector-llm

# Farklı bir test veri seti kullanmak için:
python evaluate.py --mode all --input data/my_eval_questions.json
```

### Metrikler
- **Hit Rate**: Doğru dokümanın getirilip getirilmediği.
- **Answer Match Rate**: Üretilen cevabın beklenen cevaba ne kadar benzediği (fuzzy match/LLM eval).
- **Latency**: Ortalama cevap süresi.
