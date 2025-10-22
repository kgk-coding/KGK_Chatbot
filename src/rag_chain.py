import os
import json
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from sentence_transformers import SentenceTransformer

# Model yükleme
model = SentenceTransformer('all-MiniLM-L6-v2')

# JSON dosyasının yolu (repo yapına göre)
BASE_DIR = os.path.dirname(__file__)
json_path = os.path.join(BASE_DIR, "soru_cevap.json")  # dosya adını ve yerini değiştirmedik

with open(json_path, "r", encoding="utf-8") as f:
    faq_data = json.load(f)

faq_questions = [item['soru'] for item in faq_data]
faq_embeddings = model.encode(faq_questions, convert_to_numpy=True)

def retrieve_answer(user_question: str) -> str:
    user_emb = model.encode([user_question], convert_to_numpy=True)
    similarities = cosine_similarity(user_emb, faq_embeddings)[0]

    threshold = 0.68  # Yakınlık eşik değeri
    best_idx = np.argmax(similarities)
    if similarities[best_idx] >= threshold:
        return faq_data[best_idx]['cevap']
    else:
        return "Sorunuzu tam olarak cevaplayamıyorum. Lütfen daha detaylı sorar mısınız?"
