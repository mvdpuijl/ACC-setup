import streamlit as st

# 1. Pagina Configuratie
st.set_page_config(page_title="ACC Ultimate Master v5.2", layout="wide")

# 2. Volledige Database
cars_data = {
    "Ferrari 296 GT3": {"bb": "54.2", "diff": "80", "steer": "13.0", "wr_f": "160", "wr_r": "130"},
    "Porsche 911 GT3 R (992)": {"bb": "50.2", "diff": "120", "steer": "12.0", "wr_f": "190", "wr_r": "150"},
    "BMW M4 GT3": {"bb": "57.5", "diff": "40", "steer": "14.0", "wr_f": "150", "wr_r": "120"},
    "Lamborghini EVO2": {"bb": "55.2", "diff": "90", "steer": "13.0", "wr_f": "165", "wr_r": "135"},
    "McLaren 720S EVO": {"bb": "53.2", "diff": "70", "steer": "13.0", "wr_f": "155", "wr_r": "125"},
    "Mercedes AMG EVO": {"bb": "56.8", "diff": "65", "steer": "14.0", "wr_f": "170", "wr_r": "140"},
    "Audi R8 EVO II": {"bb": "54.0", "diff": "110", "steer": "13.0", "wr_f": "160", "wr_r": "130"},
    "Aston Martin EVO": {"bb": "56.2", "diff": "55", "steer": "14.0", "wr_f": "155", "wr_r": "125"},
    "Ford Mustang GT3": {"bb": "57.0", "diff": "50", "steer": "14.0", "wr_f": "160", "wr_r": "130"},
    "Corvette Z06 GT3.R": {"bb": "54.8", "diff": "75", "steer": "13.0", "wr_f": "160", "wr_r": "130"}
}

circuits_map = {
    "High Downforce": ["Spa", "Zandvoort", "Kyalami", "Barcelona", "Hungaroring", "Suzuka", "Donington"],
    "Low Downforce": ["Monza", "Paul Ricard", "Bathurst", "Silverstone"],
    "Street/Bumpy": ["Zolder", "Mount Panorama", "Laguna Seca", "Misano", "Imola", "Valencia"]
}

# --- SELECTIE ---
st.title("🏎️ ACC Setup Master v5.2")

c1, c2 = st.columns(2)
with c1:
    auto = st.selectbox("🚗 Kies Auto:", list(cars_data.keys()))
with c2:
    circuit = st.selectbox("📍 Kies Circuit:", [c for sub in circuits_map.values() for c in sub])

# DIT IS DE MOTOR: Een unieke ID voor deze specifieke combinatie
# Als deze verandert, worden ALLE onderliggende widgets gereset.
engine_id = f"{auto}_{circuit}".replace(" ", "_")

# Berekeningen voor deze combinatie
car = cars_data[auto]
ctype = next((k for k, v in circuits_map.items() if circuit in v), "High Downforce")

psi_val = "26.8" if ctype == "High Downforce" else "26.2"
wing_val = 11 if ctype == "High Downforce" else 2 if ctype == "Low Downforce" else 7
arb_f = "4" if ctype != "Street/Bumpy" else "3"
arb_r = "3" if ctype != "Street/Bumpy" else "2"
d = [5, 10, 8, 12] if ctype != "Street/Bumpy" else [8, 15, 6, 10]

# --- TABS ---
tabs = st.tabs(["🛞 Tyres", "⚡ Electronics", "⛽ Fuel & Strategy", "⚙️ Mechanical Grip", "☁️ Dampers", "✈️ Aero"])

