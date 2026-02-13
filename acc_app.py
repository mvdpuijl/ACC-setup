import streamlit as st
import pandas as pd

# 1. Configuratie
st.set_page_config(page_title="ACC Ultimate Master v5.5", layout="wide")

# 2. Volledige Database
cars_db = {
    "Ferrari 296 GT3": {"bb": "54.2", "diff": "80", "steer": "13.0", "wr_f": "160", "wr_r": "130", "tips": "Focus op aero-rake."},
    "Porsche 911 GT3 R (992)": {"bb": "50.2", "diff": "120", "steer": "12.0", "wr_f": "190", "wr_r": "150", "tips": "Motor achterin, wees voorzichtig met remmen."},
    "BMW M4 GT3": {"bb": "57.5", "diff": "40", "steer": "14.0", "wr_f": "150", "wr_r": "120", "tips": "Stabiel over curbs."},
    "Lamborghini EVO2": {"bb": "55.2", "diff": "90", "steer": "13.0", "wr_f": "165", "wr_r": "135", "tips": "Veel rotatie."},
    "McLaren 720S EVO": {"bb": "53.2", "diff": "70", "steer": "13.0", "wr_f": "155", "wr_r": "125", "tips": "Gevoelig voor rijhoogte."},
    "Mercedes AMG EVO": {"bb": "56.8", "diff": "65", "steer": "14.0", "wr_f": "170", "wr_r": "140", "tips": "Sterke tractie."},
    "Audi R8 EVO II": {"bb": "54.0", "diff": "110", "steer": "13.0", "wr_f": "160", "wr_r": "130", "tips": "Nerveus platform."},
    "Aston Martin EVO": {"bb": "56.2", "diff": "55", "steer": "14.0", "wr_f": "155", "wr_r": "125", "tips": "Stabiel en voorspelbaar."},
    "Ford Mustang GT3": {"bb": "57.0", "diff": "50", "steer": "14.0", "wr_f": "160", "wr_r": "130", "tips": "Veel koppel."},
    "Corvette Z06 GT3.R": {"bb": "54.8", "diff": "75", "steer": "13.0", "wr_f": "160", "wr_r": "130", "tips": "Goede allrounder."}
}

circuits_db = {
    "High Downforce": ["Spa", "Zandvoort", "Kyalami", "Barcelona", "Hungaroring", "Suzuka", "Donington"],
    "Low Downforce": ["Monza", "Paul Ricard", "Bathurst", "Silverstone"],
    "Street/Bumpy": ["Zolder", "Mount Panorama", "Laguna Seca", "Misano", "Imola", "Valencia"]
}

# 3. Selectie & Motor
st.title("🏎️ ACC Setup Master v5.5 - Absolute Version")

col1, col2 = st.columns(2)
with col1:
    auto = st.selectbox("🚗 Kies Auto:", list(cars_db.keys()))
with col2:
    circuit = st.selectbox("📍 Kies Circuit:", [c for sub in circuits_db.values() for c in sub])

# Dit is de unieke ID die de refresh forceert
ukey = f"{auto}_{circuit}".replace(" ", "_").replace(".", "")

# Berekeningen
car = cars_db[auto]
ctype = next((k for k, v in circuits_db.items() if circuit in v), "High Downforce")
psi = "26.8" if ctype == "High Downforce" else "26.2"
wing = 11 if ctype == "High Downforce" else 2 if ctype == "Low Downforce" else 7
arb_f = "4" if ctype != "Street/Bumpy" else "3"
arb_r = "3" if ctype != "Street/Bumpy" else "2"
d = [5, 10, 8, 12] if ctype != "Street/Bumpy" else [8, 15, 6, 10]

# --- 4. TABS (Alles Handmatig Uitgeschreven) ---
tabs = st.tabs(["🛞 Tyres", "⚡ Electronics", "⛽ Fuel & Strategy", "⚙️ Mechanical Grip", "☁️ Dampers", "✈️ Aero"])

with tabs[0]: # TYRES & ALIGNMENT
    st.subheader("Banden & Uitlijning")
    c1, c2 = st.columns(2)
    with c1:
        st.write("**Front**")
        st.text_input("LF PSI", psi, key=f"psi_lf_{ukey}")
        st.text_input("RF PSI", psi, key=f"psi_rf_{ukey}")
        st.text_input("LF Toe", "0.06", key=f"toe_lf_{ukey}")
        st.text_input("RF Toe", "0.06", key=f"toe_rf_{ukey}")
        st.text_input("LF Camber", "-3.5", key=f"cam_lf_{ukey}")
        st.text_input("RF Camber", "-3.5", key=f"cam_rf_{ukey}")
        st.text_input("LF Caster", "12.0", key=f"cas_lf_{ukey}")
        st.text_input("RF Caster", "12.0", key=f"cas_rf_{ukey}")
    with c2:
        st.write("**Rear**")
        st.text_input("LR PSI", psi, key=f"psi_lr_{ukey}")
        st.text_input("RR PSI", psi, key=f"psi_rr_{ukey}")
        st.text_input("LR Toe", "0.10", key=f"toe_lr_{ukey}")
        st.text_input("RR Toe", "0.10", key=f"toe_rr_{ukey}")
        st.text_input("LR Camber", "-3.0", key=f"cam_lr_{ukey}")
        st.text_input("RR Camber", "-3.0", key=f"cam_rr_{ukey}")

