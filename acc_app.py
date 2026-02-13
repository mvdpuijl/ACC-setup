import streamlit as st

# 1. Pagina Configuratie
st.set_page_config(page_title="ACC Setup Master v7.2", layout="wide")

# 2. Volledige Database (Directe bron voor alle widgets)
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
st.title("🏎️ ACC Setup Master v7.2 - Absolute Sync")
col_a, col_c = st.columns(2)
with col_a:
    auto = st.selectbox("🚗 Kies Auto:", list(cars_db.keys()))
with col_c:
    circuit = st.selectbox("📍 Kies Circuit:", [c for sub in circuits_db.values() for c in sub])

# Dit is de unieke ID die de refresh forceert
ukey = f"{auto}_{circuit}".replace(" ", "_").replace(".", "")

# Berekeningen (Direct gekoppeld aan UI)
car = cars_db[auto]
ctype = next((k for k, v in circuits_db.items() if circuit in v), "High Downforce")

# Dynamische waarden
psi_val = "26.8" if ctype == "High Downforce" else "26.2"
wing_val = 11 if ctype == "High Downforce" else 2 if ctype == "Low Downforce" else 7
arb_f = "4" if ctype != "Street/Bumpy" else "3"
arb_r = "3" if ctype != "Street/Bumpy" else "2"
d = [5, 10, 8, 12] if ctype != "Street/Bumpy" else [8, 15, 6, 10]

# --- 4. TABS (Alles Handmatig Uitgeschreven met Mechanical Grip-logica) ---
tabs = st.tabs(["🛞 Tyres", "⚡ Electronics", "⛽ Fuel & Strategy", "⚙️ Mechanical Grip", "☁️ Dampers", "✈️ Aero"])

with tabs[0]: # TYRES
    st.subheader("Banden & Uitlijning")
    c1, c2 = st.columns(2)
    with c1:
        st.write("**Front**")
        st.text_input("LF PSI", str(psi_val), key=f"lfpsi_{ukey}")
        st.text_input("RF PSI", str(psi_val), key=f"rfpsi_{ukey}")
        st.text_input("LF Toe", "0.06", key=f"lftoe_{ukey}")
        st.text_input("LF Camber", "-3.5", key=f"lfcam_{ukey}")
        st.text_input("LF Caster", "12.0", key=f"lfcas_{ukey}")
    with c2:
        st.write("**Rear**")
        st.text_input("LR PSI", str(psi_val), key=f"lrpsi_{ukey}")
        st.text_input("RR PSI", str(psi_val), key=f"rrpsi_{ukey}")
        st.text_input("LR Toe", "0.10", key=f"lrtoe_{ukey}")
        st.text_input("LR Camber", "-3.0", key=f"lrcam_{ukey}")

with tabs[1]: # ELECTRONICS
    st.subheader("Electronica")
    st.number_input("TC1", 0, 12, 3, key=f"tc1_{ukey}")
    st.number_input("TC2", 0, 12, 2, key=f"tc2_{ukey}")
    st.number_input("ABS", 0, 12, 3, key=f"abs_{ukey}")
    st.number_input("ECU Map", 1, 5, 1, key=f"ecu_{ukey}")

with tabs[2]: # FUEL & STRATEGY
    st.subheader("Brandstof & Strategie")
    st.text_input("Fuel (Litre)", "60", key=f"fuel_{ukey}")
    st.selectbox("Front Brake Pads", [1,2,3,4], key=f"fbp_{ukey}")
    st.selectbox("Rear Brake Pads", [1,2,3,4], key=f"rbp_{ukey}")

