import streamlit as st
import pandas as pd

st.set_page_config(page_title="ACC 2024 Ultimate Master v3.9", layout="wide")

# --- DATABASE ---
circuits = {
    "High Downforce": ["Spa", "Zandvoort", "Kyalami", "Barcelona", "Hungaroring", "Suzuka", "Donington"],
    "Low Downforce": ["Monza", "Paul Ricard", "Bathurst", "Silverstone"],
    "Street/Bumpy": ["Zolder", "Mount Panorama", "Laguna Seca", "Misano", "Imola", "Valencia"]
}

cars = {
    "Ferrari 296 GT3": {"type": "Mid", "bb": 54.2, "diff": 80, "steer": 13.0, "wr_f": 160, "wr_r": 130, "tips": "Stabiel, focus op aero-rake."},
    "Porsche 911 GT3 R (992)": {"type": "Rear", "bb": 50.2, "diff": 120, "steer": 12.0, "wr_f": 190, "wr_r": 150, "tips": "Motor achterin. Pas op voor oversteer."},
    "BMW M4 GT3": {"type": "Front", "bb": 57.5, "diff": 40, "steer": 14.0, "wr_f": 150, "wr_r": 120, "tips": "Sterk over curbs."},
    "Lamborghini EVO2": {"type": "Mid", "bb": 55.2, "diff": 90, "steer": 13.0, "wr_f": 165, "wr_r": 135, "tips": "Veel rotatie."},
    "McLaren 720S EVO": {"type": "Mid", "bb": 53.2, "diff": 70, "steer": 13.0, "wr_f": 155, "wr_r": 125, "tips": "Aero gevoelig."},
    "Mercedes AMG EVO": {"type": "Front", "bb": 56.8, "diff": 65, "steer": 14.0, "wr_f": 170, "wr_r": 140, "tips": "Focus op tractie."},
    "Audi R8 EVO II": {"type": "Mid", "bb": 54.0, "diff": 110, "steer": 13.0, "wr_f": 160, "wr_r": 130, "tips": "Nerveus bij remmen."},
    "Aston Martin EVO": {"type": "Front", "bb": 56.2, "diff": 55, "steer": 14.0, "wr_f": 155, "wr_r": 125, "tips": "Stabiel platform."},
    "Ford Mustang GT3": {"type": "Front", "bb": 57.0, "diff": 50, "steer": 14.0, "wr_f": 160, "wr_r": 130, "tips": "Veel koppel."},
    "Corvette Z06 GT3.R": {"type": "Mid", "bb": 54.8, "diff": 75, "steer": 13.0, "wr_f": 160, "wr_r": 130, "tips": "Goede balans."}
}

if 'saved_setups' not in st.session_state:
    st.session_state['saved_setups'] = []

st.title("🏎️ ACC Setup Master v3.9 - Full Xbox Integration")

# --- SELECTIE ---
col_a, col_c = st.columns(2)
with col_a:
    auto = st.selectbox("🚗 Kies Auto:", list(cars.keys()))
with col_c:
    circuit = st.selectbox("📍 Kies Circuit:", [c for sub in circuits.values() for c in sub])

id = f"{auto}_{circuit}".replace(" ", "_")
car_data = cars[auto]
ctype = next((k for k, v in circuits.items() if circuit in v), "High Downforce")

# Dynamische waarden
wing_v = 10 if ctype == "High Downforce" else 3 if ctype == "Low Downforce" else 7
psi_v = "26.7" if ctype == "High Downforce" else "26.3"
f_arb_v = "4" if ctype != "Street/Bumpy" else "3"
r_arb_v = "3" if ctype != "Street/Bumpy" else "2"
d_vals = [5, 10, 8, 12] if ctype != "Street/Bumpy" else [8, 15, 6, 10]

# --- SIDEBAR DOKTER ---
st.sidebar.header("🩺 De Setup Dokter")
klacht = st.sidebar.selectbox("Wat doet de auto?", ["Perfect", "Onderstuur (Bocht in)", "Onderstuur (Bocht uit)", "Overstuur (Bocht in)", "Overstuur (Bocht uit)", "Auto stuitert over curbs", "Instabiel bij hard remmen"])

if klacht != "Perfect":
    st.sidebar.warning("**Ingenieur Advies:**")
    if "Onderstuur" in klacht:
        st.sidebar.write("- Verlaag Front Anti-roll bar\n- Verhoog Rear Ride Height\n- Verhoog Front Bumpstop Range")
    elif "Overstuur" in klacht:
        st.sidebar.write("- Verlaag Rear Anti-roll bar\n- Verhoog Rear Wing\n- Verlaag Rear Ride Height")
    elif "stuitert" in klacht:
        st.sidebar.write("- Verlaag Fast Bump (Dampers)\n- Verlaag Wheel Rate")
    elif "remmen" in klacht:
        st.sidebar.write("- Verhoog Brake Bias (naar voren)\n- Verhoog Diff Preload")

st.sidebar.divider()
st.sidebar.info(f"💡 **Pro Tip voor de {auto}:**\n{car_data['tips']}")

# --- TABS ---
tabs = st.tabs(["🛞 Tyres", "⚡ Electronics", "⛽ Fuel & Strategy", "⚙️ Mechanical Grip", "☁️ Dampers", "✈️ Aero"])

