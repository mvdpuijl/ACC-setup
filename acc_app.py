import streamlit as st
import pandas as pd

st.set_page_config(page_title="ACC Ultimate Master v6.2", layout="wide")

# --- 1. DE DATABASE ---
cars_db = {
    "Ferrari 296 GT3": {"bb": 54.2, "diff": 80, "steer": 13.0, "wr_f": 160, "wr_r": 130, "tips": "Focus op aero-rake."},
    "Porsche 911 GT3 R (992)": {"bb": 50.2, "diff": 120, "steer": 12.0, "wr_f": 190, "wr_r": 150, "tips": "Motor achterin, pas op bij remmen."},
    "BMW M4 GT3": {"bb": 57.5, "diff": 40, "steer": 14.0, "wr_f": 150, "wr_r": 120, "tips": "Stabiel over curbs."},
    "Lamborghini EVO2": {"bb": 55.2, "diff": 90, "steer": 13.0, "wr_f": 165, "wr_r": 135, "tips": "Veel rotatie."},
    "McLaren 720S EVO": {"bb": 53.2, "diff": 70, "steer": 13.0, "wr_f": 155, "wr_r": 125, "tips": "Gevoelig voor rijhoogte."},
    "Mercedes AMG EVO": {"bb": 56.8, "diff": 65, "steer": 14.0, "wr_f": 170, "wr_r": 140, "tips": "Sterke tractie."},
    "Audi R8 EVO II": {"bb": 54.0, "diff": 110, "steer": 13.0, "wr_f": 160, "wr_r": 130, "tips": "Nerveus platform."},
    "Aston Martin EVO": {"bb": 56.2, "diff": 55, "steer": 14.0, "wr_f": 155, "wr_r": 125, "tips": "Stabiel en voorspelbaar."},
    "Ford Mustang GT3": {"bb": 57.0, "diff": 50, "steer": 14.0, "wr_f": 160, "wr_r": 130, "tips": "Veel koppel achter."},
    "Corvette Z06 GT3.R": {"bb": 54.8, "diff": 75, "steer": 13.0, "wr_f": 160, "wr_r": 130, "tips": "Goede balans."}
}

circuits_db = {
    "High Downforce": ["Spa", "Zandvoort", "Kyalami", "Barcelona", "Hungaroring", "Suzuka", "Donington"],
    "Low Downforce": ["Monza", "Paul Ricard", "Bathurst", "Silverstone"],
    "Street/Bumpy": ["Zolder", "Mount Panorama", "Laguna Seca", "Misano", "Imola", "Valencia"]
}

# --- 2. DE FORCE-INJECT FUNCTIE ---
def reset_values():
    auto = st.session_state.sel_auto
    circuit = st.session_state.sel_circuit
    ctype = "High Downforce"
    for k, v in circuits_db.items():
        if circuit in v:
            ctype = k
            break
    car = cars_db[auto]
    psi = "26.8" if ctype == "High Downforce" else "26.2"
    wing = 11 if ctype == "High Downforce" else 2 if ctype == "Low Downforce" else 7
    arb_f = "4" if ctype != "Street/Bumpy" else "3"
    arb_r = "3" if ctype != "Street/Bumpy" else "2"
    d = [5, 10, 8, 12] if ctype != "Street/Bumpy" else [8, 15, 6, 10]

    # Injectie in Session State
    st.session_state["psi_lf"] = st.session_state["psi_rf"] = st.session_state["psi_lr"] = st.session_state["psi_rr"] = psi
    st.session_state["bb_val"] = str(car["bb"])
    st.session_state["diff_val"] = str(car["diff"])
    st.session_state["steer_val"] = str(car["steer"])
    st.session_state["wing_val"] = wing
    st.session_state["arb_f_v"] = arb_f
    st.session_state["arb_r_v"] = arb_r
    st.session_state["wr_lf_v"] = st.session_state["wr_rf_v"] = str(car["wr_f"])
    st.session_state["wr_lr_v"] = st.session_state["wr_rr_v"] = str(car["wr_r"])
    # Dampers expliciet
    st.session_state["b_lf"] = st.session_state["b_rf"] = st.session_state["b_lr"] = st.session_state["b_rr"] = d[0]
    st.session_state["fb_lf"] = st.session_state["fb_rf"] = st.session_state["fb_lr"] = st.session_state["fb_rr"] = d[1]
    st.session_state["r_lf"] = st.session_state["r_rf"] = st.session_state["r_lr"] = st.session_state["r_rr"] = d[2]
    st.session_state["fr_lf"] = st.session_state["fr_rf"] = st.session_state["fr_lr"] = st.session_state["fr_rr"] = d[3]

if "sel_auto" not in st.session_state:
    st.session_state.sel_auto = "Ferrari 296 GT3"
    st.session_state.sel_circuit = "Spa"
    reset_values()

st.title("🏎️ ACC Setup Master v6.2 - Absolute Explicit Edition")

# --- 3. SELECTIE ---
c1, c2 = st.columns(2)
with c1:
    st.selectbox("🚗 Kies Auto:", list(cars_db.keys()), key="sel_auto", on_change=reset_values)
with c2:
    st.selectbox("📍 Kies Circuit:", [c for sub in circuits_db.values() for c in sub], key="sel_circuit", on_change=reset_values)

# --- 4. DE TABS (GEEN LOOPS, ALLES VOLUIT) ---
tabs = st.tabs(["🛞 Tyres", "⚡ Electronics", "⛽ Fuel & Strategy", "⚙️ Mechanical Grip", "☁️ Dampers", "✈️ Aero"])

