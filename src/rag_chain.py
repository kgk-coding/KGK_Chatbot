import json
import os

# JSON dosyasının repo kökünden yolu
json_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "soru_cevap.json")

# JSON dosyasını yükleme
try:
    with open(json_path, "r", encoding="utf-8") as f:
        faq_data = json.load(f)
except FileNotFoundError:
    raise FileNotFoundError(f"{json_path} bulunamadı. Lütfen JSON dosyasını repo köküne koyun.")

def retrieve_answer(user_question):
    user_question_lower = user_question.lower()

    for item in faq_data:
        question_lower = item["soru"].lower()
        # Kelime bazlı yakın eşleşme
        if any(word in user_question_lower for word in question_lower.split()):
            return f"Cevap: {item['cevap']}"
    
    # Hiçbir uygun cevap yoksa
    return "Cevap: Sorunuzu tam olarak cevaplayamıyorum. Lütfen daha detaylı sorar mısınız?"
