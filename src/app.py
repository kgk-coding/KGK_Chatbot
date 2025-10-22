# src/app.py

import streamlit as st
import os
import chromadb
from src.ingest import create_chroma_db, debug_print_collection_info
from rag_chain import retrieve_answer

st.set_page_config(page_title="Köksal Gürkan Koçluk Chatbot", page_icon="💬")

st.title("💬 Köksal Gürkan Koçluk Chatbot")
st.write(
    "Merhaba 👋 Ben Köksal Gürkan Koçluk için oluşturulmuş koçluk odaklı Chatbot'um. "
    "Koçlukla ilgili temel bilgiler, süreçler, akış, koçluğa uygunluk ve benzeri konularda merak ettiklerini sorabilirsin."
)

PERSIST_DIR = os.path.join("chroma_db")

# Veri tabanı yoksa veya boşsa oluştur (sessiz, kullanıcıya mesaj gösterme istemiyorsun)
if not os.path.exists(PERSIST_DIR) or not os.listdir(PERSIST_DIR):
    with st.spinner("Veritabanı hazırlanıyor..."):
        create_chroma_db()
# (Bilgi mesajı göstermiyoruz - talebine göre gizledim)

st.markdown("---")


# DEBUG bölümü (isteğe bağlı) - sadece geliştirirken aktifleştir
with st.expander("Geliştirici / Debug Kontrolleri (isteğe bağlı)"):
    if st.button("Veritabanı bilgilerini göster"):
        info = debug_print_collection_info()
        st.json(info)
    st.write("Not: Bu paneli test bitince kaldırabilirsin.")

st.markdown("---")


# Kullanıcı girişi
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
