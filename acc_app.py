import streamlit as st
import pandas as pd

# 1. Pagina Configuratie
st.set_page_config(page_title="ACC Setup Master v9.20", layout="wide")

# THEME CSS (High-Contrast, Midnight Sidebar, Focus Borders)
st.markdown("""
    <style>
    .stApp { background-color: #000000 !important; color: #FFFFFF !important; }
    [data-testid="stSidebar"] { background-color: #0A0C10 !important; border-right: 1px solid #1E1E1E; }
    [data-testid="stSidebar"] .stSelectbox { margin-top: 52px; }
    label, p, span, h1, h2, h3, .stMarkdown, [data-testid="stWidgetLabel"] p {
        color: #FFFFFF !important; font-weight: 600 !important;
    }
    .stSelectbox div[data-baseweb="select"]:focus-within { border: 2px solid #FF4B4B !important; }
    .stButton button { background-color: #FFFFFF !important; color: #000000 !important; font-weight: bold !important; width: 100%; }
    .stDownloadButton button { background-color: #58A6FF !important; color: #000000 !important; font-weight: bold !important; width: 100%; }
    .stTextInput input { background-color: #161B22 !important; color: #FFFFFF !important; border: 1px solid #30363D !important; }
    .stTabs [data-baseweb="tab-list"] { background-color: #161B22; border-radius: 5px; }
    .stTabs [aria-selected="true"] { background-color: #FF4B4B !important; }
    .stTable, table { background-color: #000000 !important; color: #FFFFFF !important; border: 1px solid #30363D !important; }
    thead th { background-color: #161B22 !important; color: #FF4B4B !important; }
    .advice-box { padding: 15px; border-radius: 5px; background-color: #000000; margin-top: 10px; border-left: 5px solid; }
    </style>
    """, unsafe_allow_html=True)

# 2. DATABASE (v9.11-v9.19)
cars_db = {
    "Ferrari 296 GT3": {"bb": 54.2, "diff": 80, "steer": 13.0, "tips": "Focus op aero-rake."},
    "Porsche 911 GT3 R (992)": {"bb": 50.2, "diff": 120, "steer": 12.0, "tips": "Motor achterin; beheer lift-off."},
    "BMW M4 GT3": {"bb": 57.5, "diff": 40, "steer": 14.0, "tips": "Sterk over curbs."},
    "Lamborghini EVO2": {"bb": 55.2, "diff": 90, "steer": 13.0, "tips": "Veel mechanische grip."},
    "McLaren 720S EVO": {"bb": 53.2, "diff": 70, "steer": 13.0, "tips": "Aero-gevoelig platform."},
    "Mercedes AMG EVO": {"bb": 56.8, "diff": 65, "steer": 14.0, "tips": "Focus op tractie."},
    "Audi R8 EVO II": {"bb": 54.0, "diff": 110, "steer": 13.0, "tips": "Nerveus bij remmen."},
    "Aston Martin EVO": {"bb": 56.2, "diff": 55, "steer": 14.0, "tips": "Zeer stabiel platform."},
    "Ford Mustang GT3": {"bb": 57.0, "diff": 50, "steer": 14.0, "tips": "Veel koppel; beheer banden."},
    "Corvette Z06 GT3.R": {"bb": 54.8, "diff": 75, "steer": 13.0, "tips": "Goede balans."}
}

circuits_db = {
    "High Downforce": ["Spa-Francorchamps", "Zandvoort", "Kyalami", "Barcelona", "Hungaroring", "Suzuka", "Donington Park", "Oulton Park", "Misano", "Valencia", "Nürburgring"],
    "Low Downforce": ["Monza", "Paul Ricard", "Bathurst", "Silverstone", "Indianapolis", "Jeddah"],
    "Street/Bumpy": ["Zolder", "Mount Panorama", "Laguna Seca", "Imola", "Snetterton", "Watkins Glen", "Red Bull Ring", "Magny-Cours"]
}

if 'history' not in st.session_state: st.session_state['history'] = []

# 3. SELECTIE
st.title("🏎️ :red[ACC] Setup Master v9.20")
col_a, col_c = st.columns(2)
with col_a: auto = st.selectbox("🚗 Kies Auto:", list(cars_db.keys()))
with col_c: 
    all_circuits = sorted([c for sub in circuits_db.values() for c in sub])
    circuit = st.selectbox("📍 Kies Circuit:", all_circuits)

# ENGINEER LOGICA
car = cars_db[auto]
ctype = next((k for k, v in circuits_db.items() if circuit in v), "High Downforce")
if ctype == "Low Downforce":
    psi, wing, bb_mod, arb_f, arb_r, bduct = "26.2", "2", 1.5, "5", "1", "1"
    rh_f, rh_r, spl = "45", "62", "0"
elif ctype == "Street
