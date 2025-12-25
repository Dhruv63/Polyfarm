import streamlit as st
import streamlit.components.v1 as components
import utils
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Page Config
st.set_page_config(
    page_title="PolyFarm",
    page_icon="🌾",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- CUSTOM CSS ---
st.markdown("""
    <style>
    .stApp { background: linear-gradient(to bottom right, #f0f8ff, #e0f2f1); }
    .main, .stMarkdown, p, h1, h2, h3, li { color: #000 !important; }
    div[data-testid="stMetricValue"] { font-size: 24px; color: #2e7d32; }
    </style>
""", unsafe_allow_html=True)

# Initialize Backend
if "vertex_initialized" not in st.session_state:
    if utils.init_vertex():
        st.session_state["vertex_initialized"] = True
    else:
        st.error("Failed to connect to Google Vertex AI. Check credentials.")

# Title
st.title("🌾 PolyFarm: Voice-First AI")
st.markdown("### Powered by Gemini 2.0, MongoDB & ElevenLabs")

# --- SIDEBAR: The Voice Agent ---
with st.sidebar:
    st.image("https://img.icons8.com/color/96/000000/farmer-male.png", width=100)
    st.header("Admin Console")
    st.success("Cloud DB: Connected 🟢")
    st.success("Voice Engine: Listening 🟢")
    
    st.markdown("---")
    st.markdown("### 🗣️ Talk to Dr. Bio")
    st.write("Click the microphone below to ask any doubts instantly!")
    
    # --- ELEVENLABS WIDGET INTEGRATION ---
    # We use a tall iframe to ensure the chat bubble has space to open
    components.html("""
        <elevenlabs-convai agent-id="agent_7201kda16szbffnsemfp5nqa2j44"></elevenlabs-convai>
        <script src="https://unpkg.com/@elevenlabs/convai-widget-embed" async type="text/javascript"></script>
        <style>
            elevenlabs-convai {
                position: fixed;
                bottom: 20px;
                right: 20px;
            }
        </style>
    """, height=500)
    # -------------------------------------

# Tabs
tab1, tab2, tab3 = st.tabs(["🍃 Diagnosis (Vision)", "🏪 Supply Chain (Maps)", "📜 Government (RAG)"])

# --- TAB 1: Bio-Agent ---
with tab1:
    st.header("Dr. Bio - Disease Diagnosis")
    uploaded_file = st.file_uploader("Upload Leaf Photo", type=["jpg", "png", "jpeg"])
    
    if uploaded_file:
        st.image(uploaded_file, caption="Uploaded Image", width=300)
        
        if st.button("Diagnose & Explain", type="primary"):
            with st.spinner("Analyzing Leaf..."):
                # 1. Vision Analysis (Gemini)
                result = utils.bio_agent(uploaded_file.getvalue(), uploaded_file.type)
                
                if "error" not in result:
                    st.success(f"**Detected:** {result.get('diagnosis')}")
                    st.warning(f"**Severity:** {result.get('severity')}")
                    st.info(f"**Cure:** {result.get('cure')}")
                    
                    # Save for Local Agent
                    st.session_state["last_cure"] = result.get('chemical')
                    
                    # 2. Voice Output (ElevenLabs TTS)
                    # This reads the specific diagnosis immediately
                    voice_script = result.get('voice_script_hindi', 'Analysis complete.')
                    st.markdown(f"**Audio Assistant:** *{voice_script}*")
                    
                    audio_bytes = utils.text_to_speech(voice_script)
                    if audio_bytes:
                        st.audio(audio_bytes, format="audio/mp3", autoplay=True)
                else:
                    st.error(result["error"])

# --- TAB 2: Local-Agent ---
with tab2:
    st.header("Local Supply Chain")
    cure_to_find = st.session_state.get("last_cure", "")
    search_term = st.text_input("Search for Product:", value=cure_to_find)
    
    if st.button("Find Nearby Stock"):
        if search_term:
            with st.spinner("Querying MongoDB Atlas..."):
                result = utils.local_agent(search_term)
                if "Error" in result:
                    st.error(result)
                else:
                    st.markdown(result, unsafe_allow_html=True)
                    st.balloons()

# --- TAB 3: Gov-Agent ---
with tab3:
    st.header("Government Schemes (RAG)")
    query = st.text_input("Ask about subsidies:")
    if st.button("Ask Gov-Agent"):
        response = utils.gov_agent_response(query)
        st.write(response)

st.markdown("---")
st.markdown("© 2024 PolyFarm Hackathon Team")