with tabs[0]: # TYRES
    c1, c2 = st.columns(2)
    with c1:
        st.write("**Front**")
        for h in ["LF", "RF"]:
            st.text_input(f"{h} PSI", psi_v, key=f"psi_{h}_{id}")
            st.text_input(f"{h} Toe", "0.06", key=f"t_{h}_{id}")
            st.text_input(f"{h} Camber", "-3.5", key=f"c_{h}_{id}")
            st.text_input(f"{h} Caster", "12.0", key=f"cs_{h}_{id}")
    with c2:
        st.write("**Rear**")
        for h in ["LR", "RR"]:
            st.text_input(f"{h} PSI", psi_v, key=f"psi_{h}_{id}")
            st.text_input(f"{h} Toe", "0.10", key=f"t_{h}_{id}")
            st.text_input(f"{h} Camber", "-3.0", key=f"c_{h}_{id}")
            st.text_input(f"{h} Caster", "0.0", key=f"cs_{h}_{id}")

with tabs[1]: # ELECTRONICS
    st.number_input("TC", 0, 12, 3, key=f"tc1_{id}")
    st.number_input("TC2", 0, 12, 2, key=f"tc2_{id}")
    st.number_input("ABS", 0, 12, 3, key=f"abs_{id}")
    st.number_input("ECU Map", 1, 5, 1, key=f"ecu_{id}")

with tabs[2]: # FUEL & STRATEGY
    st.subheader("Fuel & Pit Strategy")
    st.text_input("Fuel (Litre)", "60", key=f"fuel_{id}")
    st.text_input("Tyre Set", "1", key=f"tset_{id}")
    st.selectbox("Front Brake Pads", [1, 2, 3, 4], key=f"fbrakep_{id}")
    st.selectbox("Rear Brake Pads", [1, 2, 3, 4], key=f"rbrakep_{id}")

with tabs[3]: # MECHANICAL GRIP
    st.subheader("Mechanical Grip")
    cm1, cm2 = st.columns(2)
    with cm1:
        st.write("**Front Settings**")
        st.text_input("Front Anti-roll bar", f_arb_v, key=f"farb_{id}")
        st.text_input("Brake Bias (%)", str(car_data["bb"]), key=f"bb_{id}")
        st.text_input("Steer Ratio", str(car_data["steer"]), key=f"sr_{id}")
        for h in ["LF", "RF"]:
            st.write(f"*{h} Suspension*")
            st.text_input(f"Wheel Rate {h}", str(car_data["wr_f"]), key=f"wr_{h}_{id}")
            st.text_input(f"Bumpstop Rate {h}", "500", key=f"bsr_{h}_{id}")
            st.text_input(f"Bumpstop Range {h}", "20", key=f"bsran_{h}_{id}")
    with cm2:
        st.write("**Rear Settings**")
        st.text_input("Rear Anti-roll bar", r_arb_v, key=f"rarb_{id}")
        st.text_input("Preload Differential (Nm)", str(car_data["diff"]), key=f"diff_{id}")
        for h in ["LR", "RR"]:
            st.write(f"*{h} Suspension*")
            st.text_input(f"Wheel Rate {h}", str(car_data["wr_r"]), key=f"wr_{h}_{id}")
            st.text_input(f"Bumpstop Rate {h}", "400", key=f"bsr_{h}_{id}")
            st.text_input(f"Bumpstop Range {h}", "15", key=f"bsran_{h}_{id}")

with tabs[4]: # DAMPERS
    st.subheader("Dampers (4-Way Matrix)")
    cd1, cd2, cd3, cd4 = st.columns(4)
    for i, h in enumerate(["LF", "RF", "LR", "RR"]):
        with [cd1, cd2, cd3, cd4][i]:
            st.write(f"**{h}**")
            st.number_input(f"Bump {h}", 0, 40, d_vals[0], key=f"b_{h}_{id}")
            st.number_input(f"Fast Bump {h}", 0, 40, d_vals[1], key=f"fb_{h}_{id}")
            st.number_input(f"Rebound {h}", 0, 40, d_vals[2], key=f"r_{h}_{id}")
            st.number_input(f"Fast Rebound {h}", 0, 40, d_vals[3], key=f"fr_{h}_{id}")

with tabs[5]: # AERO
    st.subheader("Aerodynamics")
    ca1, ca2 = st.columns(2)
    with ca1:
        st.write("**Front Aero**")
        st.text_input("Ride Height Front", "48", key=f"frh_{id}")
        st.text_input("Splitter", "0", key=f"spl_{id}")
        st.text_input("Brake Ducts Front", "2", key=f"fdb_{id}")
    with ca2:
        st.write("**Rear Aero**")
        st.text_input("Ride Height Rear", "68", key=f"rrh_{id}")
        st.number_input("Rear Wing", 0, 20, wing_v, key=f"wing_{id}")
        st.text_input("Brake Ducts Rear", "2", key=f"rdb_{id}")

# --- OPSLAG & EXPORT ---
st.divider()
if st.button("💾 Sla Setup op"):
    st.session_state['saved_setups'].append({"Auto": auto, "Circuit": circuit, "PSI": psi_v, "Wing": wing_v, "BB": car_data["bb"]})
    st.success("Setup opgeslagen!")

if st.session_state['saved_setups']:
    df = pd.DataFrame(st.session_state['saved_setups'])
    st.table(df)
    csv = df.to_csv(index=False).encode('utf-8')
    st.download_button("📥 Download Database (CSV)", data=csv, file_name='acc_setups.csv', mime='text/csv')
