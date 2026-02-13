import streamlit as st

# 1. Pagina Configuratie
st.set_page_config(page_title="ACC Setup Master v7.4", layout="wide")

# 2. De Volledige Database (Bron van alle waarheid)
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
st.title("🏎️ ACC Setup Master v7.4 - Absolute Memory Reset")
col_a, col_c = st.columns(2)
with col_a:
    auto = st.selectbox("🚗 Kies Auto:", list(cars_db.keys()))
with col_c:
    circuit = st.selectbox("📍 Kies Circuit:", [c for sub in circuits_db.values() for c in sub])

# DIT IS DE FIX: De sleutel is nu 100% uniek per auto/circuit combinatie
ukey = f"key_{auto}_{circuit}".replace(" ", "_").replace(".", "").replace("(", "").replace(")", "")

# Data ophalen
car = cars_db[auto]
ctype = next((k for k, v in circuits_db.items() if circuit in v), "High Downforce")

# Waarden bepalen
psi_v = "26.8" if ctype == "High Downforce" else "26.2"
wing_v = "11" if ctype == "High Downforce" else "2" if ctype == "Low Downforce" else "7"
arb_f = "4" if ctype != "Street/Bumpy" else "3"
arb_r = "3" if ctype != "Street/Bumpy" else "2"
d_b, d_fb, d_r, d_fr = ("5", "10", "8", "12") if ctype != "Street/Bumpy" else ("8", "15", "6", "10")

# --- 4. TABS (Alles met de unieke Hard-Reset sleutel) ---
tabs = st.tabs(["🛞 Tyres", "⚡ Electronics", "⛽ Fuel & Strategy", "⚙️ Mechanical Grip", "☁️ Dampers", "✈️ Aero"])

with tabs[0]: # TYRES
    c1, c2 = st.columns(2)
    with c1:
        st.write("**Front**")
        st.text_input("LF PSI", psi_v, key=f"psi_lf_{ukey}")
        st.text_input("RF PSI", psi_v, key=f"psi_rf_{ukey}")
        st.text_input("LF Toe", "0.06", key=f"toe_lf_{ukey}")
        st.text_input("LF Camber", "-3.5", key=f"cam_lf_{ukey}")
    with c2:
        st.write("**Rear**")
        st.text_input("LR PSI", psi_v, key=f"psi_lr_{ukey}")
        st.text_input("RR PSI", psi_v, key=f"psi_rr_{ukey}")
        st.text_input("LR Toe", "0.10", key=f"toe_lr_{ukey}")
        st.text_input("LR Camber", "-3.0", key=f"cam_lr_{ukey}")

with tabs[1]: # ELECTRONICS
    st.text_input("TC", "3", key=f"tc1_{ukey}")
    st.text_input("TC2", "2", key=f"tc2_{ukey}")
    st.text_input("ABS", "3", key=f"abs_{ukey}")
    st.text_input("ECU Map", "1", key=f"ecu_{ukey}")

with tabs[2]: # FUEL
    st.text_input("Fuel (Litre)", "60", key=f"fuel_{ukey}")
    st.text_input("Front Brake Pads", "1", key=f"fbp_{ukey}")
    st.text_input("Rear Brake Pads", "1", key=f"rbp_{ukey}")

with tabs[3]: # MECHANICAL GRIP
    m1, m2 = st.columns(2)
    with m1:
        st.text_input("Front Anti-roll bar", arb_f, key=f"farb_{ukey}")
        st.text_input("Brake Bias (%)", car["bb"], key=f"bb_{ukey}")
        st.text_input("Wheel Rate LF", car["wr_f"], key=f"wrlf_{ukey}")
        st.text_input("Bumpstop Rate LF", "500", key=f"bsrlf_{ukey}")
    with m2:
        st.text_input("Rear Anti-roll bar", arb_r, key=f"rarb_{ukey}")
        st.text_input("Preload Differential", car["diff"], key=f"diff_{ukey}")
        st.text_input("Wheel Rate LR", car["wr_r"], key=f"wrlr_{ukey}")
        st.text_input("Bumpstop Rate LR", "400", key=f"bsrlr_{ukey}")

with tabs[4]: # DAMPERS
    d1, d2, d3, d4 = st.columns(4)
    # LF
    with d1:
        st.write("**LF**")
        st.text_input("B LF", d_b, key=f"b_lf_{ukey}")
        st.text_input("FB LF", d_fb, key=f"fb_lf_{ukey}")
        st.text_input("R LF", d_r, key=f"r_lf_{ukey}")
        st.text_input("FR LF", d_fr, key=f"fr_lf_{ukey}")
    # RF
    with d2:
        st.write("**RF**")
        st.text_input("B RF", d_b, key=f"b_rf_{ukey}")
        st.text_input("FB RF", d_fb, key=f"fb_rf_{ukey}")
        st.text_input("R RF", d_r, key=f"r_rf_{ukey}")
        st.text_input("FR RF", d_fr, key=f"fr_rf_{ukey}")
    # LR
    with d3:
        st.write("**LR**")
        st.text_input("B LR", d_b, key=f"b_lr_{ukey}")
        st.text_input("FB LR", d_fb, key=f"fb_lr_{ukey}")
        st.text_input("R LR", d_r, key=f"r_lr_{ukey}")
        st.text_input("FR LR", d_fr, key=f"fr_lr_{ukey}")
    # RR
    with d4:
        st.write("**RR**")
        st.text_input("B RR", d_b, key=f"b_rr_{ukey}")
        st.text_input("FB RR", d_fb, key=f"fb_rr_{ukey}")
        st.text_input("R RR", d_r, key=f"r_rr_{ukey}")
        st.text_input("FR RR", d_fr, key=f"fr_rr_{ukey}")

with tabs[5]: # AERO
    a1, a2 = st.columns(2)
    with a1:
        st.text_input("Ride Height Front", "48", key=f"rhf_{ukey}")
        st.text_input("Splitter", "0", key=f"spl_{ukey}")
    with a2:
        st.text_input("Ride Height Rear", "68", key=f"rhr_{ukey}")
        st.text_input("Rear Wing", wing_v, key=f"wing_{ukey}")

# SIDEBAR
st.sidebar.info(f"💡 **Tip voor {auto}:**\n{car['tips']}")
