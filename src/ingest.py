# src/ingest.py
import os
import re
import chromadb
from sentence_transformers import SentenceTransformer

# -----------------------------
# Klasör ve dosya yolları
# -----------------------------
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC_DIR = os.path.dirname(os.path.abspath(__file__))
PERSIST_DIR = os.path.join(BASE_DIR, "chroma_db")
DATA_PATH = os.path.join(SRC_DIR, "soru_cevap.md")  # src klasöründe

# Embed modeli
embedder = SentenceTransformer("all-MiniLM-L6-v2")

# -----------------------------
# ChromaDB oluşturma ve veri ekleme
# -----------------------------
def create_chroma_db():
    """Markdown dosyasını okuyup ChromaDB oluşturur ve embed ekler."""
    os.makedirs(PERSIST_DIR, exist_ok=True)
    client = chromadb.PersistentClient(path=PERSIST_DIR)
    collection = client.get_or_create_collection("kgk_chatbot")

    # Dosya mevcut değilse uyar
    if not os.path.exists(DATA_PATH):
        print(f"⚠️ Veri dosyası bulunamadı: {DATA_PATH}")
        return

    with open(DATA_PATH, "r", encoding="utf-8-sig") as f:
        content = f.read()

    # Regex ile soru-cevap bloklarını yakala
    pattern = r"\*\*Soru:\*\*\s*(.*?)\s*\*\*Cevap:\*\*\s*(.*?)(?=\n\s*\*\*Soru:\*\*|$)"
    matches = re.findall(pattern, content, re.DOTALL)

    if not matches:
        print("⚠️ Dosyada soru-cevap yapısı bulunamadı.")
        return

    documents = []
    for i, (question, answer) in enumerate(matches):
        question = question.strip().replace("\n", " ")
        answer = answer.strip()
        doc_text = f"Soru: {question}\nCevap: {answer}"
        documents.append(doc_text)

        # Embed oluştur ve ChromaDB'ye ekle
        try:
            embedding = embedder.encode(doc_text).tolist()
            collection.add(
                documents=[doc_text],
                embeddings=[embedding],
                ids=[f"doc_{i}"]
            )
            print(f"✅ {i+1}. doküman eklendi")
        except Exception as e:
            print(f"❌ Doküman eklenemedi: {e}")

    print(f"ℹ️ Toplam {len(documents)} doküman ChromaDB'ye işlendi.")

# -----------------------------
# Debug / koleksiyon bilgisi
# -----------------------------
def debug_print_collection_info():
    """ChromaDB koleksiyon bilgilerini döndürür."""
    client = chromadb.PersistentClient(path=PERSIST_DIR)
    collection = client.get_or_create_collection("kgk_chatbot")
    try:
        count = collection.count()
    except Exception:
        count = 0

    return {
        "collection_name": "kgk_chatbot",
        "document_count": count
    }
