import numpy as np
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity

# Modeli başlat
model = SentenceTransformer('all-MiniLM-L6-v2')

# Örnek soru-cevap listesi
faq_data = [
    {"question": "Koçluk almaya uygun muyum?", 
     "answer": "Genelde çoğu kişi koçluk almaya uygundur. Ancak belirli referans durumları teyit etmemiz gerekir ki bundan emin olalım."},
    {"question": "Koçluk seansları ne kadar sürer?", 
     "answer": "Tipik bir koçluk seansı 45-60 dakika sürer."},
    {"question": "Koçluk online yapılabilir mi?", 
     "answer": "Evet, koçluk seansları online veya yüz yüze yapılabilir."}
]

# Embeddingleri önceden hesaplayabiliriz
questions = [item["question"] for item in faq_data]
question_embeddings = model.encode(questions)

def retrieve_answer(user_question):
    user_embedding = model.encode([user_question])
    similarities = cosine_similarity(user_embedding, question_embeddings)
    best_idx = np.argmax(similarities)

    # Benzerlik düşükse default cevap
    if similarities[0][best_idx] < 0.5:
        return "Bu konuda yeterli verimiz yok, lütfen soruyu yeniden formüle edin."

    return faq_data[best_idx]["answer"]
