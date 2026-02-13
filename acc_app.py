import streamlit as st

# 1. Pagina Configuratie
st.set_page_config(page_title="ACC Ultimate Setup Master v8.0", layout="wide")

# 2. Volledige Database
cars_db = {
    "Ferrari 296 GT3": {"bb": "54.2", "diff": "80", "steer": "13.0", "wr_f": "160", "wr_r": "130", "f_cam": "-3.5", "r_cam": "-3.0", "f_toe": "0.06", "r_toe": "0.10", "tips": "Focus op aero-rake."},
    "Porsche 911 GT3 R (992)": {"bb": "50.2", "diff": "120", "steer": "12.0", "wr_f": "190", "wr_r": "150", "f_cam": "-3.8", "r_cam": "-3.2", "f_toe": "-0.04", "r_toe": "0.15", "tips": "Motor achterin."},
    "BMW M4 GT3": {"bb": "57.5", "diff": "40", "steer": "14.0", "wr_f": "150", "wr_r": "120", "f_cam": "-3.2", "r_cam": "-2.8", "f_toe": "0.05", "r_toe": "0.12", "tips": "Sterk over curbs."},
    "Lamborghini EVO2": {"bb": "55.2", "diff": "90", "steer": "13.0", "wr_f": "165", "wr_r": "135", "f_cam": "-3.6", "r_cam": "-3.1", "f_toe": "0.06", "r_toe": "0.10", "tips": "Veel rotatie."},
    "McLaren 720S EVO": {"bb": "53.2", "diff": "70", "steer": "13.0", "wr_f": "155", "wr_r": "125", "f_cam": "-3.5", "r_cam": "-3.0", "f_toe": "0.06", "r_toe": "0.10", "tips": "Aero gevoelig."},
    "Mercedes AMG EVO": {"bb": "56.8", "diff": "65", "steer": "14.0", "wr_f": "170", "wr_r": "140", "f_cam": "-3.4", "r_cam": "-2.9", "f_toe": "0.07", "r_toe": "0.11", "tips": "Focus op tractie."},
    "Audi R8 EVO II": {"bb": "54.0", "diff": "110", "steer": "13.0", "wr_f": "160", "wr_r": "130", "f_cam": "-3.7", "r_cam": "-3.1", "f_toe": "0.06", "r_toe": "0.10", "tips": "Nerveus bij remmen."},
    "Aston Martin EVO": {"bb": "56.2", "diff": "55", "steer": "14.0", "wr_f": "155", "wr_r": "125", "f_cam": "-3.3", "r_cam": "-2.8", "f_toe": "0.06", "r_toe": "0.10", "tips": "Stabiel platform."},
    "Ford Mustang GT3": {"bb": "57.0", "diff": "50", "steer": "14.0", "wr_f": "160", "wr_r": "130", "f_cam": "-3.5", "r_cam": "-3.0", "f_toe": "0.06", "r_toe": "0.10", "tips": "Veel koppel."},
    "Corvette Z06 GT3.R": {"bb": "54.8", "diff": "75", "steer": "13.0", "wr_f": "160", "wr_r": "130", "f_cam": "-3.5", "r_cam": "-3.0", "f_toe": "0.06", "r_toe": "0.10", "tips": "Goede balans."}
}

circuits_db = {
    "High Downforce": ["Spa", "Zandvoort", "Kyalami", "Barcelona", "Hungaroring", "Suzuka", "Donington"],
    "Low Downforce": ["Monza", "Paul Ricard", "Bathurst", "Silverstone"],
    "Street/Bumpy": ["Zolder", "Mount Panorama", "Laguna Seca", "Misano", "Imola", "Valencia"]
}

# 3. Keuzemenu
st.title("🏎️ ACC Ultimate Master v8.0")
c1, c2 = st.columns(2)
with c1:
    auto = st.selectbox("🚗 Kies Auto:", list(cars_db.keys()))
with c2:
    circuit = st.selectbox("📍 Kies Circuit:", [c for sub in circuits_db.values() for c in sub])

# UNIEKE ID ENGINE
ukey = f"v8_{auto}_{circuit}".replace(" ", "_").replace(".", "")

# Berekeningen
car = cars_db[auto]
ctype = next((k for k, v in circuits_db.items() if circuit in v), "High Downforce")
psi_v = "26.8" if ctype == "High Downforce" else "26.2"
wing_v = "11" if ctype == "High Downforce" else "2" if ctype == "Low Downforce" else "7"
arb_f = "4" if ctype != "Street/Bumpy" else "3"
arb_r = "3" if ctype != "Street/Bumpy" else "2"
d = ["5", "10", "8", "12"] if ctype != "Street/Bumpy" else ["8", "15", "6", "10"]

