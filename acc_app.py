import streamlit as st
import pandas as pd

# 1. Pagina Configuratie
st.set_page_config(page_title="ACC Setup Master v9.36", layout="wide")

# Styling v9.14 (Stealth)
st.markdown("""<style>.stTabs [data-baseweb="tab-list"] { gap: 8px; }
.stTabs [aria-selected="true"] { background-color: #ff4b4b !important; color: white !important; }</style>""", unsafe_allow_html=True)

# 2. DATABASE
cars_db = {
    "Ferrari 296 GT3": {"bb": 54.2, "diff": 80, "steer": 13.0, "f_cam": -3.5, "r_cam": -3.0, "tips": "Aero-rake focus."},
    "Porsche 911 GT3 R (992)": {"bb": 50.2, "diff": 120, "steer": 12.0, "f_cam": -3.8, "r_cam": -3.2, "tips": "Beheer lift-off."},
    "BMW M4 GT3": {"bb": 57.5, "diff": 40, "steer": 14.0, "f_cam": -3.2, "r_cam": -2.8, "tips": "Sterk op curbs."},
    "Lamborghini EVO2": {"bb": 55.2, "diff": 90, "steer": 13.0, "f_cam": -3.6, "r_cam": -3.1, "tips": "Mech-grip."},
    "McLaren 720S EVO": {"bb": 53.2, "diff": 70, "steer": 13.0, "f_cam": -3.5, "r_cam": -3.0, "tips": "Aero-gevoelig."},
    "Mercedes AMG EVO": {"bb": 56.8, "diff": 65, "steer": 14.0, "f_cam": -3.4, "r_cam": -2.9, "tips": "Focus op tractie."},
    "Audi R8 EVO II": {"bb": 54.0, "diff": 110, "steer": 13.0, "f_cam": -3.7, "r_cam": -3.1, "tips": "Nerveus remmen."},
    "Aston Martin EVO": {"bb": 56.2, "diff": 55, "steer": 14.0, "f_cam": -3.3, "r_cam": -2.8, "tips": "Stabiel."},
    "Ford Mustang GT3": {"bb": 57.0, "diff": 50, "steer": 14.0, "f_cam": -3.5, "r_cam": -3.0, "tips": "Veel koppel."},
    "Corvette Z06 GT3.R": {"bb": 54.8, "diff": 75, "steer": 13.0, "f_cam": -3.5, "r_cam": -3.0, "tips": "Goede balans."}
}

circuits_db = {
    "High Downforce": ["Spa-Francorchamps", "Zandvoort", "Kyalami", "Barcelona", "Hungaroring", "Suzuka", "Nürburgring"],
    "Low Downforce": ["Monza", "Paul Ricard", "Bathurst", "Silverstone"],
    "Street/Bumpy": ["Zolder", "Mount Panorama", "Laguna Seca", "Imola"]
}

if 'history' not in st.session_state: st.session_state['history'] = []

# 3. SELECTIE
st.title("🏎️ ACC Master v9.36")
col_a, col_c = st.columns(2)
with col_a: auto = st.selectbox("🚗 Auto:", list(cars_db.keys()))
with col_c: 
    clist = sorted([c for sub in circuits_db.values() for c in sub])
    circuit = st.selectbox("📍 Circuit:", clist)

car = cars_db[auto]
ctype = next((k for k, v in circuits_db.items() if circuit in v), "High Downforce")

if ctype == "Low Downforce":
    psi, wing, bb_m, af, ar, dmp = "26.2", "2", 1.5, "5", "1", ["4", "9", "7", "11"]
    hf, hr, spl, bd = "45", "62", "0", "1"
elif ctype == "Street/Bumpy":
    psi, wing, bb_m, af, ar, dmp = "26.6", "8", -0.5, "3", "2", ["8", "15", "6", "10"]
    hf, hr, spl, bd = "52", "75", "2", "3"
