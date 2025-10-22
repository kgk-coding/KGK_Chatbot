import streamlit as st
from rag_chain import retrieve_answer

st.title("Koçluk Chatbot (Streamlit)")

if "history" not in st.session_state:
    st.session_state.history = []

user_input = st.text_input("Sorunuzu yazın:")

if user_input:
    answer = retrieve_answer(user_input)
    st.session_state.history.append((user_input, answer))

for q, a in st.session_state.history:
    st.markdown(f"**Soru:** {q}")
    st.markdown(f"**Cevap:** {a}")
