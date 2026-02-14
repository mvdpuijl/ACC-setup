import streamlit as st
import pandas as pd

# 1. Pagina Configuratie
st.set_page_config(page_title="ACC Setup Master v9.33", layout="wide")

# Styling v9.14 (Stealth)
st.markdown("""<style>.stTabs [data-baseweb="tab-list"] { gap: 8px; }
.stTabs [aria-selected="true"] { background-color: #ff4b4b !important; color: white !important; }</style>""", unsafe_allow_html=True)

# 2. DATABASE
cars_db = {
    "Ferrari 296 GT3": {"bb": 54.2, "diff": 80, "steer": 13.0, "f_cam": -3.5, "r_cam": -3.0, "tips": "Aero-rake focus."},
    "Porsche 911 GT3 R (992)": {"bb": 50.2, "diff": 120, "steer": 12.0, "f_cam": -3.8, "r_cam": -3.2, "tips": "Beheer lift-off."},
    "BMW M4 GT3": {"bb": 57.5, "diff": 40, "steer": 14.0, "f_cam": -3.2, "r_cam": -2.8, "tips": "Sterk op curbs."},
    "Lamborghini EVO2": {"bb": 55.2, "diff": 90, "steer": 13.0, "f_cam": -3.6, "r_cam": -3.1, "tips": "Mech-grip."},
    "McLaren 720S EVO": {"bb": 53.2, "diff": 70, "steer": 13.0, "f_cam": -3.5, "r_cam": -3.0, "tips": "Aero-gevoelig."},
    "Mercedes AMG EVO": {"bb": 56.8, "diff": 65, "steer": 14.0, "f_cam": -3.4, "r_cam": -2.9, "tips": "Focus op tractie."},
    "Audi R8 EVO II": {"bb": 54.0, "diff": 110, "steer": 13.0, "f_cam": -3.7, "r_cam": -3.1, "tips": "Nerveus remmen."},
    "Aston Martin EVO": {"bb": 56.2, "diff": 55, "steer": 14.0, "f_cam": -3.3, "r_cam": -2.8, "tips": "Stabiel."},
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
st.title("🏎️ :red[ACC] Master v9.33")
col_a, col_c = st.columns(2)
with col_a: auto = st.selectbox("🚗 Auto:", list(cars_db.keys()))
with col_c: 
    cl = sorted([c for sub in circs_db.values() for c in sub])
    circuit = st.selectbox("📍 Circuit:", cl)

car = cars_db[auto]
ctype = next((k for k, v in circs_db.items() if circuit in v), "High Downforce")
if ctype == "Low Downforce":
    psi, wing, bb_m, arb_f, arb_r, damp = "26.2", "2", 1.5, "5", "1", ["4", "9", "7", "11"]
    rh_f, rh_r, spl, bduct = "45", "62", "0", "1"
elif ctype == "Street/Bumpy":
    psi, wing, bb_m, arb_f, arb_r, damp = "26.6", "8", -0.5, "3", "2", ["8", "15", "6", "10"]
    rh_f, rh_r, spl, bduct = "52", "75", "2", "3"
else:
    psi, wing, bb_m, arb_f, arb_r, damp = "26.8", "11", 0.0, "4", "3", ["5", "10", "8", "12"]
    rh_f, rh_r, spl, bduct = "48", "68", "0", "2"

uk = f"v33_{auto}_{circuit}".replace(" ", "")

# 4. SIDEBAR - SETUP DOKTER (Compacte logica tegen afbreken)
st.sidebar.header("🩺 Dokter")
kl = st.sidebar.selectbox("Klacht?", ["Geen", "Onderstuur", "Overstuur", "Curbs"], key=f"dr_{uk}")
if kl != "Geen":
    if kl == "Onderstuur": st.sidebar.warning(f"F-ARB naar {int(arb_f)-1}")
    elif kl == "Overstuur": st.sidebar.warning(f"R-ARB naar {int(arb_r)-1}")
    elif kl == "Curbs": st.sidebar.warning("RH +2mm")
st.sidebar.info(f"💡 Tip: {car['tips']}")

# 5. TABS
tabs = st.tabs(["🛞 Tyres", "⚡ Electronics", "⛽ Fuel", "⚙️ Mechanical", "☁️ Dampers", "✈️ Aero"])

with tabs[1]: # Electronics
    e1, e2 = st.columns(2)
    with e1:
        tc1 = st.text_input("TC1", "3", key=f"t1_{uk}")
        tc2 = st.text_input("TC2", "3", key=f"t2_{uk}")
    with e2:
        abs_v = st.text_input("ABS", "3", key=f"ab_{uk}")
        ecu = st.text_input("ECU", "1", key=f"ec_{uk}")

with tabs[4]: # Dampers
    d1, d2, d3, d4 = st.columns(4)
    cols, lbls = [d1, d2, d3, d4], ["LF", "RF", "LR", "RR"]
    for i in range(4):
        with cols[i]:
            st.write(f"**{lbls[i]}**")
            st.text_input("Bump", damp[0], key=f"b{lbls[i]}_{uk}")
            st.text_input("F-B", damp[1], key=f"f{lbls[i]}_{uk}")
            st.text_input("Reb", damp[2], key=f"r{lbls[i]}_{uk}")
            st.text_input("F-R", damp
