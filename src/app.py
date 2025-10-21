# src/app.py
import streamlit as st
from rag_chain import retrieve_answer
from ingest import create_chroma_db
import os
import chromadb


# DEBUG: Veritabanı kayıt sayısını logla
client = chromadb.PersistentClient(path="chroma_db")
collection = client.get_or_create_collection("kgk_chatbot")
print(f"DEBUG >>> ChromaDB kayıt sayısı: {collection.count()}")

# Sayfa ayarları
st.set_page_config(page_title="Köksal Gürkan Koçluk Chatbot", page_icon="💬")

# Başlık ve açıklama
st.title("💬 Köksal Gürkan Koçluk Chatbot")
st.write(
    "Merhaba 👋 Ben Köksal Gürkan Koçluk için oluşturulmuş koçluk odaklı Chatbot'um. "
    "Koçlukla ilgili temel bilgiler, süreçler, akış, koçluğa uygunluk ve benzeri konularda merak ettiklerini sorabilirsin."
)

# ChromaDB dizin yolu
PERSIST_DIR = os.path.join("chroma_db")

# 🔹 Her zaman ChromaDB kontrolü (boşsa yeniden oluşturur)
if not os.path.exists(PERSIST_DIR) or not os.listdir(PERSIST_DIR):
    with st.spinner("Veri tabanı hazırlanıyor..."):
        create_chroma_db()
    st.success("Veri tabanı oluşturuldu. ✅")


# 🔹 Kullanıcıdan soru al
user_q = st.text_input("Sorunuzu yazın:", key="user_input")

if st.button("Cevabı Göster"):
    if user_q.strip():
        with st.spinner("Düşünüyorum..."):
            try:
                answer = retrieve_answer(user_q)
                st.markdown(answer)
            except Exception as e:
                st.error(f"Bir hata oluştu: {e}")
    else:
        st.warning("Lütfen bir soru yazın.")

st.markdown("---")
st.caption("Bu uygulama, Köksal Gürkan Koçluk web sitesine dayalı örnek bir RAG tabanlı chatbot projesidir.")
