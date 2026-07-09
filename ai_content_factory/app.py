import os
import json
import streamlit as str_app # streamlit ismini çakışmasın diye str_app yaptık
from google import genai
from google.genai import types
from pydantic import BaseModel, Field

# Eğer Streamlit bulutundaysak gizli ayarlardan al, lokaldeysek bilgisayar hafızasından oku
if "GEMINI_API_KEY" in str_app.secrets:
    os.environ["GEMINI_API_KEY"] = str_app.secrets["GEMINI_API_KEY"]

# 2. Gemini İstemcisini Başlat
client = genai.Client()

# 3. Pydantic Çıktı Kalıbı
class SosyalMedyaIcerigi(BaseModel):
    linkedin_post: str = Field(description="LinkedIn için yazılmış, emojili ve profesyonel post.")
    twitter_flood: list[str] = Field(description="Twitter için yazılmış, maksimum 3 tweetlik flood listesi.")

# --- STREAMLIT ARAYÜZ AYARLARI ---
str_app.set_page_config(page_title="AI İçerik Fabrikası", page_icon="🚀", layout="wide")

str_app.title("🚀 AI İçerik Fabrikası")
str_app.write("Ham fikrinizi veya teknik konunuzu girin, yapay zeka sizin için LinkedIn ve Twitter içeriklerini anında üretsin.")

# Kullanıcıdan girdi alacağımız büyük metin kutusu
kullanici_konusu = str_app.text_area(
    "Hangi konuda içerik üretmek istiyorsunuz?", 
    placeholder="Örn: Yapay zeka mühendisi olmak için neden doğrudan LLM'lerle başlamalıyız?",
    height=150
)

# Üret butonu
if str_app.button("İçerikleri Üret ✨", type="primary"):
    if not kullanici_konusu:
        str_app.warning("Lütfen önce bir konu veya fikir girin!")
    else:
        with str_app.spinner("Yapay zeka içerikleri hazırlıyor, lütfen bekleyin..."):
            try:
                # Yapay zekayı tetikliyoruz
                response = client.models.generate_content(
                    model='gemini-2.5-flash',
                    contents=f"Sana verilen konuyu al ve LinkedIn ile Twitter için harika içerikler üret. Konu: {kullanici_konusu}",
                    config=types.GenerateContentConfig(
                        response_mime_type="application/json",
                        response_schema=SosyalMedyaIcerigi,
                        temperature=0.7
                    ),
                )
                
                # Gelen ham JSON metnini Python sözlüğüne (dict) çeviriyoruz
                sonuc_data = json.loads(response.text)
                
                str_app.success("İçerikler başarıyla üretildi!")
                str_app.markdown("---")
                
                # Ekranı iki sütuna bölüyoruz: Sol tarafa LinkedIn, Sağ tarafa Twitter gelecek
                col1, col2 = str_app.columns(2)
                
                with col1:
                    str_app.subheader("💼 LinkedIn Paylaşımı")
                    # Yapay zekanın ürettiği postu buraya basıyoruz
                    str_app.info(sonuc_data["linkedin_post"])
                    
                with col2:
                    str_app.subheader("🐦 Twitter / X Floodu")
                    # Liste halindeki tweetleri döngüyle ekrana basıyoruz
                    for i, tweet in enumerate(sonuc_data["twitter_flood"], 1):
                        str_app.warning(f"**Tweet {i}:**\n\n{tweet}")
                        
            except Exception as e:
                str_app.error(f"Bir hata oluştu: {e}")
