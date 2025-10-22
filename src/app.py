import streamlit as st
from rag_chain import retrieve_answer

st.set_page_config(page_title="Koçluk Chatbot", layout="centered")
st.title("Koçluk Chatbot")

user_input = st.text_input("Sorunuzu yazın ve Enter'a basın:")

if user_input:
    cevap = retrieve_answer(user_input)
    st.markdown(f"**Cevap:** {cevap}")
