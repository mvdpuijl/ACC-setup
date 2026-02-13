import streamlit as st

# 1. Pagina Configuratie
st.set_page_config(page_title="ACC Setup Master v7.3", layout="wide")

# 2. Volledige Database
cars_db = {
    "Ferrari 296 GT3": {"bb": "54.2", "diff": "80", "steer": "13.0", "wr_f": "160", "wr_r": "130", "tips": "Focus op aero-rake."},
    "Porsche 911 GT3 R (992)": {"bb": "50.2", "diff": "120", "steer": "12.0", "wr_f": "190", "wr_r": "150", "tips": "Motor achterin."},
    "BMW M4 GT3": {"bb": "57.5", "diff": "40", "steer": "14.0", "wr_f": "150", "wr_r": "120", "tips": "Stabiel over curbs."},
    "Lamborghini EVO2": {"bb": "55.2", "diff": "90", "steer": "13.0", "wr_f": "165", "wr_r": "135", "tips": "Veel rotatie."},
    "McLaren 720S EVO": {"bb": "53.2", "diff": "70", "steer": "13.0", "wr_f": "155", "wr_r": "125", "tips": "Aero gevoelig."},
    "Mercedes AMG EVO": {"bb": "56.8", "diff": "65", "steer": "14.0", "wr_f": "170", "wr_r": "140", "tips": "Focus op tractie."},
    "Audi R8 EVO II": {"bb": "54.0", "diff": "110", "steer": "13.0", "wr_f": "160", "wr_r": "130", "tips": "Nerveus bij remmen."},
    "Aston Martin EVO": {"bb": "56.2", "diff": "55", "steer": "14.0", "wr_f": "155", "wr_r": "125", "tips": "Stabiel platform."},
    "Ford Mustang GT3": {"bb": "57.0", "diff": "50", "steer": "14.0", "wr_f": "160", "wr_r": "130", "tips": "Veel koppel."},
    "Corvette Z06 GT3.R": {"bb": "54.8", "diff": "75", "steer": "13.0", "wr_f": "160", "wr_r": "130", "tips": "Goede balans."}
}

circuits_db = {
    "High Downforce": ["Spa", "Zandvoort", "Kyalami", "Barcelona", "Hungaroring", "Suzuka", "Donington"],
    "Low Downforce": ["Monza", "Paul Ricard", "Bathurst", "Silverstone"],
    "Street/Bumpy": ["Zolder", "Mount Panorama", "Laguna Seca", "Misano", "Imola", "Valencia"]
}

# 3. Selectie
st.title("🏎️ ACC Setup Master v7.3 - String Force Sync")
col_a, col_c = st.columns(2)
with col_a:
    auto = st.selectbox("🚗 Kies Auto:", list(cars_db.keys()))
with col_c:
    circuit = st.selectbox("📍 Kies Circuit:", [c for sub in circuits_db.values() for c in sub])

# De Refresh-Key
ukey = f"{auto}_{circuit}".replace(" ", "_").replace(".", "")

# Data berekeningen
car = cars_db[auto]
ctype = next((k for k, v in circuits_db.items() if circuit in v), "High Downforce")

psi_val = "26.8" if ctype == "High Downforce" else "26.2"
wing_val = "11" if ctype == "High Downforce" else "2" if ctype == "Low Downforce" else "7"
arb_f = "4" if ctype != "Street/Bumpy" else "3"
arb_r = "3" if ctype != "Street/Bumpy" else "2"
d_b = "5" if ctype != "Street/Bumpy" else "8"
d_fb = "10" if ctype != "Street/Bumpy" else "15"
d_r = "8" if ctype != "Street/Bumpy" else "6"
d_fr = "12" if ctype != "Street/Bumpy" else "10"

# --- 4. TABS (Alles als TEXT_INPUT voor maximale refresh) ---
tabs = st.tabs(["🛞 Tyres", "⚡ Electronics", "⛽ Fuel & Strategy", "⚙️ Mechanical Grip", "☁️ Dampers", "✈️ Aero"])

