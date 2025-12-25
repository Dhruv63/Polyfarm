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
    initial_sidebar_state="expanded"
)

# ... (CSS remains same) ...

# ... (Logic remains same) ...



# STRICT GREEN & WHITE THEME
st.markdown("""
    <style>
    /* Force Light Mode & White Background */
    [data-testid="stAppViewContainer"] {
        background-color: #ffffff !important;
        background-image: none !important;
    }
    
    [data-testid="stHeader"] {
        background-color: rgba(255, 255, 255, 0) !important;
    }
    
    /* Main Content */
    .main .block-container {
        padding-top: 2rem !important;
        max_width: 800px !important;
    }

    /* Headings */
    h1 {
        color: #1b5e20 !important; /* Dark Green */
        font-family: 'Helvetica Neue', sans-serif !important;
        font-weight: 800 !important;
        text-align: center;
        margin-bottom: 0px !important;
    }
    
    h3 {
        color: #2e7d32 !important; /* Medium Green */
        text-align: center;
        font-weight: 500 !important;
        margin-top: 0px !important;
    }

    /* Tabs Styling */
    .stTabs [data-baseweb="tab-list"] {
        justify-content: center;
        gap: 10px;
        margin-bottom: 20px;
    }

    .stTabs [data-baseweb="tab"] {
        background-color: #e8f5e9 !important; /* Light Green */
        border-radius: 20px !important;
        color: #1b5e20 !important;
        padding: 8px 16px !important;
        border: 1px solid #c8e6c9 !important;
    }

    .stTabs [aria-selected="true"] {
        background-color: #2e7d32 !important; /* Green */
        color: white !important;
        border: none !important;
    }

    /* Buttons */
    .stButton > button {
        width: 100%;
        background-color: #2e7d32 !important;
        color: white !important;
        border-radius: 12px !important;
        padding: 0.75rem !important;
        font-weight: bold !important;
        border: none !important;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1) !important;
    }
    
    .stButton > button:hover {
        background-color: #1b5e20 !important;
        box-shadow: 0 6px 8px rgba(0, 0, 0, 0.15) !important;
    }

    /* Cards/Containers */
    .element-container { 
        margin-bottom: 1rem; 
    }
    
    /* File Uploader */
    .stFileUploader {
        border: 2px dashed #4caf50;
        border-radius: 15px;
        padding: 20px;
        background-color: #f1f8f4;
    }

    /* Inputs */
    .stTextInput > div > div > input {
        border-radius: 10px !important;
        border: 1px solid #a5d6a7 !important;
    }

    /* Shop Card Style */
    .shop-card {
        background-color: #f9fbe7;
        border-left: 5px solid #8bc34a;
        padding: 15px;
        border-radius: 8px;
        margin-bottom: 15px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.05);
    }

    /* Aggressive Overrides */
    html, body, [class*="css"] {
        font-family: 'Helvetica Neue', sans-serif;
    }
    
    /* Target the main Streamlit container directly */
    .stApp {
        background-color: #ffffff !important;
        background-image: none !important;
    }
    
    /* Hide the top header decoration */
    header[data-testid="stHeader"] {
        background-color: transparent !important;
    }
    
    /* Force text colors */
    .stMarkdown, .stMarkdown p, .stMarkdown h1, .stMarkdown h2, .stMarkdown h3 {
        color: #1b5e20 !important;
    }
    </style>
""", unsafe_allow_html=True)

# Initialize Backend
if "vertex_initialized" not in st.session_state:
    if utils.init_vertex():
        st.session_state["vertex_initialized"] = True

# --- HEADER ---
st.markdown("<h1>🌾 PolyFarm AI</h1>", unsafe_allow_html=True)
st.markdown("<h3>Smart Disease Diagnosis & Supply Chain</h3>", unsafe_allow_html=True)
st.markdown("---")

# --- TABS ---
tab1, tab2, tab3 = st.tabs(["📸 Diagnose", "🏥 Shops", "🏛 Schemes"])

# --- TAB 1: DIAGNOSIS ---
with tab1:
    st.markdown("<div style='text-align: center; color: #555; margin-bottom: 10px;'>Upload a photo of your crop leaf</div>", unsafe_allow_html=True)
    
    uploaded_file = st.file_uploader("Upload Leaf", type=["jpg", "png", "jpeg"], label_visibility="collapsed")
    
    if uploaded_file:
        st.image(uploaded_file, caption="Uploaded Image", use_container_width=True)
        
        if st.button("🔍 ANALYZE DISEASE"):
            with st.spinner("Analyzing..."):
                result = utils.smart_orchestrator(uploaded_file.getvalue(), uploaded_file.type)
                
                if result["status"] == "success":
                    diagnosis = result["diagnosis"]
                    
                    st.success(f"**Detected:** {diagnosis.get('diagnosis', 'Unknown')}")
                    st.warning(f"**Severity:** {diagnosis.get('severity', 'N/A')}")
                    st.info(f"**Cure:** {diagnosis.get('cure', 'N/A')}")
                    
                    # Audio
                    if result.get("audio"):
                        st.markdown("**🔊 Listen:**")
                        st.audio(result["audio"], format="audio/mp3")
                    
                    # Save Data
                    st.session_state["last_chemical"] = diagnosis.get('chemical', '')
                    st.session_state["shops_data"] = result.get("shops", [])
                    
                    st.success("✅ switch to 'Shops' tab for medicine availability.")
                else:
                    st.error(f"Error: {result.get('message', 'Unknown error')}")

# --- TAB 2: SHOPS ---
with tab2:
    st.markdown("<div style='text-align: center; margin-bottom: 10px;'>Find medicine & supplies nearby</div>", unsafe_allow_html=True)
    
    chemical = st.session_state.get("last_chemical", "")
    search = st.text_input("Product Name", value=chemical, placeholder="e.g. Urea, Pesticide")
    
    if st.button("🗺️ FIND SHOPS"):
        if search:
            with st.spinner("Locating..."):
                shops = utils.get_shops_data(search)
                st.session_state["shops_data"] = shops
    
    if "shops_data" in st.session_state and st.session_state["shops_data"]:
        for shop in st.session_state["shops_data"]:
            st.markdown(f"""
            <div class="shop-card">
                <div style="font-weight: bold; font-size: 1.1rem; color: #33691e;">{shop.get('name', 'Shop')}</div>
                <div style="color: #558b2f;">📞 {shop.get('phone', 'N/A')}</div>
                <div style="color: #555;">📍 {shop.get('dist', 'N/A')} km</div>
            </div>
            """, unsafe_allow_html=True)

# --- TAB 3: SCHEMES ---
with tab3:
    query = st.text_input("Ask about Government Schemes", placeholder="Subsidy details...")
    if st.button("💬 ASK AI"):
        if query:
            with st.spinner("Searching..."):
                response = utils.gov_agent_response(query)
                st.info(response)

# --- VOICE ASSISTANT (Sidebar Integration) ---
with st.sidebar:
    st.markdown("---")
    st.markdown("### 🎙️ AI Voice Assistant", unsafe_allow_html=True)
    st.markdown("Click below to talk to Dr. Bio", unsafe_allow_html=True)
    
    # We place the widget here with sufficient height
    components.html("""
        <script src="https://unpkg.com/@elevenlabs/convai-widget-embed" async type="text/javascript"></script>
        <elevenlabs-convai agent-id="agent_7201kda16szbffnsemfp5nqa2j44"></elevenlabs-convai>
        <style>
            elevenlabs-convai { 
                width: 100%; 
                height: 500px;
            }
        </style>
    """, height=520)