with tabs[0]: # TYRES
    t1, t2 = st.columns(2)
    with t1:
        st.write("**Front**")
        st.text_input("LF PSI", psi_val, key=f"lf_p_{engine_id}")
        st.text_input("RF PSI", psi_val, key=f"rf_p_{engine_id}")
        st.text_input("LF Toe", "0.06", key=f"lf_t_{engine_id}")
        st.text_input("LF Camber", "-3.5", key=f"lf_c_{engine_id}")
        st.text_input("LF Caster", "12.0", key=f"lf_ca_{engine_id}")
    with t2:
        st.write("**Rear**")
        st.text_input("LR PSI", psi_val, key=f"lr_p_{engine_id}")
        st.text_input("RR PSI", psi_val, key=f"rr_p_{engine_id}")
        st.text_input("LR Toe", "0.10", key=f"lr_t_{engine_id}")
        st.text_input("LR Camber", "-3.0", key=f"lr_c_{engine_id}")

with tabs[1]: # ELECTRONICS
    st.number_input("TC", 0, 12, 3, key=f"tc_{engine_id}")
    st.number_input("TC2", 0, 12, 2, key=f"tc2_{engine_id}")
    st.number_input("ABS", 0, 12, 3, key=f"abs_{engine_id}")
    st.number_input("ECU Map", 1, 5, 1, key=f"ecu_{engine_id}")

with tabs[2]: # FUEL
    st.text_input("Fuel (L)", "60", key=f"fuel_{engine_id}")
    st.selectbox("Front Brake Pads", [1,2,3,4], key=f"fpad_{engine_id}")
    st.selectbox("Rear Brake Pads", [1,2,3,4], key=f"rpad_{engine_id}")

with tabs[3]: # MECHANICAL
    m1, m2 = st.columns(2)
    with m1:
        st.write("**Front Settings**")
        st.text_input("Brake Bias (%)", car["bb"], key=f"bb_{engine_id}")
        st.text_input("Front ARB", arb_f, key=f"farb_{engine_id}")
        st.text_input("Wheel Rate LF", car["wr_f"], key=f"wlf_{engine_id}")
        st.text_input("Bumpstop Rate LF", "500", key=f"bslf_{engine_id}")
        st.text_input("Bumpstop Range LF", "20", key=f"brlf_{engine_id}")
    with m2:
        st.write("**Rear Settings**")
        st.text_input("Preload Diff", car["diff"], key=f"diff_{engine_id}")
        st.text_input("Rear ARB", arb_r, key=f"rarb_{engine_id}")
        st.text_input("Wheel Rate LR", car["wr_r"], key=f"wlr_{engine_id}")
        st.text_input("Bumpstop Rate LR", "400", key=f"bslr_{engine_id}")

with tabs[4]: # DAMPERS
    d1, d2, d3, d4 = st.columns(4)
    for i, h in enumerate(["LF", "RF", "LR", "RR"]):
        with [d1, d2, d3, d4][i]:
            st.write(f"**{h}**")
            st.number_input(f"Bump {h}", 0, 40, d[0], key=f"b_{h}_{engine_id}")
            st.number_input(f"Fast Bump {h}", 0, 40, d[1], key=f"fb_{h}_{engine_id}")
            st.number_input(f"Rebound {h}", 0, 40, d[2], key=f"r_{h}_{engine_id}")
            st.number_input(f"Fast Rebound {h}", 0, 40, d[3], key=f"fr_{h}_{engine_id}")

with tabs[5]: # AERO
    a1, a2 = st.columns(2)
    with a1:
        st.text_input("Ride Height Front", "48", key=f"rhf_{engine_id}")
        st.text_input("Splitter", "0", key=f"spl_{engine_id}")
    with a2:
        st.text_input("Ride Height Rear", "68", key=f"rhr_{engine_id}")
        st.number_input("Rear Wing", 0, 20, wing_val, key=f"wing_{engine_id}")

# SIDEBAR DOKTER
st.sidebar.header("🩺 Setup Dokter")
klacht = st.sidebar.selectbox("Klacht?", ["Geen", "Onderstuur", "Overstuur"], key=f"dr_{engine_id}")
if klacht != "Geen":
    st.sidebar.info("Advies: Pas je ARB of Wing aan.")
