# Köksal Gürkan Koçluk - Koçluk için Chatbot

Bu proje, **Köksal Gürkan Koçluk** için oluşturulmuş RAG tabanlı bir chatbot örneğidir.  
Amaç, Köksal Gürkan Koçluk için web sitesi üzerinden koçluk hakkında sık sorulan sorulara hızlı, doğal ve bilgilendirici yanıtlar sunmaktır.
Data seti tamamen https://www.koksalgurkan.com.tr/ sitesi ve kişisel deneyimlere dayalı hazırlanmış özel içerikten oluşmaktadır.


## 🔹 Proje Özeti
- **Proje Adı:** Koçluk için Chatbot  
- **Amaç:** RAG (Retrieval Augmented Generation) mantığıyla bilgiye dayalı yanıtlar üretmek.  
- **Veri:** `data/embeddings.json` (Özel hazırlanmış soru-cevap çiftlerinden lokalde oluşturulmuş json veri dosyası.)
- **Model:** `SentenceTransformer`  
- **Vektör DB:** Chroma (lokal persist directory)  
- **Web Arayüzü:** Streamlit  
- **Bulut Ortamı:** [Streamlit Community Cloud](https://streamlit.app)

## 🔹 Dosya Yapısı

KGK_Chatbot/
│
├─ src/
│   ├─ __init__.py
│   ├─ app.py                # Streamlit uygulaması
│   ├─ rag_chain.py          # Embed ve retrieval mantığı
│   └─ local_embed_create.py # JSON embed dosyası oluşturma
│
├─ data/
│   └─ soru_cevap.json       # Lokalde ürettiğimm embed dosyası
│
├─ chroma_db/
│   └─ .keep                 # Boş klasör için git track
│
├─ requirements.txt
├─ runtime.txt
├─ .gitignore
├─ setup.sh
└─ README.md



# KGK Chatbot

Bu proje, profesyonel koç Köksal Gürkan için geliştirilmiş bir soru-cevap chatbotudur. 
Özel hazırlanmış soru setininden oluşturulmuş json dosyasından yanıt alır ve Streamlit üzerinden çalışır.

## Kurulum ve Kullanım

1. Repository'yi klonla
2. Python 3.10+ ve virtualenv ile ortam oluştur
3. Gereksinimleri yükle:
    pip install -r requirements.txt
4. Streamlit uygulamasını çalıştır:
    streamlit run src/app.py


## Gereksinimler
  - huggingface_hub==0.16.4
  - sentence-transformers==2.2.2
  - torch==2.2.0
  - streamlit==1.50.0
  - chromadb==1.2.1
  - pandas==2.2.3
  - numpy==1.26.4
  - scikit-learn==1.3.2
  - rich==14.2.0
  - markdown-it-py==4.0.0
  - mdurl==0.1.2
  - pygments==2.19.2


## 🔹 Deploy Linki
[KGK Koçluk Chatbot](https://kgkchatbot.streamlit.app/)

---
© 2025 Köksal Gürkan Koçluk — Tüm hakları saklıdır.


