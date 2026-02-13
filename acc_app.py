import streamlit as st

st.set_page_config(page_title="ACC Ultimate Setup Master & Dokter", layout="wide")

# --- DATABASE PER AUTO (GT3 2024) ---
car_db = {
    "Ferrari 296 GT3": {"motor": "Mid", "bb": "54.2", "wing": 8, "arb": "4/2", "diff": 80, "damp": [5, 10, 7, 12], "tips": "Stabiel platform, focus op aero-rake."},
    "Porsche 911 GT3 R (992)": {"motor": "Rear", "bb": "50.2", "wing": 10, "arb": "3/4", "diff": 120, "damp": [3, 8, 10, 14], "tips": "Motor achterin. Pas op voor lift-off oversteer."},
    "BMW M4 GT3": {"motor": "Front", "bb": "57.5", "wing": 5, "arb": "6/1", "diff": 40, "damp": [8, 12, 5, 9], "tips": "Kan agressief over curbs rijden."},
    "Lamborghini EVO2": {"motor": "Mid", "bb": "55.2", "wing": 9, "arb": "4/3", "diff": 90, "damp": [4, 9, 8, 12], "tips": "Goede rotatie, gevoelig op de achterbanden."},
    "McLaren 720S GT3 Evo": {"motor": "Mid", "bb": "53.2", "wing": 7, "arb": "3/2", "diff": 70, "damp": [6, 11, 7, 11], "tips": "Focus op splitter-efficiency."},
    "Mercedes-AMG GT3 Evo": {"motor": "Front", "bb": "56.8", "wing": 6, "arb": "5/2", "diff": 65, "damp": [7, 13, 6, 10], "tips": "Focus op tractie uit de bocht."},
    "Audi R8 LMS EVO II": {"motor": "Mid", "bb": "54.0", "wing": 8, "arb": "4/4", "diff": 110, "damp": [4, 8, 9, 13], "tips": "Nerveus bij hard remmen."},
    "Aston Martin Vantage EVO": {"motor": "Front", "bb": "56.2", "wing": 6, "arb": "4/2", "diff": 55, "damp": [6, 12, 6, 10], "tips": "Zeer voorspelbaar weggedrag."},
    "Ford Mustang GT3": {"motor": "Front", "bb": "57.0", "wing": 7, "arb": "5/2", "diff": 50, "damp": [7, 11, 5, 9], "tips": "Nieuw voor 2024, krachtige motor."},
    "Corvette Z06 GT3.R": {"motor": "Mid", "bb": "54.8", "wing": 8, "arb": "4/3", "diff": 75, "damp": [5, 10, 8, 12], "tips": "Goede mechanische grip balans."}
}

# --- SIDEBAR: DE SETUP DOKTER ---
st.sidebar.header("🩺 De Setup Dokter")
st.sidebar.write("Wat doet de auto op de Xbox?")
klacht = st.sidebar.selectbox("Selecteer klacht:", [
    "Auto rijdt perfect",
    "Onderstuur (Bocht ingaan)",
    "Onderstuur (Bocht uitgaan)",
    "Overstuur (Bocht ingaan)",
    "Overstuur (Bocht uitgaan)",
    "Auto stuitert/springt over curbs",
    "Instabiel bij hard remmen",
    "Banden worden te heet (>27.0 PSI)"
])

if klacht != "Auto rijdt perfect":
    st.sidebar.warning("**Aanbevolen acties:**")
    if "Onderstuur" in klacht:
        st.sidebar.write("- ⚙️ Verlaag Front ARB")
        st.sidebar.write("- ✈️ Verhoog Rear Ride Height")
        st.sidebar.write("- ⚙️ Verhoog Bumpstop Range (Front)")
    elif "Overstuur" in klacht:
        st.sidebar.write("- ⚙️ Verlaag Rear ARB")
        st.sidebar.write("- ✈️ Verhoog Rear Wing")
        st.sidebar.write("- ⚡ Verhoog TC of TC2")
    elif "curbs" in klacht:
        st.sidebar.write("- ☁️ Verlaag Fast Bump (Dampers)")
        st.sidebar.write("- ⚙️ Verlaag Wheel Rate (Veren)")
    elif "remmen" in klacht:
        st.sidebar.write("- ⚙️ Verhoog Brake Bias naar voren")
        st.sidebar.write("- ⚙️ Verhoog Diff Preload")
    elif "PSI" in klacht:
        st.sidebar.write("- 🛞 Verlaag koude bandenspanning")
        st.sidebar.write("- ✈️ Open Brake Ducts (+1)")

