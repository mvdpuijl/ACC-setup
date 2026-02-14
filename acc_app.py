import streamlit as st
import pandas as pd
import io

# 1. Pagina Configuratie (Strikt v9.41)
st.set_page_config(page_title="ACC Setup Master v9.55", layout="wide")

# Styling v9.41 (Grayscale Stealth)
st.markdown("""<style>
    .stApp { background-color: #000000; color: #FFFFFF; }
    [data-testid="stSidebar"] { background-color: #0A0C10; }
    .stTabs [aria-selected="true"] { background-color: #333333 !important; color: #FFFFFF !important; border-bottom: 2px solid #FFFFFF !important; }
    .stTabs [data-baseweb="tab"] { color: #888888; }
    input { background-color: #111111 !important; color: #FFFFFF !important; border: 1px solid #333 !important; }
    .stButton>button { border: 1px solid #444; background-color: #000; color: #fff; width: 100%; }
</style>""", unsafe_allow_html=True)

# 2. DATABASE (v9.41 structuur + Mercedes Evo data)
cars_db = {
    "Mercedes AMG EVO": {"bb": 56.8, "diff": 65, "steer": 14.0, "f_cam": -3.4, "r_cam": -2.9, "f_toe": 0.07, "r_toe": 0.12, "caster": 13.5, "tips": "Front-engine: focus op tractie en stabiel remmen."},
    "Ferrari 296 GT3": {"bb": 54.2, "diff": 80, "steer": 13.0, "f_cam": -3.5, "r_cam": -3.0, "f_toe": 0.06, "r_toe": 0.12, "caster": 12.5, "tips": "Aero-rake focus."},
    "Porsche 911 GT3 R (992)": {"bb": 50.2, "diff": 120, "steer": 12.0, "f_cam": -3.8, "r_cam": -3.2, "f_toe": -0.04, "r_toe": 0.20, "caster": 13.2, "tips": "Beheer lift-off overstuur."},
    "BMW M4 GT3": {"bb": 57.5, "diff": 40, "steer": 14.0, "f_cam": -3.2, "r_cam": -2.8, "f_toe": 0.05, "r_toe": 0.10, "caster": 11.8, "tips": "Sterk op curbs."},
    "Lamborghini EVO2": {"bb": 55.2, "diff": 90, "steer": 13.0, "f_cam": -3.6, "r_cam": -3.1, "f_toe": 0.06, "r_toe": 0.14, "caster": 12.8, "tips": "Mechanische grip focus."},
    "Audi R8 EVO II": {"bb": 54.0, "diff": 110, "steer": 13.0, "f_cam": -3.7, "r_cam": -3.1, "f_toe": 0.06, "r_toe": 0.11, "caster": 12.4, "tips": "Nerveus bij remmen."},
    "Aston Martin EVO": {"bb": 56.2, "diff": 55, "steer": 14.0, "f_cam": -3.3, "r_cam": -2.8, "f_toe": 0.06, "r_toe": 0.10, "caster": 12.2, "tips": "Zeer stabiel platform."},
}

circuits_db = {
    "High Downforce": ["Spa-Francorchamps", "Zandvoort", "Kyalami", "Barcelona", "Hungaroring", "Suzuka", "Nürburgring"],
    "Low Downforce": ["Monza", "Paul Ricard", "Bathurst", "Silverstone"],
    "Street/Bumpy": ["Zolder", "Mount Panorama", "Laguna Seca", "Imola"]
}

if 'history' not in st.session_state: st.session_state['history'] = []

# 3. SELECTIE
st.title("🏎️ ACC Master v9.55")
col_a, col_c = st.columns(2)
with col_a: auto = st.selectbox("🚗 Auto:", list(cars_db.keys()))
with col_c: 
    clist = sorted([c for sub in circuits_db.values() for c in sub])
    circuit = st.selectbox("📍 Circuit:", clist)

car = cars_db[auto]
ctype = next((k for k, v in circuits_db.items() if circuit in v), "High Downforce")

# v9.41 ENGINEER LOGICA
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
    if klacht == "Onderstuur": st.sidebar.warning(f"F-ARB naar {int(af)-1}")
    elif klacht == "Overstuur": st.sidebar.warning(f"R-ARB naar {int(ar)-1}")
    elif klacht == "Curbs": st.sidebar.warning("RH +2mm")
