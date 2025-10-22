import streamlit as st
from rag_chain import retrieve_answer

st.set_page_config(page_title="KGK Koçluk Chatbot", layout="centered")
st.title("KGK Koçluk Chatbot")
st.write(
    "Merhaba. Ben Köksal Gürkan Koçluk için oluşturulmuş koçluk odaklı Chatbot'um. "
    "Koçlukla ilgili temel bilgiler, süreçler, akış, koçluğa uygunluk ve benzeri konularda merak ettiklerini sorabilirsin."
    ""
)


st.write("Sorunuzu yazıp Enter'a basarak cevap alabilirsiniz.")

# Kullanıcıdan input
user_input = st.text_input("Sorunuz:")

# Enter tuşu ile cevap göster
if user_input:
    answer = retrieve_answer(user_input)
    st.write(answer)

st.markdown("---")
st.caption("Bu uygulama, [Köksal Gürkan Koçluk](https://www.koksalgurkan.com.tr/) web sitesine dayalı örnek bir RAG tabanlı chatbot projesidir.")

