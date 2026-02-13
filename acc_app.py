import streamlit as st
import pandas as pd

# 1. Pagina Configuratie
st.set_page_config(page_title="ACC Ultimate Master v4.6", layout="wide")

# 2. De Volledige Database
circuits = {
    "High Downforce": ["Spa", "Zandvoort", "Kyalami", "Barcelona", "Hungaroring", "Suzuka", "Donington"],
    "Low Downforce": ["Monza", "Paul Ricard", "Bathurst", "Silverstone"],
    "Street/Bumpy": ["Zolder", "Mount Panorama", "Laguna Seca", "Misano", "Imola", "Valencia"]
}

cars = {
    "Ferrari 296 GT3": {"bb": 54.2, "diff": 80, "steer": 13.0, "wr_f": 160, "wr_r": 130, "tips": "Focus op aero-rake."},
    "Porsche 911 GT3 R (992)": {"bb": 50.2, "diff": 120, "steer": 12.0, "wr_f": 190, "wr_r": 150, "tips": "Motor achterin, pas op bij remmen."},
    "BMW M4 GT3": {"bb": 57.5, "diff": 40, "steer": 14.0, "wr_f": 150, "wr_r": 120, "tips": "Stabiel over curbs."},
    "Lamborghini EVO2": {"bb": 55.2, "diff": 90, "steer": 13.0, "wr_f": 165, "wr_r": 135, "tips": "Veel rotatie."},
    "McLaren 720S EVO": {"bb": 53.2, "diff": 70, "steer": 13.0, "wr_f": 155, "wr_r": 125, "tips": "Gevoelig voor rijhoogte."},
    "Mercedes AMG EVO": {"bb": 56.8, "diff": 65, "steer": 14.0, "wr_f": 170, "wr_r": 140, "tips": "Sterke tractie."},
    "Audi R8 EVO II": {"bb": 54.0, "diff": 110, "steer": 13.0, "wr_f": 160, "wr_r": 130, "tips": "Nerveus platform."},
    "Aston Martin EVO": {"bb": 56.2, "diff": 55, "steer": 14.0, "wr_f": 155, "wr_r": 125, "tips": "Stabiel en voorspelbaar."},
    "Ford Mustang GT3": {"bb": 57.0, "diff": 50, "steer": 14.0, "wr_f": 160, "wr_r": 130, "tips": "Veel koppel achter."},
    "Corvette Z06 GT3.R": {"bb": 54.8, "diff": 75, "steer": 13.0, "wr_f": 160, "wr_r": 130, "tips": "Goede allrounder."}
}

if 'saved_setups' not in st.session_state:
    st.session_state['saved_setups'] = []

# --- SELECTIE ---
st.title("🏎️ ACC Setup Master v4.6")

c1, c2 = st.columns(2)
with c1:
    auto = st.selectbox("🚗 Kies Auto:", list(cars.keys()))
with c2:
    circuit = st.selectbox("📍 Kies Circuit:", [c for sub in circuits.values() for c in sub])

# DIT IS DE MOTOR: De unieke ID voor elk veld
id = f"{auto}_{circuit}".replace(" ", "_")

# BEREKENINGEN OP BASIS VAN KEUZE
car_data = cars[auto]
ctype = next((k for k, v in circuits.items() if circuit in v), "High Downforce")

# Dynamische waarden die MOETEN veranderen per circuit
psi_v = "26.8" if ctype == "High Downforce" else "26.2"
wing_v = 11 if ctype == "High Downforce" else 2 if ctype == "Low Downforce" else 7
f_arb_v = "4" if ctype != "Street/Bumpy" else "3"
r_arb_v = "3" if ctype != "Street/Bumpy" else "2"
d_vals = [5, 10, 8, 12] if ctype != "Street/Bumpy" else [8, 15, 6, 10]

# --- SIDEBAR DOKTER ---
st.sidebar.header("🩺 De Setup Dokter")
klacht = st.sidebar.selectbox("Wat doet de auto?", ["Perfect", "Onderstuur (Entry)", "Overstuur (Exit)", "Auto stuitert"], key=f"dr_{id}")
if klacht != "Perfect":
    st.sidebar.warning("**Ingenieur Advies:**")
    if "Onderstuur" in klacht: st.sidebar.write("- Verlaag Front ARB\n- Verhoog Rear Ride Height")
    elif "Overstuur" in klacht: st.sidebar.write("- Verlaag Rear ARB\n- Verhoog Rear Wing")
st.sidebar.info(f"💡 **Tip voor {auto}:**\n{car_data['tips']}")

# --- TABS (VOLLEDIG UITGESCHREVEN) ---
tabs = st.tabs(["🛞 Tyres", "⚡ Electronics", "⛽ Fuel & Strategy", "⚙️ Mechanical Grip", "☁️ Dampers", "✈️ Aero"])

