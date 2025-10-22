import streamlit as st
from rag_chain import retrieve_answer

st.set_page_config(page_title="Koçluk Chatbot", layout="centered")
st.title("Koçluk Chatbot")

# Kullanıcı sorusu
query = st.text_input("Sorunuzu yazın ve Enter'a basın:")

if query:
    answer = retrieve_answer(query)
    st.markdown(answer)