with tabs[3]: # MECHANICAL GRIP
    st.subheader("Mechanische Grip")
    cm1, cm2 = st.columns(2)
    with cm1:
        st.text_input("Front Anti-roll bar", str(arb_f), key=f"farb_{ukey}")
        st.text_input("Brake Bias (%)", str(car["bb"]), key=f"bb_{ukey}")
        st.text_input("Steer Ratio", str(car["steer"]), key=f"sr_{ukey}")
        st.text_input("Wheel Rate LF", str(car["wr_f"]), key=f"wrlf_{ukey}")
        st.text_input("Bumpstop Rate LF", "500", key=f"bsrlf_{ukey}")
        st.text_input("Bumpstop Range LF", "20", key=f"brlf_{ukey}")
    with cm2:
        st.text_input("Rear Anti-roll bar", str(arb_r), key=f"rarb_{ukey}")
        st.text_input("Preload Differential", str(car["diff"]), key=f"diff_{ukey}")
        st.text_input("Wheel Rate LR", str(car["wr_r"]), key=f"wrlr_{ukey}")
        st.text_input("Bumpstop Rate LR", "400", key=f"bsrlr_{ukey}")

with tabs[4]: # DAMPERS
    st.subheader("Dampers (B / FB / R / FR)")
    d1, d2, d3, d4 = st.columns(4)
    # LF
    with d1:
        st.write("**LF**")
        st.number_input("Bump LF", 0, 40, int(d[0]), key=f"blf_{ukey}")
        st.number_input("Fast Bump LF", 0, 40, int(d[1]), key=f"fblf_{ukey}")
        st.number_input("Rebound LF", 0, 40, int(d[2]), key=f"rlf_{ukey}")
        st.number_input("Fast Rebound LF", 0, 40, int(d[3]), key=f"frlf_{ukey}")
    # RF
    with d2:
        st.write("**RF**")
        st.number_input("Bump RF", 0, 40, int(d[0]), key=f"brf_{ukey}")
        st.number_input("Fast Bump RF", 0, 40, int(d[1]), key=f"fbrf_{ukey}")
        st.number_input("Rebound RF", 0, 40, int(d[2]), key=f"rrf_{ukey}")
        st.number_input("Fast Rebound RF", 0, 40, int(d[3]), key=f"frrf_{ukey}")
    # LR
    with d3:
        st.write("**LR**")
        st.number_input("Bump LR", 0, 40, int(d[0]), key=f"blr_{ukey}")
        st.number_input("Fast Bump LR", 0, 40, int(d[1]), key=f"fblr_{ukey}")
        st.number_input("Rebound LR", 0, 40, int(d[2]), key=f"rlr_{ukey}")
        st.number_input("Fast Rebound LR", 0, 40, int(d[3]), key=f"frlr_{ukey}")
    # RR
    with d4:
        st.write("**RR**")
        st.number_input("Bump RR", 0, 40, int(d[0]), key=f"brr_{ukey}")
        st.number_input("Fast Bump RR", 0, 40, int(d[1]), key=f"fbrr_{ukey}")
        st.number_input("Rebound RR", 0, 40, int(d[2]), key=f"rrr_{ukey}")
        st.number_input("Fast Rebound RR", 0, 40, int(d[3]), key=f"frrr_{ukey}")

with tabs[5]: # AERO
    st.subheader("Aerodynamica")
    ca1, ca2 = st.columns(2)
    with ca1:
        st.text_input("Ride Height Front", "48", key=f"rhf_{ukey}")
        st.text_input("Splitter", "0", key=f"spl_{ukey}")
        st.text_input("Brake Ducts Front", "2", key=f"bdf_{ukey}")
    with ca2:
        st.text_input("Ride Height Rear", "68", key=f"rhr_{ukey}")
        st.number_input("Rear Wing", 0, 20, int(wing_val), key=f"wing_{ukey}")
        st.text_input("Brake Ducts Rear", "2", key=f"bdr_{ukey}")

# --- SIDEBAR DOKTER ---
st.sidebar.header("🩺 Setup Dokter")
klacht = st.sidebar.selectbox("Klacht?", ["Geen", "Onderstuur", "Overstuur"], key=f"dr_{ukey}")
st.sidebar.info(f"💡 **Tip voor {auto}:**\n{car['tips']}")
