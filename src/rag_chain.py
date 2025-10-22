import numpy as np
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity

# Modeli yükle
model = SentenceTransformer('all-MiniLM-L6-v2')

# Soru-cevap verisi
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

def retrieve_answer(user_question, similarity_threshold=0.5):
    """
    Kullanıcı sorusuna en uygun cevabı döndürür.
    Eğer similarity threshold'un altında ise, standart uyarı mesajı döner.
    """
    user_embedding = model.encode([user_question])
    similarities = cosine_similarity(user_embedding, question_embeddings)
    best_idx = np.argmax(similarities)
    best_score = similarities[0][best_idx]

    if best_score < similarity_threshold:
        return "Sorunuzu tam olarak cevaplayamıyorum. Lütfen daha detaylı sorar mısınız?"

    return faq_data[best_idx]["answer"]
