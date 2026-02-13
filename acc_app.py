import streamlit as st
import pandas as pd

# 1. Pagina configuratie
st.set_page_config(page_title="ACC Ultimate Master v4.5", layout="wide")

# 2. Uitgebreide Database
circuits = {
    "High Downforce": ["Spa", "Zandvoort", "Kyalami", "Barcelona", "Hungaroring", "Suzuka", "Donington"],
    "Low Downforce": ["Monza", "Paul Ricard", "Bathurst", "Silverstone"],
    "Street/Bumpy": ["Zolder", "Mount Panorama", "Laguna Seca", "Misano", "Imola", "Valencia"]
}

cars = {
    "Ferrari 296 GT3": {"bb": 54.2, "diff": 80, "steer": 13.0, "wr_f": 160, "wr_r": 130, "tips": "Stabiel, focus op aero-rake."},
    "Porsche 911 GT3 R (992)": {"bb": 50.2, "diff": 120, "steer": 12.0, "wr_f": 190, "wr_r": 150, "tips": "Motor achterin. Pas op voor oversteer."},
    "BMW M4 GT3": {"bb": 57.5, "diff": 40, "steer": 14.0, "wr_f": 150, "wr_r": 120, "tips": "Sterk over curbs door lange wielbasis."},
    "Lamborghini EVO2": {"bb": 55.2, "diff": 90, "steer": 13.0, "wr_f": 165, "wr_r": 135, "tips": "Veel rotatie, agressief op achterbanden."},
    "McLaren 720S EVO": {"bb": 53.2, "diff": 70, "steer": 13.0, "wr_f": 155, "wr_r": 125, "tips": "Aero gevoelig, rijhoogte is cruciaal."},
    "Mercedes AMG EVO": {"bb": 56.8, "diff": 65, "steer": 14.0, "wr_f": 170, "wr_r": 140, "tips": "Focus op tractie en bandenbehoud."},
    "Audi R8 EVO II": {"bb": 54.0, "diff": 110, "steer": 13.0, "wr_f": 160, "wr_r": 130, "tips": "Nerveus bij hard remmen."},
    "Aston Martin EVO": {"bb": 56.2, "diff": 55, "steer": 14.0, "wr_f": 155, "wr_r": 125, "tips": "Zeer voorspelbaar platform."},
    "Ford Mustang GT3": {"bb": 57.0, "diff": 50, "steer": 14.0, "wr_f": 160, "wr_r": 130, "tips": "Veel koppel, nieuw platform."},
    "Corvette Z06 GT3.R": {"bb": 54.8, "diff": 75, "steer": 13.0, "wr_f": 160, "wr_r": 130, "tips": "Goede balans topsnelheid/bochten."}
}

if 'saved_setups' not in st.session_state:
    st.session_state['saved_setups'] = []

st.title("🏎️ ACC Setup Master v4.5 - Full & Dynamic")

# 3. Selectie
col_a, col_c = st.columns(2)
with col_a:
    auto = st.selectbox("🚗 Kies Auto:", list(cars.keys()))
with col_c:
    circuit = st.selectbox("📍 Kies Circuit:", [c for sub in circuits.values() for c in sub])

# Unieke ID voor geforceerde vernieuwing
ukey = f"{auto}_{circuit}".replace(" ", "_")

# 4. Berekeningen voor dynamische velden
car_data = cars[auto]
ctype = next((k for k, v in circuits.items() if circuit in v), "High Downforce")

psi_v = "26.8" if ctype == "High Downforce" else "26.2"
wing_v = 11 if ctype == "High Downforce" else 2 if ctype == "Low Downforce" else 7
f_arb_v = "4" if ctype != "Street/Bumpy" else "3"
r_arb_v = "3" if ctype != "Street/Bumpy" else "2"
d_vals = [5, 10, 8, 12] if ctype != "Street/Bumpy" else [8, 15, 6, 10]

# 5. Sidebar Dokter
st.sidebar.header("🩺 De Setup Dokter")
klacht = st.sidebar.selectbox("Wat doet de auto?", ["Perfect", "Onderstuur (Bocht in)", "Onderstuur (Bocht uit)", "Overstuur (Bocht in)", "Overstuur (Bocht uit)", "Auto stuitert over curbs", "Instabiel bij hard remmen"], key=f"dr_{ukey}")
if klacht != "Perfect":
    st.sidebar.warning("**Advies:**")
    if "Onderstuur" in klacht: st.sidebar.write("- Verlaag Front ARB\n- Verhoog Rear Ride Height")
    elif "Overstuur" in klacht: st.sidebar.write("- Verlaag Rear ARB\n- Verhoog Rear Wing")
st.sidebar.divider()
st.sidebar.info(f"💡 **Tip:** {car_data['tips']}")

# 6. Tabs
tabs = st.tabs(["🛞 Tyres", "⚡ Electronics", "⛽ Fuel & Strategy", "⚙️ Mechanical Grip", "☁️ Dampers", "✈️ Aero"])

