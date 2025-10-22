# -*- coding: utf-8 -*-
# src/rag_chain.py

import json
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from sentence_transformers import SentenceTransformer

# Modeli yükle
model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")

# Embed edilmiş verileri yükle
with open("src/embeddings.json", "r", encoding="utf-8") as f:
    data = json.load(f)

if not data:
    print("⚠️ Uyarı: embeddings.json dosyası boş!")
else:
    print(f"✅ {len(data)} doküman yüklendi.")

# Embedding’leri ve metinleri hazırla
texts = [item["document"] for item in data]
embeddings = np.array([item["embedding"] for item in data])


def retrieve_answer(question, dialog_memory=None):
    """
    Kullanıcının sorusuna en uygun cevabı döndürür.
    dialog_memory: önceki soru-cevap çiftlerini tutar (isteğe bağlı)
    """

    # Eğer hafızada benzer bir soru varsa önce oraya bakalım
    if dialog_memory:
        for entry in reversed(dialog_memory[-3:]):  # son 3 etkileşimi kontrol et
            if entry["question"].lower() == question.lower():
                return f"Bunu az önce sormuştunuz: {entry['answer']}"

    # Eğer veritabanı boşsa uyarı ver
    if embeddings.size == 0:
        return "Henüz veritabanında embed edilmiş bir doküman yok."

    # Soruyu embed et
    question_embedding = model.encode([question])

    # Benzerlikleri hesapla
    similarities = cosine_similarity(question_embedding, embeddings)[0]

    # En benzer dokümanı bul
    top_idx = np.argmax(similarities)
    top_score = similarities[top_idx]
    best_match = texts[top_idx]

    # Eşik belirle (çok alakasızsa)
    if top_score < 0.45:
        return "Bu konuyla ilgili doğrudan bir bilgi bulamadım. Ne hakkında konuştuğunu biraz daha açar mısın?"

    # Dokümandan cevabı çıkar
    if "Cevap:" in best_match:
        answer = best_match.split("Cevap:")[1].strip()
    else:
        answer = best_match

    return answer
