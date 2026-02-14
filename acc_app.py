import streamlit as st
import pandas as pd
import io

# 1. Pagina Configuratie
st.set_page_config(page_title="ACC Setup Master v9.50", layout="wide")

# Styling: EXACTE v9.40 Grayscale Stealth
st.markdown("""<style>
    .stApp { background-color: #000000 !important; color: #FFFFFF !important; }
    [data-testid="stSidebar"] { background-color: #0A0C10 !important; }
    .stTabs [aria-selected="true"] { background-color: #333333 !important; color: #FFFFFF !important; border-bottom: 2px solid #FFFFFF !important; }
    .stTabs [data-baseweb="tab"] { color: #888888 !important; }
    .stSelectbox div[data-baseweb="select"]:focus-within { border: 1px solid #FFFFFF !important; }
    input { background-color: #111111 !important; color: #FFFFFF !important; border: 1px solid #333 !important; }
    .stButton>button { border: 1px solid #444; background-color: #000; color: #fff; width: 100%; }
    .stButton>button:hover { border-color: #fff; color: #fff; }
</style>""", unsafe_allow_html=True)

# 2. CORE DATABASE
cars_db = {
    "Ferrari 296 GT3": {"bb": 54.2, "diff": 80, "steer": 13.0, "f_cam": -3.5, "r_cam": -3.0, "f_toe": 0.06, "r_toe": 0.12, "caster": 12.5},
    "Porsche 911 GT3 R (992)": {"bb": 50.2, "diff": 120, "steer": 12.0, "f_cam": -3.8, "r_cam": -3.2, "f_toe": -0.04, "r_toe": 0.20, "caster": 13.2},
    "BMW M4 GT3": {"bb": 57.5, "diff": 40, "steer": 14.0, "f_cam": -3.2, "r_cam": -2.8, "f_toe": 0.05, "r_toe": 0.10, "caster": 11.8},
    "Lamborghini EVO2": {"bb": 55.2, "diff": 90, "steer": 13.0, "f_cam": -3.6, "r_cam": -3.1, "f_toe": 0.06, "r_toe": 0.14, "caster": 12.8},
    "McLaren 720S EVO": {"bb": 53.2, "diff": 70, "steer": 13.0, "f_cam": -3.5, "r_cam": -3.0, "f_toe": 0.06, "r_toe": 0.10, "caster": 12.0},
    "Mercedes AMG EVO": {"bb": 56.8, "diff": 65, "steer": 14.0, "f_cam": -3.4, "r_cam": -2.9, "f_toe": 0.07, "r_toe": 0.12, "caster": 13.5},
    "Audi R8 EVO II": {"bb": 54.0, "diff": 110, "steer": 13.0, "f_cam": -3.7, "r_cam": -3.1, "f_toe": 0.06, "r_toe": 0.11, "caster": 12.4},
    "Aston Martin EVO": {"bb": 56.2, "diff": 55, "steer": 14.0, "f_cam": -3.3, "r_cam": -2.8, "f_toe": 0.06, "r_toe": 0.10, "caster": 12.2},
    "Ford Mustang GT3": {"bb": 57.0, "diff": 50, "steer": 14.0, "f_cam": -3.5, "r_cam": -3.0, "f_toe": 0.06, "r_toe": 0.13, "caster": 12.0},
    "Corvette Z06 GT3.R": {"bb": 54.8, "diff": 75, "steer": 13.0, "f_cam": -3.5, "r_cam": -3.0, "f_toe": 0.06, "r_toe": 0.12, "caster": 12.6}
}

circ_db = {
    "High": ["Spa-Francorchamps", "Zandvoort", "Kyalami", "Barcelona", "Hungaroring", "Suzuka", "Nürburgring", "Misano", "Valencia"],
    "Low": ["Monza", "Paul Ricard", "Bathurst", "Silverstone", "Indianapolis", "Jeddah"],
    "Bumpy": ["Zolder", "Mount Panorama", "Laguna Seca", "Imola", "Watkins Glen", "Red Bull Ring"]
}

if 'history' not in st.session_state: st.session_state['history'] = []

# 3. HELPER & EXPORT
def get_vals(a, c):
    car = cars_db[a]; ct = next((k for k, v in circ_db.items() if c in v), "High")
    if ct == "Low": p, w, bm, af, ar = "26.2", "2", 1.5, "5", "1"
    elif ct == "Bumpy": p, w, bm, af, ar = "26.6", "8", -0.5, "3", "2"
    else: p, w, bm, af, ar = "26.8", "11", 0.0, "4", "3"
    return {"Auto": a, "Circuit": c, "PSI": p, "Wing": w, "BB": car["bb"]+bm, "Steer": car["steer"], "F-Toe": car["f_toe"], "F-Cam": car["f_cam"]}

st.sidebar.header("Master Database")
if st.sidebar.button("Genereer Alle Combinaties"):
    rows = [get_vals(a, c) for c in [i for s in circ_db.values() for i in s] for a in cars_db.keys()]
    df_bulk = pd.DataFrame(rows)
    buf = io.BytesIO()
    with pd.ExcelWriter(buf, engine='xlsxwriter') as wr:
        df_bulk.to_
