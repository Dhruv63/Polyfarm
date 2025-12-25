# 🌾 PolyFarm: AI for Farmers

**PolyFarm** is a Multi-Agent System designed to empower Indian farmers by integrating Computer Vision, Location Services, and Knowledge Retrieval into a simple mobile-friendly interface. Built for the AgriTech Hackathon.

![Status](https://img.shields.io/badge/Status-Prototype-green)
![Tech Stack](https://img.shields.io/badge/Tech-Streamlit%20|%20Gemini%20Pro%20|%20LangChain-blue)

## 🚀 Features

### 1. 🍃 Bio-Agent (Vision)
- **Problem**: Farmers struggle to identify crop diseases accurately.
- **Solution**: Upload a photo of a leaf/crop. The Bio-Agent (powered by **Gemini 2.0 Flash**) diagnoses the disease, assesses severity, and recommends a specific chemical cure.

### 2. 🏪 Local-Agent (Location)
- **Problem**: Knowing the cure is useless if you can't find it nearby.
- **Solution**: Automatically takes the recommended chemical from the Bio-Agent and searches a local database (`shops.json`) to find the nearest agricultural store.
- **Tech**: Uses `geopy` for distance calculation.

### 3. 📜 Gov-Agent (Knowledge)
- **Problem**: Government schemes (PM Kisan, Soil Health Card) are complex and hard to understand.
- **Solution**: A RAG (Retrieval-Augmented Generation) pipeline that lets farmers ask questions in plain language.
- **Tech**: **LangChain** + **Vertex AI Embeddings** + **ChromaDB** to search through official PDF documents.

---

## 🛠️ Installation

### Prerequisites
- Python 3.9+
- Google Cloud Project with Vertex AI API enabled.
- Service Account Credentials JSON.

### Steps
1. **Clone the Repository**
   ```bash
   git clone https://github.com/your-username/polyfarm.git
   cd polyfarm
   ```

2. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Setup Environment**
   - Place your Google Cloud Service Account key in the root folder as `credentials.json`.
   - Create a `.env` file:
     ```env
     GOOGLE_APPLICATION_CREDENTIALS="credentials.json"
     PROJECT_ID="your-gcp-project-id"
     location="us-central1"
     ```
   - Ensure you have some PDF schemes in `data/` (e.g., `scheme1.pdf`) and the valid `shops.json`.

4. **Run the App**
   ```bash
   streamlit run app.py
   ```

---

## 📂 Project Structure

```
PolyFarm/
├── app.py              # Main Streamlit Application (UI)
├── utils.py            # Backend Logic (Agents & AI integrations)
├── requirements.txt    # Python Dependencies
├── .env                # API Keys (Not uploaded to Git)
├── credentials.json    # Google Cloud Key (Not uploaded to Git)
└── data/
    ├── shops.json      # Mock Database of Local Shops
    └── scheme1.pdf     # Knowledge Base for Gov-Agent
```

## 🤖 How to Demo (The "Happy Path")
1. **Diagnosis**: Go to "Bio-Agent" tab. Upload a leaf image (e.g., Apple Rust). Wait for diagnosis.
2. **Handshake**: Note the recommended chemical (e.g., "Mancozeb").
3. **Action**: Go to "Local-Agent" tab. The search bar auto-fills "Mancozeb". Click **Find Local Shops**.
4. **Result**: See the nearest shop (Kisan Seva Kendra) displayed on a card and map.

---

## 🛡️ License
This project is created for educational/hackathon purposes.
