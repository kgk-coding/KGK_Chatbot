# src/ingest.py
import os
import re
import chromadb
from sentence_transformers import SentenceTransformer

# Klasör yollarını ayarla
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC_DIR = os.path.dirname(os.path.abspath(__file__))
PERSIST_DIR = os.path.join(BASE_DIR, "chroma_db")
DATA_PATH = os.path.join(SRC_DIR, "soru_cevap.md")  # src klasöründe

embedder = SentenceTransformer("all-MiniLM-L6-v2")

def create_chroma_db():
    """Markdown dosyasını okuyup ChromaDB oluşturur."""
    os.makedirs(PERSIST_DIR, exist_ok=True)
    client = chromadb.PersistentClient(path=PERSIST_DIR)
    collection = client.get_or_create_collection("kgk_chatbot")

    # === DEBUG BLOĞU ===
    print("DEBUG >>> Çalışma dizini:", os.getcwd())
    print("DEBUG >>> BASE_DIR:", BASE_DIR)
    print("DEBUG >>> SRC_DIR:", SRC_DIR)
    print("DEBUG >>> Aranan dosya yolu:", DATA_PATH)
    print("DEBUG >>> Dosya mevcut mu?", os.path.exists(DATA_PATH))
    if os.path.exists(DATA_PATH):
        print("DEBUG >>> Dosya boyutu:", os.path.getsize(DATA_PATH))
    else:
        print("DEBUG >>> SRC dizininde mevcut dosyalar:", os.listdir(SRC_DIR))
    # ====================

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

    # UTF-8-SIG ile aç (BOM karakterini yok sayar)
    with open(DATA_PATH, "r", encoding="utf-8-sig") as f:
        content = f.read()

    # Regex ile soru-cevap bloklarını yakala
    pattern = r"\*\*Soru:\*\*\s*(.*?)\s*\*\*Cevap:\*\*\s*(.*?)(?=\n\s*\*\*Soru:\*\*|$)"
    matches = re.findall(pattern, content, re.DOTALL)

    if not matches:
        print("⚠️ Dosyada soru-cevap yapısı bulunamadı.")
        return

    documents = []
    for question, answer in matches:
        question = question.strip().replace("\n", " ")
        answer = answer.strip()
        documents.append(f"Soru: {question}\nCevap: {answer}")

    # Örnek olarak koleksiyona ekleme
    # (Kendi embed ve Chroma ekleme mantığını burada uygula)
    print(f"✅ {len(documents)} doküman ChromaDB'ye hazır.")

def debug_print_collection_info():
    """ChromaDB koleksiyon bilgilerini döndürür (debug amaçlı)."""
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
