import streamlit as st
import pandas as pd

st.set_page_config(page_title="ACC Ultimate Master v4.3", layout="wide")

# --- DATABASE ---
circuits = {
    "High Downforce": ["Spa", "Zandvoort", "Kyalami", "Barcelona", "Hungaroring", "Suzuka", "Donington"],
    "Low Downforce": ["Monza", "Paul Ricard", "Bathurst", "Silverstone"],
    "Street/Bumpy": ["Zolder", "Mount Panorama", "Laguna Seca", "Misano", "Imola", "Valencia"]
}

cars = {
    "Ferrari 296 GT3": {"bb": 54.2, "diff": 80, "steer": 13.0, "wr_f": 160, "wr_r": 130, "tips": "Stabiel, focus op aero-rake."},
    "Porsche 911 GT3 R (992)": {"bb": 50.2, "diff": 120, "steer": 12.0, "wr_f": 190, "wr_r": 150, "tips": "Motor achterin. Pas op voor oversteer."},
    "BMW M4 GT3": {"bb": 57.5, "diff": 40, "steer": 14.0, "wr_f": 150, "wr_r": 120, "tips": "Sterk over curbs."},
    "Lamborghini EVO2": {"bb": 55.2, "diff": 90, "steer": 13.0, "wr_f": 165, "wr_r": 135, "tips": "Veel rotatie."},
    "McLaren 720S EVO": {"bb": 53.2, "diff": 70, "steer": 13.0, "wr_f": 155, "wr_r": 125, "tips": "Aero gevoelig."},
    "Mercedes AMG EVO": {"bb": 56.8, "diff": 65, "steer": 14.0, "wr_f": 170, "wr_r": 140, "tips": "Focus op tractie."},
    "Audi R8 EVO II": {"bb": 54.0, "diff": 110, "steer": 13.0, "wr_f": 160, "wr_r": 130, "tips": "Nerveus bij remmen."},
    "Aston Martin EVO": {"bb": 56.2, "diff": 55, "steer": 14.0, "wr_f": 155, "wr_r": 125, "tips": "Stabiel platform."},
    "Ford Mustang GT3": {"bb": 57.0, "diff": 50, "steer": 14.0, "wr_f": 160, "wr_r": 130, "tips": "Veel koppel."},
    "Corvette Z06 GT3.R": {"bb": 54.8, "diff": 75, "steer": 13.0, "wr_f": 160, "wr_r": 130, "tips": "Goede balans."}
}

# --- SELECTIE ---
col_a, col_c = st.columns(2)
with col_a:
    auto = st.selectbox("🚗 Kies Auto:", list(cars.keys()))
with col_c:
    circuit = st.selectbox("📍 Kies Circuit:", [c for sub in circuits.values() for c in sub])

# DIT IS DE MOTOR VAN DE REFRESH: De ukey verandert bij elke klik
ukey = f"{auto}_{circuit}".replace(" ", "_")
car_data = cars[auto]
ctype = next((k for k, v in circuits.items() if circuit in v), "High Downforce")

# Berekeningen
psi_v = "26.8" if ctype == "High Downforce" else "26.2"
wing_v = 11 if ctype == "High Downforce" else 2 if ctype == "Low Downforce" else 7
f_arb_v = "4" if ctype != "Street/Bumpy" else "3"
r_arb_v = "3" if ctype != "Street/Bumpy" else "2"
d_vals = [5, 10, 8, 12] if ctype != "Street/Bumpy" else [8, 15, 6, 10]

# --- SIDEBAR DOKTER ---
st.sidebar.header("🩺 De Setup Dokter")
klacht = st.sidebar.selectbox("Wat doet de auto?", ["Perfect", "Onderstuur (Bocht in)", "Onderstuur (Bocht uit)", "Overstuur (Bocht in)", "Overstuur (Bocht uit)", "Auto stuitert over curbs", "Instabiel bij hard remmen"], key=f"dr_{ukey}")
if klacht != "Perfect":
    st.sidebar.warning("**Advies:**")
    if "Onderstuur" in klacht: st.sidebar.write("- Verlaag Front ARB\n- Verhoog Rear Ride Height\n- Verhoog Front Bumpstop Range")
    elif "Overstuur" in klacht: st.sidebar.write("- Verlaag Rear ARB\n- Verhoog Rear Wing")
st.sidebar.divider()
st.sidebar.info(f"💡 **Tip voor {auto}:**\n{car_data['tips']}")

# --- TABS (ALLES VOLLEDIG UITGESCHREVEN) ---
tabs = st.tabs(["🛞 Tyres", "⚡ Electronics", "⛽ Fuel & Strategy", "⚙️ Mechanical Grip", "☁️ Dampers", "✈️ Aero"])

