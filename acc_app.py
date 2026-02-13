import streamlit as st

# 1. Pagina Configuratie
st.set_page_config(page_title="ACC Setup Master v9.1", layout="wide")

# 2. DATABASE: Auto-specifieke basiswaarden
cars_db = {
    "Ferrari 296 GT3": {"bb": 54.2, "diff": 80, "steer": 13.0, "wr_f": 160, "wr_r": 130, "cam": -3.5, "toe": 0.06},
    "Porsche 911 GT3 R (992)": {"bb": 50.2, "diff": 120, "steer": 12.0, "wr_f": 190, "wr_r": 150, "cam": -3.8, "toe": -0.04},
    "BMW M4 GT3": {"bb": 57.5, "diff": 40, "steer": 14.0, "wr_f": 150, "wr_r": 120, "cam": -3.2, "toe": 0.05},
    "Lamborghini EVO2": {"bb": 55.2, "diff": 90, "steer": 13.0, "wr_f": 165, "wr_r": 135, "cam": -3.6, "toe": 0.06},
    "McLaren 720S EVO": {"bb": 53.2, "diff": 70, "steer": 13.0, "wr_f": 155, "wr_r": 125, "cam": -3.5, "toe": 0.06},
    "Mercedes AMG EVO": {"bb": 56.8, "diff": 65, "steer": 14.0, "wr_f": 170, "wr_r": 140, "cam": -3.4, "toe": 0.07},
    "Audi R8 EVO II": {"bb": 54.0, "diff": 110, "steer": 13.0, "wr_f": 160, "wr_r": 130, "cam": -3.7, "toe": 0.06},
    "Aston Martin EVO": {"bb": 56.2, "diff": 55, "steer": 14.0, "wr_f": 155, "wr_r": 125, "cam": -3.3, "toe": 0.06},
    "Ford Mustang GT3": {"bb": 57.0, "diff": 50, "steer": 14.0, "wr_f": 160, "wr_r": 130, "cam": -3.5, "toe": 0.06},
    "Corvette Z06 GT3.R": {"bb": 54.8, "diff": 75, "steer": 13.0, "wr_f": 160, "wr_r": 130, "cam": -3.5, "toe": 0.06}
}

# DATABASE: ALLE CIRCUITS (25+)
circuits_db = {
    "High Downforce": ["Spa-Francorchamps", "Zandvoort", "Kyalami", "Barcelona", "Hungaroring", "Suzuka", "Donington Park", "Oulton Park", "Misano", "Valencia", "Nürburgring"],
    "Low Downforce": ["Monza", "Paul Ricard", "Bathurst", "Silverstone", "Indianapolis", "Jeddah"],
    "Street/Bumpy": ["Zolder", "Mount Panorama", "Laguna Seca", "Imola", "Snetterton", "Watkins Glen", "Red Bull Ring", "Magny-Cours"]
}

# 3. Selectie
st.title("🏎️ ACC Setup Master v9.1 - Volledige Versie")
col_a, col_c = st.columns(2)
with col_a:
    auto = st.selectbox("🚗 Kies Auto:", list(cars_db.keys()))
with col_c:
    all_circuits = sorted([c for sub in circuits_db.values() for c in sub])
    circuit = st.selectbox("📍 Kies Circuit:", all_circuits)

# --- ENGINEER LOGICA ---
car = cars_db[auto]
ctype = next((k for k, v in circuits_db.items() if circuit in v), "High Downforce")

# Bereken waarden op basis van categorie
if ctype == "Low Downforce":
    psi, wing, bb_mod, arb_f, arb_r = "26.2", "2", 1.5, 5, 1
    damp = ["4", "9", "7", "11"]
elif ctype == "Street/Bumpy":
    psi, wing, bb_mod, arb_f, arb_r = "26.6", "8", -0.5, 3, 2
    damp = ["8", "15", "6", "10"]
else: # High Downforce
    psi, wing, bb_mod, arb_f, arb_r = "26.8", "11", 0.0, 4, 3
    damp = ["5", "10", "8", "12"]

# Unieke ID voor refresh
ukey = f"v91final_{auto}_{circuit}".replace(" ", "_").replace(".", "").replace("-", "")

# --- 4. TABS (Volledig handmatig uitgeschreven) ---
tabs = st.tabs(["🛞 Tyres", "⚡ Electronics", "⛽ Fuel & Strategy", "⚙️ Mechanical Grip", "☁️ Dampers", "✈️ Aero"])

