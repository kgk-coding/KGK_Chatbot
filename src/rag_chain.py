import json
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity

# JSON dosyasını yükle
with open("data/embeddings.json", "r", encoding="utf-8") as f:
    data = json.load(f)

# Dokümanlardan embedding ve metinleri ayır
documents = [item["document"] for item in data]
embeddings = np.array([item["embedding"] for item in data])

def retrieve_answer(query_embedding, top_k=1):
    """
    Soru embedding'ini alır, cosine similarity ile en benzer dokümanı bulur.
    """
    if embeddings.size == 0:
        return "Henüz veritabanında embed edilmiş bir doküman yok."

    # Cosine similarity hesapla
    similarities = cosine_similarity([query_embedding], embeddings)[0]
    top_indices = similarities.argsort()[-top_k:][::-1]

    # En benzer dokümanı döndür
    response = documents[top_indices[0]]
    return response

def embed_query(query, embed_func):
    """
    Soru cümlesini embedding'e çevirir.
    embed_func: embedding hesaplama fonksiyonu (örn: OpenAI veya SentenceTransformer)
    """
    return embed_func(query)
