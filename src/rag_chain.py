import os
import json
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from sentence_transformers import SentenceTransformer

# JSON dosya yolu: repo kökü / data / embeddings.json
base_dir = os.path.dirname(os.path.dirname(__file__))  # src üstü = repo kökü
json_path = os.path.join(base_dir, "data", "embeddings.json")

# JSON'u yükle
try:
    with open(json_path, "r", encoding="utf-8") as f:
        data = json.load(f)
except FileNotFoundError:
    raise FileNotFoundError(f"{json_path} bulunamadı. Lütfen data klasörüne embeddings.json koyun.")

# JSON bir liste değilse listeye çevir
if isinstance(data, dict):
    faq_data = [data]
else:
    faq_data = data

# Her item'da "cevap" anahtarı yoksa fallback'leri kontrol et
for item in faq_data:
    if "cevap" not in item:
        for alt in ["answer", "response", "Cevap"]:
            if alt in item:
                item["cevap"] = item[alt]
                break

# Model
model = SentenceTransformer('all-MiniLM-L6-v2')

# Embedding dizilerini yükle
faq_embeddings = [np.array(item["embedding"]) for item in faq_data if "embedding" in item]

def retrieve_answer(user_question, threshold=0.6):
    """
    Kullanıcının sorusuna en yakın cevabı getirir.
    threshold: Benzerlik eşiği
    """
    if not faq_embeddings:
        return "Cevap: Veri yüklenemedi. Lütfen embeddings.json içeriğini kontrol edin."

    user_embedding = model.encode(user_question)
    similarities = [cosine_similarity([user_embedding], [faq_emb])[0][0] for faq_emb in faq_embeddings]

    max_idx = int(np.argmax(similarities))
    max_score = similarities[max_idx]

    if max_score >= threshold:
        return f"Cevap: {faq_data[max_idx].get('cevap', 'Yanıt bulunamadı.')}"
    else:
        return "Cevap: Sorunuzu tam olarak cevaplayamıyorum. Lütfen daha detaylı sorar mısınız?"
