# ai-content-factory
## 🚀 Project Overview
AI Content Factory, ham fikirleri ve teknik metinleri analiz ederek LinkedIn ve Twitter/X için optimize edilmiş içerikler üreten AI-native bir web uygulamasıdır. 

### 🛠️ Technical Stack & Architecture
* **LLM Engine:** Google Gemini 2.5 Flash
* **Framework / UI:** Streamlit
* **Data Validation:** Pydantic (Structured JSON Output)

### 💡 Engineering Approach (Why this project matters?)
Yapay zeka modellerinin serbest metin üretimindeki halüsinasyonlarını ve düzensiz çıktılarını engellemek adına, model `response_schema` kullanılarak katı bir Pydantic veri iskeletine zorlanmıştır. Bu sayede modelden gelen ham veriler, bir yazılım sisteminin (API/UI) işleyebileceği güvenilir bir JSON objesine dönüştürülmüş ve Streamlit arayüzündeki dinamik bileşenlere hatasız bir şekilde dağıtılmıştır.
