# -*- coding: utf-8 -*-
import streamlit as st
from rag_chain import retrieve_answer, embed_query
from sentence_transformers import SentenceTransformer

# Başlık
st.title("Koçluk Chatbot (Cloud Test)")

# Kullanıcı dialog memory (önceki sorular ve cevaplar)
if "history" not in st.session_state:
    st.session_state.history = []

# Embedding modeli
embed_model = SentenceTransformer("all-MiniLM-L6-v2")  # veya cloud'da uygun model

# Kullanıcı girişi
user_input = st.text_input("Sorunuzu yazın:")

if user_input:
    # Soru embedding
    query_emb = embed_query(user_input, embed_model.encode)
    
    # Cevap
    answer = retrieve_answer(query_emb)
    
    # Dialog memory'ye ekle
    st.session_state.history.append({"user": user_input, "bot": answer})

# Dialog geçmişini göster
for chat in st.session_state.history:
    st.markdown(f"**Soru:** {chat['user']}")
    st.markdown(f"**Cevap:** {chat['bot']}")