with tabs[0]: # TYRES
    t_c1, t_c2 = st.columns(2)
    with t_c1:
        st.write("**Front**")
        st.text_input("LF PSI", psi_v, key=f"lfpsi_{ukey}")
        st.text_input("RF PSI", psi_v, key=f"rfpsi_{ukey}")
        st.text_input("LF Toe", "0.06", key=f"lftoe_{ukey}")
        st.text_input("RF Toe", "0.06", key=f"rftoe_{ukey}")
        st.text_input("LF Camber", "-3.5", key=f"lfcam_{ukey}")
        st.text_input("RF Camber", "-3.5", key=f"rfcam_{ukey}")
        st.text_input("LF Caster", "12.0", key=f"lfcas_{ukey}")
        st.text_input("RF Caster", "12.0", key=f"rfcas_{ukey}")
    with t_c2:
        st.write("**Rear**")
        st.text_input("LR PSI", psi_v, key=f"lrpsi_{ukey}")
        st.text_input("RR PSI", psi_v, key=f"rrpsi_{ukey}")
        st.text_input("LR Toe", "0.10", key=f"lrtoe_{ukey}")
        st.text_input("RR Toe", "0.10", key=f"rrtoe_{ukey}")
        st.text_input("LR Camber", "-3.0", key=f"lrcam_{ukey}")
        st.text_input("RR Camber", "-3.0", key=f"rrcam_{ukey}")

with tabs[1]: # ELECTRONICS
    st.number_input("TC", 0, 12, 3, key=f"tc_{ukey}")
    st.number_input("TC2", 0, 12, 2, key=f"tc2_{ukey}")
    st.number_input("ABS", 0, 12, 3, key=f"abs_{ukey}")
    st.number_input("ECU Map", 1, 5, 1, key=f"ecu_{ukey}")

with tabs[2]: # FUEL & STRATEGY
    st.text_input("Fuel (Litre)", "60", key=f"fuel_{ukey}")
    st.text_input("Tyre Set", "1", key=f"tset_{ukey}")
    st.selectbox("Front Brake Pads", [1,2,3,4], key=f"fbp_{ukey}")
    st.selectbox("Rear Brake Pads", [1,2,3,4], key=f"rbp_{ukey}")

with tabs[3]: # MECHANICAL GRIP
    m1, m2 = st.columns(2)
    with m1:
        st.text_input("Front Anti-roll bar", f_arb_v, key=f"farb_{ukey}")
        st.text_input("Brake Bias (%)", str(car_data["bb"]), key=f"bb_{ukey}")
        st.text_input("Steer Ratio", str(car_data["steer"]), key=f"sr_{ukey}")
        st.write("*Left Front*")
        st.text_input("Wheel Rate LF", str(car_data["wr_f"]), key=f"wlf_{ukey}")
        st.text_input("Bumpstop Rate LF", "500", key=f"brlf_{ukey}")
        st.text_input("Bumpstop Range LF", "20", key=f"brnlf_{ukey}")
        st.write("*Right Front*")
        st.text_input("Wheel Rate RF", str(car_data["wr_f"]), key=f"wrf_{ukey}")
        st.text_input("Bumpstop Rate RF", "500", key=f"brrf_{ukey}")
        st.text_input("Bumpstop Range RF", "20", key=f"brnrf_{ukey}")
    with m2:
        st.text_input("Rear Anti-roll bar", r_arb_v, key=f"rarb_{ukey}")
        st.text_input("Preload Differential", str(car_data["diff"]), key=f"diff_{ukey}")
        st.write("*Left Rear*")
        st.text_input("Wheel Rate LR", str(car_data["wr_r"]), key=f"wlr_{ukey}")
        st.text_input("Bumpstop Rate LR", "400", key=f"brlr_{ukey}")
        st.text_input("Bumpstop Range LR", "15", key=f"brnlr_{ukey}")
        st.write("*Right Rear*")
        st.text_input("Wheel Rate RR", str(car_data["wr_r"]), key=f"wrr_{ukey}")
        st.text_input("Bumpstop Rate RR", "400", key=f"brrr_{ukey}")
        st.text_input("Bumpstop Range RR", "15", key=f"brnrr_{ukey}")

with tabs[4]: # DAMPERS
    d1, d2, d3, d4 = st.columns(4)
    hoeken = ["LF", "RF", "LR", "RR"]
    for i, h in enumerate(hoeken):
        with [d1, d2, d3, d4][i]:
            st.write(f"**{h}**")
            st.number_input(f"Bump {h}", 0, 40, d_vals[0], key=f"b_{h}_{ukey}")
            st.number_input(f"FBump {h}", 0, 40, d_vals[1], key=f"fb_{h}_{ukey}")
            st.number_input(f"Rebound {h}", 0, 40, d_vals[2], key=f"r_{h}_{ukey}")
            st.number_input(f"FRebound {h}", 0, 40, d_vals[3], key=f"fr_{h}_{ukey}")

with tabs[5]: # AERO
    a1, a2 = st.columns(2)
    with a1:
        st.text_input("Ride Height Front", "48", key=f"frh_{ukey}")
        st.text_input("Splitter", "0", key=f"spl_{ukey}")
        st.text_input("Brake Ducts Front", "2", key=f"bdf_{ukey}")
    with a2:
        st.text_input("Ride Height Rear", "68", key=f"rrh_{ukey}")
        st.number_input("Rear Wing", 0, 20, wing_v, key=f"wing_{ukey}")
        st.text_input("Brake Ducts Rear", "2", key=f"bdr_{ukey}")

# --- OPSLAG ---
st.divider()
if st.button("💾 Sla Setup op"):
    st.success("Setup opgeslagen in tijdelijk geheugen!")
