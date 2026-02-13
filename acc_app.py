import streamlit as st

st.set_page_config(page_title="ACC Setup Master v5.3", layout="wide")

# --- 1. DATABASE ---
cars_db = {
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

circuits_db = {
    "High Downforce": ["Spa", "Zandvoort", "Kyalami", "Barcelona", "Hungaroring", "Suzuka", "Donington"],
    "Low Downforce": ["Monza", "Paul Ricard", "Bathurst", "Silverstone"],
    "Street/Bumpy": ["Zolder", "Mount Panorama", "Laguna Seca", "Misano", "Imola", "Valencia"]
}

# --- 2. SELECTIE ---
st.title("🏎️ ACC Setup Master v5.3")

col1, col2 = st.columns(2)
with col1:
    auto = st.selectbox("🚗 Kies Auto:", list(cars_db.keys()))
with col2:
    circuit = st.selectbox("📍 Kies Circuit:", [c for sub in circuits_db.values() for c in sub])

# DIT IS DE RESET MOTOR
# Elke keer als 'auto' of 'circuit' verandert, krijgt 'ukey' een nieuwe waarde.
# Alle widgets die 'ukey' in hun naam hebben, worden GEFORCEERD herladen.
ukey = f"{auto}_{circuit}".replace(" ", "_")

# Bereken waarden voor de geselecteerde combo
car = cars_db[auto]
ctype = next((k for k, v in circuits_db.items() if circuit in v), "High Downforce")

psi = "26.8" if ctype == "High Downforce" else "26.2"
wing = 11 if ctype == "High Downforce" else 2 if ctype == "Low Downforce" else 7
arb_f = "4" if ctype != "Street/Bumpy" else "3"
arb_r = "3" if ctype != "Street/Bumpy" else "2"
d = [5, 10, 8, 12] if ctype != "Street/Bumpy" else [8, 15, 6, 10]

# --- 3. DE INTERFACE (MET UNIEKE KEYS) ---
tabs = st.tabs(["🛞 Tyres", "⚡ Electronics", "⛽ Fuel & Strategy", "⚙️ Mechanical Grip", "☁️ Dampers", "✈️ Aero"])

with tabs[0]: # TYRES
    t_c1, t_c2 = st.columns(2)
    with t_c1:
        st.write("**Front**")
        st.text_input("LF PSI", psi, key=f"lf_p_{ukey}")
        st.text_input("RF PSI", psi, key=f"rf_p_{ukey}")
        st.text_input("LF Toe", "0.06", key=f"lf_t_{ukey}")
        st.text_input("LF Camber", "-3.5", key=f"lf_c_{ukey}")
        st.text_input("LF Caster", "12.0", key=f"lf_cs_{ukey}")
    with t_c2:
        st.write("**Rear**")
        st.text_input("LR PSI", psi, key=f"lr_p_{ukey}")
        st.text_input("RR PSI", psi, key=f"rr_p_{ukey}")
        st.text_input("LR Toe", "0.10", key=f"lr_t_{ukey}")
        st.text_input("LR Camber", "-3.0", key=f"lr_c_{ukey}")

with tabs[1]: # ELECTRONICS
    st.number_input("TC", 0, 12, 3, key=f"tc_{ukey}")
    st.number_input("TC2", 0, 12, 2, key=f"tc2_{ukey}")
    st.number_input("ABS", 0, 12, 3, key=f"abs_{ukey}")
    st.number_input("ECU Map", 1, 5, 1, key=f"ecu_{ukey}")

with tabs[2]: # FUEL & STRATEGY
    st.text_input("Fuel (L)", "60", key=f"fuel_{ukey}")
    st.selectbox("Front Brake Pads", [1,2,3,4], key=f"fbp_{ukey}")
    st.selectbox("Rear Brake Pads", [1,2,3,4], key=f"rbp_{ukey}")

with tabs[3]: # MECHANICAL GRIP
    m1, m2 = st.columns(2)
    with m1:
        st.write("**Front**")
        st.text_input("Brake Bias (%)", car["bb"], key=f"bb_{ukey}")
        st.text_input("Front ARB", arb_f, key=f"farb_{ukey}")
        st.text_input("Wheel Rate LF", car["wr_f"], key=f"wlf_{ukey}")
        st.text_input("Bumpstop Rate LF", "500", key=f"bsf_{ukey}")
        st.text_input("Bumpstop Range LF", "20", key=f"brf_{ukey}")
    with m2:
        st.write("**Rear**")
        st.text_input("Preload Diff", car["diff"], key=f"diff_{ukey}")
        st.text_input("Rear ARB", arb_r, key=f"rarb_{ukey}")
        st.text_input("Wheel Rate LR", car["wr_r"], key=f"wlr_{ukey}")
        st.text_input("Bumpstop Rate LR", "400", key=f"bsr_{ukey}")

with tabs[4]: # DAMPERS
    d1, d2, d3, d4 = st.columns(4)
    hoeken = ["LF", "RF", "LR", "RR"]
    for i, h in enumerate(hoeken):
        with [d1, d2, d3, d4][i]:
            st.write(f"**{h}**")
            st.number_input(f"B {h}", 0, 40, d[0], key=f"b_{h}_{ukey}")
            st.number_input(f"FB {h}", 0, 40, d[1], key=f"fb_{h}_{ukey}")
            st.number_input(f"R {h}", 0, 40, d[2], key=f"r_{h}_{ukey}")
            st.number_input(f"FR {h}", 0, 40, d[3], key=f"fr_{h}_{ukey}")

with tabs[5]: # AERO
    a1, a2 = st.columns(2)
    with a1:
        st.text_input("Ride Height Front", "48", key=f"rhf_{ukey}")
        st.text_input("Splitter", "0", key=f"spl_{ukey}")
    with a2:
        st.text_input("Ride Height Rear", "68", key=f"rhr_{ukey}")
        st.number_input("Rear Wing", 0, 20, wing, key=f"wing_{ukey}")

# --- SIDEBAR DOKTER ---
st.sidebar.header("🩺 De Setup Dokter")
klacht = st.sidebar.selectbox("Wat doet de auto?", ["Perfect", "Onderstuur", "Overstuur"], key=f"doc_{ukey}")
if klacht != "Perfect":
    st.sidebar.warning("Ingenieur: Pas ARB of Wing aan!")
