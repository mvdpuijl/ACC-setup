import streamlit as st
import pandas as pd
import io

# 1. Pagina Configuratie
st.set_page_config(page_title="ACC Setup Master v9.47", layout="wide")

# Styling v9.40 (Grayscale Stealth - Geen Rood)
st.markdown("""<style>
    .stApp { background-color: #000000 !important; color: #FFFFFF !important; }
    [data-testid="stSidebar"] { background-color: #0A0C10 !important; }
    /* Tabs: v9.40 Stijl (Wit geselecteerd, geen rood) */
    .stTabs [aria-selected="true"] { 
        background-color: #333333 !important; 
        color: #FFFFFF !important; 
        border-radius: 4px; 
    }
    .stTabs [data-baseweb="tab-list"] { gap: 10px; }
    .stTabs [data-baseweb="tab"] { color: #888888; }
    /* Inputs en Selectboxen */
    .stSelectbox div[data-baseweb="select"]:focus-within { border: 1px solid #FFFFFF !important; }
    input { background-color: #111111 !important; color: #FFFFFF !important; border: 1px solid #333 !important; }
</style>""", unsafe_allow_html=True)

# 2. CORE DATABASE
cars_db = {
    "Ferrari 296 GT3": {"bb": 54.2, "diff": 80, "steer": 13.0, "f_cam": -3.5, "r_cam": -3.0, "f_toe": 0.06, "r_toe": 0.12, "caster": 12.5},
    "Porsche 911 GT3 R (992)": {"bb": 50.2, "diff": 120, "steer": 12.0, "f_cam": -3.8, "r_cam": -3.2, "f_toe": -0.04, "r_toe": 0.20, "caster": 13.2},
    "BMW M4 GT3": {"bb": 57.5, "diff": 40, "steer": 14.0, "f_cam": -3.2, "r_cam": -2.8, "f_toe": 0.05, "r_toe": 0.10, "caster": 11.8},
    "Lamborghini EVO2": {"bb": 55.2, "diff": 90, "steer": 13.0, "f_cam": -3.6, "r_cam": -3.1, "f_toe": 0.06, "r_toe": 0.14, "caster": 12.8},
    "McLaren 720S EVO": {"bb": 53.2, "diff": 70, "steer": 13.0, "f_cam": -3.5, "r_cam": -3.0, "f_toe": 0.06, "r_toe": 0.10, "caster": 12.0},
    "Mercedes AMG EVO": {"bb": 56.8, "diff": 65, "steer": 14.0, "f_cam": -3.4, "r_cam": -2.9, "f_toe": 0.07, "r_toe": 0.12, "caster": 13.5},
    "Audi R8 EVO II": {"bb": 54.0, "diff": 110, "steer": 13.0, "f_cam": -3.7, "r_cam": -3.1, "f_toe": 0.06, "r_toe": 0.11, "caster": 12.4},
    "Aston Martin EVO": {"bb": 56.2, "diff": 55, "steer": 14.0, "f_cam": -3.3, "r_cam": -2.8, "f_toe": 0.06, "r_toe": 0.10, "caster": 12.2},
    "Ford Mustang GT3": {"bb": 57.0, "diff": 50, "steer": 14.0, "f_cam": -3.5, "r_cam": -3.0, "f_toe": 0.06, "r_toe": 0.13, "caster": 12.0},
    "Corvette Z06 GT3.R": {"bb": 54.8, "diff": 75, "steer": 13.0, "f_cam": -3.5, "r_cam": -3.0, "f_toe": 0.06, "r_toe": 0.12, "caster": 12.6}
}

circ_db = {
    "High": ["Spa-Francorchamps", "Zandvoort", "Kyalami", "Barcelona", "Hungaroring", "Suzuka", "Nürburgring", "Misano", "Valencia"],
    "Low": ["Monza", "Paul Ricard", "Bathurst", "Silverstone", "Indianapolis", "Jeddah"],
    "Bumpy": ["Zolder", "Mount Panorama", "Laguna Seca", "Imola", "Watkins Glen", "Red Bull Ring"]
}

if 'history' not in st.session_state: st.session_state['history'] = []

# 3. SIDEBAR MASTER EXPORT LOGICA
def get_vals(a, c):
    car = cars_db[a]; ct = next((k for k, v in circ_db.items() if c in v), "High")
    if ct == "Low": p, w, bm, af, ar = "26.2", "2", 1.5, "5", "1"
    elif ct == "Bumpy": p, w, bm, af, ar = "26.6", "8", -0.5, "3", "2"
    else: p, w, bm, af, ar = "26.8", "11", 0.0, "4", "3"
    return {"Auto": a, "Circuit": c, "Type": ct, "PSI": p, "Wing": w, "BB": car["bb"]+bm, 
            "Steer": car["steer"], "F-Toe": car["f_toe"], "F-Cam": car["f_cam"], "Caster": car["caster"]}

st.sidebar.header("Master Database")
if st.sidebar.button("Genereer Alle Combinaties"):
    rows = [get_vals(a, c) for c in [i for s in circ_db.values() for i in s] for a in cars_db.keys()]
    df_bulk = pd.DataFrame(rows)
    buf = io.BytesIO()
    with pd.ExcelWriter(buf, engine='xlsxwriter') as wr:
        df_bulk.to_excel(wr, index=False)
    st.sidebar.download_button("Download Master Excel", data=buf.getvalue(), file_name="ACC_Master.xlsx")