st.sidebar.info(f"💡 Tip: {car['tips']}")

# 5. TABS (Exact v9.41 Hersteld)
tabs = st.tabs(["🛞 Tyres", "⚡ Electronics", "⛽ Fuel", "⚙️ Mechanical", "☁️ Dampers", "✈️ Aero"])

with tabs[0]: # Tyres + Alignment
    c1, c2 = st.columns(2)
    with c1:
        st.write("**Front**")
        lf_p = st.text_input("LF PSI", psi, key=f"lp_{u}")
        rf_p = st.text_input("RF PSI", psi, key=f"rp_{u}")
        st.text_input("F-Toe", str(car["f_toe"]), key=f"ft_{u}")
        st.text_input("F-Cam", str(car["f_cam"]), key=f"fc_{u}")
        st.text_input("Caster", str(car["caster"]), key=f"cs_{u}")
    with c2:
        st.write("**Rear**")
        lr_p = st.text_input("LR PSI", psi, key=f"lr_{u}")
        rr_p = st.text_input("RR PSI", psi, key=f"rr_{u}")
        st.text_input("R-Toe", str(car["r_toe"]), key=f"rt_{u}")
        st.text_input("R-Cam", str(car["r_cam"]), key=f"rc_{u}")

with tabs[1]: # Electronics
    e1, e2 = st.columns(2)
    tc1 = e1.text_input("TC1", "3", key=f"t1_{u}")
    tc2 = e1.text_input("TC2", "3", key=f"t2_{u}")
    abs_v = e2.text_input("ABS", "3", key=f"ab_{u}")
    ecu = e2.text_input("ECU Map", "1", key=f"ec_{u}")

with tabs[2]: # Fuel
    st.text_input("Fuel (L)", "60", key=f"fu_{u}")
    st.checkbox("Strategy 1 (Safe)", value=True, key=f"s1_{u}")

with tabs[3]: # Mechanical
    m1, m2 = st.columns(2)
    with m1:
        st.text_input("F-ARB", af, key=f"fa_{u}")
        st.text_input("BB", str(car["bb"] + bb_m), key=f"bb_{u}")
    with m2:
        st.text_input("R-ARB", ar, key=f"ra_{u}")
        st.text_input("Steer Ratio", str(car["steer"]), key=f"st_{u}")

with tabs[4]: # Dampers
    [Image of a racing car damper showing bump and rebound internal components]
    d1, d2, d3, d4 = st.columns(4)
    cols, lbls = [d1, d2, d3, d4], ["LF", "RF", "LR", "RR"]
    for i in range(4):
        with cols[i]:
            st.write(f"**{lbls[i]}**")
            st.text_input("Bump", dmp[0], key=f"b{i}_{u}")
            st.text_input("F-Bump", dmp[1], key=f"f{i}_{u}")
            st.text_input("Reb", dmp[2], key=f"r{i}_{u}")
            st.text_input("F-Reb", dmp[3], key=f"g{i}_{u}")

with tabs[5]: # Aero
    a1, a2 = st.columns(2)
    with a1:
        st.text_input("RH F", hf, key=f"hf_{u}")
        st.text_input("Splitter", spl, key=f"sp_{uk}")
    with a2:
        st.text_input("RH R", hr, key=f"hr_{u}")
        st.text_input("Wing", wing, key=f"wi_{u}")

# 6. OPSLAG & EXCEL EXPORT
st.divider()
if st.button("💾 Sla Setup op"):
    st.session_state['history'].append({"Auto": auto, "Circ": circuit, "TC1": tc1, "BB": str(car["bb"] + bb_m), "Wing": wing})
    st.success("Opgeslagen!")

if st.session_state['history']:
    df = pd.DataFrame(st.session_state['history'])
    buf = io.BytesIO()
    with pd.ExcelWriter(buf, engine='xlsxwriter') as writer:
        df.to_excel(writer, index=False)
    st.download_button("📥 Excel Download", data=buf.getvalue(), file_name="acc_setups.xlsx")
    st.table(df)