with tabs[0]: # TYRES
    st.subheader("Banden & Uitlijning")
    c1, c2 = st.columns(2)
    with c1:
        st.write("**Front**")
        st.text_input("LF PSI", psi, key=f"lf_p_{ukey}")
        st.text_input("RF PSI", psi, key=f"rf_p_{ukey}")
        st.text_input("Front Toe", str(car["toe"]), key=f"f_t_{ukey}")
        st.text_input("Front Camber", str(car["cam"]), key=f"f_c_{ukey}")
    with c2:
        st.write("**Rear**")
        st.text_input("LR PSI", psi, key=f"lr_p_{ukey}")
        st.text_input("RR PSI", psi, key=f"rr_p_{ukey}")
        st.text_input("Rear Toe", "0.10", key=f"r_t_{ukey}")
        st.text_input("Rear Camber", str(car["cam"] + 0.5), key=f"r_c_{ukey}")

with tabs[1]: # ELECTRONICS
    st.subheader("Electronica")
    st.text_input("TC1", "3", key=f"tc1_{ukey}")
    st.text_input("TC2", "2", key=f"tc2_{ukey}")
    st.text_input("ABS", "3", key=f"abs_{ukey}")
    st.text_input("ECU Map", "1", key=f"ecu_{ukey}")

with tabs[2]: # FUEL & STRATEGY
    st.subheader("Brandstof & Remmen")
    st.text_input("Fuel (Litre)", "62", key=f"f_{ukey}")
    st.text_input("Brake Pads Front", "1", key=f"bpf_{ukey}")
    st.text_input("Brake Pads Rear", "1", key=f"bpr_{ukey}")

with tabs[3]: # MECHANICAL GRIP
    st.subheader("Mechanische Grip")
    mc1, mc2 = st.columns(2)
    with mc1:
        st.text_input("Front Anti-roll bar", str(arb_f), key=f"faf_{ukey}")
        st.text_input("Brake Bias (%)", str(car["bb"] + bb_mod), key=f"bb_{ukey}")
        st.text_input("Wheel Rate LF", str(car["wr_f"]), key=f"wlf_{ukey}")
        st.text_input("Bumpstop Rate LF", "500", key=f"bsf_{ukey}")
    with mc2:
        st.text_input("Rear Anti-roll bar", str(arb_r), key=f"rar_{ukey}")
        st.text_input("Preload Differential", str(car["diff"]), key=f"diff_{ukey}")
        st.text_input("Wheel Rate LR", str(car["wr_r"]), key=f"wlr_{ukey}")
        st.text_input("Bumpstop Rate LR", "400", key=f"bsr_{ukey}")

with tabs[4]: # DAMPERS
    st.subheader("Dampers (B / FB / R / FR)")
    dc1, dc2, dc3, dc4 = st.columns(4)
    hoeken = ["LF", "RF", "LR", "RR"]
    for i, h in enumerate(hoeken):
        with [dc1, dc2, dc3, dc4][i]:
            st.write(f"**{h}**")
            st.text_input(f"B {h}", damp[0], key=f"b_{h}_{ukey}")
            st.text_input(f"FB {h}", damp[1], key=f"fb_{h}_{ukey}")
            st.text_input(f"R {h}", damp[2], key=f"r_{h}_{ukey}")
            st.text_input(f"FR {h}", damp[3], key=f"fr_{h}_{ukey}")

with tabs[5]: # AERO
    st.subheader("Aerodynamica")
    ac1, ac2 = st.columns(2)
    with ac1:
        st.text_input("Ride Height Front", "48" if ctype != "Street/Bumpy" else "52", key=f"rhf_{ukey}")
        st.text_input("Splitter", "0", key=f"spl_{ukey}")
    with ac2:
        st.text_input("Ride Height Rear", "68" if ctype != "Street/Bumpy" else "75", key=f"rhr_{ukey}")
        st.text_input("Rear Wing", wing, key=f"wing_{ukey}")

# --- SIDEBAR DOKTER ---
st.sidebar.header("🩺 De Setup Dokter")
klacht = st.sidebar.selectbox("Klacht?", ["Geen", "Onderstuur", "Overstuur"], key=f"dr_{ukey}")
if klacht != "Geen":
    st.sidebar.warning("Advies: Wijzig de ARB of vleugelstand.")
