import streamlit as st
import pandas as pd

st.set_page_config(page_title="ACC 2024 Ultimate Master", layout="wide")

# --- DATABASE LOGICA (De intelligentie van de app) ---
circuits = {
    "High Downforce": ["Spa", "Zandvoort", "Kyalami", "Barcelona", "Hungaroring", "Suzuka", "Donington"],
    "Low Downforce": ["Monza", "Paul Ricard", "Bathurst", "Silverstone"],
    "Street/Bumpy": ["Zolder", "Mount Panorama", "Laguna Seca", "Misano", "Imola", "Valencia"]
}

cars = {
    "Ferrari 296 GT3": {"type": "Mid", "bb": 54.2, "diff": 80, "steer": 13.0, "wr": 160, "tips": "Stabiel platform, profiteert van aero-rake."},
    "Porsche 911 GT3 R (992)": {"type": "Rear", "bb": 50.2, "diff": 120, "steer": 12.0, "wr": 190, "tips": "Motor achterin. Pas op voor lift-off oversteer."},
    "BMW M4 GT3": {"type": "Front", "bb": 57.5, "diff": 40, "steer": 14.0, "wr": 150, "tips": "Lange wielbasis, zeer vergevingsgezind over curbs."},
    "Lamborghini EVO2": {"type": "Mid", "bb": 55.2, "diff": 90, "steer": 13.0, "wr": 165, "tips": "Goede rotatie, maar wees voorzichtig met de achterbanden."},
    "McLaren 720S EVO": {"type": "Mid", "bb": 53.2, "diff": 70, "steer": 13.0, "wr": 155, "tips": "Heel gevoelig voor de juiste rijhoogte."},
    "Mercedes AMG EVO": {"type": "Front", "bb": 56.8, "diff": 65, "steer": 14.0, "wr": 170, "tips": "Sterke motor, focus op tractie bij het uitkomen."},
    "Audi R8 EVO II": {"type": "Mid", "bb": 54.0, "diff": 110, "steer": 13.0, "wr": 160, "tips": "Snelle rotatie, kan nerveus zijn bij hard remmen."},
    "Aston Martin EVO": {"type": "Front", "bb": 56.2, "diff": 55, "steer": 14.0, "wr": 155, "tips": "Zeer voorspelbaar en stabiel onder remmen."},
    "Ford Mustang GT3": {"type": "Front", "bb": 57.0, "diff": 50, "steer": 14.0, "wr": 160, "tips": "Veel koppel, focus op mechanische grip achter."},
    "Corvette Z06 GT3.R": {"type": "Mid", "bb": 54.8, "diff": 75, "steer": 13.0, "wr": 160, "tips": "Goede balans tussen topsnelheid en bochten."}
}

# Initialiseer opslag voor setups
if 'saved_setups' not in st.session_state:
    st.session_state['saved_setups'] = []

st.title("🏎️ ACC Setup Master v3.2 - Global 2024")

# --- SELECTIE ---
col_a, col_c = st.columns(2)
with col_a:
    auto = st.selectbox("🚗 Selecteer Auto:", list(cars.keys()))
with col_c:
    circuit = st.selectbox("📍 Selecteer Circuit:", [c for sub in circuits.values() for c in sub])

# Berekening van slimme basiswaarden
car_data = cars[auto]
ctype = next((k for k, v in circuits.items() if circuit in v), "High Downforce")

# Dynamische aanbevelingen op basis van circuit-type en auto-layout
wing_rec = 10 if ctype == "High Downforce" else 3 if ctype == "Low Downforce" else 7
psi_rec = "26.7" if ctype == "High Downforce" else "26.3"
f_arb_rec = 4 if ctype != "Street/Bumpy" else 3
r_arb_rec = 3 if ctype != "Street/Bumpy" else 2
d_vals = [5, 10, 8, 12] if ctype != "Street/Bumpy" else [8, 15, 6, 10]

# --- SIDEBAR DOKTER ---
st.sidebar.header("🩺 De Setup Dokter")
klacht = st.sidebar.selectbox("Wat doet de auto?", ["Perfect", "Onderstuur (Bocht in)", "Onderstuur (Bocht uit)", "Overstuur (Bocht in)", "Overstuur (Bocht uit)", "Stuitert over curbs", "Instabiel bij remmen"])
if klacht != "Perfect":
    st.sidebar.warning("**Advies:**")
    if "Onderstuur" in klacht: st.sidebar.write("- Verlaag Front ARB\n- Verhoog Rear Ride Height\n- Verhoog Front Bumpstop Range")
    elif "Overstuur" in klacht: st.sidebar.write("- Verlaag Rear ARB\n- Verhoog Rear Wing\n- Verlaag Rear Ride Height")
    elif "curbs" in klacht: st.sidebar.write("- Verlaag Fast Bump (Dampers)\n- Verlaag Wheel Rate")
    elif "remmen" in klacht: st.sidebar.write("- Verhoog Brake Bias naar voren\n- Verhoog Diff Preload")

