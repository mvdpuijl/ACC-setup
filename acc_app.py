import streamlit as st
import pandas as pd
import io

st.set_page_config(page_title="ACC Setup Master v9.38", layout="wide")

st.markdown("""<style>.stTabs [aria-selected="true"] { background-color: #ff4b4b !important; }</style>""", unsafe_allow_html=True)

# DATABASE
cars_db = {
    "Ferrari 296 GT3": {"bb": 54.2, "diff": 80, "steer": 13.0, "f_cam": -3.5, "r_cam": -3.0},
    "Porsche 911 GT3 R (992)": {"bb": 50.2, "diff": 120, "steer": 12.0, "f_cam": -3.8, "r_cam": -3.2},
    "BMW M4 GT3": {"bb": 57.5, "diff": 40, "steer": 14.0, "f_cam": -3.2, "r_cam": -2.8},
    "Lamborghini EVO2": {"bb": 55.2, "diff": 90, "steer": 13.0, "f_cam": -3.6, "r_cam": -3.1},
    "McLaren 720S EVO": {"bb": 53.2, "diff": 70, "steer": 13.0, "f_cam": -3.5, "r_cam": -3.0},
    "Mercedes AMG EVO": {"bb": 56.8, "diff": 65, "steer": 14.0, "f_cam": -3.4, "r_cam": -2.9},
    "Audi R8 EVO II": {"bb": 54.0, "diff": 110, "steer": 13.0, "f_cam": -3.7, "r_cam": -3.1},
    "Aston Martin EVO": {"bb": 56.2, "diff": 55, "steer": 14.0, "f_cam": -3.3, "r_cam": -2.8},
    "Ford Mustang GT3": {"bb": 57.0, "diff": 50, "steer": 14.0, "f_cam": -3.5, "r_cam": -3.0},
    "Corvette Z06 GT3.R": {"bb": 54.8, "diff": 75, "steer": 13.0, "f_cam": -3.5, "r_cam": -3.0}
}

circuits_db = {"High": ["Spa-Francorchamps", "Zandvoort", "Suzuka"], "Low": ["Monza", "Silverstone"], "Bumpy": ["Zolder", "Imola"]}

if 'history' not in st.session_state: st.session_state['history'] = []

# SELECTIE
st.title("🏎️ ACC Master v9.38")
c_a, c_c = st.columns(2)
with c_a: auto = st.selectbox("🚗 Auto:", list(cars_db.keys()))
with c_c: 
    clist = sorted([c for sub in circuits_db.values() for c in sub])
    circuit = st.selectbox("📍 Circuit:", clist)

car = cars_db[auto]
ctype = next((k for k, v in circuits_db.items() if circuit in v), "High")

if ctype == "Low":
    psi, wing, bb_m, af, ar, dmp = "26.2", "2", 1.5, "5", "1", ["4", "9", "7", "11"]
    hf, hr, spl, bd = "45", "62", "0", "1"
elif ctype == "Bumpy":
    psi, wing, bb_m, af, ar, dmp = "26.6", "8", -0.5, "3", "2", ["8", "15", "6", "10"]
    hf, hr, spl, bd = "52", "75", "2", "3"
else:
    psi, wing, bb_m, af, ar, dmp = "26.8", "11", 0.0, "4", "3", ["5", "10", "8", "12"]
    hf, hr, spl, bd = "48", "68", "0", "2"

u = f"{auto[:3]}{circuit[:3]}".replace(" ", "")

# SIDEBAR DOKTER
st.sidebar.header("🩺 Dokter")
klacht = st.sidebar.selectbox("Klacht?", ["Geen", "Onderstuur", "Overstuur", "Curbs"], key=f"dr_{u}")
if klacht != "Geen":
    if klacht == "Onderstuur": st.sidebar.warning(f"F-ARB naar {int(af)-1}")
    elif klacht == "Overstuur": st.sidebar.warning(f"R-ARB naar {int(ar)-1}")
    elif klacht == "Curbs": st.sidebar.warning("RH +2mm")

# TABS
tabs = st.tabs(["🛞 Tyres", "⚡ Electronics", "⛽ Fuel", "⚙️ Mechanical", "☁️ Dampers", "✈️ Aero"])

with tabs[0]:
    c1, c2 = st.columns(2)
    lf_p = c1.text_input("LF PSI", psi, key=f"lp_{u}"); rf_p = c1.text_input("RF PSI", psi, key=f"rp_{u}")
    lr_p = c2.text_input("LR PSI", psi, key=f"lr_{u}"); rr_p = c2.text_input("RR PSI", psi, key=f"rr_{u}")

with tabs[1]:
    e1, e2 = st.columns(2)
    tc1 = e1.text_input("TC1", "3", key=f"t1_{u}"); tc2 = e1.text_input("TC2", "3", key=f"t2_{u}")
    abs_v = e2.text_input("ABS", "3", key=f"ab_{u}"); ecu = e2.text_input("ECU", "1", key=f"ec_{u}")

with tabs[3]:
    m1, m2 = st.columns(2)
    farb = m1.text_input("F-ARB", af, key=f"fa_{u}"); bb = m1.text_input("BB", str(car["bb"]+bb_m), key=f"bb_{u}")
    rarb = m2.text_input("R-ARB", ar, key=f"ra_{u}"); str_r = m2.text_input("Steer", str(car["steer"]), key=f"st_{u}")

with tabs[4]:
    cols = st.columns(4); lbls = ["LF", "RF", "LR", "RR"]
    for i, col in enumerate(cols):
        with col:
            st.write(f"**{lbls[i]}**")
            st.text_input("Bump", dmp[0], key=f"b{i}_{u}"); st.text_input("Reb", dmp[2], key=f"r{i}_{u}")

with tabs[5]:
    a1, a2 = st.columns(2)
    rhf = a1.text_input("RH F", hf, key=f"hf_{u}"); spl = a1.text_input("Splitter", spl, key=f"sp_{u}")
    rhr = a2.text_input("RH R", hr, key=f"hr_{u}"); wng = a2.text_input("Wing", wing, key=f"w_{u}")

# OPSLAG LOGICA (Alle velden)
st.divider()
if st.button("💾 Sla Setup op"):
    data = {
        "Auto": auto, "Circuit": circuit, "LF_PSI": lf_p, "RF_PSI": rf_p, "LR_PSI": lr_p, "RR_PSI": rr_p,
        "TC1": tc1, "TC2": tc2, "ABS": abs_v, "ECU": ecu, "F_ARB": farb, "R_ARB": rarb, "BB": bb,
        "Steer": str_r, "RH_F": rhf, "RH_R": rhr, "Splitter": spl, "Wing": wng
    }
    st.session_state['history'].append(data)
    st.success("Volledige setup opgeslagen!")

if st.session_state['history']:
    df = pd.DataFrame(st.session_state['history'])
    buf = io.BytesIO()
    with pd.ExcelWriter(buf, engine='xlsxwriter') as wr:
        df.to_excel(wr, index=False)
    st.download_button("📥 Download Volledige Excel", data=buf.getvalue(), file_name="acc_full_setups.xlsx")
    st.table(df)
