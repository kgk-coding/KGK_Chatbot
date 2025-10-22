import streamlit as st
from rag_chain import retrieve_answer

st.set_page_config(page_title="Koçluk Chatbot", layout="centered")
st.title("Koçluk Chatbot")

user_input = st.text_input("Sorunuzu yazın:")

if user_input:
    answer = retrieve_answer(user_input)
    st.write("Cevap:", answer)  # sadece cevabı gösteriyoruz
