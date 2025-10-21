# src/rag_chain.py
import os
import chromadb
from sentence_transformers import SentenceTransformer

# Kalıcı ChromaDB dizini
PERSIST_DIR = os.path.join("chroma_db")

# Aynı embedding modeli
embedder = SentenceTransformer("all-MiniLM-L6-v2")

# ChromaDB'ye bağlan
client = chromadb.PersistentClient(path=PERSIST_DIR)
collection = client.get_or_create_collection("kgk_chatbot")

def retrieve_answer(user_question, k=3):
    """
    Kullanıcının sorusuna en yakın yanıtı döndürür.
    Boş sonuç durumunda kullanıcıya anlamlı bir mesaj verir.
    """
    # Soru embedding'i oluştur
    query_emb = embedder.encode(user_question).tolist()
    
    # ChromaDB sorgusu
    results = collection.query(
        query_embeddings=[query_emb],
        n_results=k,
        include=["documents", "distances"]
    )

    docs = results["documents"][0]  # Arama sonucu doküman listesi
    distances = results["distances"][0]

    # Eğer sonuç yoksa kullanıcıya bilgilendirici mesaj dön
    if not docs or len(docs) == 0:
        return (
            f"**Soru:** {user_question}\n\n"
            "Üzgünüm, bu konuda elimde bir bilgi yok. "
            "Lütfen farklı bir soru deneyin veya web sitemi inceleyin."
        )

    # En yakın cevabı al
    best_text = docs[0]

    # Koçluk formatında döndür
    return format_coaching_answer(user_question, best_text)

def format_coaching_answer(user_question, doc_text):
    """
    Bulunan cevabı koçluk diline uygun sade bir biçimde döndürür.
    """
    if "Cevap:" in doc_text:
        answer = doc_text.split("Cevap:", 1)[1].strip()
    else:
        answer = doc_text.strip()

    response = (
        f"**Soru:** {user_question}\n\n"
        f"**Cevap:** {answer}\n\n"
        "Eğer bu konuda daha fazla bilgi almak istersen, web sitemi detaylı inceleyebilirsin."
    )
    return response