with tabs[0]: # TYRES
    c1, c2 = st.columns(2)
    with c1:
        st.write("**Front**")
        st.text_input("LF PSI", psi_v, key=f"psi_lf_{ukey}"); st.text_input("RF PSI", psi_v, key=f"psi_rf_{ukey}")
        st.text_input("LF Toe", "0.06", key=f"t_lf_{ukey}"); st.text_input("RF Toe", "0.06", key=f"t_rf_{ukey}")
        st.text_input("LF Camber", "-3.5", key=f"c_lf_{ukey}"); st.text_input("RF Camber", "-3.5", key=f"c_rf_{ukey}")
        st.text_input("LF Caster", "12.0", key=f"cs_lf_{ukey}"); st.text_input("RF Caster", "12.0", key=f"cs_rf_{ukey}")
    with c2:
        st.write("**Rear**")
        st.text_input("LR PSI", psi_v, key=f"psi_lr_{ukey}"); st.text_input("RR PSI", psi_v, key=f"psi_rr_{ukey}")
        st.text_input("LR Toe", "0.10", key=f"t_lr_{ukey}"); st.text_input("RR Toe", "0.10", key=f"t_rr_{ukey}")
        st.text_input("LR Camber", "-3.0", key=f"c_lr_{ukey}"); st.text_input("RR Camber", "-3.0", key=f"c_rr_{ukey}")

with tabs[1]: # ELECTRONICS
    st.number_input("TC", 0, 12, 3, key=f"tc1_{ukey}")
    st.number_input("TC2", 0, 12, 2, key=f"tc2_{ukey}")
    st.number_input("ABS", 0, 12, 3, key=f"abs_{ukey}")
    st.number_input("ECU Map", 1, 5, 1, key=f"ecu_{ukey}")

with tabs[2]: # FUEL & STRATEGY
    st.text_input("Fuel (Litre)", "60", key=f"fuel_{ukey}")
    st.text_input("Tyre Set", "1", key=f"tset_{ukey}")
    st.selectbox("Front Brake Pads", [1, 2, 3, 4], key=f"fbp_{ukey}")
    st.selectbox("Rear Brake Pads", [1, 2, 3, 4], key=f"rbp_{ukey}")

with tabs[3]: # MECHANICAL GRIP
    cm1, cm2 = st.columns(2)
    with cm1:
        st.write("**Front Settings**")
        st.text_input("Front Anti-roll bar", f_arb_v, key=f"faf_{ukey}")
        st.text_input("Brake Bias (%)", str(car_data["bb"]), key=f"bb_{ukey}")
        st.text_input("Steer Ratio", str(car_data["steer"]), key=f"sr_{ukey}")
        st.text_input("Wheel Rate LF", str(car_data["wr_f"]), key=f"wlf_{ukey}"); st.text_input("Wheel Rate RF", str(car_data["wr_f"]), key=f"wrf_{ukey}")
        st.text_input("Bumpstop Rate LF", "500", key=f"blf_{ukey}"); st.text_input("Bumpstop Range LF", "20", key=f"brlf_{ukey}")
    with cm2:
        st.write("**Rear Settings**")
        st.text_input("Rear Anti-roll bar", r_arb_v, key=f"rar_{ukey}")
        st.text_input("Preload Differential (Nm)", str(car_data["diff"]), key=f"df_{ukey}")
        st.text_input("Wheel Rate LR", str(car_data["wr_r"]), key=f"wlr_{ukey}"); st.text_input("Wheel Rate RR", str(car_data["wr_r"]), key=f"wrr_{ukey}")
        st.text_input("Bumpstop Rate LR", "400", key=f"blr_{ukey}"); st.text_input("Bumpstop Range LR", "15", key=f"brlr_{ukey}")

with tabs[4]: # DAMPERS
    cd1, cd2, cd3, cd4 = st.columns(4)
    for i, h in enumerate(["LF", "RF", "LR", "RR"]):
        with [cd1, cd2, cd3, cd4][i]:
            st.write(f"**{h}**")
            st.number_input(f"B {h}", 0, 40, d_vals[0], key=f"b_{h}_{ukey}")
            st.number_input(f"FB {h}", 0, 40, d_vals[1], key=f"fb_{h}_{ukey}")
            st.number_input(f"R {h}", 0, 40, d_vals[2], key=f"r_{h}_{ukey}")
            st.number_input(f"FR {h}", 0, 40, d_vals[3], key=f"fr_{h}_{ukey}")

with tabs[5]: # AERO
    ca1, ca2 = st.columns(2)
    with ca1:
        st.text_input("Ride Height Front", "48", key=f"frh_{ukey}")
        st.text_input("Splitter", "0", key=f"spl_{ukey}")
        st.text_input("Brake Ducts Front", "2", key=f"fdb_{ukey}")
    with ca2:
        st.text_input("Ride Height Rear", "68", key=f"rrh_{ukey}")
        st.number_input("Rear Wing", 0, 20, wing_v, key=f"wing_{ukey}")
        st.text_input("Brake Ducts Rear", "2", key=f"rdb_{ukey}")

# --- OPSLAG & EXPORT ---
st.divider()
if st.button("💾 Sla Setup op"):
    st.session_state['saved_setups'].append({"Auto": auto, "Circuit": circuit, "PSI": psi_v, "Wing": wing_v})
    st.success("Setup toegevoegd!")

if st.session_state['saved_setups']:
    df = pd.DataFrame(st.session_state['saved_setups'])
    st.table(df)
    csv = df.to_csv(index=False).encode('utf-8')
    st.download_button("📥 Download Database (CSV)", data=csv, file_name='acc_setups.csv', mime='text/csv')
