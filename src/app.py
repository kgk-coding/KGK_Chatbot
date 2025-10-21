# src/app.py
import streamlit as st
from src.rag_chain import retrieve_answer
from src.ingest import create_chroma_db
import os

st.set_page_config(page_title="Köksal Gürkan Koçluk Chatbot", page_icon="💬")

st.title("💬 Köksal Gürkan Koçluk Chatbot")
st.write(
    "Merhaba 👋 Ben Köksal Gürkan Koçluk için oluşturulmuş koçluk odaklı Chatbot'um. "
    "Koçlukla ilgili temel bilgiler, süreçleri, akış, koçluğa uygunluk ve benzeri konularda merak ettiklerini sorabilirsin."
)

# DB var mı kontrol et
if not os.path.exists("chroma_db") or not os.listdir("chroma_db"):
    with st.spinner("Veri tabanı oluşturuluyor..."):
        create_chroma_db()
    st.success("Veri tabanı hazır!")

# Kullanıcı girişi
user_q = st.text_input("Sorunuzu yazın:", key="input")

if st.button("Cevabı Göster"):
    if user_q.strip():
        with st.spinner("Düşünüyorum..."):
            answer = retrieve_answer(user_q)
        st.markdown(answer)
    else:
        st.warning("Lütfen bir soru yazın.")

st.markdown("---")
st.caption("Bu uygulama, Köksal Gürkan Koçluk sitesine dayalı örnek bir RAG tabanlı chatbot projesidir.")
