# src/rag_chain.py
import os
import chromadb
from chromadb.config import Settings
from sentence_transformers import SentenceTransformer

PERSIST_DIR = os.path.join("chroma_db")

# Aynı embedding modeli
embedder = SentenceTransformer("all-MiniLM-L6-v2")

# Chroma'ya bağlan
client = chromadb.Client(Settings(chroma_db_impl="duckdb+parquet", persist_directory=PERSIST_DIR))
collection = client.get_or_create_collection("kgk_chatbot")

def retrieve_answer(user_question, k=3):
    """Kullanıcının sorusuna en yakın yanıtı döndürür."""
    query_emb = embedder.encode(user_question).tolist()
    results = collection.query(query_embeddings=[query_emb], n_results=k, include=["documents", "distances"])
    docs = results["documents"][0]
    distances = results["distances"][0]

    # En yakın cevabı seç
    best_text = docs[0]
    # İstersen güven puanını da göster
    return format_coaching_answer(user_question, best_text)

def format_coaching_answer(user_question, doc_text):
    """Bulunan cevabı koçluk diline uygun sade bir biçimde döndürür."""
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
