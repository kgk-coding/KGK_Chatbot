# src/ingest.py
import os
import chromadb
from sentence_transformers import SentenceTransformer

PERSIST_DIR = os.path.join("chroma_db")
DATA_PATH = os.path.join("data", "soru_cevap.md")

embedder = SentenceTransformer("all-MiniLM-L6-v2")

def create_chroma_db():
    client = chromadb.PersistentClient(path=PERSIST_DIR)
    collection = client.get_or_create_collection("kgk_chatbot")

    # Koleksiyon boşsa yükle
    if collection.count() == 0:
        print("📘 Veri ChromaDB'ye ekleniyor...")
        with open(DATA_PATH, "r", encoding="utf-8") as f:
            content = f.read()

        # Soru-cevap çiftlerini ayır
        entries = content.split("**Soru:**")[1:]
        questions, answers = [], []

        for entry in entries:
            if "**Cevap:**" in entry:
                q_part, a_part = entry.split("**Cevap:**", 1)
                question = q_part.strip()
                answer = a_part.strip()
                questions.append(question)
                answers.append(answer)

        # Embedding oluştur
        embeddings = embedder.encode(questions).tolist()

        # Chroma'ya ekle
        collection.add(
            documents=answers,
            embeddings=embeddings,
            ids=[f"id_{i}" for i in range(len(questions))]
        )

        print(f"✅ {len(questions)} kayıt başarıyla eklendi.")
    else:
        print(f"ℹ️ ChromaDB zaten dolu ({collection.count()} kayıt var).")