# --- HOOFDSCHERM ---
st.title("🏎️ ACC Setup Master - GT3 2024")

col1, col2 = st.columns(2)
with col1:
    auto = st.selectbox("🚗 Kies Auto:", list(car_db.keys()))
with col2:
    circuit = st.selectbox("📍 Kies Circuit:", ["Spa", "Monza", "Zolder", "Zandvoort", "Nürburgring", "Kyalami", "Suzuka", "Mount Panorama"])

data = car_db[auto]
d = data["damp"]

tabs = st.tabs(["🛞 Tyres", "⚡ Electronics", "⛽ Fuel & Strategy", "⚙️ Mechanical Grip", "☁️ Dampers", "✈️ Aero"])

with tabs[0]: # TYRES
    c1, c2, c3, c4 = st.columns(4)
    for i, side in enumerate(["LF", "RF", "LR", "RR"]):
        with [c1, c2, c3, c4][i]:
            st.write(f"**{side}**")
            st.text_input("PSI", "26.5", key=f"p_{side}")
            st.text_input("Toe", "0.06", key=f"t_{side}")
            st.text_input("Camber", "-3.5", key=f"c_{side}")
            st.text_input("Caster", "8.0", key=f"ca_{side}")

with tabs[1]: # ELECTRONICS
    ce1, ce2 = st.columns(2)
    with ce1:
        st.number_input("TC", 0, 12, 3)
        st.number_input("TC2", 0, 12, 2)
    with ce2:
        st.number_input("ABS", 0, 12, 3)
        st.number_input("ECU Map", 1, 4, 1)

with tabs[3]: # MECHANICAL GRIP
    cm1, cm2 = st.columns(2)
    with cm1:
        st.write("**Front**")
        st.text_input("Anti-roll bar", data["arb"].split('/')[0])
        st.text_input("Brake Bias (%)", data["bb"])
        st.text_input("Steer Ratio", "13.0")
        st.text_input("Wheel Rate", "160")
        st.text_input("Bumpstop Rate", "500")
        st.text_input("Bumpstop Range", "20")
    with cm2:
        st.write("**Rear**")
        st.text_input("Anti-roll bar ", data["arb"].split('/')[1])
        st.text_input("Preload Differential", f"{data['diff']}Nm")
        st.text_input("Wheel Rate ", "130")
        st.text_input("Bumpstop Rate ", "400")
        st.text_input("Bumpstop Range ", "15")

with tabs[4]: # DAMPERS
    cd1, cd2, cd3, cd4 = st.columns(4)
    for i, hoek in enumerate(["LF", "RF", "LR", "RR"]):
        with [cd1, cd2, cd3, cd4][i]:
            st.write(f"**{hoek}**")
            st.number_input("Bump", 0, 40, d[0], key=f"b_{hoek}")
            st.number_input("Fast Bump", 0, 40, d[1], key=f"fb_{hoek}")
            st.number_input("Rebound", 0, 40, d[2], key=f"r_{hoek}")
            st.number_input("Fast Rebound", 0, 40, d[3], key=f"fr_{hoek}")

with tabs[5]: # AERO
    ca1, ca2 = st.columns(2)
    with ca1:
        st.write("**Front**")
        st.text_input("Ride Height", "50mm")
        st.text_input("Splitter", "0")
        st.text_input("Brake Ducts", "2")
    with ca2:
        st.write("**Rear**")
        st.text_input("Ride Height ", "70mm")
        st.number_input("Rear Wing", 0, 20, data["wing"])
        st.text_input("Brake Ducts ", "2")

st.sidebar.divider()
st.sidebar.info(f"💡 **Tip voor de {auto}:**\n{data['tips']}")
