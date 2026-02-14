import streamlit as st
import pandas as pd
import io

# 1. Pagina Configuratie
st.set_page_config(page_title="ACC Setup Master v9.28", layout="wide")

# Styling Stealth
st.markdown("""<style>
.stApp { background-color: #000000 !important; color: #FFFFFF !important; }
[data-testid="stSidebar"] { background-color: #0A0C10 !important; }
[data-testid="stSidebar"] .stSelectbox { margin-top: 52px; }
.stSelectbox div[data-baseweb="select"]:focus-within { border: 2px solid #FF4B4B !important; }
.stTabs [aria-selected="true"] { background-color: #ff4b4b !important; }
.advice-box { padding: 12px; border-left: 5px solid #FF4B4B; background: #161B22; margin-bottom: 10px; }
</style>""", unsafe_allow_html=True)

# 2. DATABASE
cars_db = {
    "Ferrari 296 GT3": {"bb": 54.2, "diff": 80, "steer": 13.0, "f_cam": -3.5, "r_cam": -3.0, "tips": "Check aero-rake."},
    "Porsche 911 GT3 R (992)": {"bb": 50.2, "diff": 120, "steer": 12.0, "f_cam": -3.8, "r_cam": -3.2, "tips": "Beheer lift-off."},
    "BMW M4 GT3": {"bb": 57.5, "diff": 40, "steer": 14.0, "f_cam": -3.2, "r_cam": -2.8, "tips": "Sterk op curbs."},
    "Lamborghini EVO2": {"bb": 55.2, "diff": 90, "steer": 13.0, "f_cam": -3.6, "r_cam": -3.1, "tips": "Mech-grip."},
    "McLaren 720S EVO": {"bb": 53.2, "diff": 70, "steer": 13.0, "f_cam": -3.5, "r_cam": -3.0, "tips": "Aero-gevoelig."},
    "Mercedes AMG EVO": {"bb": 56.8, "diff": 65, "steer": 14.0, "f_cam": -3.4, "r_cam": -2.9, "tips": "Focus tractie."},
    "Audi R8 EVO II": {"bb": 54.0, "diff": 110, "steer": 13.0, "f_cam": -3.7, "r_cam": -3.1, "tips": "Nerveus remmen."},
    "Aston Martin EVO": {"bb": 56.2, "diff": 55, "steer": 14.0, "f_cam": -3.3, "r_cam": -2.8, "tips": "Zeer stabiel."},
    "Ford Mustang GT3": {"bb": 57.0, "diff": 50, "steer": 14.0, "f_cam": -3.5, "r_cam": -3.0, "tips": "Veel koppel."},
    "Corvette Z06 GT3.R": {"bb": 54.8, "diff": 75, "steer": 13.0, "f_cam": -3.5, "r_cam": -3.0, "tips": "Goede balans."}
}

circs_db = {
    "High Downforce": ["Spa-Francorchamps", "Zandvoort", "Kyalami", "Barcelona", "Hungaroring", "Suzuka", "Nürburgring"],
    "Low Downforce": ["Monza", "Paul Ricard", "Bathurst", "Silverstone"],
    "Street/Bumpy": ["Zolder", "Mount Panorama", "Laguna Seca", "Imola"]
}

if 'history' not in st.session_state: st.session_state['history'] = []

# 3. SELECTIE
st.title("🏎️ :red[ACC] Master v9.28")
col_a, col_c = st.columns(2)
with col_a: auto = st.selectbox("🚗 Auto:", list(cars_db.keys()))
with col_c: 
    clist = sorted([c for sub in circs_db.values() for c in sub])
    circuit = st.selectbox("📍 Circuit:", clist)

car = cars_db[auto]
ctype = next((k for k, v in circs_db.items() if circuit in v), "High Downforce")
if ctype == "Low Downforce":
    psi, wing, bb_m, arb_f, arb_r, damp = "26.2", "2", 1.5, "5", "1", ["4", "9", "7", "11"]
    rh_f, rh_r, spl, bduct = "45", "62", "0", "1"
elif ctype == "Street/Bumpy":
    psi, wing, bb_m, arb_f, arb_r, damp
