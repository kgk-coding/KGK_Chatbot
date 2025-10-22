# src/ingest.py
import os
import re
import chromadb
from sentence_transformers import SentenceTransformer

# 🔹 Dosya yolları mutlak hale getirildi
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PERSIST_DIR = os.path.join(BASE_DIR, "chroma_db")
DATA_PATH = os.path.join(BASE_DIR, "data", "soru_cevap.md")

embedder = SentenceTransformer("all-MiniLM-L6-v2")

def create_chroma_db():
    """
    data/soru_cevap.md içindeki soru-cevap çiftlerini algılayıp Chroma'ya ekler.
    Regex kullanıldığı için satır boşluklarından veya format farklarından etkilenmez.
    """
    os.makedirs(PERSIST_DIR, exist_ok=True)
    client = chromadb.PersistentClient(path=PERSIST_DIR)
    collection = client.get_or_create_collection("kgk_chatbot")

    try:
        count = collection.count()
    except Exception:
        count = 0

    if count and count > 0:
        print(f"ℹ️ ChromaDB zaten dolu ({count} kayıt var).")
        return

    if not os.path.exists(DATA_PATH):
        print(f"⚠️ Veri dosyası bulunamadı: {DATA_PATH}")
        return

    with open(DATA_PATH, "r", encoding="utf-8") as f:
        content = f.read()

    pattern = r"\*\*Soru:\*\*\s*(.*?)\s*\*\*Cevap:\*\*\s*(.*?)(?=\n\s*\*\*Soru:\*\*|$)"
    matches = re.findall(pattern, content, re.DOTALL)

    if not matches:
        print("⚠️ Dosyada soru-cevap yapısı bulunamadı.")
        return

    documents, embeddings, ids = [], [], []

    for i, (question, answer) in enumerate(matches):
        question = question.strip().replace("\n", " ")
        answer = answer.strip()
        doc_text = f"Soru: {question}\nCevap: {answer}"
        documents.append(doc_text)
        embeddings.append(embedder.encode(doc_text).tolist())
        ids.append(f"q_{i}")

    collection.add(ids=ids, documents=documents, embeddings=embeddings)
    client.persist()
    print(f"✅ {len(documents)} kayıt başarıyla ChromaDB'ye eklendi.")

def debug_print_collection_info():
    """
    Debug için ChromaDB'deki kayıt sayısı ve örnek kayıtları döndürür.
    """
    client = chromadb.PersistentClient(path=PERSIST_DIR)
    collection = client.get_or_create_collection("kgk_chatbot")
    try:
        count = collection.count()
    except Exception:
        count = 0

    sample_docs = []
    if count > 0:
        res = collection.get(limit=3, include=["documents"])
        sample_docs = res.get("documents", [])

    info = {"count": count, "sample_documents": sample_docs}
    print(f"DEBUG >>> {info}")
    return info
