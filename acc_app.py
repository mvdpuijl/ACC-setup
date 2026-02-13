import streamlit as st
import pandas as pd

st.set_page_config(page_title="ACC Ultimate Master v5.0", layout="wide")

# --- 1. DE DATABASE (Hardcoded voor directe toegang) ---
cars_db = {
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

# --- 2. DE REFRESH LOGICA ---
def sync_data():
    # Bepaal circuit type
    ctype = "High Downforce"
    for k, v in circuits_db.items():
        if st.session_state.sel_circuit in v:
            ctype = k
            break
    
    # Haal auto data
    car = cars_db[st.session_state.sel_auto]
    
    # Bereken nieuwe waarden
    psi = "26.8" if ctype == "High Downforce" else "26.2"
    wing = 11 if ctype == "High Downforce" else 2 if ctype == "Low Downforce" else 7
    arb_f = "4" if ctype != "Street/Bumpy" else "3"
    arb_r = "3" if ctype != "Street/Bumpy" else "2"
    damp = [5, 10, 8, 12] if ctype != "Street/Bumpy" else [8, 15, 6, 10]

    # UPDATE SESSION STATE (Dit forceert de widgets)
    st.session_state["lf_p"] = st.session_state["rf_p"] = st.session_state["lr_p"] = st.session_state["rr_p"] = psi
    st.session_state["wing"] = wing
    st.session_state["bb"] = car["bb"]
    st.session_state["diff"] = car["diff"]
    st.session_state["farb"] = arb_f
    st.session_state["rarb"] = arb_r
    st.session_state["wr_f"] = car["wr_f"]
    st.session_state["wr_r"] = car["wr_r"]
    st.session_state["b_val"] = damp[0]
    st.session_state["fb_val"] = damp[1]
    st.session_state["r_val"] = damp[2]
    st.session_state["fr_val"] = damp[3]

# Initialisatie bij eerste keer laden
if "lf_p" not in st.session_state:
    st.session_state.sel_auto = "Ferrari 296 GT3"
    st.session_state.sel_circuit = "Spa"
    sync_data()

# --- 3. UI KEUZE ---
st.title("🏎️ ACC Setup Master v5.0")
c1, c2 = st.columns(2)
with c1:
    st.selectbox("🚗 Kies Auto:", list(cars_db.keys()), key="sel_auto", on_change=sync_data)
with c2:
    st.selectbox("📍 Kies Circuit:", [c for sub in circuits_db.values() for c in sub], key="sel_circuit", on_change=sync_data)

# --- 4. TABS (VOLLEDIG UITGESCHREVEN) ---
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
    st.selectbox("Front Brake Pads", [1,2,3,4])
    st.selectbox("Rear Brake Pads", [1,2,3,4])

with tabs[3]: # MECHANICAL GRIP
    m1, m2 = st.columns(2)
    with m1:
        st.write("**Front**")
        st.text_input("Brake Bias (%)", key="bb")
        st.text_input("Anti-roll bar Front", key="farb")
        st.text_input("Wheel Rate LF", key="wr_f")
        st.text_input("Bumpstop Rate LF", "500")
        st.text_input("Bumpstop Range LF", "20")
    with m2:
        st.write("**Rear**")
        st.text_input("Preload Differential", key="diff")
        st.text_input("Anti-roll bar Rear", key="rarb")
        st.text_input("Wheel Rate LR", key="wr_r")
        st.text_input("Bumpstop Rate LR", "400")
        st.text_input("Bumpstop Range LR", "15")

with tabs[4]: # DAMPERS
    st.subheader("Damper Matrix")
    d1, d2, d3, d4 = st.columns(4)
    for i, h in enumerate(["LF", "RF", "LR", "RR"]):
        with [d1, d2, d3, d4][i]:
            st.write(f"**{h}**")
            st.number_input(f"B {h}", 0, 40, key="b_val")
            st.number_input(f"FB {h}", 0, 40, key="fb_val")
            st.number_input(f"R {h}", 0, 40, key="r_val")
            st.number_input(f"FR {h}", 0, 40, key="fr_val")

with tabs[5]: # AERO
    a1, a2 = st.columns(2)
    with a1:
        st.text_input("Ride Height Front", "48")
        st.text_input("Splitter", "0")
        st.text_input("Brake Ducts Front", "2")
    with a2:
        st.text_input("Ride Height Rear", "68")
        st.number_input("Rear Wing", 0, 20, key="wing")
        st.text_input("Brake Ducts Rear", "2")

# --- 5. SIDEBAR DOKTER ---
st.sidebar.header("🩺 De Setup Dokter")
klacht = st.sidebar.selectbox("Wat doet de auto?", ["Perfect", "Onderstuur", "Overstuur", "Stuitert"])
if klacht != "Perfect":
    st.sidebar.warning("Ingenieur advies: Pas Aero of ARB aan.")