# 4. HOOFD INTERFACE
st.title("ACC Master v9.47")
ca, cc = st.columns(2)
with ca: auto = st.selectbox("Auto:", list(cars_db.keys()))
with cc: 
    alist = sorted([c for sub in circ_db.values() for c in sub])
    circuit = st.selectbox("Circuit:", alist)

car = cars_db[auto]
ctype = next((k for k, v in circ_db.items() if circuit in v), "High")

# ENGINEER LOGICA
if ctype == "Low":
    psi, wing, bb_m, af, ar, dmp = "26.2", "2", 1.5, "5", "1", ["4", "9", "7", "11"]
    hf, hr, spl, bd = "45", "62", "0", "1"
elif ctype == "Bumpy":
    psi, wing, bb_m, af, ar, dmp = "26.6", "8", -0.5, "3", "2", ["8", "15", "6", "10"]
    hf, hr, spl, bd = "52", "75", "2", "3"
else:
    psi, wing, bb_m, af, ar, dmp = "26.8", "11", 0.0, "4", "3", ["5", "10", "8", "12"]
    hf, hr, spl, bd = "48", "68", "0", "2"

uk = f"{auto}_{circuit}".replace(" ", "")

# SIDEBAR DOKTER
st.sidebar.divider()
st.sidebar.header("Setup Dokter")
kl = st.sidebar.selectbox("Klacht?", ["Geen", "Onderstuur", "Overstuur", "Curbs"], key=f"dr_{uk}")
if kl != "Geen":
    if kl == "Onderstuur": st.sidebar.info(f"F-ARB naar {int(af)-1}")
    elif kl == "Overstuur": st.sidebar.info(f"R-ARB naar {int(ar)-1}")
    elif kl == "Curbs": st.sidebar.info("RH +2mm")

# 5. TABS
t = st.tabs(["Tyres", "Electronics", "Fuel", "Mechanical", "Dampers", "Aero"])

with t[0]: # TYRES
    c1, c2 = st.columns(2)
    with c1:
        st.write("**Front**")
        lf_p = st.text_input("LF PSI", psi, key=f"lp_{uk}"); rf_p = st.text_input("RF PSI", psi, key=f"rp_{uk}")
        ft = st.text_input("F-Toe", str(car["f_toe"]), key=f"ft_{uk}"); fc = st.text_input("F-Cam", str(car["f_cam"]), key=f"fc_{uk}")
        cs = st.text_input("Caster", str(car["caster"]), key=f"cs_{uk}")
    with c2:
        st.write("**Rear**")
        lr_p = st.text_input("LR PSI", psi, key=f"lr_{uk}"); rr_p = st.text_input("RR PSI", psi, key=f"rr_{uk}")
        rt = st.text_input("R-Toe", str(car["r_toe"]), key=f"rt_{uk}"); rc = st.text_input("R-Cam", str(car["r_cam"]), key=f"rc_{uk}")

with t[1]: # ELECTRONICS
    e1, e2 = st.columns(2)
    tc1 = e1.text_input("TC1", "3", key=f"t1_{uk}"); tc2 = e1.text_input("TC2", "3", key=f"t2_{uk}")
    absv = e2.text_input("ABS", "3", key=f"ab_{uk}"); ecum = e2.text_input("ECU Map", "1", key=f"ec_{uk}")

with t[3]: # MECHANICAL
    m1, m2 = st.columns(2)
    farb = m1.text_input("F-ARB", af, key=f"fa_{uk}"); bb_v = m1.text_input("BB", str(car["bb"] + bb_m), key=f"bb_{uk}")
    rarb = m2.text_input("R-ARB", ar, key=f"ra_{uk}"); ster = m2.text_input("Steer", str(car["steer"]), key=f"st_{uk}")

with t[4]: # DAMPERS
    cols, lbls = st.columns(4), ["LF", "RF", "LR", "RR"]
    for i, col in enumerate(cols):
        with col:
            st.write(f"**{lbls[i]}**")
            st.text_input("Bump", dmp[0], key=f"b{i}_{uk}"); st.text_input("F-Bump", dmp[1], key=f"f{i}_{uk}")
            st.text_input("Reb", dmp[2], key=f"r{i}_{uk}"); st.text_input("F-Reb", dmp[3], key=f"g{i}_{uk}")

with t[5]: # AERO
    a1, a2 = st.columns(2)
    rhf = a1.text_input("RH F", hf, key=f"hf_{uk}"); spli = a1.text_input("Split", spl, key=f"sp_{uk}")
    rhr = a2.text_input("RH R", hr, key=f"hr_{uk}"); wng = a2.text_input("Wing", wing, key=f"w_{uk}")

# 6. OPSLAG
st.divider()
if st.button("Sla Setup op"):
    st.session_state['history'].append({"Auto": auto, "Circ": circuit, "BB": bb_v, "Wing": wng})
    st.success("Opgeslagen!")

if st.session_state['history']:
    df_h = pd.DataFrame(st.session_state['history'])
    st.table(df_h)
