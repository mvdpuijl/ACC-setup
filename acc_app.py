import streamlit as st
import pandas as pd
import io

# 1. Pagina Configuratie
st.set_page_config(page_title="ACC Setup Master v9.45", layout="wide")

# Styling Stealth
st.markdown("""<style>
    .stApp { background-color: #000000; color: #FFFFFF; }
    [data-testid="stSidebar"] { background-color: #0A0C10; }
    .stTabs [aria-selected="true"] { background-color: #ff4b4b !important; color: white !important; }
</style>""", unsafe_allow_html=True)

# 2. CORE DATABASE (Volledige DNA per auto)
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

# 3. HELPER FUNCTIE VOOR BULK EXPORT
def get_values(a_name, c_name):
    car = cars_db[a_name]
    ctype = next((k for k, v in circ_db.items() if c_name in v), "High")
    if ctype == "Low": p, w, bm, af, ar = "26.2", "2", 1.5, "5", "1"
    elif ctype == "Bumpy": p, w, bm, af, ar = "26.6", "8", -0.5, "3", "2"
    else: p, w, bm, af, ar = "26.8", "11", 0.0, "4", "3"
    return {"Auto": a_name, "Circuit": c_name, "Type": ctype, "PSI": p, "Wing": w, 
            "BB": car["bb"]+bm, "Steer": car["steer"], "F-Toe": car["f_toe"], 
            "F-Cam": car["f_cam"], "Caster": car["caster"], "F-ARB": af, "R-ARB": ar}

# 4. SIDEBAR - MASTER DATABASE & DOKTER
st.sidebar.header("📊 Master Database")
if st.sidebar.button("Genereer Alle Combinaties"):
    master_rows = [get_values(a, c) for c in [i for s in circ_db.values() for i in s] for a in cars_db.keys()]
    df_bulk = pd.DataFrame(master_rows)
    buf = io.BytesIO()
    with pd.ExcelWriter(buf, engine='xlsxwriter') as wr:
        df_bulk.to_excel(wr, index=False)
    st.sidebar.download_button("📥 Download Master Excel", data=buf.getvalue(), file_name="ACC_Master_DB.xlsx")

# 5. INDIVIDUELE SELECTIE
st.title("🏎️ ACC Master v9.45")
col_a, col_c = st.columns(2)
with col_a: auto = st.selectbox("🚗 Kies Auto:", list(cars_db.keys()))
with col_c: 
    all_c = sorted([c for sub in circ_db.values() for c in sub])
    circuit = st.selectbox("📍 Kies Circuit:", all_c)

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

# SETUP DOKTER (Sidebar)
st.sidebar.divider()
kl = st.sidebar.selectbox("🩺 Klacht?", ["Geen", "Onderstuur", "Overstuur", "Curbs"], key=f"dr_{uk}")
if kl != "Geen":
    if kl == "Onderstuur": st.sidebar.warning(f"F-ARB naar {int(af)-1}")
    elif kl == "Overstuur": st.sidebar.warning(f"R-ARB naar {int(ar)-1}")
    elif kl == "Curbs": st.sidebar.warning("RH +2mm")

# 6. TABS (V9.40 Interface)
tabs = st.tabs(["🛞 Tyres", "⚡ Electronics", "⛽ Fuel", "⚙️ Mechanical", "☁️ Dampers", "✈️ Aero"])

with tabs[0]: # Tyres + Alignment
    c1, c2 = st.columns(2)
    with c1:
        st.write("**Front**")
        lf_p = st.text_input("LF PSI", psi, key=f"lp_{uk}"); rf_p = st.text_input("RF PSI", psi, key=f"rp_{uk}")
        ftoe = st.text_input("F-Toe", str(car["f_toe"]), key=f"ft_{uk}"); fcam = st.text_input("F-Cam", str(car["f_cam"]), key=f"fc_{uk}")
        cast = st.text_input("Caster", str(car["caster"]), key=f"cs_{uk}")
    with c2:
        st.write("**Rear**")
        lr_p = st.text_input("LR PSI", psi, key=f"lr_{uk}"); rr_p = st.text_input("RR PSI", psi, key=f"rr_{uk}")
        rtoe = st.text_input("R-Toe", str(car["r_toe"]), key=f"rt_{uk}"); rcam = st.text_input("R-Cam", str(car["r_cam"]), key=f"rc_{uk}")

with tabs[1]: # Electronics
    e1, e2 = st.columns(2)
    tc1 = e1.text_input("TC1", "3", key=f"t1_{uk}"); tc2 = e1.text_input("TC2", "3", key=f"t2_{uk}")
    absv = e2.text_input("ABS", "3", key=f"ab_{uk}"); ecum = e2.text_input("ECU", "1", key=f"ec_{uk}")

with tabs[3]: # Mechanical
    m1, m2 = st.columns(2)
    farb = m1.text_input("F-ARB", af, key=f"fa_{uk}"); bb_v = m1.text_input("BB", str(car["bb"] + bb_m), key=f"bb_{uk}")
    rarb = m2.text_input("R-ARB", ar, key=f"ra_{uk}"); ster = m2.text_input("Steer", str(car["steer"]), key=f"st_{uk}")

with tabs[4]: # Dampers
    cols, lbls = st.columns(4), ["LF", "RF", "LR", "RR"]
    for i, col in enumerate(cols):
        with col:
            st.write(f"**{lbls[i]}**")
            st.text_input("Bump", dmp[0], key=f"b{i}_{uk}"); st.text_input("F-Bump", dmp[1], key=f"f{i}_{uk}")
            st.text_input("Reb", dmp[2], key=f"r{i}_{uk}"); st.text_input("F-Reb", dmp[3], key=f"g{i}_{uk}")

with tabs[5]: # Aero
    a1, a2 = st.columns(2)
    rh_f = a1.text_input("RH F", hf, key=f"hf_{uk}"); spli = a1.text_input("Split", spl, key=f"sp_{uk}")
    rh_r = a2.text_input("RH R", hr, key=f"hr_{uk}"); wing_v = a2.text_input("Wing", wing, key=f"w_{uk}")

# 7. OPSLAG & EXPORT
st.divider()
if st.button("💾 Sla Huidige Setup op"):
    st.session_state['history'].append({"Auto": auto, "Circ": circuit, "TC1": tc1, "BB": bb_v, "Wing": wing_v})
    st.success("Huidige setup opgeslagen in lijst!")

if st.session_state['history']:
    df_h = pd.DataFrame(st.session_state['history'])
    buf_h = io.BytesIO()
    with pd.ExcelWriter(buf_h, engine='xlsxwriter') as wr:
        df_h.to_excel(wr, index=False)
    st.download_button("📥 Download Selectie Excel", data=buf_h.getvalue(), file_name="mijn_setups.xlsx")
    st.table(df_h)