with tabs[0]: # TYRES
    tc1, tc2 = st.columns(2)
    with tc1:
        st.write("**Front**")
        st.text_input("LF PSI", psi_v, key=f"lf_p_{id}"); st.text_input("RF PSI", psi_v, key=f"rf_p_{id}")
        st.text_input("LF Toe", "0.06", key=f"lf_t_{id}"); st.text_input("RF Toe", "0.06", key=f"rf_t_{id}")
        st.text_input("LF Camber", "-3.5", key=f"lf_c_{id}"); st.text_input("RF Camber", "-3.5", key=f"rf_c_{id}")
        st.text_input("LF Caster", "12.0", key=f"lf_ca_{id}"); st.text_input("RF Caster", "12.0", key=f"rf_ca_{id}")
    with tc2:
        st.write("**Rear**")
        st.text_input("LR PSI", psi_v, key=f"lr_p_{id}"); st.text_input("RR PSI", psi_v, key=f"rr_p_{id}")
        st.text_input("LR Toe", "0.10", key=f"lr_t_{id}"); st.text_input("RR Toe", "0.10", key=f"rr_t_{id}")
        st.text_input("LR Camber", "-3.0", key=f"lr_c_{id}"); st.text_input("RR Camber", "-3.0", key=f"rr_c_{id}")

with tabs[1]: # ELECTRONICS
    st.subheader("Electronics")
    st.number_input("TC", 0, 12, 3, key=f"tc1_{id}")
    st.number_input("TC2", 0, 12, 2, key=f"tc2_{id}")
    st.number_input("ABS", 0, 12, 3, key=f"abs_{id}")
    st.number_input("ECU Map", 1, 5, 1, key=f"ecu_{id}")

with tabs[2]: # STRATEGY
    st.subheader("Fuel & Strategy")
    st.text_input("Fuel (Litre)", "60", key=f"fuel_{id}")
    st.text_input("Tyre Set", "1", key=f"tset_{id}")
    st.selectbox("Front Brake Pads", [1, 2, 3, 4], key=f"fbp_{id}")
    st.selectbox("Rear Brake Pads", [1, 2, 3, 4], key=f"rbp_{id}")

with tabs[3]: # MECHANICAL
    m1, m2 = st.columns(2)
    with m1:
        st.write("**Front Settings**")
        st.text_input("Front Anti-roll bar", f_arb_v, key=f"farb_{id}")
        st.text_input("Brake Bias (%)", str(car_data["bb"]), key=f"bb_{id}")
        st.text_input("Steer Ratio", str(car_data["steer"]), key=f"sr_{id}")
        st.write("*Left Front*")
        st.text_input("Wheel Rate LF", str(car_data["wr_f"]), key=f"wlf_{id}")
        st.text_input("Bumpstop Rate LF", "500", key=f"bslf_{id}")
        st.text_input("Bumpstop Range LF", "20", key=f"brlf_{id}")
        st.write("*Right Front*")
        st.text_input("Wheel Rate RF", str(car_data["wr_f"]), key=f"wrf_{id}")
        st.text_input("Bumpstop Rate RF", "500", key=f"bsrf_{id}")
        st.text_input("Bumpstop Range RF", "20", key=f"brrf_{id}")
    with m2:
        st.write("**Rear Settings**")
        st.text_input("Rear Anti-roll bar", r_arb_v, key=f"rarb_{id}")
        st.text_input("Preload Differential", str(car_data["diff"]), key=f"diff_{id}")
        st.write("*Left Rear*")
        st.text_input("Wheel Rate LR", str(car_data["wr_r"]), key=f"wlr_{id}")
        st.text_input("Bumpstop Rate LR", "400", key=f"bslr_{id}")
        st.text_input("Bumpstop Range LR", "15", key=f"brlr_{id}")
        st.write("*Right Rear*")
        st.text_input("Wheel Rate RR", str(car_data["wr_r"]), key=f"wrr_{id}")
        st.text_input("Bumpstop Rate RR", "400", key=f"bsrr_{id}")
        st.text_input("Bumpstop Range RR", "15", key=f"brrr_{id}")

with tabs[4]: # DAMPERS
    d1, d2, d3, d4 = st.columns(4)
    for i, h in enumerate(["LF", "RF", "LR", "RR"]):
        with [d1, d2, d3, d4][i]:
            st.write(f"**{h}**")
            st.number_input(f"Bump {h}", 0, 40, d_vals[0], key=f"b_{h}_{id}")
            st.number_input(f"FBump {h}", 0, 40, d_vals[1], key=f"fb_{h}_{id}")
            st.number_input(f"Rebound {h}", 0, 40, d_vals[2], key=f"r_{h}_{id}")
            st.number_input(f"FRebound {h}", 0, 40, d_vals[3], key=f"fr_{h}_{id}")

with tabs[5]: # AERO
    a1, a2 = st.columns(2)
    with a1:
        st.write("**Front Aero**")
        st.text_input("Ride Height Front", "48", key=f"frh_{id}")
        st.text_input("Splitter", "0", key=f"spl_{id}")
        st.text_input("Brake Ducts Front", "2", key=f"fdb_{id}")
    with ca2:
        st.write("**Rear Aero**")
        st.text_input("Ride Height Rear", "68", key=f"rrh_{id}")
        st.number_input("Rear Wing", 0, 20, wing_v, key=f"wing_{id}")
        st.text_input("Brake Ducts Rear", "2", key=f"rdb_{id}")

# --- OPSLAG ---
st.divider()
if st.button("💾 Sla Setup op"):
    st.success("Toegevoegd aan overzicht!")
