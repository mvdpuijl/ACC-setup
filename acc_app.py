import streamlit as st
import pandas as pd

st.set_page_config(page_title="ACC 2024 Ultimate Master v3.5", layout="wide")

# --- DATABASE LOGICA ---
circuits = {
    "High Downforce": ["Spa", "Zandvoort", "Kyalami", "Barcelona", "Hungaroring", "Suzuka", "Donington"],
    "Low Downforce": ["Monza", "Paul Ricard", "Bathurst", "Silverstone"],
    "Street/Bumpy": ["Zolder", "Mount Panorama", "Laguna Seca", "Misano", "Imola", "Valencia"]
}

cars = {
    "Ferrari 296 GT3": {"type": "Mid", "bb": 54.2, "diff": 80, "steer": 13.0, "wr": 160, "tips": "Stabiel, focus op aero-rake."},
    "Porsche 911 GT3 R (992)": {"type": "Rear", "bb": 50.2, "diff": 120, "steer": 12.0, "wr": 190, "tips": "Motor achterin. Pas op voor lift-off oversteer."},
    "BMW M4 GT3": {"type": "Front", "bb": 57.5, "diff": 40, "steer": 14.0, "wr": 150, "tips": "Vergevingsgezind over curbs door lange wielbasis."},
    "Lamborghini EVO2": {"type": "Mid", "bb": 55.2, "diff": 90, "steer": 13.0, "wr": 165, "tips": "Goede rotatie, agressief op achterbanden."},
    "McLaren 720S EVO": {"type": "Mid", "bb": 53.2, "diff": 70, "steer": 13.0, "wr": 155, "tips": "Gevoelig voor splitter-hoogte."},
    "Mercedes AMG EVO": {"type": "Front", "bb": 56.8, "diff": 65, "steer": 14.0, "wr": 170, "tips": "Focus op tractie en bandenbehoud."},
    "Audi R8 EVO II": {"type": "Mid", "bb": 54.0, "diff": 110, "steer": 13.0, "wr": 160, "tips": "Snelle rotatie, nerveus bij hard remmen."},
    "Aston Martin EVO": {"type": "Front", "bb": 56.2, "diff": 55, "steer": 14.0, "wr": 155, "tips": "Stabiel platform."},
    "Ford Mustang GT3": {"type": "Front", "bb": 57.0, "diff": 50, "steer": 14.0, "wr": 160, "tips": "Veel koppel, nieuw platform."},
    "Corvette Z06 GT3.R": {"type": "Mid", "bb": 54.8, "diff": 75, "steer": 13.0, "wr": 160, "tips": "Balans tussen topsnelheid en bochten."}
}

if 'saved_setups' not in st.session_state:
    st.session_state['saved_setups'] = []

st.title("🏎️ ACC Setup Master v3.5 - Dynamic Specs")

# --- SELECTIE ---
col_a, col_c = st.columns(2)
with col_a:
    auto = st.selectbox("🚗 Selecteer Auto:", list(cars.keys()))
with col_c:
    circuit = st.selectbox("📍 Selecteer Circuit:", [c for sub in circuits.values() for c in sub])

# --- DYNAMISCHE REFRESH IDENTIFIER ---
# Deze 'id' zorgt ervoor dat Streamlit alle velden vernieuwt bij een nieuwe keuze
id = f"{auto}_{circuit}"

# --- LOGICA: BEREKEN DYNAMISCHE WAARDEN ---
car_data = cars[auto]
ctype = next((k for k, v in circuits.items() if circuit in v), "High Downforce")

wing_val = 10 if ctype == "High Downforce" else 3 if ctype == "Low Downforce" else 7
psi_val = "26.7" if ctype == "High Downforce" else "26.3"
f_arb_val = "4" if ctype != "Street/Bumpy" else "3"
r_arb_val = "3" if ctype != "Street/Bumpy" else "2"
frh_val = "48" if ctype != "Low Downforce" else "45"
rrh_val = "68" if ctype != "Low Downforce" else "60"
wr_f_val = str(car_data["wr"])
wr_r_val = str(int(car_data["wr"] * 0.85))
d_vals = [5, 10, 8, 12] if ctype != "Street/Bumpy" else [8, 15, 6, 10]

