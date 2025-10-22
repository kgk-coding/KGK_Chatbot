import streamlit as st
from src.rag_chain import retrieve_answer

st.set_page_config(page_title="Koçluk Chatbot", page_icon="🤖")
st.title("Koçluk Chatbot (Cloud)")

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

user_input = st.text_input("Sorunuzu yazın:")

if st.button("Gönder") and user_input:
    answer = retrieve_answer(user_input)
    st.session_state.chat_history.append({"user": user_input, "bot": answer})

for chat in st.session_state.chat_history:
    st.markdown(f"**Sen:** {chat['user']}")
    st.markdown(f"**Bot:** {chat['bot']}")
