import os
import json
from sentence_transformers import SentenceTransformer

# Modeli yükle
model = SentenceTransformer('all-MiniLM-L6-v2')

# Örnek dokümanlar (lokal olarak değiştirebilirsin)
docs = [
    {
        "id": "doc_0",
        "document": "Soru: Koçluk nedir?\nCevap: Koçluk, kişinin kendi hedeflerine ulaşmasını destekleyen bir süreçtir.",
    },
    {
        "id": "doc_1",
        "document": "Soru: Ben koç olabilir miyim?\nCevap: Koç olabilmek için resmi bir eğitim almanız gerekir.",
    },
]

# Embedleri oluştur
for item in docs:
    item["embedding"] = model.encode(item["document"]).tolist()

# data klasörünü oluştur
os.makedirs("data", exist_ok=True)

# JSON olarak kaydet
with open("data/embeddings.json", "w", encoding="utf-8") as f:
    json.dump(docs, f, ensure_ascii=False, indent=4)

print(f"✅ {len(docs)} doküman embed edildi ve data/embeddings.json dosyasına kaydedildi.")