with tabs[0]: # TYRES
    col1, col2 = st.columns(2)
    with col1:
        st.write("**Front**")
        st.text_input("LF PSI", key="psi_lf")
        st.text_input("RF PSI", key="psi_rf")
        st.text_input("LF Toe", "0.06")
        st.text_input("RF Toe", "0.06")
        st.text_input("LF Camber", "-3.5")
        st.text_input("RF Camber", "-3.5")
        st.text_input("LF Caster", "12.0")
        st.text_input("RF Caster", "12.0")
    with col2:
        st.write("**Rear**")
        st.text_input("LR PSI", key="psi_lr")
        st.text_input("RR PSI", key="psi_rr")
        st.text_input("LR Toe", "0.10")
        st.text_input("RR Toe", "0.10")
        st.text_input("LR Camber", "-3.0")
        st.text_input("RR Camber", "-3.0")

with tabs[1]: # ELECTRONICS
    st.number_input("TC", 0, 12, 3)
    st.number_input("TC2", 0, 12, 2)
    st.number_input("ABS", 0, 12, 3)
    st.number_input("ECU Map", 1, 5, 1)

with tabs[2]: # FUEL & STRATEGY
    st.text_input("Fuel (Litre)", "60")
    st.text_input("Tyre Set", "1")
    st.selectbox("Front Brake Pads", [1, 2, 3, 4])
    st.selectbox("Rear Brake Pads", [1, 2, 3, 4])

with tabs[3]: # MECHANICAL GRIP
    m_col1, m_col2 = st.columns(2)
    with m_col1:
        st.write("**Front Settings**")
        st.text_input("Front Anti-roll bar", key="arb_f_v")
        st.text_input("Brake Bias (%)", key="bb_val")
        st.text_input("Steer Ratio", key="steer_val")
        st.text_input("Wheel Rate LF", key="wr_lf_v")
        st.text_input("Wheel Rate RF", key="wr_rf_v")
        st.text_input("Bumpstop Rate LF", "500")
        st.text_input("Bumpstop Rate RF", "500")
        st.text_input("Bumpstop Range LF", "20")
        st.text_input("Bumpstop Range RF", "20")
    with m_col2:
        st.write("**Rear Settings**")
        st.text_input("Rear Anti-roll bar", key="arb_r_v")
        st.text_input("Preload Differential", key="diff_val")
        st.text_input("Wheel Rate LR", key="wr_lr_v")
        st.text_input("Wheel Rate RR", key="wr_rr_v")
        st.text_input("Bumpstop Rate LR", "400")
        st.text_input("Bumpstop Rate RR", "400")
        st.text_input("Bumpstop Range LR", "15")
        st.text_input("Bumpstop Range RR", "15")

with tabs[4]: # DAMPERS (VOLLEDIG UITGESCHREVEN)
    d_c1, d_c2, d_c3, d_c4 = st.columns(4)
    with d_c1:
        st.write("**LEFT FRONT**")
        st.number_input("Bump LF", 0, 40, key="b_lf")
        st.number_input("Fast Bump LF", 0, 40, key="fb_lf")
        st.number_input("Rebound LF", 0, 40, key="r_lf")
        st.number_input("Fast Rebound LF", 0, 40, key="fr_lf")
    with d_c2:
        st.write("**RIGHT FRONT**")
        st.number_input("Bump RF", 0, 40, key="b_rf")
        st.number_input("Fast Bump RF", 0, 40, key="fb_rf")
        st.number_input("Rebound RF", 0, 40, key="r_rf")
        st.number_input("Fast Rebound RF", 0, 40, key="fr_rf")
    with d_c3:
        st.write("**LEFT REAR**")
        st.number_input("Bump LR", 0, 40, key="b_lr")
        st.number_input("Fast Bump LR", 0, 40, key="fb_lr")
        st.number_input("Rebound LR", 0, 40, key="r_lr")
        st.number_input("Fast Rebound LR", 0, 40, key="fr_lr")
    with d_c4:
        st.write("**RIGHT REAR**")
        st.number_input("Bump RR", 0, 40, key="b_rr")
        st.number_input("Fast Bump RR", 0, 40, key= "fb_rr")
        st.number_input("Rebound RR", 0, 40, key="r_rr")
        st.number_input("Fast Rebound RR", 0, 40, key="fr_rr")

with tabs[5]: # AERO
    a_col1, a_col2 = st.columns(2)
    with a_col1:
        st.write("**Front Aero**")
        st.text_input("Ride Height Front", "48")
        st.text_input("Splitter", "0")
        st.text_input("Brake Ducts Front", "2")
    with a_col2:
        st.write("**Rear Aero**")
        st.text_input("Ride Height Rear", "68")
        st.number_input("Rear Wing", 0, 20, key="wing_val")
        st.text_input("Brake Ducts Rear", "2")

# --- SIDEBAR DOKTER ---
st.sidebar.header("🩺 De Setup Dokter")
klacht = st.sidebar.selectbox("Wat doet de auto?", ["Perfect", "Onderstuur", "Overstuur", "Stuitert"])
if klacht != "Perfect":
    st.sidebar.warning("Advies: Wijzig ARB of Aero Wing.")
st.sidebar.info(f"💡 **Tip:** {cars_db[st.session_state.sel_auto]['tips']}")
