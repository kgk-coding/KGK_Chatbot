import streamlit as st
from rag_chain import retrieve_answer

st.set_page_config(page_title="Koçluk Chatbot", layout="centered")
st.title("Koçluk Chatbot")

# Enter ile cevap alma
user_input = st.text_input("Sorunuzu buraya yazın:")

if user_input:
    response = retrieve_answer(user_input)
    st.write(response)
