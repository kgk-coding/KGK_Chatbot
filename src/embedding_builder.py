import json
from sentence_transformers import SentenceTransformer
from pathlib import Path

# Kaynak dosyan
DATA_PATH = Path(__file__).parent.parent / "data" / "soru_cevap.json"
OUTPUT_PATH = Path(__file__).parent.parent / "data" / "embeddings.json"

model = SentenceTransformer("all-MiniLM-L6-v2")

with open(DATA_PATH, "r", encoding="utf-8") as f:
    faq_data = json.load(f)

embeddings = []
for item in faq_data:
    soru = item.get("soru") or item.get("question")
    cevap = item.get("cevap") or item.get("answer")
    if not soru or not cevap:
        continue
    vector = model.encode(soru)
    embeddings.append({"soru": soru, "cevap": cevap, "embedding": vector.tolist()})

with open(OUTPUT_PATH, "w", encoding="utf-8") as f:
    json.dump(embeddings, f, ensure_ascii=False, indent=2)

print(f"✅ Yeni embedding dosyası oluşturuldu: {OUTPUT_PATH}")
