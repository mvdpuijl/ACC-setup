import streamlit as st
import pandas as pd

# 1. Pagina Configuratie
st.set_page_config(page_title="ACC Setup Master v9.25", layout="wide")

# Styling v9.14
st.markdown("""<style>.stTabs [data-baseweb="tab-list"] { gap: 8px; }
.stTabs [aria-selected="true"] { background-color: #ff4b4b !important; color: white !important; }</style>""", unsafe_allow_html=True)

# 2. DATABASE (v9.14)
cars_db = {
    "Ferrari 296 GT3": {"bb": 54.2, "diff": 80, "steer": 13.0, "f_cam": -3.5, "r_cam": -3.0, "f_toe": 0.06, "r_toe": 0.12, "caster": 12.5, "tips": "Aero-rake focus."},
    "Porsche 911 GT3 R (992)": {"bb": 50.2, "diff": 120, "steer": 12.0, "f_cam": -3.8, "r_cam": -3.2, "f_toe": -0.04, "r_toe": 0.20, "caster": 13.2, "tips": "Beheer lift-off."},
    "BMW M4 GT3": {"bb": 57.5, "diff": 40, "steer": 14.0, "f_cam": -3.2, "r_cam": -2.8, "f_toe": 0.05, "r_toe": 0.10, "caster": 11.8, "tips": "Sterk op curbs."},
    "Lamborghini EVO2": {"bb": 55.2, "diff": 90, "steer": 13.0, "f_cam": -3.6, "r_cam": -3.1, "f_toe": 0.06, "r_toe": 0.14, "caster": 12.8, "tips": "Mech-grip."},
    "McLaren 720S EVO": {"bb": 53.2, "diff": 70, "steer": 13.0, "f_cam": -3.5, "r_cam": -3.0, "f_toe": 0.06, "r_toe": 0.10, "caster": 12.0, "tips": "Aero-gevoelig."},
    "Mercedes AMG EVO": {"bb": 56.8, "diff": 65, "steer": 14.0, "f_cam": -3.4, "r_cam": -2.9, "f_toe": 0.07, "r_toe": 0.12, "caster": 13.5, "tips": "Focus op tractie."},
    "Audi R8 EVO II": {"bb": 54.0, "diff": 110, "steer": 13.0, "f_cam": -3.7, "r_cam": -3.1, "f_toe": 0.06, "r_toe": 0.11, "caster": 12.4, "tips": "Nerveus remmen."},
    "Aston Martin EVO": {"bb": 56.2, "diff": 55, "steer": 14.0, "f_cam": -3.3, "r_cam": -2.8, "f_toe": 0.06, "r_toe": 0.10, "caster": 12.2, "tips": "Zeer stabiel."},
    "Ford Mustang GT3": {"bb": 57.0, "diff": 50, "steer": 14.0, "f_cam": -3.5, "r_cam": -3.0, "f_toe": 0.06, "r_toe": 0.13, "caster": 12.0, "tips": "Veel koppel."},
    "Corvette Z06 GT3.R": {"bb": 54.8, "diff": 75, "steer": 13.0, "f_cam": -3.5, "r_cam": -3.0, "f_toe": 0.06, "r_toe": 0.12, "caster": 12.6, "tips": "Goede balans."}
}

circuits_db = {
    "High Downforce": ["Spa-Francorchamps", "Zandvoort", "Kyalami", "Barcelona", "Hungaroring", "Suzuka", "Donington Park", "Oulton Park", "Misano", "Valencia", "Nürburgring"],
    "Low Downforce": ["Monza", "Paul Ricard", "Bathurst", "Silverstone", "Indianapolis", "Jeddah"],
    "Street/Bumpy": ["Zolder", "Mount Panorama", "Laguna Seca", "Imola", "Snetterton", "Watkins Glen", "Red Bull Ring", "Magny-Cours"]
}

if 'history' not in st.session_state: st.session_state['history'] = []

# 3. SELECTIE
st.title("🏎️ :red[ACC] Master v9.25")
col_a, col_c = st.columns(2)
with col_a: auto = st.selectbox("🚗 Auto:", list(cars_db.keys()))
with col_c: 
    clist = sorted([c for sub in circuits_db.values() for c in sub])
    circuit = st.selectbox("📍 Circuit:", clist)

# ENGINEER LOGICA
car = cars_db[auto]
ctype = next((k for k, v in circuits_db.items() if circuit in v), "High Downforce")
if ctype == "Low Downforce":
    psi, wing, bb_mod, arb_f, arb_r, damp = "26.2", "2", 1.5, "5", "1", ["4", "9", "7", "11"]
    rh_f, rh_r, spl, bduct = "45", "62", "0", "1"
