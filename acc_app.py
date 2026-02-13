import streamlit as st
import pandas as pd

st.set_page_config(page_title="ACC Ultimate Master v4.1", layout="wide")

# --- DATABASE ---
circuits = {
    "High Downforce": ["Spa", "Zandvoort", "Kyalami", "Barcelona", "Hungaroring", "Suzuka", "Donington"],
    "Low Downforce": ["Monza", "Paul Ricard", "Bathurst", "Silverstone"],
    "Street/Bumpy": ["Zolder", "Mount Panorama", "Laguna Seca", "Misano", "Imola", "Valencia"]
}

cars = {
    "Ferrari 296 GT3": {"type": "Mid", "bb": 54.2, "diff": 80, "steer": 13.0, "wr_f": 160, "wr_r": 130, "tips": "Stabiel, focus op aero-rake."},
    "Porsche 911 GT3 R (992)": {"type": "Rear", "bb": 50.2, "diff": 120, "steer": 12.0, "wr_f": 190, "wr_r": 150, "tips": "Motor achterin. Pas op voor oversteer."},
    "BMW M4 GT3": {"type": "Front", "bb": 57.5, "diff": 40, "steer": 14.0, "wr_f": 150, "wr_r": 120, "tips": "Sterk over curbs door lange wielbasis."},
    "Lamborghini EVO2": {"type": "Mid", "bb": 55.2, "diff": 90, "steer": 13.0, "wr_f": 165, "wr_r": 135, "tips": "Veel rotatie, agressief op achterbanden."},
    "McLaren 720S EVO": {"type": "Mid", "bb": 53.2, "diff": 70, "steer": 13.0, "wr_f": 155, "wr_r": 125, "tips": "Aero gevoelig, rijhoogte is cruciaal."},
    "Mercedes AMG EVO": {"type": "Front", "bb": 56.8, "diff": 65, "steer": 14.0, "wr_f": 170, "wr_r": 140, "tips": "Focus op tractie en bandenbehoud."},
    "Audi R8 EVO II": {"type": "Mid", "bb": 54.0, "diff": 110, "steer": 13.0, "wr_f": 160, "wr_r": 130, "tips": "Nerveus bij hard remmen."},
    "Aston Martin EVO": {"type": "Front", "bb": 56.2, "diff": 55, "steer": 14.0, "wr_f": 155, "wr_r": 125, "tips": "Zeer voorspelbaar platform."},
    "Ford Mustang GT3": {"type": "Front", "bb": 57.0, "diff": 50, "steer": 14.0, "wr_f": 160, "wr_r": 130, "tips": "Veel koppel, focus op mechanische grip achter."},
    "Corvette Z06 GT3.R": {"type": "Mid", "bb": 54.8, "diff": 75, "steer": 13.0, "wr_f": 160, "wr_r": 130, "tips": "Goede balans topsnelheid/bochten."}
}

if 'saved_setups' not in st.session_state:
    st.session_state['saved_setups'] = []

st.title("🏎️ ACC Setup Master v4.1 - Definitive")

# --- SELECTIE ---
col_a, col_c = st.columns(2)
with col_a:
    auto = st.selectbox("🚗 Kies Auto:", list(cars.keys()))
with col_c:
    circuit = st.selectbox("📍 Kies Circuit:", [c for sub in circuits.values() for c in sub])

# FORCE REFRESH KEY
id_key = f"{auto}_{circuit}".replace(" ", "_")

car_data = cars[auto]
ctype = next((k for k, v in circuits.items() if circuit in v), "High Downforce")

# Dynamische berekende waarden
wing_v = 10 if ctype == "High Downforce" else 3 if ctype == "Low Downforce" else 7
psi_v = "26.7" if ctype == "High Downforce" else "26.3"
f_arb_v = "4" if ctype != "Street/Bumpy" else "3"
r_arb_v = "3" if ctype != "Street/Bumpy" else "2"
d_vals = [5, 10, 8, 12] if ctype != "Street/Bumpy" else [8, 15, 6, 10]

# --- SIDEBAR DOKTER ---
st.sidebar.header("🩺 De Setup Dokter")
klacht = st.sidebar.selectbox("Wat doet de auto?", ["Perfect", "Onderstuur (Bocht in)", "Onderstuur (Bocht uit)", "Overstuur (Bocht in)", "Overstuur (Bocht uit)", "Auto stuitert over curbs", "Instabiel bij hard remmen"], key=f"doc_{id_key}")
if klacht != "Perfect":
    st.sidebar.warning("**Advies:**")
    if "Onderstuur" in klacht: st.sidebar.write("- Verlaag Front ARB\n- Verhoog Rear Ride Height")
    elif "Overstuur" in klacht: st.sidebar.write("- Verlaag Rear ARB\n- Verhoog Rear Wing")
    elif "stuitert" in klacht: st.sidebar.write("- Verlaag Fast Bump\n- Verlaag Wheel Rate")
    elif "remmen" in klacht: st.sidebar.write("- Verhoog Brake Bias naar voren")

st.sidebar.divider()
st.sidebar.info(f"💡 **Tip:** {car_data['tips']}")

# --- TABS ---
tabs = st.tabs(["🛞 Tyres", "⚡ Electronics", "⛽ Fuel & Strategy", "⚙️ Mechanical Grip", "☁️ Dampers", "✈️ Aero"])

