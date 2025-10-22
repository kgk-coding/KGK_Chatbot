import json
import numpy as np
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity

model = SentenceTransformer('all-MiniLM-L6-v2')

# embeddings.json dosyasını yükle
with open("data/embeddings.json", "r", encoding="utf-8") as f:
    data = json.load(f)

documents = [item["document"] for item in data]
embeddings = np.array([item["embedding"] for item in data])

def retrieve_answer(question: str, top_k: int = 1):
    q_emb = model.encode([question])
    similarities = cosine_similarity(q_emb, embeddings)[0]
    top_idx = np.argsort(similarities)[::-1][:top_k]
    if similarities[top_idx[0]] < 0.3:
        return "Bu konuyla ilgili doğrudan bir bilgi bulamadım. Ne hakkında konuştuğunu biraz daha açar mısın?"
    return documents[top_idx[0]]
