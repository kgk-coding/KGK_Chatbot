# src/rag_chain.py
import os
import chromadb
from sentence_transformers import SentenceTransformer

PERSIST_DIR = os.path.join("chroma_db")
embedder = SentenceTransformer("all-MiniLM-L6-v2")

# Chroma bağlan
client = chromadb.PersistentClient(path=PERSIST_DIR)
collection = client.get_or_create_collection("kgk_chatbot")

def retrieve_answer(user_question, k=3):
    """
    Kullanıcı sorgusunu embed edip Chroma'da arama yapar.
    Eğer sonuç yoksa uygun mesaj verir; varsa en yakın sonucu alır.
    """
    if not user_question or user_question.strip() == "":
        return "Lütfen bir soru yazın."

    q_emb = embedder.encode(user_question).tolist()

    # collection.query döndürülen yapıya dikkat et
    results = collection.query(
        query_embeddings=[q_emb],
        n_results=k,
        include=["documents", "distances"]
    )

    docs = []
    distances = []
    try:
        docs = results.get("documents", [[]])[0]
        distances = results.get("distances", [[]])[0]
    except Exception:
        docs = []

    if not docs:
        # fallback: yakın eşleşme yok
        return (
            f"**Soru:** {user_question}\n\n"
            "Üzgünüm, bu konuda elimde bir bilgi yok. "
            "Lütfen farklı bir soru deneyin veya web sitemi inceleyin."
        )

    # en yakın dokümanı al
    best_doc = docs[0]
    # docs içinde 'Soru: ...\\nCevap: ...' formatında kayıt var — Cevap kısmını ayıklayalım
    if "Cevap:" in best_doc:
        answer = best_doc.split("Cevap:", 1)[1].strip()
    else:
        answer = best_doc.strip()

    response = (
        f"**Soru:** {user_question}\n\n"
        f"**Cevap:** {answer}\n\n"
        "Eğer daha kapsamlı bir destek istersen, koçluk görüşmeleri hakkında bilgi almak için web sitemi ziyaret edebilirsin."
    )
    return response
