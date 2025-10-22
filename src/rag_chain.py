import json
import os
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from sentence_transformers import SentenceTransformer

# data klasöründeki embeddings.json dosyasını kullan
base_dir = os.path.dirname(os.path.dirname(__file__))  # src üstü = repo kökü
json_path = os.path.join(base_dir, "data", "embeddings.json")

# JSON dosyasını yükle
try:
    with open(json_path, "r", encoding="utf-8") as f:
        faq_data = json.load(f)
except FileNotFoundError:
    raise FileNotFoundError(f"{json_path} bulunamadı. Lütfen data klasörüne embeddings.json koyun.")

# SentenceTransformer modelini yükle
model = SentenceTransformer('all-MiniLM-L6-v2')

# Önceden embed edilmiş vektörleri JSON'dan al
faq_embeddings = [np.array(item['embedding']) for item in faq_data]

def retrieve_answer(user_question, threshold=0.6):
    """
    user_question: Kullanıcının sorusu
    threshold: Benzerlik eşiği (0-1)
    """
    user_embedding = model.encode(user_question)
    
    # Benzerlik skorlarını hesapla
    similarities = [cosine_similarity([user_embedding], [faq_emb])[0][0] for faq_emb in faq_embeddings]
    
    # En yüksek benzerlik indeksini bul
    max_idx = int(np.argmax(similarities))
    max_score = similarities[max_idx]
    
    if max_score >= threshold:
        return f"Cevap: {faq_data[max_idx]['cevap']}"
    else:
        return "Cevap: Sorunuzu tam olarak cevaplayamıyorum. Lütfen daha detaylı sorar mısınız?"
