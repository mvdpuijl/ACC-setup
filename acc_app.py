import streamlit as st
import pandas as pd

# 1. Pagina Configuratie
st.set_page_config(page_title="ACC Setup Master v7.0", layout="wide")

# 2. Volledige Database
cars = {
    "Ferrari 296 GT3": {"bb": 54.2, "diff": 80, "steer": 13.0, "wr_f": 160, "wr_r": 130, "tips": "Focus op aero-rake."},
    "Porsche 911 GT3 R (992)": {"bb": 50.2, "diff": 120, "steer": 12.0, "wr_f": 190, "wr_r": 150, "tips": "Motor achterin, pas op bij remmen."},
    "BMW M4 GT3": {"bb": 57.5, "diff": 40, "steer": 14.0, "wr_f": 150, "wr_r": 120, "tips": "Stabiel over curbs."},
    "Lamborghini EVO2": {"bb": 55.2, "diff": 90, "steer": 13.0, "wr_f": 165, "wr_r": 135, "tips": "Veel rotatie."},
    "McLaren 720S EVO": {"bb": 53.2, "diff": 70, "steer": 13.0, "wr_f": 155, "wr_r": 125, "tips": "Gevoelig voor rijhoogte."},
    "Mercedes AMG EVO": {"bb": 56.8, "diff": 65, "steer": 14.0, "wr_f": 170, "wr_r": 140, "tips": "Sterke tractie."},
    "Audi R8 EVO II": {"bb": 54.0, "diff": 110, "steer": 13.0, "wr_f": 160, "wr_r": 130, "tips": "Nerveus platform."},
    "Aston Martin EVO": {"bb": 56.2, "diff": 55, "steer": 14.0, "wr_f": 155, "wr_r": 125, "tips": "Stabiel en voorspelbaar."},
    "Ford Mustang GT3": {"bb": 57.0, "diff": 50, "steer": 14.0, "wr_f": 160, "wr_r": 130, "tips": "Veel koppel achter."},
    "Corvette Z06 GT3.R": {"bb": 54.8, "diff": 75, "steer": 13.0, "wr_f": 160, "wr_r": 130, "tips": "Goede allrounder."}
}

circuits = {
    "High Downforce": ["Spa", "Zandvoort", "Kyalami", "Barcelona", "Hungaroring", "Suzuka", "Donington"],
    "Low Downforce": ["Monza", "Paul Ricard", "Bathurst", "Silverstone"],
    "Street/Bumpy": ["Zolder", "Mount Panorama", "Laguna Seca", "Misano", "Imola", "Valencia"]
}

# 3. Selectie
st.title("🏎️ ACC Setup Master v7.0")
col_a, col_c = st.columns(2)
with col_a:
    auto = st.selectbox("🚗 Kies Auto:", list(cars.keys()))
with col_c:
    circuit = st.selectbox("📍 Kies Circuit:", [c for sub in circuits.values() for c in sub])

# DIT IS DE MOTOR: De unieke suffix forceert een complete widget refresh
ukey = f"{auto}_{circuit}".replace(" ", "_").replace(".", "")

# Berekeningen op basis van circuit type
ctype = next((k for k, v in circuits.items() if circuit in v), "High Downforce")
psi_v = "26.8" if ctype == "High Downforce" else "26.2"
wing_v = 11 if ctype == "High Downforce" else 2 if ctype == "Low Downforce" else 7
arb_f_v = "4" if ctype != "Street/Bumpy" else "3"
arb_r_v = "3" if ctype != "Street/Bumpy" else "2"
d_vals = [5, 10, 8, 12] if ctype != "Street/Bumpy" else [8, 15, 6, 10]
car_data = cars[auto]

# 4. Tabs (Volledig uitgeschreven)
tabs = st.tabs(["🛞 Tyres", "⚡ Electronics", "⛽ Fuel & Strategy", "⚙️ Mechanical Grip", "☁️ Dampers", "✈️ Aero"])

with tabs[0]: # TYRES
    t1, t2 = st.columns(2)
    with t1:
        st.write("**Front**")
        st.text_input("LF PSI", psi_v, key=f"psi_lf_{ukey}")
        st.text_input("RF PSI", psi_v, key=f"psi_rf_{ukey}")
        st.text_input("LF Toe", "0.06", key=f"toe_lf_{ukey}")
        st.text_input("RF Toe", "0.06", key=f"toe_rf_{ukey}")
        st.text_input("LF Camber", "-3.5", key=f"cam_lf_{ukey}")
        st.text_input("RF Camber", "-3.5", key=f"cam_rf_{ukey}")
        st.text_input("LF Caster", "12.0", key=f"cas_lf_{ukey}")
        st.text_input("RF Caster", "12.0", key=f"cas_rf_{ukey}")
    with t2:
        st.write("**Rear**")
        st.text_input("LR PSI", psi_v, key=f"psi_lr_{ukey}")
        st.text_input("RR PSI", psi_v, key=f"psi_rr_{ukey}")
        st.text_input("LR Toe", "0.10", key=f"toe_lr_{ukey}")
        st.text_input("RR Toe", "0.10", key=f"toe_rr_{ukey}")
        st.text_input("LR Camber", "-3.0", key=f"cam_lr_{ukey}")
        st.text_input("RR Camber", "-3.0", key=f"cam_rr_{ukey}")

with tabs[1]: # ELECTRONICS
    st.subheader("Electronics")
    st.number_input("TC", 0, 12, 3, key=f"tc1_{ukey}")
    st.number_input("TC2", 0, 12, 2, key=f"tc2_{ukey}")
    st.number_input("ABS", 0, 12, 3, key=f"abs_{ukey}")
    st.number_input("ECU Map", 1, 5, 1, key=f"ecu_{ukey}")