with tabs[0]: # TYRES
    st.subheader("Banden & Uitlijning")
    c1, c2 = st.columns(2)
    with c1:
        st.write("**Front**")
        st.text_input("LF PSI", psi_val, key=f"lfpsi_{ukey}")
        st.text_input("RF PSI", psi_val, key=f"rfpsi_{ukey}")
        st.text_input("LF Toe", "0.06", key=f"lft_{ukey}")
        st.text_input("LF Camber", "-3.5", key=f"lfc_{ukey}")
    with c2:
        st.write("**Rear**")
        st.text_input("LR PSI", psi_val, key=f"lrpsi_{ukey}")
        st.text_input("RR PSI", psi_val, key=f"rrpsi_{ukey}")
        st.text_input("LR Toe", "0.10", key=f"lrt_{ukey}")
        st.text_input("LR Camber", "-3.0", key=f"lrc_{ukey}")

with tabs[1]: # ELECTRONICS
    st.subheader("Electronica")
    st.text_input("TC", "3", key=f"tc_{ukey}")
    st.text_input("TC2", "2", key=f"tc2_{ukey}")
    st.text_input("ABS", "3", key=f"abs_{ukey}")
    st.text_input("ECU Map", "1", key=f"ecu_{ukey}")

with tabs[2]: # FUEL & STRATEGY
    st.subheader("Brandstof & Strategie")
    st.text_input("Fuel (Litre)", "60", key=f"f_{ukey}")
    st.text_input("Front Brake Pads", "1", key=f"fbp_{ukey}")
    st.text_input("Rear Brake Pads", "1", key=f"rbp_{ukey}")

with tabs[3]: # MECHANICAL GRIP
    st.subheader("Mechanische Grip")
    m1, m2 = st.columns(2)
    with m1:
        st.text_input("Front Anti-roll bar", arb_f, key=f"farb_{ukey}")
        st.text_input("Brake Bias (%)", car["bb"], key=f"bb_{ukey}")
        st.text_input("Wheel Rate LF", car["wr_f"], key=f"wlf_{ukey}")
        st.text_input("Bumpstop Rate LF", "500", key=f"bsf_{ukey}")
    with m2:
        st.text_input("Rear Anti-roll bar", arb_r, key=f"rarb_{ukey}")
        st.text_input("Preload Differential", car["diff"], key=f"diff_{ukey}")
        st.text_input("Wheel Rate LR", car["wr_r"], key=f"wlr_{ukey}")
        st.text_input("Bumpstop Rate LR", "400", key=f"bsr_{ukey}")

with tabs[4]: # DAMPERS
    st.subheader("Dampers (B / FB / R / FR)")
    d1, d2, d3, d4 = st.columns(4)
    hoeken = ["LF", "RF", "LR", "RR"]
    for i, h in enumerate(hoeken):
        with [d1, d2, d3, d4][i]:
            st.write(f"**{h}**")
            st.text_input(f"B {h}", d_b, key=f"b_{h}_{ukey}")
            st.text_input(f"FB {h}", d_fb, key=f"fb_{h}_{ukey}")
            st.text_input(f"R {h}", d_r, key=f"r_{h}_{ukey}")
            st.text_input(f"FR {h}", d_fr, key=f"fr_{h}_{ukey}")

with tabs[5]: # AERO
    st.subheader("Aerodynamica")
    ca1, ca2 = st.columns(2)
    with ca1:
        st.text_input("Ride Height Front", "48", key=f"rhf_{ukey}")
        st.text_input("Splitter", "0", key=f"spl_{ukey}")
    with ca2:
        st.text_input("Ride Height Rear", "68", key=f"rhr_{ukey}")
        st.text_input("Rear Wing", wing_val, key=f"wing_{ukey}")

# SIDEBAR DOKTER
st.sidebar.header("🩺 Setup Dokter")
st.sidebar.info(f"💡 **Tip voor {auto}:**\n{car['tips']}")
