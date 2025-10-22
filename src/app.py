import streamlit as st
from rag_chain import retrieve_answer

st.set_page_config(page_title="Koçluk Chatbot", layout="centered")
st.title("Koçluk Chatbot")

st.write("Sorunuzu yazıp Enter'a basarak cevap alabilirsiniz.")

# Kullanıcıdan input
user_input = st.text_input("Sorunuz:")

# Enter tuşu ile cevap göster
if user_input:
    answer = retrieve_answer(user_input)
    st.write(answer)
