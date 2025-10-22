# -*- coding: utf-8 -*-
import os
import re
import json
from sentence_transformers import SentenceTransformer

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_PATH = os.path.join(SRC_DIR, "soru_cevap.md")
EMBED_PATH = os.path.join(SRC_DIR, "embeddings.json")

embedder = SentenceTransformer("all-MiniLM-L6-v2")

def create_embeddings():
    if not os.path.exists(DATA_PATH):
        print(f"?? Veri dosyasý bulunamadý: {DATA_PATH}")
        return

    with open(DATA_PATH, "r", encoding="utf-8-sig") as f:
        content = f.read()

    # Regex ile soru-cevap bloklarýný yakala
    pattern = r"\*\*Soru:\*\*\s*(.*?)\s*\*\*Cevap:\*\*\s*(.*?)(?=\n\s*\*\*Soru:\*\*|$)"
    matches = re.findall(pattern, content, re.DOTALL)

    if not matches:
        print("?? Dosyada soru-cevap yapýsý bulunamadý.")
        return

    items = []
    for i, (question, answer) in enumerate(matches):
        question = question.strip().replace("\n", " ")
        answer = answer.strip()
        embedding = embedder.encode([f"Soru: {question}\nCevap: {answer}"])[0].tolist()
        items.append({
            "question": question,
            "answer": answer,
            "embedding": embedding
        })
        print(f"? {i+1}. dokuman embed edildi")

    with open(EMBED_PATH, "w", encoding="utf-8") as f:
        json.dump(items, f, ensure_ascii=False, indent=2)

    print(f"? Toplam {len(items)} dokuman embed edildi ve {EMBED_PATH} dosyasýna kaydedildi.")

if __name__ == "__main__":
    create_embeddings()
