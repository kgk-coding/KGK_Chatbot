import json
import numpy as np
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity

model = SentenceTransformer('all-MiniLM-L6-v2')

# Embed dosyasını yükle
with open("data/embeddings.json", "r", encoding="utf-8") as f:
    data = json.load(f)

documents = [item["document"] for item in data]
embeddings = np.array([item["embedding"] for item in data])

def embed_query(query):
    return model.encode(query)

def retrieve_answer(user_question, dialog_memory=None):
    if len(embeddings) == 0:
        return "Henüz veritabanında embed edilmiş bir doküman yok."

    query_vec = embed_query(user_question).reshape(1, -1)
    sim_scores = cosine_similarity(query_vec, embeddings)
    best_idx = np.argmax(sim_scores)

    if sim_scores[0, best_idx] < 0.4:
        return "Bu konuyla ilgili doğrudan bir bilgi bulamadım. Ne hakkında konuştuğunu biraz daha açar mısın?"

    return documents[best_idx]