st.sidebar.divider()
st.sidebar.info(f"💡 **Tip voor de {auto}:**\n{car_data['tips']}")

# --- TABS VOOR INPUT ---
tabs = st.tabs(["🛞 Tyres", "⚡ Electronics", "⚙️ Mechanical Grip", "☁️ Dampers", "✈️ Aero"])

with tabs[0]: # TYRES
    st.subheader("Tyres & Alignment")
    c1, c2 = st.columns(2)
    with c1:
        st.write("**Front**")
        psi_f = st.text_input("PSI (Warm Target 26.5-27.0)", psi_rec, key="pf")
        toe_f = st.text_input("Toe Front", "0.06")
        cam_f = st.text_input("Camber Front", "-3.5")
    with c2:
        st.write("**Rear**")
        psi_r = st.text_input("PSI (Warm Target 26.5-27.0) ", psi_rec, key="pr")
        toe_r = st.text_input("Toe Rear", "0.10")
        cam_r = st.text_input("Camber Rear", "-3.0")

with tabs[1]: # ELECTRONICS
    st.subheader("Electronics")
    ce1, ce2 = st.columns(2)
    with ce1:
        tc1 = st.number_input("TC1", 0, 12, 3)
        tc2 = st.number_input("TC2", 0, 12, 3)
    with ce2:
        abs_v = st.number_input("ABS", 0, 12, 3)
        ecu_v = st.number_input("ECU Map", 1, 4, 1)

with tabs[2]: # MECHANICAL GRIP
    st.subheader("Suspension & Mechanical")
    cm1, cm2 = st.columns(2)
    with cm1:
        st.write("**General & Front**")
        bb_v = st.text_input("Brake Bias (%)", car_data["bb"])
        f_arb_v = st.text_input("Anti-roll bar (F)", f_arb_rec)
        sr_v = st.text_input("Steer Ratio", car_data["steer"])
        wr_f_v = st.text_input("Wheel Rate (F)", car_data["wr"])
        bsr_f_v = st.text_input("Bumpstop Rate (F)", "500")
        bsran_f_v = st.text_input("Bumpstop Range (F)", "20")
    with cm2:
        st.write("**Differential & Rear**")
        diff_v = st.text_input("Preload Diff (Nm)", car_data["diff"])
        r_arb_v = st.text_input("Anti-roll bar (R)", r_arb_rec)
        wr_r_v = st.text_input("Wheel Rate (R)", int(car_data["wr"] * 0.8))
        bsr_r_v = st.text_input("Bumpstop Rate (R)", "400")
        bsran_r_v = st.text_input("Bumpstop Range (R)", "15")

with tabs[3]: # DAMPERS
    st.subheader("Dampers (4-Way)")
    cd1, cd2, cd3, cd4 = st.columns(4)
    for i, hoek in enumerate(["LF", "RF", "LR", "RR"]):
        with [cd1, cd2, cd3, cd4][i]:
            st.write(f"**{hoek}**")
            st.number_input("Bump", 0, 40, d_vals[0], key=f"b_{hoek}")
            st.number_input("F-Bump", 0, 40, d_vals[1], key=f"fb_{hoek}")
            st.number_input("Rebound", 0, 40, d_vals[2], key=f"r_{hoek}")
            st.number_input("F-Rebound", 0, 40, d_vals[3], key=f"fr_{hoek}")

with tabs[4]: # AERO
    st.subheader("Aerodynamics")
    ca1, ca2 = st.columns(2)
    with ca1:
        st.write("**Front**")
        frh_v = st.text_input("Ride Height (F)", "48")
        split_v = st.text_input("Splitter", "0")
        fduct_v = st.text_input("Brake Ducts (F)", "2")
    with ca2:
        st.write("**Rear**")
        rrh_v = st.text_input("Ride Height (R)", "68")
        wing_v = st.number_input("Rear Wing", 0, 20, wing_rec)
        rduct_v = st.text_input("Brake Ducts (R)", "2")

# --- SAVE & EXPORT ---
st.divider()
c_sv, c_dl = st.columns(2)

with c_sv:
    if st.button("💾 Sla Setup op voor deze sessie"):
        entry = {
            "Auto": auto, "Circuit": circuit, "PSI": psi_f, 
            "Wing": wing_v, "BB": bb_v, "TC": tc1, "Diff": diff_v
        }
        st.session_state['saved_setups'].append(entry)
        st.success("Setup toegevoegd aan lijst!")

with c_dl:
    if st.session_state['saved_setups']:
        df = pd.DataFrame(st.session_state['saved_setups'])
        csv = df.to_csv(index=False).encode('utf-8')
        st.download_button("📥 Download alle setups (CSV)", data=csv, file_name='acc_setups.csv', mime='text/csv')

# --- TABEL WEERGAVE ---
if st.session_state['saved_setups']:
    st.subheader("📋 Opgeslagen in deze sessie")
    st.table(pd.DataFrame(st.session_state['saved_setups']))
