# Köksal Gürkan Koçluk - Koçluk için Chatbot

Bu proje, **Köksal Gürkan Koçluk** için oluşturulmuş RAG tabanlı bir chatbot örneğidir.  
Amaç, Köksal Gürkan Koçluk için web sitesi üzerinden koçluk hakkında sık sorulan sorulara hızlı, doğal ve bilgilendirici yanıtlar sunmaktır.
Data seti tamamen https://www.koksalgurkan.com.tr/ sitesi ve kişisel deneyimlere dayalı hazırlanmış özel içerikten oluşmaktadır.


## 🔹 Proje Özeti
- **Proje Adı:** Koçluk için Chatbot  
- **Amaç:** RAG (Retrieval Augmented Generation) mantığıyla bilgiye dayalı yanıtlar üretmek.  
- **Veri:** `data/embeddings.json` (Özel hazırlanmış soru-cevap çiftlerinden lokalde oluşturulmuş json veri dosyası.)
- **Model:** `sentence-transformers (all-MiniLM-L6-v2)`  
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
│   └─ embeddings.json       # Lokalde ürettiğimm embed dosyası
│
├─ chroma_db/
│   └─ .keep                 # Boş klasör için git track
│
├─ requirements.txt
├─ runtime.txt
├─ .gitignore
└─ README.md



## 🔹 Nasıl Çalışır
1. `soru_cevap.md` dosyası okunur.
2. Soru-cevap çiftleri embedding’e dönüştürülür.
3. Chroma veritabanına kaydedilir.
4. Kullanıcı bir soru girdiğinde, en benzer kayıtlar sorgulanır.
5. En uygun yanıt kullanıcıya sunulur.

## 🔹 Çalıştırma (Streamlit Cloud)
1. Bu repo'yu GitHub'da açın.
2. [Streamlit Cloud](https://share.streamlit.io/) hesabınızla yeni bir app oluşturun.
3. “Main file path” olarak `src/app.py` dosyasını seçin.
4. Uygulama otomatik olarak deploy edilir.

## 🔹 Deploy Linki
[https://<senin-streamlit-uygulama-linkin>.streamlit.app](https://<senin-streamlit-uygulama-linkin>.streamlit.app)

---
© 2025 Köksal Gürkan Koçluk — Tüm hakları saklıdır.


