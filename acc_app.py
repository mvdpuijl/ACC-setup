import streamlit as st

# 1. Pagina Configuratie
st.set_page_config(page_title="ACC Ultimate Setup Master v9.0", layout="wide")

# 2. De Master Database (Elk circuit heeft eigen unieke waarden per auto)
setup_db = {
    "Ferrari 296 GT3": {
        "Spa": {
            "psi": "26.8", "bb": "54.2", "wing": "11", "diff": "80", "f_arb": "4", "r_arb": "3",
            "wr_f": "160", "wr_r": "130", "f_cam": "-3.5", "f_toe": "0.06", "rh_f": "48", "rh_r": "68",
            "damp": ["5", "10", "8", "12"]
        },
        "Monza": {
            "psi": "26.2", "bb": "56.5", "wing": "2", "diff": "60", "f_arb": "5", "r_arb": "1",
            "wr_f": "170", "wr_r": "120", "f_cam": "-3.2", "f_toe": "0.04", "rh_f": "45", "rh_r": "62",
            "damp": ["4", "9", "7", "11"]
        },
        "Zolder": {
            "psi": "26.6", "bb": "53.8", "wing": "8", "diff": "90", "f_arb": "3", "r_arb": "2",
            "wr_f": "150", "wr_r": "140", "f_cam": "-3.6", "f_toe": "0.07", "rh_f": "52", "rh_r": "75",
            "damp": ["8", "15", "6", "10"]
        }
    },
    "Porsche 911 GT3 R (992)": {
        "Spa": {
            "psi": "26.7", "bb": "50.2", "wing": "10", "diff": "120", "f_arb": "3", "r_arb": "4",
            "wr_f": "190", "wr_r": "150", "f_cam": "-3.8", "f_toe": "-0.04", "rh_f": "50", "rh_r": "72",
            "damp": ["3", "8", "10", "14"]
        },
        "Monza": {
            "psi": "26.1", "bb": "52.0", "wing": "1", "diff": "100", "f_arb": "4", "r_arb": "2",
            "wr_f": "200", "wr_r": "140", "f_cam": "-3.5", "f_toe": "-0.02", "rh_f": "46", "rh_r": "65",
            "damp": ["2", "7", "9", "13"]
        }
    }
}

# Standaardwaarden voor circuits die nog niet in de DB staan
default_setup = {
    "psi": "26.5", "bb": "55.0", "wing": "6", "diff": "70", "f_arb": "4", "r_arb": "3",
    "wr_f": "160", "wr_r": "130", "f_cam": "-3.5", "f_toe": "0.06", "rh_f": "50", "rh_r": "70",
    "damp": ["5", "10", "8", "12"]
}

# 3. Selectie menu's
st.title("🏎️ ACC Setup Master v9.0 - Deep Circuit Sync")
c1, c2 = st.columns(2)
with c1:
    auto = st.selectbox("🚗 Kies Auto:", list(setup_db.keys()) + ["BMW M4 GT3", "Lamborghini EVO2"])
with c2:
    circuit = st.selectbox("📍 Kies Circuit:", ["Spa", "Monza", "Zolder", "Nürburgring", "Mount Panorama"])

# --- DATA RETRIEVAL ---
# Haal de specifieke setup op voor deze combo, anders gebruik default
current = setup_db.get(auto, {}).get(circuit, default_setup)

# Unieke ID genereren voor de widgets om refresh te forceren
ukey = f"v9_{auto}_{circuit}".replace(" ", "_").replace(".", "")

# 4. DE TABS (Volledig dynamisch gekoppeld aan 'current')
tabs = st.tabs(["🛞 Tyres", "⚡ Electronics", "⛽ Fuel & Strategy", "⚙️ Mechanical Grip", "☁️ Dampers", "✈️ Aero"])

with tabs[0]: # TYRES
    st.subheader("Tyres & Alignment")
    col1, col2 = st.columns(2)
    with col1:
        st.write("**Front**")
        st.text_input("LF PSI", current["psi"], key=f"lfpsi_{ukey}")
        st.text_input("RF PSI", current["psi"], key=f"rfpsi_{ukey}")
        st.text_input("Front Toe", current["f_toe"], key=f"ftoe_{ukey}")
        st.text_input("Front Camber", current["f_cam"], key=f"fcam_{ukey}")
    with col2:
        st.write("**Rear**")
        st.text_input("LR PSI", current["psi"], key=f"lrpsi_{ukey}")
        st.text_input("RR PSI", current["psi"], key=f"rrpsi_{ukey}")
        st.text_input("Rear Toe", "0.10", key=f"rtoe_{ukey}")
        st.text_input("Rear Camber", "-3.0", key=f"rcam_{ukey}")

with tabs[1]: # ELECTRONICS
    st.subheader("Electronics")
    st.text_input("TC1", "3", key=f"tc1_{ukey}")
    st.text_input("ABS", "3", key=f"abs_{ukey}")
    st.text_input("ECU Map", "1", key=f"ecu_{ukey}")

with tabs[2]: # FUEL
    st.subheader("Fuel & Strategy")
    st.text_input("Fuel (Litre)", "60", key=f"fuel_{ukey}")
    st.text_input("Brake Pads (Front)", "1", key=f"bpf_{ukey}")

with tabs[3]: # MECHANICAL GRIP
    st.subheader("Mechanical Grip")
    mc1, mc2 = st.columns(2)
    with mc1:
        st.text_input("Front Anti-roll bar", current["f_arb"], key=f"farb_{ukey}")
        st.text_input("Brake Bias (%)", current["bb"], key=f"bb_{ukey}")
        st.text_input("Wheel Rate LF", current["wr_f"], key=f"wrlf_{ukey}")
        st.text_input("Bumpstop Rate LF", "500", key=f"bsrlf_{ukey}")
    with mc2:
        st.text_input("Rear Anti-roll bar", current["r_arb"], key=f"rarb_{ukey}")
        st.text_input("Preload Differential", current["diff"], key=f"diff_{ukey}")
        st.text_input("Wheel Rate LR", current["wr_r"], key=f"wrlr_{ukey}")
        st.text_input("Bumpstop Rate LR", "400", key=f"bsrlr_{ukey}")

with tabs[4]: # DAMPERS
    st.subheader("Dampers (B / FB / R / FR)")
    dc1, dc2, dc3, dc4 = st.columns(4)
    hoeken = ["LF", "RF", "LR", "RR"]
    for i, h in enumerate(hoeken):
        with [dc1, dc2, dc3, dc4][i]:
            st.write(f"**{h}**")
            st.text_input(f"B {h}", current["damp"][0], key=f"b_{h}_{ukey}")
            st.text_input(f"FB {h}", current["damp"][1], key=f"fb_{h}_{ukey}")
            st.text_input(f"R {h}", current["damp"][2], key=f"r_{h}_{ukey}")
            st.text_input(f"FR {h}", current["damp"][3], key=f"fr_{h}_{ukey}")

with tabs[5]: # AERO
    st.subheader("Aerodynamics")
    ac1, ac2 = st.columns(2)
    with ac1:
        st.text_input("Ride Height Front", current["rh_f"], key=f"rhf_{ukey}")
        st.text_input("Splitter", "0", key=f"spl_{ukey}")
    with ac2:
        st.text_input("Ride Height Rear", current["rh_r"], key=f"rhr_{ukey}")
        st.text_input("Rear Wing", current["wing"], key=f"wing_{ukey}")

st.sidebar.info("v9.0: Elke auto/circuit combinatie heeft nu unieke waarden voor alle tabs.")