# 4. VOLLEDIGE TABS
tabs = st.tabs(["🛞 Tyres", "⚡ Electronics", "⛽ Fuel & Strategy", "⚙️ Mechanical Grip", "☁️ Dampers", "✈️ Aero"])

with tabs[0]: # TYRES & ALIGNMENT
    tc1, tc2 = st.columns(2)
    with tc1:
        st.write("**Front**")
        st.text_input("LF PSI", psi_v, key=f"lfpsi_{ukey}")
        st.text_input("RF PSI", psi_v, key=f"rfpsi_{ukey}")
        st.text_input("LF Toe", car["f_toe"], key=f"lftoe_{ukey}")
        st.text_input("LF Camber", car["f_cam"], key=f"lfcam_{ukey}")
        st.text_input("LF Caster", "12.0", key=f"lfcas_{ukey}")
    with tc2:
        st.write("**Rear**")
        st.text_input("LR PSI", psi_v, key=f"lrpsi_{ukey}")
        st.text_input("RR PSI", psi_v, key=f"rrpsi_{ukey}")
        st.text_input("LR Toe", car["r_toe"], key=f"lrtoe_{ukey}")
        st.text_input("LR Camber", car["r_cam"], key=f"lrcam_{ukey}")

with tabs[1]: # ELECTRONICS
    st.text_input("TC", "3", key=f"tc_{ukey}")
    st.text_input("TC2", "2", key=f"tc2_{ukey}")
    st.text_input("ABS", "3", key=f"abs_{ukey}")
    st.text_input("ECU Map", "1", key=f"ecu_{ukey}")

with tabs[2]: # FUEL & STRATEGY
    st.text_input("Fuel (Litre)", "60", key=f"fuel_{ukey}")
    st.text_input("Tyre Set", "1", key=f"tset_{ukey}")
    st.text_input("Front Brake Pads", "1", key=f"fbp_{ukey}")
    st.text_input("Rear Brake Pads", "1", key=f"rbp_{ukey}")

with tabs[3]: # MECHANICAL GRIP (VOLLEDIG)
    mc1, mc2 = st.columns(2)
    with mc1:
        st.text_input("Front Anti-roll bar", arb_f, key=f"farb_{ukey}")
        st.text_input("Brake Bias (%)", car["bb"], key=f"bb_{ukey}")
        st.text_input("Steer Ratio", car["steer"], key=f"sr_{ukey}")
        st.text_input("Wheel Rate LF", car["wr_f"], key=f"wlf_{ukey}")
        st.text_input("Bumpstop Rate LF", "500", key=f"bsf_{ukey}")
        st.text_input("Bumpstop Range LF", "20", key=f"brf_{ukey}")
    with mc2:
        st.text_input("Rear Anti-roll bar", arb_r, key=f"rarb_{ukey}")
        st.text_input("Preload Diff", car["diff"], key=f"df_{ukey}")
        st.text_input("Wheel Rate LR", car["wr_r"], key=f"wlr_{ukey}")
        st.text_input("Bumpstop Rate LR", "400", key=f"bsr_{ukey}")
        st.text_input("Bumpstop Range LR", "15", key=f"brr_{ukey}")

with tabs[4]: # DAMPERS (PER HOEK)
    dc1, dc2, dc3, dc4 = st.columns(4)
    hoeken = [("LF", dc1), ("RF", dc2), ("LR", dc3), ("RR", dc4)]
    for h, col in hoeken:
        with col:
            st.write(f"**{h}**")
            st.text_input(f"B {h}", d[0], key=f"b_{h}_{ukey}")
            st.text_input(f"FB {h}", d[1], key=f"fb_{h}_{ukey}")
            st.text_input(f"R {h}", d[2], key=f"r_{h}_{ukey}")
            st.text_input(f"FR {h}", d[3], key=f"fr_{h}_{ukey}")

with tabs[5]: # AERO
    ac1, ac2 = st.columns(2)
    with ac1:
        st.text_input("Ride Height Front", "48", key=f"rhf_{ukey}")
        st.text_input("Splitter", "0", key=f"spl_{ukey}")
        st.text_input("Brake Ducts Front", "2", key=f"bdf_{ukey}")
    with ac2:
        st.text_input("Ride Height Rear", "68", key=f"rhr_{ukey}")
        st.text_input("Rear Wing", wing_v, key=f"wing_{ukey}")
        st.text_input("Brake Ducts Rear", "2", key=f"bdr_{ukey}")

# SIDEBAR
st.sidebar.header("🩺 Dokter")
st.sidebar.info(f"💡 **Tip:** {car['tips']}")
