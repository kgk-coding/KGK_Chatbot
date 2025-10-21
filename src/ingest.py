# src/ingest.py
import os
import chromadb
from chromadb.config import Settings
from sentence_transformers import SentenceTransformer
import uuid

DATA_FILE = os.path.join("data", "soru_cevap.md")
PERSIST_DIR = os.path.join("chroma_db")

def parse_qna(md_path):
    """Soru-Cevap çiftlerini .md dosyasından ayıklar"""
    items = []
    with open(md_path, "r", encoding="utf-8") as f:
        text = f.read()
    parts = text.split("**Soru:**")
    for p in parts:
        p = p.strip()
        if not p:
            continue
        if "**Cevap:**" in p:
            q, a = p.split("**Cevap:**", 1)
            q = q.strip().replace("\n", " ")
            a = a.strip()
            items.append({"question": q, "answer": a})
    return items

def create_chroma_db():
    os.makedirs(PERSIST_DIR, exist_ok=True)
    client = chromadb.Client(Settings(chroma_db_impl="duckdb+parquet", persist_directory=PERSIST_DIR))
    collection = client.get_or_create_collection("kgk_chatbot")

    model = SentenceTransformer("all-MiniLM-L6-v2")

    data = parse_qna(DATA_FILE)
    ids, texts, metas, embeddings = [], [], [], []

    for i, item in enumerate(data):
        text = f"Soru: {item['question']}\nCevap: {item['answer']}"
        emb = model.encode(text).tolist()
        ids.append(str(uuid.uuid4()))
        texts.append(text)
        metas.append({"soru": item["question"]})
        embeddings.append(emb)

    collection.upsert(ids=ids, documents=texts, metadatas=metas, embeddings=embeddings)
    client.persist()
    print(f"Chroma DB oluşturuldu. Toplam {len(ids)} kayıt eklendi.")

if __name__ == "__main__":
    create_chroma_db()
