import streamlit as st
import pandas as pd

st.set_page_config(page_title="ACC Ultimate Master v5.1", layout="wide")

# --- 1. DE DATABASE ---
if 'db' not in st.session_state:
    st.session_state.db = {
        "Ferrari 296 GT3": {"bb": "54.2", "diff": "80", "steer": "13.0", "wr_f": "160", "wr_r": "130"},
        "Porsche 911 GT3 R (992)": {"bb": "50.2", "diff": "120", "steer": "12.0", "wr_f": "190", "wr_r": "150"},
        "BMW M4 GT3": {"bb": "57.5", "diff": "40", "steer": "14.0", "wr_f": "150", "wr_r": "120"},
        "Lamborghini EVO2": {"bb": "55.2", "diff": "90", "steer": "13.0", "wr_f": "165", "wr_r": "135"},
        "McLaren 720S EVO": {"bb": "53.2", "diff": "70", "steer": "13.0", "wr_f": "155", "wr_r": "125"},
        "Mercedes AMG EVO": {"bb": "56.8", "diff": "65", "steer": "14.0", "wr_f": "170", "wr_r": "140"},
        "Audi R8 EVO II": {"bb": "54.0", "diff": "110", "steer": "13.0", "wr_f": "160", "wr_r": "130"},
        "Aston Martin EVO": {"bb": "56.2", "diff": "55", "steer": "14.0", "wr_f": "155", "wr_r": "125"},
        "Ford Mustang GT3": {"bb": "57.0", "diff": "50", "steer": "14.0", "wr_f": "160", "wr_r": "130"},
        "Corvette Z06 GT3.R": {"bb": "54.8", "diff": "75", "steer": "13.0", "wr_f": "160", "wr_r": "130"}
    }

circuits_db = {
    "High Downforce": ["Spa", "Zandvoort", "Kyalami", "Barcelona", "Hungaroring", "Suzuka", "Donington"],
    "Low Downforce": ["Monza", "Paul Ricard", "Bathurst", "Silverstone"],
    "Street/Bumpy": ["Zolder", "Mount Panorama", "Laguna Seca", "Misano", "Imola", "Valencia"]
}

# --- 2. DE REFRESH FUNCTIE ---
def sync_data():
    ctype = "High Downforce"
    for k, v in circuits_db.items():
        if st.session_state.sel_circuit in v:
            ctype = k
            break
    
    car = st.session_state.db[st.session_state.sel_auto]
    
    psi = "26.8" if ctype == "High Downforce" else "26.2"
    wing = 11 if ctype == "High Downforce" else 2 if ctype == "Low Downforce" else 7
    arb_f = "4" if ctype != "Street/Bumpy" else "3"
    arb_r = "3" if ctype != "Street/Bumpy" else "2"
    d = [5, 10, 8, 12] if ctype != "Street/Bumpy" else [8, 15, 6, 10]

    # Harde reset van alle session_state keys
    keys_to_update = {
        "lf_p": psi, "rf_p": psi, "lr_p": psi, "rr_p": psi,
        "wing": wing, "bb": car["bb"], "diff": car["diff"],
        "farb": arb_f, "rarb": arb_r,
        "wr_lf": car["wr_f"], "wr_rf": car["wr_f"],
        "wr_lr": car["wr_r"], "wr_rr": car["wr_r"],
        "b_lf": d[0], "fb_lf": d[1], "r_lf": d[2], "fr_lf": d[3],
        "b_rf": d[0], "fb_rf": d[1], "r_rf": d[2], "fr_rf": d[3],
        "b_lr": d[0], "fb_lr": d[1], "r_lr": d[2], "fr_lr": d[3],
        "b_rr": d[0], "fb_rr": d[1], "r_rr": d[2], "fr_rr": d[3]
    }
    for key, val in keys_to_update.items():
        st.session_state[key] = val

# Initialisatie
if "lf_p" not in st.session_state:
    st.session_state.sel_auto = "Ferrari 296 GT3"
    st.session_state.sel_circuit = "Spa"
    sync_data()

