import streamlit as st
import pandas as pd

st.set_page_config(page_title="ACC 2024 Ultimate Master v3.4", layout="wide")

# --- DATABASE LOGICA ---
circuits = {
    "High Downforce": ["Spa", "Zandvoort", "Kyalami", "Barcelona", "Hungaroring", "Suzuka", "Donington"],
    "Low Downforce": ["Monza", "Paul Ricard", "Bathurst", "Silverstone"],
    "Street/Bumpy": ["Zolder", "Mount Panorama", "Laguna Seca", "Misano", "Imola", "Valencia"]
}

cars = {
    "Ferrari 296 GT3": {"type": "Mid", "bb": 54.2, "diff": 80, "steer": 13.0, "wr": 160, "tips": "Stabiel, focus op aero-rake."},
    "Porsche 911 GT3 R (992)": {"type": "Rear", "bb": 50.2, "diff": 120, "steer": 12.0, "wr": 190, "tips": "Motor achterin. Pas op voor lift-off oversteer."},
    "BMW M4 GT3": {"type": "Front", "bb": 57.5, "diff": 40, "steer": 14.0, "wr": 150, "tips": "Lange wielbasis, zeer vergevingsgezind over curbs."},
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

st.title("🏎️ ACC Setup Master v3.4 - Full Specs")

# --- SELECTIE ---
col_a, col_c = st.columns(2)
with col_a:
    auto = st.selectbox("🚗 Selecteer Auto:", list(cars.keys()))
with col_c:
    circuit = st.selectbox("📍 Selecteer Circuit:", [c for sub in circuits.values() for c in sub])

# --- LOGICA: BEREKEN DYNAMISCHE WAARDEN ---
car_data = cars[auto]
ctype = next((k for k, v in circuits.items() if circuit in v), "High Downforce")

# Dynamische variabelen berekenen voor de velden
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
klacht = st.sidebar.selectbox("Klacht over weggedrag?", ["Geen", "Onderstuur (Entry)", "Overstuur (Exit)", "Auto stuitert"])
if klacht != "Geen":
    st.sidebar.warning("Advies: Pas ARB of Rijhoogte aan.")

# --- TABS ---
tabs = st.tabs(["🛞 Tyres", "⚡ Electronics", "⚙️ Mechanical Grip", "☁️ Dampers", "✈️ Aero"])

with tabs[0]: # TYRES
    st.subheader("Tyres & Alignment")
    c1, c2 = st.columns(2)
    with c1:
        st.write("**Front**")
        psi_lf = st.text_input("LF PSI", psi_val)
        psi_rf = st.text_input("RF PSI", psi_val)
        toe_f = st.text_input("Toe Front", "0.06")
    with c2:
        st.write("**Rear**")
        psi_lr = st.text_input("LR PSI", psi_val)
        psi_rr = st.text_input("RR PSI", psi_val)
        toe_r = st.text_input("Toe Rear", "0.10")

with tabs[1]: # ELECTRONICS
    st.subheader("Electronics")
    tc1 = st.number_input("TC1", 0, 12, 3)
    tc2 = st.number_input("TC2", 0, 12, 2)
    abs_v = st.number_input("ABS", 0, 12, 3)
    ecu_v = st.number_input("ECU Map", 1, 4, 1)

with tabs[2]: # MECHANICAL GRIP
    st.subheader("Mechanical Grip & Suspension")
    cm1, cm2 = st.columns(2)
    with cm1:
        st.write("**Front Settings**")
        f_arb = st.text_input("Anti-Roll Bar Front", f_arb_val)
        bb = st.text_input("Brake Bias (%)", str(car_data["bb"]))
        steer = st.text_input("Steer Ratio", str(car_data["steer"]))
        wr_f = st.text_input("Wheel Rate (Front)", wr_f_val)
        bsr_f = st.text_input("Bumpstop Rate (Front)", "500")
        bsran_f = st.text_input("Bumpstop Range (Front)", "20")
    with cm2:
        st.write("**Rear Settings**")
        r_arb = st.text_input("Anti-Roll Bar Rear", r_arb_val)
        diff = st.text_input("Preload Differential (Nm)", str(car_data["diff"]))
        wr_r = st.text_input("Wheel Rate (Rear)", wr_r_val)
        bsr_r = st.text_input("Bumpstop Rate (Rear)", "400")
        bsran_r = st.text_input("Bumpstop Range (Rear)", "15")

with tabs[3]: # DAMPERS
    st.subheader("Dampers (Bump, Fast Bump, Rebound, Fast Rebound)")
    cd1, cd2, cd3, cd4 = st.columns(4)
    hoeken = ["LF", "RF", "LR", "RR"]
    for i, h in enumerate(hoeken):
        with [cd1, cd2, cd3, cd4][i]:
            st.write(f"**{h}**")
            st.number_input(f"B ({h})", 0, 40, d_vals[0], key=f"b_{h}")
            st.number_input(f"FB ({h})", 0, 40, d_vals[1], key=f"fb_{h}")
            st.number_input(f"R ({h})", 0, 40, d_vals[2], key=f"r_{h}")
            st.number_input(f"FR ({h})", 0, 40, d_vals[3], key=f"fr_{h}")

with tabs[4]: # AERO
    st.subheader("Aerodynamics")
    ca1, ca2 = st.columns(2)
    with ca1:
        st.write("**Front Aero**")
        frh = st.text_input("Ride Height Front", frh_val)
        split = st.text_input("Splitter", "0")
        fduct = st.text_input("Brake Ducts Front", "2")
    with ca2:
        st.write("**Rear Aero**")
        rrh = st.text_input("Ride Height Rear", rrh_val)
        wing = st.number_input("Rear Wing", 0, 20, wing_val)
        rduct = st.text_input("Brake Ducts Rear", "2")

# --- SAVE & EXPORT ---
st.divider()
c_sv, c_dl = st.columns(2)
with c_sv:
    if st.button("💾 Sla Setup op"):
        entry = {"Auto": auto, "Circuit": circuit, "PSI": psi_lf, "Wing": wing, "BB": bb, "Diff": diff}
        st.session_state['saved_setups'].append(entry)
        st.success("Toegevoegd!")

with c_dl:
    if st.session_state['saved_setups']:
        df = pd.DataFrame(st.session_state['saved_setups'])
        csv = df.to_csv(index=False).encode('utf-8')
        st.download_button("📥 Download Database (CSV)", data=csv, file_name='acc_setups.csv', mime='text/csv')

if st.session_state['saved_setups']:
    st.subheader("📋 Opgeslagen Setups")
    st.table(pd.DataFrame(st.session_state['saved_setups']))