with tabs[1]: # ELECTRONICS
    st.subheader("Electronica")
    st.number_input("TC", 0, 12, 3, key=f"tc1_{ukey}")
    st.number_input("TC2", 0, 12, 2, key=f"tc2_{ukey}")
    st.number_input("ABS", 0, 12, 3, key=f"abs_{ukey}")
    st.number_input("ECU Map", 1, 5, 1, key=f"ecu_{ukey}")

with tabs[2]: # FUEL & STRATEGY
    st.subheader("Brandstof & Strategie")
    st.text_input("Fuel (Litre)", "60", key=f"fuel_{ukey}")
    st.text_input("Tyre Set", "1", key=f"tset_{ukey}")
    st.selectbox("Front Brake Pads", [1,2,3,4], key=f"fbp_{ukey}")
    st.selectbox("Rear Brake Pads", [1,2,3,4], key=f"rbp_{ukey}")

with tabs[3]: # MECHANICAL GRIP
    st.subheader("Mechanische Grip")
    cm1, cm2 = st.columns(2)
    with cm1:
        st.write("**Front Settings**")
        st.text_input("Front Anti-roll bar", arb_f, key=f"farb_{ukey}")
        st.text_input("Brake Bias (%)", car["bb"], key=f"bb_{ukey}")
        st.text_input("Steer Ratio", car["steer"], key=f"sr_{ukey}")
        st.write("*Left Front*")
        st.text_input("Wheel Rate LF", car["wr_f"], key=f"wrlf_{ukey}")
        st.text_input("Bumpstop Rate LF", "500", key=f"bsrlf_{ukey}")
        st.text_input("Bumpstop Range LF", "20", key=f"bsranlf_{ukey}")
        st.write("*Right Front*")
        st.text_input("Wheel Rate RF", car["wr_f"], key=f"wrrf_{ukey}")
        st.text_input("Bumpstop Rate RF", "500", key=f"bsrrf_{ukey}")
        st.text_input("Bumpstop Range RF", "20", key=f"bsranrf_{ukey}")
    with cm2:
        st.write("**Rear Settings**")
        st.text_input("Rear Anti-roll bar", arb_r, key=f"rarb_{ukey}")
        st.text_input("Preload Differential (Nm)", car["diff"], key=f"diff_{ukey}")
        st.write("*Left Rear*")
        st.text_input("Wheel Rate LR", car["wr_r"], key=f"wrlr_{ukey}")
        st.text_input("Bumpstop Rate LR", "400", key=f"bsrlr_{ukey}")
        st.text_input("Bumpstop Range LR", "15", key=f"bsranlr_{ukey}")
        st.write("*Right Rear*")
        st.text_input("Wheel Rate RR", car["wr_r"], key=f"wrrr_{ukey}")
        st.text_input("Bumpstop Rate RR", "400", key=f"bsrrr_{ukey}")
        st.text_input("Bumpstop Range RR", "15", key=f"bsranrr_{ukey}")

with tabs[4]: # DAMPERS
    st.subheader("Dampers (Bump / Fast Bump / Rebound / Fast Rebound)")
    d1, d2, d3, d4 = st.columns(4)
    hoeken = ["LF", "RF", "LR", "RR"]
    for i, h in enumerate(hoeken):
        with [d1, d2, d3, d4][i]:
            st.write(f"**{h}**")
            st.number_input(f"Bump {h}", 0, 40, d[0], key=f"b_{h}_{ukey}")
            st.number_input(f"Fast Bump {h}", 0, 40, d[1], key=f"fb_{h}_{ukey}")
            st.number_input(f"Rebound {h}", 0, 40, d[2], key=f"r_{h}_{ukey}")
            st.number_input(f"Fast Rebound {h}", 0, 40, d[3], key=f"fr_{h}_{ukey}")

with tabs[5]: # AERO
    st.subheader("Aerodynamica")
    ca1, ca2 = st.columns(2)
    with ca1:
        st.write("**Front Aero**")
        st.text_input("Ride Height Front", "48", key=f"frh_{ukey}")
        st.text_input("Splitter", "0", key=f"spl_{ukey}")
        st.text_input("Brake Ducts Front", "2", key=f"fdb_{ukey}")
    with ca2:
        st.write("**Rear Aero**")
        st.text_input("Ride Height Rear", "68", key=f"rrh_{ukey}")
        st.number_input("Rear Wing", 0, 20, wing, key=f"wing_{ukey}")
        st.text_input("Brake Ducts Rear", "2", key=f"rdb_{ukey}")

# 5. Zijbalk Dokter
st.sidebar.header("🩺 De Setup Dokter")
klacht = st.sidebar.selectbox("Klacht?", ["Geen", "Onderstuur (Entry)", "Onderstuur (Exit)", "Overstuur (Entry)", "Overstuur (Exit)", "Auto stuitert"], key=f"dr_{ukey}")
if klacht != "Geen":
    st.sidebar.warning("Advies:")
    if "Onderstuur" in klacht: st.sidebar.write("- Verlaag Front ARB\n- Verhoog Rear Ride Height")
    elif "Overstuur" in klacht: st.sidebar.write("- Verhoog Wing\n- Verlaag Rear Ride Height")
st.sidebar.divider()
st.sidebar.info(f"💡 **Tip voor {auto}:**\n{car['tips']}")