elif ctype == "Street/Bumpy":
    psi, wing, bb_mod, arb_f, arb_r, damp = "26.6", "8", -0.5, "3", "2", ["8", "15", "6", "10"]
    rh_f, rh_r, spl, bduct = "52", "75", "2", "3"
else: # High Downforce
    psi, wing, bb_mod, arb_f, arb_r, damp = "26.8", "11", 0.0, "4", "3", ["5", "10", "8", "12"]
    rh_f, rh_r, spl, bduct = "48", "68", "0", "2"

ukey = f"v925_{auto}_{circuit}".replace(" ", "_")

# 4. SIDEBAR
st.sidebar.header("🩺 Dokter")
klacht = st.sidebar.selectbox("Klacht?", ["Geen", "Onderstuur", "Overstuur"], key=f"dr_{ukey}")
st.sidebar.info(f"💡 Tip: {car['tips']}")

# 5. TABS
tabs = st.tabs(["🛞 Tyres", "⚡ Electronics", "⛽ Fuel", "⚙️ Mechanical", "☁️ Dampers", "✈️ Aero"])

with tabs[0]: # TYRES
    c1, c2 = st.columns(2)
    with c1:
        st.text_input("LF PSI", psi, key=f"lf_{ukey}")
        st.text_input("RF PSI", psi, key=f"rf_{ukey}")
        st.text_input("F-Camber", str(car["f_cam"]), key=f"fc_{ukey}")
    with c2:
        st.text_input("LR PSI", psi, key=f"lr_{ukey}")
        st.text_input("RR PSI", psi, key=f"rr_{ukey}")
        st.text_input("R-Camber", str(car["r_cam"]), key=f"rc_{ukey}")

with tabs[1]: # ELECTRONICS (TC2 & ECU Map toegevoegd)
    e1, e2 = st.columns(2)
    with e1:
        tc1 = st.text_input("TC1", "3", key=f"tc1_{ukey}")
        tc2 = st.text_input("TC2", "3", key=f"tc2_{ukey}")
    with e2:
        abs_v = st.text_input("ABS", "3", key=f"abs_{ukey}")
        ecu = st.text_input("ECU Map", "1", key=f"ecu_{ukey}")

with tabs[2]: # FUEL
    st.text_input("Fuel", "62", key=f"f_{ukey}")
    st.text_input("Brake Duct Front", bduct, key=f"bdf_{ukey}")
    st.text_input("Brake Duct Rear", bduct, key=f"bdr_{ukey}")

with tabs[3]: # MECHANICAL
    m1, m2 = st.columns(2)
    with m1:
        st.text_input("Front ARB", arb_f, key=f"fa_{ukey}")
        st.text_input("Brake Bias", str(car["bb"] + bb_mod), key=f"bb_{ukey}")
    with m2:
        st.text_input("Rear ARB", arb_r, key=f"ra_{ukey}")
        st.text_input("Steer Ratio", str(car["steer"]), key=f"st_{ukey}")

with tabs[4]: # DAMPERS
    d1, d2 = st.columns(2)
    with d1:
        st.text_input("Bump LF", damp[0], key=f"blf_{ukey}")
        st.text_input("Fast Bump LF", damp[1], key=f"fblf_{ukey}")
    with d2:
        st.text_input("Rebound LR", damp[2], key=f"rlr_{ukey}")
        st.text_input("Fast Rebound LR", damp[3], key=f"frlr_{ukey}")

with tabs[5]: # AERO
    a1, a2 = st.columns(2)
    with a1:
        st.text_input("RH Front", rh_f, key=f"rhf_{ukey}")
        st.text_input("Splitter", spl, key=f"spl_{ukey}")
    with a2:
        st.text_input("RH Rear", rh_r, key=f"rhr_{ukey}")
        st.text_input("Wing", wing, key=f"w_{ukey}")

# 6. OPSLAG
st.divider()
if st.button("💾 Sla Setup op"):
    st.session_state['history'].append({"Auto": auto, "Circ": circuit, "TC1": tc1, "TC2": tc2, "ECU": ecu, "Wing": wing})
    st.success("Setup opgeslagen!")

if st.session_state['history']:
    df = pd.DataFrame(st.session_state['history'])
    st.download_button("📥 Download CSV", data=df.to_csv(index=False).encode('utf-8'), file_name='acc.csv')
    st.table(df)