# --- SIDEBAR DOKTER ---
st.sidebar.header("🩺 De Setup Dokter")
st.sidebar.info(f"💡 **Tip voor de {auto}:**\n{car_data['tips']}")

# --- TABS ---
tabs = st.tabs(["🛞 Tyres", "⚡ Electronics", "⚙️ Mechanical Grip", "☁️ Dampers", "✈️ Aero"])

with tabs[0]: # TYRES
    c1, c2 = st.columns(2)
    with c1:
        psi_lf = st.text_input("LF PSI", psi_val, key=f"psi_lf_{id}")
        psi_rf = st.text_input("RF PSI", psi_val, key=f"psi_rf_{id}")
    with c2:
        psi_lr = st.text_input("LR PSI", psi_val, key=f"psi_lr_{id}")
        psi_rr = st.text_input("RR PSI", psi_val, key=f"psi_rr_{id}")

with tabs[1]: # ELECTRONICS
    tc1 = st.number_input("TC1", 0, 12, 3, key=f"tc1_{id}")
    tc2 = st.number_input("TC2", 0, 12, 2, key=f"tc2_{id}")
    abs_v = st.number_input("ABS", 0, 12, 3, key=f"abs_{id}")
    ecu_v = st.number_input("ECU Map", 1, 4, 1, key=f"ecu_{id}")

with tabs[2]: # MECHANICAL GRIP
    cm1, cm2 = st.columns(2)
    with cm1:
        f_arb = st.text_input("Anti-Roll Bar Front", f_arb_val, key=f"farb_{id}")
        bb = st.text_input("Brake Bias (%)", str(car_data["bb"]), key=f"bb_{id}")
        wr_f = st.text_input("Wheel Rate (Front)", wr_f_val, key=f"wrf_{id}")
    with cm2:
        r_arb = st.text_input("Anti-Roll Bar Rear", r_arb_val, key=f"rarb_{id}")
        diff = st.text_input("Preload Differential (Nm)", str(car_data["diff"]), key=f"diff_{id}")
        wr_r = st.text_input("Wheel Rate (Rear)", wr_r_val, key=f"wrr_{id}")

with tabs[3]: # DAMPERS
    st.subheader("Dampers (B / FB / R / FR)")
    cd1, cd2 = st.columns(2)
    with cd1:
        st.write("**Front (L/R)**")
        st.number_input("Bump Front", 0, 40, d_vals[0], key=f"bf_{id}")
        st.number_input("F-Bump Front", 0, 40, d_vals[1], key=f"fbf_{id}")
    with cd2:
        st.write("**Rear (L/R)**")
        st.number_input("Rebound Rear", 0, 40, d_vals[2], key=f"rr_{id}")
        st.number_input("F-Rebound Rear", 0, 40, d_vals[3], key=f"frr_{id}")

with tabs[4]: # AERO
    ca1, ca2 = st.columns(2)
    with ca1:
        frh = st.text_input("Ride Height Front", frh_val, key=f"frh_{id}")
        fduct = st.text_input("Brake Ducts Front", "2", key=f"fd_{id}")
    with ca2:
        rrh = st.text_input("Ride Height Rear", rrh_val, key=f"rrh_{id}")
        wing = st.number_input("Rear Wing", 0, 20, wing_val, key=f"wing_{id}")

# --- SAVE & EXPORT ---
st.divider()
if st.button("💾 Sla Setup op"):
    entry = {"Auto": auto, "Circuit": circuit, "PSI": psi_lf, "Wing": wing, "BB": bb}
    st.session_state['saved_setups'].append(entry)
    st.success("Opgeslagen!")

if st.session_state['saved_setups']:
    df = pd.DataFrame(st.session_state['saved_setups'])
    st.table(df)
    csv = df.to_csv(index=False).encode('utf-8')
    st.download_button("📥 Download CSV", data=csv, file_name='acc_setups.csv', mime='text/csv')
