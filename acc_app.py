import streamlit as st
import pandas as pd

# 1. Pagina Configuratie
st.set_page_config(page_title="ACC Setup Master v9.23", layout="wide")

# THEME CSS
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

# 2. DATABASE
cars_db = {
    "Ferrari 296 GT3": {"bb": 54.2, "diff": 80, "steer": 13.0, "f_cam": -3.5, "r_cam": -3.0, "tips": "Check aero-rake."},
    "Porsche 911 GT3 R (992)": {"bb": 50.2, "diff": 120, "steer": 12.0, "f_cam": -3.8, "r_cam": -3.2, "tips": "Beheer lift-off."},
    "BMW M4 GT3": {"bb": 57.5, "diff": 40, "steer": 14.0, "f_cam": -3.2, "r_cam": -2.8, "tips": "Goed op curbs."},
    "Lamborghini EVO2": {"bb": 55.2, "diff": 90, "steer": 13.0, "f_cam": -3.6, "r_cam": -3.1, "tips": "Veel mech-grip."},
    "McLaren 720S EVO": {"bb": 53.2, "diff": 70, "steer": 13.0, "f_cam": -3.5, "r_cam": -3.0, "tips": "Aero-gevoelig."},
    "Mercedes AMG EVO": {"bb": 56.8, "diff": 65, "steer": 14.0, "f_cam": -3.4, "r_cam": -2.9, "tips": "Check tractie."},
    "Audi R8 EVO II": {"bb": 54.0, "diff": 110, "steer": 13.0, "f_cam": -3.7, "r_cam": -3.1, "tips": "Nerveus remmen."},
    "Aston Martin EVO": {"bb": 56.2, "diff": 55, "steer": 14.0, "f_cam": -3.3, "r_cam": -2.8, "tips": "Zeer stabiel."},
    "Ford Mustang GT3": {"bb": 57.0, "diff": 50, "steer": 14.0, "f_cam": -3.5, "r_cam": -3.0, "tips": "Veel koppel."},
    "Corvette Z06 GT3.R": {"bb": 54.8, "diff": 75, "steer": 13.0, "f_cam": -3.5, "r_cam": -3.0, "tips": "Goede balans."}
}

circuits_db = {
    "High Downforce": ["Spa-Francorchamps", "Zandvoort", "Kyalami", "Barcelona", "Hungaroring", "Suzuka", "Donington Park", "Oulton Park", "Misano", "Valencia", "Nürburgring"],
    "Low Downforce": ["Monza", "Paul Ricard", "Bathurst", "Silverstone", "Indianapolis", "Jeddah"],
    "Street/Bumpy": ["Zolder", "Mount Panorama", "Laguna Seca", "Imola", "Snetterton", "Watkins Glen", "Red Bull Ring", "Magny-Cours"]
}

if 'history' not in st.session_state: st.session_state['history'] = []

# 3. SELECTIE
st.title("🏎️ :red[ACC] Master v9.23")
col_a, col_c = st.columns(2)
with col_a: auto = st.selectbox("🚗 Auto:", list(cars_db.keys()))
with col_c: 
    circs = sorted([c for sub in circuits_db.values() for c in sub])
    circuit = st.selectbox("📍 Circuit:", circs)

# ENGINEER LOGICA
car = cars_db[auto]
ctype = next((k for k, v in circuits_db.items() if circuit in v), "High Downforce")
if ctype == "Low Downforce":
    psi, wing, bb_mod, arb_f, arb_r, bduct = "26.2", "2", 1.5, "5", "1", "1"
    rh_f, rh_r, spl, damp = "45", "62", "0", ["4", "9", "7", "11"]
elif ctype == "Street/Bumpy":
    psi, wing, bb_mod, arb_f, arb_r, bduct = "26.6", "8", -0.5, "3", "2", "3"
    rh_f, rh_r, spl, damp = "52", "75", "2", ["8", "15", "6", "10"]
else: # High Downforce
    psi, wing, bb_mod, arb_f, arb_r, bduct = "26.8", "11", 0.0, "4", "3", "2"
    rh_f, rh_r, spl, damp = "48", "68", "0", ["5", "10", "8", "12"]

ukey = f"v923_{auto}_{circuit}".replace(" ", "_")

# 4. SIDEBAR - DOKTER
st.sidebar.header("🩺 Dokter")
klacht = st.sidebar.selectbox("Klacht?", ["Geen", "Onderstuur (Entry)", "Onderstuur (Exit)", "Overstuur (Entry)", "Overstuur (Exit)", "Curbs"], key=f"dr_{ukey}")
if klacht != "Geen":
    adv, clr = "", "#FFFFFF"
    if "Onderstuur" in klacht: adv, clr = f"Verlaag **F-ARB** van **{arb_f}** naar **{int(arb_f)-1}**.", "#FFA500"
    elif "Overstuur" in klacht: adv, clr = f"Verlaag **R-ARB** van **{arb_r}** naar **{int(arb_r)-1}**.", "#FF4B4B"
    elif "Curbs" in klacht: adv, clr = "Verhoog **Rijhoogte** +2mm en verzacht dampers.", "#58A6FF"
    st.sidebar.markdown(f"<div class='advice-box' style='border-color: {clr}'>{adv}</div>", unsafe_allow_html=True)
st.sidebar.info(f"💡 Tip: {car['tips']}")

# 5. TABS
tabs = st.tabs(["🛞 Tyres", "⚡ Electronics", "⛽ Fuel", "⚙️ Mechanical", "☁️ Dampers", "✈️ Aero"])

with tabs[0]:
    c1, c2 = st.columns(2)
    with c1:
        st.text_input("LF PSI", psi, key=f"lf_{ukey}")
        st.text_input("F-Cam", str(car['f_cam']), key=f"fc_{ukey}")
    with c2:
        st.text_input("LR PSI", psi, key=f"lr_{ukey}")
        st.text_input("R-Cam", str(car['r_cam']), key=f"rc_{ukey}")

with tabs[1]:
    e1, e2 = st.columns(2)
    with e1:
        tc1 = st.text_input("TC1", "3", key=f"tc1_{ukey}")
        tc2 = st.text_input("TC2", "3", key=f"tc2_{ukey}")
    with e2:
        abs_v = st.text_input("ABS", "3", key=f"abs_{ukey}")
        ecu = st.text_input("ECU Map", "1", key=f"ecu_{ukey}")

with tabs[3]:
    mc1, mc2 = st.columns(2)
    with mc1:
        st.text_input("Front ARB", arb_f, key=f"farb_{ukey}")
        st.text_input("Brake Bias (%)", str(car["bb"] + bb_mod),
