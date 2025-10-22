import os
import json

# JSON dosyasının yolu
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
json_path = os.path.join(BASE_DIR, "soru_cevap.json")

with open(json_path, "r", encoding="utf-8") as f:
    faq_data = json.load(f)

def retrieve_answer(query: str) -> str:
    query_lower = query.lower()

    # Soru kelimelerine göre basit eşleştirme
    for item in faq_data:
        soru_lower = item["soru"].lower()
        if any(word in query_lower for word in soru_lower.split()):
            return f"Cevap: {item['cevap']}"

    # Hiçbir uygun cevap bulunamazsa
    return "Cevap: Sorunuzu tam olarak cevaplayamıyorum. Lütfen daha detaylı sorar mısınız?"