# --- 3. UI ---
st.title("🏎️ ACC Setup Master v5.1")
c1, c2 = st.columns(2)
with c1:
    st.selectbox("🚗 Kies Auto:", list(st.session_state.db.keys()), key="sel_auto", on_change=sync_data)
with c2:
    st.selectbox("📍 Kies Circuit:", [c for sub in circuits_db.values() for c in sub], key="sel_circuit", on_change=sync_data)

tabs = st.tabs(["🛞 Tyres", "⚡ Electronics", "⛽ Fuel & Strategy", "⚙️ Mechanical Grip", "☁️ Dampers", "✈️ Aero"])

with tabs[0]: # TYRES
    col1, col2 = st.columns(2)
    with col1:
        st.write("**Front**")
        st.text_input("LF PSI", key="lf_p")
        st.text_input("RF PSI", key="rf_p")
        st.text_input("LF Toe", "0.06")
        st.text_input("LF Camber", "-3.5")
        st.text_input("LF Caster", "12.0")
    with col2:
        st.write("**Rear**")
        st.text_input("LR PSI", key="lr_p")
        st.text_input("RR PSI", key="rr_p")
        st.text_input("LR Toe", "0.10")
        st.text_input("LR Camber", "-3.0")

with tabs[1]: # ELECTRONICS
    st.number_input("TC", 0, 12, 3)
    st.number_input("TC2", 0, 12, 2)
    st.number_input("ABS", 0, 12, 3)
    st.number_input("ECU Map", 1, 5, 1)

with tabs[2]: # FUEL & STRATEGY
    st.text_input("Fuel (L)", "60")
    st.text_input("Tyre Set", "1")
    st.selectbox("Front Brake Pads", [1,2,3,4], key="fpad")
    st.selectbox("Rear Brake Pads", [1,2,3,4], key="rpad")

with tabs[3]: # MECHANICAL GRIP
    m1, m2 = st.columns(2)
    with m1:
        st.write("**Front**")
        st.text_input("Brake Bias (%)", key="bb")
        st.text_input("Anti-roll bar Front", key="farb")
        st.text_input("Wheel Rate LF", key="wr_lf")
        st.text_input("Wheel Rate RF", key="wr_rf")
        st.text_input("Bumpstop Rate LF", "500")
        st.text_input("Bumpstop Range LF", "20")
    with m2:
        st.write("**Rear**")
        st.text_input("Preload Differential", key="diff")
        st.text_input("Anti-roll bar Rear", key="rarb")
        st.text_input("Wheel Rate LR", key="wr_lr")
        st.text_input("Wheel Rate RR", key="wr_rr")

with tabs[4]: # DAMPERS
    d1, d2, d3, d4 = st.columns(4)
    hoeken = ["lf", "rf", "lr", "rr"]
    for i, h in enumerate(hoeken):
        with [d1, d2, d3, d4][i]:
            st.write(f"**{h.upper()}**")
            st.number_input(f"Bump {h.upper()}", 0, 40, key=f"b_{h}")
            st.number_input(f"FBump {h.upper()}", 0, 40, key=f"fb_{h}")
            st.number_input(f"Rebound {h.upper()}", 0, 40, key=f"r_{h}")
            st.number_input(f"FRebound {h.upper()}", 0, 40, key=f"fr_{h}")

with tabs[5]: # AERO
    a1, a2 = st.columns(2)
    with a1:
        st.text_input("Ride Height Front", "48")
        st.text_input("Splitter", "0")
    with a2:
        st.text_input("Ride Height Rear", "68")
        st.number_input("Rear Wing", 0, 20, key="wing")

# --- SIDEBAR DOKTER ---
st.sidebar.header("🩺 De Setup Dokter")
klacht = st.sidebar.selectbox("Wat doet de auto?", ["Perfect", "Onderstuur", "Overstuur", "Stuitert"])
if klacht != "Perfect":
    st.sidebar.warning("Advies: Pas Aero of ARB aan.")