with tabs[2]: # FUEL
    st.subheader("Fuel & Strategy")
    st.text_input("Fuel (Litre)", "60", key=f"fuel_{ukey}")
    st.text_input("Tyre Set", "1", key=f"tset_{ukey}")
    st.selectbox("Front Brake Pads", [1, 2, 3, 4], key=f"fbp_{ukey}")
    st.selectbox("Rear Brake Pads", [1, 2, 3, 4], key=f"rbp_{ukey}")

with tabs[3]: # MECHANICAL GRIP
    st.subheader("Mechanical Grip")
    m1, m2 = st.columns(2)
    with m1:
        st.write("**Front Settings**")
        st.text_input("Front Anti-roll bar", arb_f_v, key=f"farb_{ukey}")
        st.text_input("Brake Bias (%)", str(car_data["bb"]), key=f"bb_{ukey}")
        st.text_input("Steer Ratio", str(car_data["steer"]), key=f"sr_{ukey}")
        st.write("*Springs & Bumpstops Front*")
        st.text_input("Wheel Rate LF", str(car_data["wr_f"]), key=f"wrlf_{ukey}")
        st.text_input("Wheel Rate RF", str(car_data["wr_f"]), key=f"wrrf_{ukey}")
        st.text_input("Bumpstop Rate LF", "500", key=f"bsrlf_{ukey}")
        st.text_input("Bumpstop Rate RF", "500", key=f"bsrrf_{ukey}")
        st.text_input("Bumpstop Range LF", "20", key=f"bsranlf_{ukey}")
        st.text_input("Bumpstop Range RF", "20", key=f"bsranrf_{ukey}")
    with m2:
        st.write("**Rear Settings**")
        st.text_input("Rear Anti-roll bar", arb_r_v, key=f"rarb_{ukey}")
        st.text_input("Preload Differential", str(car_data["diff"]), key=f"diff_{ukey}")
        st.write("*Springs & Bumpstops Rear*")
        st.text_input("Wheel Rate LR", str(car_data["wr_r"]), key=f"wrlr_{ukey}")
        st.text_input("Wheel Rate RR", str(car_data["wr_r"]), key=f"wrrr_{ukey}")
        st.text_input("Bumpstop Rate LR", "400", key=f"bsrlr_{ukey}")
        st.text_input("Bumpstop Rate RR", "400", key=f"bsrrr_{ukey}")
        st.text_input("Bumpstop Range LR", "15", key=f"bsranlr_{ukey}")
        st.text_input("Bumpstop Range RR", "15", key=f"bsranrr_{ukey}")

with tabs[4]: # DAMPERS
    st.subheader("Dampers")
    d1, d2, d3, d4 = st.columns(4)
    with d1:
        st.write("**LF**")
        st.number_input("Bump LF", 0, 40, d_vals[0], key=f"b_lf_{ukey}")
        st.number_input("Fast Bump LF", 0, 40, d_vals[1], key=f"fb_lf_{ukey}")
        st.number_input("Rebound LF", 0, 40, d_vals[2], key=f"r_lf_{ukey}")
        st.number_input("Fast Rebound LF", 0, 40, d_vals[3], key=f"fr_lf_{ukey}")
    with d2:
        st.write("**RF**")
        st.number_input("Bump RF", 0, 40, d_vals[0], key=f"b_rf_{ukey}")
        st.number_input("Fast Bump RF", 0, 40, d_vals[1], key=f"fb_rf_{ukey}")
        st.number_input("Rebound RF", 0, 40, d_vals[2], key=f"r_rf_{ukey}")
        st.number_input("Fast Rebound RF", 0, 40, d_vals[3], key=f"fr_rf_{ukey}")
    with d3:
        st.write("**LR**")
        st.number_input("Bump LR", 0, 40, d_vals[0], key=f"b_lr_{ukey}")
        st.number_input("Fast Bump LR", 0, 40, d_vals[1], key=f"fb_lr_{ukey}")
        st.number_input("Rebound LR", 0, 40, d_vals[2], key=f"r_lr_{ukey}")
        st.number_input("Fast Rebound LR", 0, 40, d_vals[3], key=f"fr_lr_{ukey}")
    with d4:
        st.write("**RR**")
        st.number_input("Bump RR", 0, 40, d_vals[0], key=f"b_rr_{ukey}")
        st.number_input("Fast Bump RR", 0, 40, d_vals[1], key=f"fb_rr_{ukey}")
        st.number_input("Rebound RR", 0, 40, d_vals[2], key=f"r_rr_{ukey}")
        st.number_input("Fast Rebound RR", 0, 40, d_vals[3], key=f"fr_rr_{ukey}")

with tabs[5]: # AERO
    st.subheader("Aero")
    a1, a2 = st.columns(2)
    with a1:
        st.text_input("Ride Height Front", "48", key=f"rhf_{ukey}")
        st.text_input("Splitter", "0", key=f"spl_{ukey}")
        st.text_input("Brake Ducts Front", "2", key=f"bdf_{ukey}")
    with a2:
        st.text_input("Ride Height Rear", "68", key=f"rhr_{ukey}")
        st.number_input("Rear Wing", 0, 20, wing_v, key=f"wing_{ukey}")
        st.text_input("Brake Ducts Rear", "2", key=f"bdr_{ukey}")

# --- SIDEBAR DOKTER ---
st.sidebar.header("🩺 Setup Dokter")
klacht = st.sidebar.selectbox("Klacht:", ["Geen", "Onderstuur", "Overstuur"], key=f"dr_{ukey}")
st.sidebar.info(f"💡 **Tip voor {auto}:**\n{car_data['tips']}")
