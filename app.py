import streamlit as st
import streamlit.components.v1 as components
import utils
import os
from dotenv import load_dotenv

load_dotenv()

# Page Config
st.set_page_config(
    page_title="PolyFarm AI",
    page_icon="🌾",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Green & White Agricultural Theme
st.markdown("""
    <style>
    /* Clean agricultural green theme */
    .stApp { 
        background: linear-gradient(to bottom, #f1f8f4 0%, #e8f5e9 100%);
    }
    
    /* Header styling */
    h1 {
        color: #2e7d32 !important;
        font-weight: 700 !important;
        text-align: center;
        margin-bottom: 0.5rem !important;
    }
    
    h2, h3 {
        color: #388e3c !important;
        font-weight: 600 !important;
    }
    
    /* Tab styling */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
        background: white;
        padding: 10px;
        border-radius: 15px;
        box-shadow: 0 2px 8px rgba(0,0,0,0.08);
    }
    
    .stTabs [data-baseweb="tab"] {
        height: 50px;
        background: #f1f8f4;
        border-radius: 10px;
        color: #2e7d32;
        font-weight: 600;
        padding: 0 20px;
    }
    
    .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, #66bb6a 0%, #43a047 100%);
        color: white !important;
    }
    
    /* Button styling */
    .stButton>button {
        width: 100%;
        background: linear-gradient(135deg, #66bb6a 0%, #43a047 100%);
        color: white !important;
        border: none;
        padding: 12px 24px;
        border-radius: 12px;
        font-weight: 600;
        font-size: 16px;
        box-shadow: 0 4px 12px rgba(67, 160, 71, 0.3);
        transition: all 0.3s;
    }
    
    .stButton>button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 16px rgba(67, 160, 71, 0.4);
    }
    
    /* File uploader */
    .stFileUploader {
        background: white;
        padding: 20px;
        border-radius: 15px;
        border: 2px dashed #66bb6a;
        box-shadow: 0 2px 8px rgba(0,0,0,0.05);
    }
    
    /* Input fields */
    .stTextInput>div>div>input {
        background: white;
        border: 2px solid #e0e0e0;
        border-radius: 10px;
        padding: 12px;
        font-size: 16px;
    }
    
    .stTextInput>div>div>input:focus {
        border-color: #66bb6a;
    }
    
    /* Success/Warning/Info boxes */
    .stSuccess {
        background: #e8f5e9;
        color: #2e7d32 !important;
        padding: 16px;
        border-radius: 12px;
        border-left: 4px solid #66bb6a;
    }
    
    .stWarning {
        background: #fff3e0;
        color: #e65100 !important;
        padding: 16px;
        border-radius: 12px;
        border-left: 4px solid #ff9800;
    }
    
    .stInfo {
        background: #e3f2fd;
        color: #1565c0 !important;
        padding: 16px;
        border-radius: 12px;
        border-left: 4px solid #2196f3;
    }
    
    /* Shop cards */
    .shop-card {
        background: white;
        padding: 20px;
        border-radius: 15px;
        margin-bottom: 12px;
        box-shadow: 0 2px 8px rgba(0,0,0,0.08);
        border-left: 4px solid #66bb6a;
        transition: all 0.3s;
    }
    
    .shop-card:hover {
        transform: translateX(5px);
        box-shadow: 0 4px 12px rgba(0,0,0,0.12);
    }
    
    .shop-name {
        color: #2e7d32;
        font-size: 18px;
        font-weight: 700;
        margin: 0 0 8px 0;
    }
    
    .shop-detail {
        color: #555;
        font-size: 14px;
        margin: 4px 0;
    }
    
    /* Images */
    img {
        border-radius: 15px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.1);
    }
    
    /* Mobile responsive */
    @media (max-width: 768px) {
        .stApp { padding: 0.5rem !important; }
        h1 { font-size: 1.75rem !important; }
        .stTabs [data-baseweb="tab"] { 
            padding: 0 12px;
            font-size: 14px;
        }
    }
    
    /* Labels */
    label {
        color: #2e7d32 !important;
        font-weight: 600 !important;
    }
    </style>
""", unsafe_allow_html=True)

# Initialize Backend
if "vertex_initialized" not in st.session_state:
    if utils.init_vertex():
        st.session_state["vertex_initialized"] = True

# Header
st.markdown("# 🌾 PolyFarm AI Assistant")
st.markdown("<p style='text-align: center; color: #666; font-size: 18px;'>Smart Agriculture • Disease Detection • Supply Chain</p>", unsafe_allow_html=True)
st.markdown("<br>", unsafe_allow_html=True)

# Tabs
tab1, tab2, tab3 = st.tabs(["🔬 Disease Diagnosis", "🏪 Find Supplies", "📜 Gov Schemes"])

# TAB 1: Disease Diagnosis
with tab1:
    st.markdown("### 📸 Upload Crop Leaf Photo")
    st.markdown("<br>", unsafe_allow_html=True)
    
    uploaded_file = st.file_uploader("Take or upload a photo of the affected leaf", type=["jpg", "png", "jpeg"])
    
    if uploaded_file:
        col1, col2 = st.columns([1, 1])
        with col1:
            st.image(uploaded_file, caption="Uploaded Image", use_container_width=True)
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        if st.button("🔍 Analyze Disease Now", type="primary"):
            with st.spinner("🔬 Analyzing leaf with AI..."):
                result = utils.smart_orchestrator(uploaded_file.getvalue(), uploaded_file.type)
                
                if result["status"] == "success":
                    diagnosis = result["diagnosis"]
                    
                    st.markdown("<br>", unsafe_allow_html=True)
                    st.success(f"**🦠 Disease Detected:** {diagnosis.get('diagnosis', 'Unknown')}")
                    st.warning(f"**⚠️ Severity Level:** {diagnosis.get('severity', 'N/A')}")
                    st.info(f"**💊 Recommended Treatment:** {diagnosis.get('cure', 'N/A')}")
                    st.info(f"**🧪 Chemical Required:** {diagnosis.get('chemical', 'N/A')}")
                    
                    # Voice output
                    if result.get("audio"):
                        st.markdown("<br>", unsafe_allow_html=True)
                        st.markdown("**🔊 Audio Explanation (Hindi/Hinglish):**")
                        st.audio(result["audio"], format="audio/mp3")
                    
                    # Save for shops tab
                    st.session_state["last_chemical"] = diagnosis.get('chemical', '')
                    st.session_state["shops_data"] = result.get("shops", [])
                    
                    st.markdown("<br>", unsafe_allow_html=True)
                    st.success("✅ **Analysis Complete!** Switch to 'Find Supplies' tab to locate nearby stores.")
                else:
                    st.error(f"❌ Error: {result.get('message', 'Unknown error')}")

# TAB 2: Supply Chain
with tab2:
    st.markdown("### 🗺️ Find Nearby Agricultural Stores")
    st.markdown("<br>", unsafe_allow_html=True)
    
    chemical = st.session_state.get("last_chemical", "")
    search = st.text_input("Search for agricultural product:", value=chemical, placeholder="e.g., Mancozeb, Fertilizer, Seeds")
    
    if st.button("🔍 Search Nearby Stores", type="primary"):
        if search:
            with st.spinner("📍 Searching nearby stores..."):
                shops = utils.get_shops_data(search)
                st.session_state["shops_data"] = shops
    
    # Display shops
    if "shops_data" in st.session_state and st.session_state["shops_data"]:
        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown(f"### 📍 Found {len(st.session_state['shops_data'])} Stores Near You")
        st.markdown("<br>", unsafe_allow_html=True)
        
        for shop in st.session_state["shops_data"]:
            st.markdown(f"""
            <div class='shop-card'>
                <p class='shop-name'>🏪 {shop.get('name', 'Agricultural Store')}</p>
                <p class='shop-detail'>📞 Phone: {shop.get('phone', 'N/A')}</p>
                <p class='shop-detail'>📍 Distance: {shop.get('dist', 'N/A')} km away</p>
            </div>
            """, unsafe_allow_html=True)

# TAB 3: Government Schemes
with tab3:
    st.markdown("### 🏛️ Government Agricultural Schemes")
    st.markdown("<br>", unsafe_allow_html=True)
    
    query = st.text_input("Ask about subsidies, loans, or schemes:", placeholder="e.g., What subsidies are available for organic farming?")
    
    if st.button("💬 Get Information", type="primary"):
        if query:
            with st.spinner("🔍 Searching government database..."):
                response = utils.gov_agent_response(query)
                st.markdown("<br>", unsafe_allow_html=True)
                st.info(response)

# Voice Assistant
st.markdown("<br><br>", unsafe_allow_html=True)
st.markdown("---")
st.markdown("### 🎤 Voice Assistant - Dr. Bio AI")
st.markdown("<p style='color: #666;'>Click the microphone icon (bottom-right) to ask questions via voice</p>", unsafe_allow_html=True)

components.html("""
    <elevenlabs-convai agent-id="agent_7201kda16szbffnsemfp5nqa2j44"></elevenlabs-convai>
    <script src="https://unpkg.com/@elevenlabs/convai-widget-embed" async type="text/javascript"></script>
    <style>
        elevenlabs-convai {
            position: fixed;
            bottom: 20px;
            right: 20px;
            z-index: 9999;
        }
    </style>
""", height=80)

st.markdown("<br>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #999; font-size: 14px;'>© 2024 PolyFarm Team • Powered by Gemini 2.0 & ElevenLabs</p>", unsafe_allow_html=True)
