import os
import json
from pathlib import Path

INPUT_DIRS = [
    "data/processed/md",
    "data/processed/txt"
]

OUTPUT_FILE = "data/chunks/chunks.jsonl"
MAX_CHARS = 1200  # iteration-2 için ideal

def chunk_text(text):
    chunks = []
    buffer = ""

    for line in text.split("\n"):
        if len(buffer) + len(line) > MAX_CHARS:
            chunks.append(buffer.strip())
            buffer = ""
        buffer += line + "\n"

    if buffer.strip():
        chunks.append(buffer.strip())

    return chunks

Path("data/chunks").mkdir(parents=True, exist_ok=True)

with open(OUTPUT_FILE, "w", encoding="utf-8") as out:
    for folder in INPUT_DIRS:
        for file in Path(folder).glob("*"):
            text = file.read_text(encoding="utf-8")
            for i, chunk in enumerate(chunk_text(text)):
                record = {
                    "source": file.name,
                    "chunk_id": i,
                    "text": chunk
                }
                out.write(json.dumps(record, ensure_ascii=False) + "\n")

print("✅ Chunk üretimi tamamlandı")
