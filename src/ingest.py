# src/ingest.py
import os
import chromadb
from sentence_transformers import SentenceTransformer

PERSIST_DIR = os.path.join("chroma_db")
DATA_PATH = os.path.join("data", "soru_cevap.md")

# Embedding modeli
embedder = SentenceTransformer("all-MiniLM-L6-v2")

def create_chroma_db():
    client = chromadb.PersistentClient(path=PERSIST_DIR)
    collection = client.get_or_create_collection("kgk_chatbot")

    # Eğer koleksiyon boşsa ekle
    if collection.count() == 0:
        print("📘 Veri ChromaDB'ye ekleniyor...")
        with open(DATA_PATH, "r", encoding="utf-8") as f:
            content = f.read()

        # Soru-cevap çiftlerini ayır
        entries = content.split("**Soru:**")[1:]
        questions, answers = [], []

        for entry in entries:
            q_part, a_part = entry.split("**Cevap:**", 1)
            question = q_part.strip()
            answer = a_part.strip()
            questions.append(question)
            answers.append(answer)

        # Embedding oluştur ve kaydet
        embeddings = embedder.encode(questions).tolist()
        collection.add(
            documents=answers,
            embeddings=embeddings,
            ids=[f"id_{i}" for i in range(len(questions))]
        )

        print("✅ Veri başarıyla ChromaDB'ye eklendi.")
    else:
        print("✅ ChromaDB zaten dolu, yeniden eklenmedi.")

if __name__ == "__main__":
    create_chroma_db()
