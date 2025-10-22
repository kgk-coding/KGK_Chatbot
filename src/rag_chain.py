from sentence_transformers import SentenceTransformer
import numpy as np
from .embed_utils import load_embeddings, cosine_similarity

# Model initialization
model = SentenceTransformer("all-MiniLM-L6-v2")

# Load JSON embeddings once at start
embeddings, documents = load_embeddings()

def embed_query(query):
    return model.encode(query)

def retrieve_answer(query, top_k=1):
    query_vec = embed_query(query)
    if not embeddings:
        return "Henüz veritabanında embed edilmiş bir doküman yok."
    
    similarities = [cosine_similarity(query_vec, emb) for emb in embeddings]
    best_idx = int(np.argmax(similarities))
    
    if similarities[best_idx] < 0.5:  # eşik, düşük benzerlik olursa yanıt yok
        return "Bu konuyla ilgili doğrudan bir bilgi bulamadım. Ne hakkında konuştuğunu biraz daha açar mısın?"
    
    return documents[best_idx]
