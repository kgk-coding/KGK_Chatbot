import json
import numpy as np

def load_embeddings(json_path="data/embeddings.json"):
    with open(json_path, "r", encoding="utf-8") as f:
        data = json.load(f)
    # her item: {"id":..., "document":..., "embedding":[...]}
    embeddings = [np.array(item["embedding"]) for item in data]
    documents = [item["document"] for item in data]
    return embeddings, documents

def cosine_similarity(vec1, vec2):
    if np.linalg.norm(vec1)==0 or np.linalg.norm(vec2)==0:
        return 0.0
    return np.dot(vec1, vec2)/(np.linalg.norm(vec1)*np.linalg.norm(vec2))
