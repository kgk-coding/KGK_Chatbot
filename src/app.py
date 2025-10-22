import streamlit as st
from rag_chain import retrieve_answer

st.set_page_config(page_title="Koçluk Chatbot", layout="centered")
st.title("Koçluk Chatbot")

# Enter ile cevaplama
user_input = st.text_input("Sorunuzu yazın ve Enter'a basın:")

if user_input:
    answer = retrieve_answer(user_input)
    st.markdown(answer)
