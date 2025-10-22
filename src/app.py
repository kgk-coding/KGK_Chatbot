import streamlit as st
from rag_chain import retrieve_answer

st.set_page_config(page_title="Koçluk Chatbot", layout="centered")
st.title("Koçluk Chatbot")

# Streamlit text_input, Enter ile submit olacak şekilde
user_question = st.text_input("Sorunuzu yazın ve Enter'a basın:")

if user_question:
    answer = retrieve_answer(user_question)
    st.markdown(f"**Cevap:** {answer}")