else:
    psi, wing, bb_m, af, ar, dmp = "26.8", "11", 0.0, "4", "3", ["5", "10", "8", "12"]
    hf, hr, spl, bd = "48", "68", "0", "2"

u = f"{auto[:3]}{circuit[:3]}".replace(" ", "")

# 4. SIDEBAR - SETUP DOKTER
st.sidebar.header("🩺 Setup Dokter")
klacht = st.sidebar.selectbox("Klacht?", ["Geen", "Onderstuur", "Overstuur", "Curbs"], key=f"dr_{u}")
if klacht != "Geen":
    if klacht == "Onderstuur":
        st.sidebar.warning(f"Verlaag F-ARB naar {int(af)-1}")
    elif klacht == "Overstuur":
        st.sidebar.warning(f"Verlaag R-ARB naar {int(ar)-1}")
    elif klacht == "Curbs":
        st.sidebar.warning("Verhoog Rijhoogte +2mm")
st.sidebar.info(f"💡 Tip: {car['tips']}")

# 5. TABS
tabs = st.tabs(["🛞 Tyres", "⚡ Electronics", "⛽ Fuel", "⚙️ Mechanical", "☁️ Dampers", "✈️ Aero"])

with tabs[0]: # Tyres
    c1, c2 = st.columns(2)
    with c1:
        st.text_input("LF PSI", psi, key=f"lp_{u}")
        st.text_input("F-Cam", str(car["f_cam"]), key=f"fc_{u}")
    with c2:
        st.text_input("RR PSI", psi, key=f"rp_{u}")
        st.text_input("R-Cam", str(car["r_cam"]), key=f"rc_{u}")

with tabs[1]: # Electronics
    e1, e2 = st.columns(2)
    with e1:
        tc1 = st.text_input("TC1", "3", key=f"t1_{u}")
        tc2 = st.text_input("TC2", "3", key=f"t2_{u}")
    with e2:
        abs_v = st.text_input("ABS", "3", key=f"ab_{u}")
        ecu = st.text_input("ECU Map", "1", key=f"ec_{u}")

with tabs[3]: # Mechanical
    m1, m2 = st.columns(2)
    with m1:
        st.text_input("F-ARB", af, key=f"fa_{u}")
        st.text_input("BB", str(car["bb"] + bb_m), key=f"bb_{u}")
    with m2:
        st.text_input("R-ARB", ar, key=f"ra_{u}")
        st.text_input("Steer", str(car["steer"]), key=f"st_{u}")

with tabs[4]: # Dampers
    d1, d2, d3, d4 = st.columns(4)
    cols = [d1, d2, d3, d4]
    lbls = ["LF", "RF", "LR", "RR"]
    for i in range(4):
        with cols[i]:
            st.write(f"**{lbls[i]}**")
            st.text_input("Bump", dmp[0], key=f"b{i}_{u}")
            st.text_input("F-Bump", dmp[1], key=f"fb{i}_{u}")
            st.text_input("Reb", dmp[2], key=f"r{i}_{u}")
            st.text_input("F-Reb", dmp[3], key=f"fr{i}_{u}")

with tabs[5]: # Aero
    a1, a2 = st.columns(2)
    with a1:
        st.text_input("RH F", hf, key=f"hf_{u}")
        st.text_input("Splitter", spl, key=f"sp_{u}")
    with a2:
        st.text_input("RH R", hr, key=f"hr_{u}")
        st.text_input("Wing", wing, key=f"wi_{u}")

# 6. OPSLAG
st.divider()
if st.button("💾 Sla Setup op"):
    st.session_state['history'].append({"Auto": auto, "Circuit": circuit, "TC1": tc1, "Wing": wing})
    st.success("Setup opgeslagen!")

if st.session_state['history']:
    df = pd.DataFrame(st.session_state['history'])
    st.download_button("📥 CSV", data=df.to_csv(index=False).encode('utf-8'), file_name='acc.csv')
    st.table(df)
