import streamlit as st
from rag_chain import retrieve_answer

st.set_page_config(page_title="Koçluk Chatbot", layout="centered")
st.title("Koçluk Chatbot")
st.write("Sorunuzu yazın ve cevap alın. Çıkmak için tarayıcıyı kapatabilirsiniz.")

# Dialog memory: Kullanıcının önceki sorularını ve botun cevaplarını geçici olarak tutacağız
if "dialog_memory" not in st.session_state:
    st.session_state.dialog_memory = []

user_input = st.text_input("Sorunuzu yazın:")

if user_input:
    answer = retrieve_answer(user_input, dialog_memory=st.session_state.dialog_memory)
    st.session_state.dialog_memory.append({"user": user_input, "bot": answer})
    st.write(f"**Cevap:** {answer}")
