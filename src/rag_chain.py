import json
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from sentence_transformers import SentenceTransformer
import os

# JSON dosya yolu (repo içinde data klasörü altında)
json_path = os.path.join("data", "soru_cevap.json")

# JSON'u yükle
with open(json_path, "r", encoding="utf-8") as f:
    faq_data = json.load(f)

# Embedding modeli
model = SentenceTransformer('all-MiniLM-L6-v2')

# FAQ sorularının embeddingleri
faq_questions = [item['soru'] for item in faq_data]
faq_embeddings = model.encode(faq_questions, convert_to_numpy=True)

def retrieve_answer(user_question: str, threshold: float = 0.4) -> str:
    user_question_clean = user_question.strip().lower()

    # 1️⃣ Kelime bazlı birebir veya kısmi eşleşme
    for item in faq_data:
        faq_soru_clean = item['soru'].strip().lower()
        if user_question_clean == faq_soru_clean or user_question_clean in faq_soru_clean or faq_soru_clean in user_question_clean:
            return f"Cevap: {item['cevap']}"

    # 2️⃣ Embedding bazlı benzerlik
    user_embedding = model.encode([user_question], convert_to_numpy=True)
    similarities = cosine_similarity(user_embedding, faq_embeddings)[0]

    max_idx = np.argmax(similarities)
    max_score = similarities[max_idx]

    if max_score >= threshold:
        return f"Cevap: {faq_data[max_idx]['cevap']}"
    else:
        return "Cevap: Sorunuzu tam olarak cevaplayamıyorum. Lütfen daha detaylı sorar mısınız?"
