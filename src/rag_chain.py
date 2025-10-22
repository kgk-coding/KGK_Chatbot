import json
import numpy as np
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity

# Modeli initialize edin (zaten varsa değiştirmeye gerek yok)
model = SentenceTransformer('all-MiniLM-L6-v2')

# Örnek veri: sorular ve cevaplar
faq_data = [
    {"question": "Koçluk almaya uygun muyum?", 
     "answer": "Genelde çoğu kişi koçluk almaya uygundur. Ancak belirli referans durumları teyit etmemiz gerekir ki bundan emin olalım."}
]

def retrieve_answer(user_question):
    # Tüm soruları al
    questions = [item["question"] for item in faq_data]
    
    # Embeddingleri al
    question_embeddings = model.encode(questions)
    user_embedding = model.encode([user_question])
    
    # Cosine similarity ile en yakın soruyu bul
    similarities = cosine_similarity(user_embedding, question_embeddings)
    best_idx = np.argmax(similarities)
    
    # Sadece cevabı dön (prefix eklemeyin)
    return faq_data[best_idx]["answer"]
