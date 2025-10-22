import numpy as np
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
import json

# Modeli yükle
model = SentenceTransformer('all-MiniLM-L6-v2')

# Soru-cevap verisi (örnek: json veya list)
# FAQ formatında
faq_data = [
    {"question": "Koçluk almaya uygun muyum?", 
     "answer": "Genelde çoğu kişi koçluk almaya uygundur. Ancak belirli durumları teyit etmemiz gerekir."},
    {"question": "Koçluk seansları ne kadar sürer?", 
     "answer": "Koçluk seansları genellikle 50-60 dakika sürer."},
    {"question": "Koçluk online olabilir mi?", 
     "answer": "Evet, koçluk online olarak da yapılabilir."},
]

# Embeddingleri hazırla
questions = [item["question"] for item in faq_data]
question_embeddings = model.encode(questions)

def retrieve_answer(user_question, similarity_threshold=0.3):
    user_embedding = model.encode([user_question])
    similarities = cosine_similarity(user_embedding, question_embeddings)
    best_idx = np.argmax(similarities)

    # Esnek eşik: düşükse bile en yakın cevabı ver
    if similarities[0][best_idx] < similarity_threshold:
        # En yakın 2 cevabı gösterebiliriz
        top_indices = similarities[0].argsort()[-2:][::-1]
        answers = [faq_data[i]["answer"] for i in top_indices]
        return "Yakın konular:\n- " + "\n- ".join(answers)

    return faq_data[best_idx]["answer"]
