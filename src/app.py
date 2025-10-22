# -*- coding: utf-8 -*-
# src/local_chat.py

from rag_chain import retrieve_answer

def main():
    print("Koçluk Chatbot")
    print("Çıkmak için 'exit' yazın")

    # Dialog memory: Kullanıcının önceki sorularını ve botun cevaplarını geçici olarak tutacağız
    dialog_memory = []

    while True:
        user_q = input("Sorunuzu yazın: ").strip()
        if user_q.lower() == "exit":
            print("Görüşürüz!")
            break
        if not user_q:
            print("Lütfen bir soru yazın.")
            continue

        try:
            # Önceki sorular ve cevaplar memory ile kullanılabilir
            answer = retrieve_answer(user_q, dialog_memory=dialog_memory)

            # Memory'ye ekle
            dialog_memory.append({"question": user_q, "answer": answer})

            print("\nCevap:", answer, "\n")
        except Exception as e:
            print(f"Hata oluştu: {e}\n")

if __name__ == "__main__":
    main()
