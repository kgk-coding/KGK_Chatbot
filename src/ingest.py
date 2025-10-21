# src/ingest.py
import os
import chromadb
from sentence_transformers import SentenceTransformer

PERSIST_DIR = os.path.join("chroma_db")
DATA_PATH = os.path.join("data", "soru_cevap.md")

# embedding modeli
embedder = SentenceTransformer("all-MiniLM-L6-v2")

def create_chroma_db():
    """
    Eğer koleksiyon boş ise data dosyasını okuyup Chroma'ya ekler.
    Her kayıt için 'Soru: ...\\nCevap: ...' formatını document olarak ekliyoruz,
    embedding de aynı metinden üretilir — sorgu ile uyumlu olması için.
    """
    os.makedirs(PERSIST_DIR, exist_ok=True)
    client = chromadb.PersistentClient(path=PERSIST_DIR)
    collection = client.get_or_create_collection("kgk_chatbot")

    # Eğer zaten kayıt varsa yeniden ekleme
    try:
        count = collection.count()
    except Exception:
        count = 0

    if count and count > 0:
        # zaten dolu ise sessizce çık
        return

    # Dosyayı oku
    with open(DATA_PATH, "r", encoding="utf-8") as f:
        content = f.read()

    entries = content.split("**Soru:**")[1:]
    documents = []
    questions = []

    for entry in entries:
        if "**Cevap:**" in entry:
            q_part, a_part = entry.split("**Cevap:**", 1)
            question = q_part.strip().replace("\n", " ")
            answer = a_part.strip()
            doc_text = f"Soru: {question}\nCevap: {answer}"
            documents.append(doc_text)
            questions.append(doc_text)  # embedding için aynı metin kullanıyoruz

    if not documents:
        print("⚠️ data/soru_cevap.md içinde hiç geçerli kayıt bulunamadı.")
        return

    embeddings = embedder.encode(questions).tolist()

    # ids - basit, deterministic id'ler
    ids = [f"q_{i}" for i in range(len(documents))]

    collection.add(
        ids=ids,
        documents=documents,
        embeddings=embeddings
    )

    client.persist()
    print(f"✅ ChromaDB'ye {len(documents)} kayıt eklendi.")

def debug_print_collection_info():
    """
    Debug için collection sayısı ve birkaç sample döner (log ve UI için kullan).
    """
    client = chromadb.PersistentClient(path=PERSIST_DIR)
    collection = client.get_or_create_collection("kgk_chatbot")
    try:
        count = collection.count()
    except Exception:
        count = 0

    # birkaç örnek al (güvenli)
    sample_docs = []
    if count > 0:
        res = collection.get(n=5, include=["documents", "metadatas", "ids"])
        sample_docs = res.get("documents", [])

    return {"count": count, "sample_documents": sample_docs}
