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

# Mobile-First CSS
st.markdown("""
    <style>
    /* Mobile-optimized design */
    .stApp { 
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    }
    .main { 
        padding: 1rem !important;
    }
    /* Card styling */
    .card {
        background: white;
        padding: 1.5rem;
        border-radius: 15px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        margin-bottom: 1rem;
    }
    /* Button styling */
    .stButton>button {
        width: 100%;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        padding: 0.75rem;
        border-radius: 10px;
        font-weight: 600;
        font-size: 1rem;
    }
    /* File uploader */
    .stFileUploader {
        background: white;
        padding: 1rem;
        border-radius: 10px;
    }
    /* Tabs */
    .stTabs [data-baseweb="tab-list"] {
        gap: 0.5rem;
    }
    .stTabs [data-baseweb="tab"] {
        padding: 0.75rem 1rem;
        background: rgba(255,255,255,0.2);
        border-radius: 10px;
        color: white;
        font-weight: 600;
    }
    /* Text colors */
    h1, h2, h3, p, label { 
        color: white !important;
    }
    /* Success/Warning/Info boxes */
    .stSuccess, .stWarning, .stInfo {
        padding: 1rem;
        border-radius: 10px;
        font-size: 1rem;
    }
    /* Image container */
    img {
        border-radius: 15px;
        max-width: 100%;
    }
    /* Mobile responsive */
    @media (max-width: 768px) {
        .main { padding: 0.5rem !important; }
        h1 { font-size: 1.75rem !important; }
        h2 { font-size: 1.25rem !important; }
    }
    </style>
""", unsafe_allow_html=True)

# Initialize Backend
if "vertex_initialized" not in st.session_state:
    if utils.init_vertex():
        st.session_state["vertex_initialized"] = True

# Header
st.markdown("# 🌾 PolyFarm AI")
st.markdown("### Smart Farming Assistant")

# Tabs
tab1, tab2, tab3 = st.tabs(["🔬 Diagnose", "🏪 Shops", "📜 Schemes"])

# TAB 1: Disease Diagnosis
with tab1:
    st.markdown("### Upload Crop Leaf Photo")
    
    uploaded_file = st.file_uploader("Take or upload photo", type=["jpg", "png", "jpeg"], label_visibility="collapsed")
    
    if uploaded_file:
        col1, col2 = st.columns([1, 1])
        with col1:
            st.image(uploaded_file, caption="Your Photo", use_container_width=True)
        
        if st.button("🔍 Analyze Disease", type="primary"):
            with st.spinner("Analyzing..."):
                result = utils.smart_orchestrator(uploaded_file.getvalue(), uploaded_file.type)
                
                if result["status"] == "success":
                    diagnosis = result["diagnosis"]
                    
                    # Results
                    st.success(f"**Disease:** {diagnosis.get('diagnosis', 'Unknown')}")
                    st.warning(f"**Severity:** {diagnosis.get('severity', 'N/A')}")
                    st.info(f"**Treatment:** {diagnosis.get('cure', 'N/A')}")
                    st.info(f"**Chemical:** {diagnosis.get('chemical', 'N/A')}")
                    
                    # Voice output
                    if result.get("audio"):
                        st.markdown("**🔊 Listen to explanation:**")
                        st.audio(result["audio"], format="audio/mp3")
                    
                    # Save for shops tab
                    st.session_state["last_chemical"] = diagnosis.get('chemical', '')
                    st.session_state["shops_data"] = result.get("shops", [])
                    
                    st.success("✅ Analysis complete! Check 'Shops' tab for nearby stores.")
                else:
                    st.error(f"Error: {result.get('message', 'Unknown error')}")

# TAB 2: Supply Chain
with tab2:
    st.markdown("### Find Nearby Agricultural Stores")
    
    chemical = st.session_state.get("last_chemical", "")
    search = st.text_input("Search for product:", value=chemical, placeholder="e.g., Mancozeb")
    
    if st.button("🔍 Find Stores", type="primary"):
        if search:
            with st.spinner("Searching..."):
                shops = utils.get_shops_data(search)
                st.session_state["shops_data"] = shops
    
    # Display shops
    if "shops_data" in st.session_state and st.session_state["shops_data"]:
        st.markdown(f"### 📍 Found {len(st.session_state['shops_data'])} stores")
        
        for shop in st.session_state["shops_data"]:
            with st.container():
                st.markdown(f"""
                <div style='background: white; padding: 1rem; border-radius: 10px; margin-bottom: 0.75rem; color: black;'>
                    <h4 style='color: #667eea; margin: 0;'>🏪 {shop.get('name', 'Store')}</h4>
                    <p style='margin: 0.5rem 0; color: #333;'>📞 {shop.get('phone', 'N/A')}</p>
                    <p style='margin: 0; color: #666;'>📍 {shop.get('dist', 'N/A')} km away</p>
                </div>
                """, unsafe_allow_html=True)

# TAB 3: Government Schemes
with tab3:
    st.markdown("### Ask About Government Schemes")
    
    query = st.text_input("Your question:", placeholder="e.g., What subsidies are available for organic farming?")
    
    if st.button("💬 Ask", type="primary"):
        if query:
            with st.spinner("Searching..."):
                response = utils.gov_agent_response(query)
                st.info(response)

# Voice Assistant Widget
st.markdown("---")
st.markdown("### 🎤 Voice Assistant")
st.markdown("Click the microphone below to talk with Dr. Bio AI")

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
""", height=100)

st.markdown("---")
st.markdown("<p style='text-align: center; color: rgba(255,255,255,0.7);'>© 2024 PolyFarm Team</p>", unsafe_allow_html=True)
