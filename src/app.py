import streamlit as st
from rag_chain import retrieve_answer

st.set_page_config(page_title="KGK Koçluk Chatbot", layout="centered")
st.title("KGK Kocluk Chatbot")
st.write("Bu chatbot, koçlukla ilgili sorularınızı https://www.koksalgurkan.com.tr/ sitesi ve kişisel deneyimlerimi referans alarak hazırlanmış özel içerik dokümandaki bilgilere göre yanıtlar.")


# Enter ile cevaplama
user_input = st.text_input("Sorunuzu yazın ve Enter'a basın:")

if user_input:
    answer = retrieve_answer(user_input)
    st.markdown(answer)
