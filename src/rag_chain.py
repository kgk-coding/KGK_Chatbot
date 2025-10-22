import json
import os

# Repo kökünden JSON dosya yolu
json_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "soru_cevap.json")

with open(json_path, "r", encoding="utf-8") as f:
    faq_data = json.load(f)

def retrieve_answer(user_question):
    user_question_lower = user_question.lower()
    
    for item in faq_data:
        question_lower = item["soru"].lower()
        if question_lower in user_question_lower or user_question_lower in question_lower:
            return f"Cevap: {item['cevap']}"
    
    # Hiçbir uygun eşleşme yoksa
    return "Cevap: Sorunuzu tam olarak cevaplayamıyorum. Lütfen daha detaylı sorar mısınız?"