with tabs[0]: # TYRES
    c1, c2 = st.columns(2)
    with c1:
        st.write("**Front**")
        for h in ["LF", "RF"]:
            st.text_input(f"{h} PSI", psi_v, key=f"psi_{h}_{id_key}")
            st.text_input(f"{h} Toe", "0.06", key=f"t_{h}_{id_key}")
            st.text_input(f"{h} Camber", "-3.5", key=f"c_{h}_{id_key}")
            st.text_input(f"{h} Caster", "12.0", key=f"cs_{h}_{id_key}")
    with c2:
        st.write("**Rear**")
        for h in ["LR", "RR"]:
            st.text_input(f"{h} PSI", psi_v, key=f"psi_{h}_{id_key}")
            st.text_input(f"{h} Toe", "0.10", key=f"t_{h}_{id_key}")
            st.text_input(f"{h} Camber", "-3.0", key=f"c_{h}_{id_key}")
            st.text_input(f"{h} Caster", "0.0", key=f"cs_{h}_{id_key}")

with tabs[1]: # ELECTRONICS
    st.number_input("TC", 0, 12, 3, key=f"tc1_{id_key}")
    st.number_input("TC2", 0, 12, 2, key=f"tc2_{id_key}")
    st.number_input("ABS", 0, 12, 3, key=f"abs_{id_key}")
    st.number_input("ECU Map", 1, 5, 1, key=f"ecu_{id_key}")

with tabs[2]: # FUEL & STRATEGY
    st.text_input("Fuel (Litre)", "60", key=f"fuel_{id_key}")
    st.text_input("Tyre Set", "1", key=f"tset_{id_key}")
    st.selectbox("Front Brake Pads", [1, 2, 3, 4], key=f"fbp_{id_key}")
    st.selectbox("Rear Brake Pads", [1, 2, 3, 4], key=f"rbp_{id_key}")

with tabs[3]: # MECHANICAL GRIP
    cm1, cm2 = st.columns(2)
    with cm1:
        st.write("**Front**")
        st.text_input("Front Anti-roll bar", f_arb_v, key=f"faf_{id_key}")
        st.text_input("Brake Bias (%)", str(car_data["bb"]), key=f"bb_{id_key}")
        st.text_input("Steer Ratio", str(car_data["steer"]), key=f"sr_{id_key}")
        for h in ["LF", "RF"]:
            st.text_input(f"Wheel Rate {h}", str(car_data["wr_f"]), key=f"wr_{h}_{id_key}")
            st.text_input(f"Bumpstop Rate {h}", "500", key=f"bsr_{h}_{id_key}")
            st.text_input(f"Bumpstop Range {h}", "20", key=f"bsran_{h}_{id_key}")
    with cm2:
        st.write("**Rear**")
        st.text_input("Rear Anti-roll bar", r_arb_v, key=f"rar_{id_key}")
        st.text_input("Preload Differential (Nm)", str(car_data["diff"]), key=f"diff_{id_key}")
        for h in ["LR", "RR"]:
            st.text_input(f"Wheel Rate {h}", str(car_data["wr_r"]), key=f"wr_{h}_{id_key}")
            st.text_input(f"Bumpstop Rate {h}", "400", key=f"bsr_{h}_{id_key}")
            st.text_input(f"Bumpstop Range {h}", "15", key=f"bsran_{h}_{id_key}")

with tabs[4]: # DAMPERS
    cd1, cd2, cd3, cd4 = st.columns(4)
    for i, h in enumerate(["LF", "RF", "LR", "RR"]):
        with [cd1, cd2, cd3, cd4][i]:
            st.write(f"**{h}**")
            st.number_input(f"Bump {h}", 0, 40, d_vals[0], key=f"b_{h}_{id_key}")
            st.number_input(f"F-Bump {h}", 0, 40, d_vals[1], key=f"fb_{h}_{id_key}")
            st.number_input(f"Rebound {h}", 0, 40, d_vals[2], key=f"r_{h}_{id_key}")
            st.number_input(f"Fast Rebound {h}", 0, 40, d_vals[3], key=f"fr_{h}_{id_key}")

with tabs[5]: # AERO
    ca1, ca2 = st.columns(2)
    with ca1:
        st.text_input("Ride Height Front", "48", key=f"frh_{id_key}")
        st.text_input("Splitter", "0", key=f"spl_{id_key}")
        st.text_input("Brake Ducts Front", "2", key=f"fdb_{id_key}")
    with ca2:
        st.text_input("Ride Height Rear", "68", key=f"rrh_{id_key}")
        st.number_input("Rear Wing", 0, 20, wing_v, key=f"wing_{id_key}")
        st.text_input("Brake Ducts Rear", "2", key=f"rdb_{id_key}")

# --- OPSLAG ---
st.divider()
if st.button("💾 Sla Setup op"):
    st.session_state['saved_setups'].append({"Auto": auto, "Circuit": circuit, "PSI": psi_v, "Wing": wing_v, "BB": car_data["bb"]})
    st.success("Setup opgeslagen!")

if st.session_state['saved_setups']:
    df = pd.DataFrame(st.session_state['saved_setups'])
    st.table(df)
    csv = df.to_csv(index=False).encode('utf-8')
    st.download_button("📥 Download CSV", data=csv, file_name='acc_setups.csv', mime='text/csv')
