import json
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from sentence_transformers import SentenceTransformer
import os

# JSON dosyasının yolu
json_path = os.path.join("data", "soru_cevap.json")

# JSON dosyasını oku
with open(json_path, "r", encoding="utf-8") as f:
    faq_data = json.load(f)

# SentenceTransformer modeli
model = SentenceTransformer('all-MiniLM-L6-v2')

# FAQ sorularının embeddinglerini önceden oluştur
faq_questions = [item["soru"] for item in faq_data]
faq_embeddings = model.encode(faq_questions, convert_to_numpy=True)

# Cevaplama fonksiyonu
def retrieve_answer(user_question: str, threshold: float = 0.6) -> str:
    """
    Kullanıcının sorusunu alır ve en yakın FAQ cevabını döndürür.
    Eğer yakınlık eşik değerini geçmezse standart uyarı mesajı verir.
    """
    if not user_question.strip():
        return "Cevap: Lütfen bir soru girin."

    user_embedding = model.encode([user_question], convert_to_numpy=True)
    similarities = cosine_similarity(user_embedding, faq_embeddings)[0]
    max_idx = np.argmax(similarities)

    if similarities[max_idx] < threshold:
        return "Cevap: Sorunuzu tam olarak cevaplayamıyorum. Lütfen daha detaylı sorar mısınız?"
    else:
        return f"Cevap: {faq_data[max_idx]['cevap']}"
