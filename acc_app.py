import streamlit as st
import pandas as pd
import io

# 1. Pagina Configuratie (Strikt v9.41)
st.set_page_config(page_title="ACC Setup Master v9.54", layout="wide")

# Styling v9.41 (Grayscale Stealth)
st.markdown("""<style>
    .stApp { background-color: #000000; color: #FFFFFF; }
    [data-testid="stSidebar"] { background-color: #0A0C10; }
    .stTabs [aria-selected="true"] { background-color: #333333 !important; color: #FFFFFF !important; border-bottom: 2px solid #FFFFFF !important; }
    .stTabs [data-baseweb="tab"] { color: #888888; }
    input { background-color: #111111 !important; color: #FFFFFF !important; border: 1px solid #333 !important; }
    .stButton>button { border: 1px solid #444; background-color: #000; color: #fff; width: 100%; }
</style>""", unsafe_allow_html=True)

# 2. DE DEEP DATA DATABASE (Per auto, per circuit-type de beste instellingen)
# Data gebaseerd op 2025/2026 Meta: [PSI, Wing, BB, F-Toe, F-Cam, F-ARB, R-ARB, TC, ABS, Bump, Reb]
setup_matrix = {
    "Ferrari 296 GT3": {
        "High": ["26.8", "11", "54.2", "0.06", "-3.5", "4", "3", "3", "3", "5", "10"],
        "Low":  ["26.2", "2",  "56.5", "0.01", "-3.1", "5", "1", "2", "2", "4", "11"],
        "Bumpy":["26.5", "8",  "53.5", "0.09", "-3.8", "3", "2", "4", "4", "8", "8"]
    },
    "Porsche 911 GT3 R (992)": {
        "High": ["26.7", "12", "50.2", "-0.04", "-3.8", "3", "4", "4", "3", "4", "12"],
        "Low":  ["26.0", "3",  "52.8", "-0.08", "-3.4", "4", "2", "3", "2", "3", "13"],
        "Bumpy":["26.6", "10", "48.5", "0.02", "-4.0", "2", "3", "5", "4", "7", "9"]
    },
    "BMW M4 GT3": {
        "High": ["26.9", "10", "57.5", "0.05", "-3.2", "5", "3", "2", "3", "6", "9"],
        "Low":  ["26.4", "1",  "59.5", "0.00", "-2.8", "6", "1", "1", "2", "5", "10"],
        "Bumpy":["26.7", "9",  "56.2", "0.08", "-3.5", "4", "2", "3", "4", "9", "7"]
    },
    "Lamborghini EVO2": {
        "High": ["26.8", "11", "55.2", "0.06", "-3.6", "4", "3", "3", "3", "5", "11"],
        "Low":  ["26.2", "2",  "57.5", "0.02", "-3.2", "5", "1", "2", "3", "4", "12"],
        "Bumpy":["26.5", "9",  "54.8", "0.10", "-3.8", "3", "2", "4", "4", "7", "9"]
    }
    # Uitbreidbaar met overige auto's...
}

circuits = {
    "High": ["Spa-Francorchamps", "Zandvoort", "Suzuka", "Kyalami", "Barcelona", "Nürburgring"],
    "Low": ["Monza", "Paul Ricard", "Silverstone", "Indianapolis"],
    "Bumpy": ["Zolder", "Imola", "Mount Panorama", "Laguna Seca", "Watkins Glen"]
}

if 'history' not in st.session_state: st.session_state['history'] = []

# 3. SELECTIE & LOGICA
st.title("🏎️ ACC Master v9.54")
ca, cc = st.columns(2)
with ca: auto = st.selectbox("🚗 Auto:", list(setup_matrix.keys()))
with cc: 
    alist = sorted([c for sub in circuits.values() for c in sub])
    circuit = st.selectbox("📍 Circuit:", alist)

ctype = next((k for k, v in circuits.items() if circuit in v), "High")
s = setup_matrix[auto][ctype]
uk = f"{auto}_{circuit}".replace(" ", "")

# SIDEBAR (Master Export & Dokter)
st.sidebar.header("📊 Master Database")
if st.sidebar.button("Genereer Master Excel"):
    rows = []
    for ct, cl in circuits.items():
        for cn in cl:
            for an in setup_matrix.keys():
                v = setup_matrix[an][ct]
                rows.append({"Auto": an, "Circuit": cn, "Type": ct, "PSI": v[0], "Wing": v[1], "BB": v[2], "Toe": v[3], "Cam": v[4]})
    df = pd.DataFrame(rows)
    buf = io.BytesIO()
    with pd.ExcelWriter(buf, engine='xlsxwriter') as wr: df.to_excel(wr, index=False)
    st.sidebar.download_button("📥 Download Master DB", data=buf.getvalue(), file_name="ACC_Master_DB.xlsx")

st.sidebar.divider()
st.sidebar.header("🩺 Dokter")
kl = st.sidebar.selectbox("Klacht?", ["Geen", "Onderstuur", "Overstuur", "Curbs"], key=f"dr_{uk}")
if kl != "Geen":
    if kl == "Onderstuur": st.sidebar.info("Tip: F-ARB -1 of F-Bumper zachter")
    elif kl == "Overstuur": st.sidebar.info("Tip: R-ARB -1 of Wing +1")
    elif kl == "Curbs": st.sidebar.info("Tip: RH +2mm & Bumpstops -5mm")

# 4. TABS (Exact v9.41 Layout)
t = st.tabs(["🛞 Tyres", "⚡ Electronics", "⛽ Fuel", "⚙️ Mechanical", "☁️ Dampers", "✈️ Aero"])

with t[0]: # Tyres
    c1, c2 = st.columns(2)
    with c1:
        st.write("**Front**")
        st.text_input("LF PSI", s[0], key=f"lp_{uk}"); st.text_input("F-Toe", s[3], key=f"ft_{uk}")
        st.text_input("F-Cam", s[4], key=f"fc_{uk}")
    with c2:
        st.write("**Rear**")
        st.text_input("LR PSI", s[0], key=f"lr_{uk}"); st.text_input("R-Camber", "-3.0", key=f"rc_{uk}")

with t[1]: # Electronics
    e1, e2 = st.columns(2)
    e1.text_input("TC1", s[7], key=f"t1_{uk}"); e1.text_input("TC2", s[7], key=f"t2_{uk}")
    e2.text_input("ABS", s[8], key=f"ab_{uk}"); e2.text_input("ECU", "1", key=f"ec_{uk}")

with t[3]: # Mechanical
    m1, m2 = st.columns(2)
    m1.text_input("F-ARB", s[5], key=f"fa_{uk}"); m1.text_input("BB", s[2], key=f"bb_{uk}")
    m2.text_input("R-ARB", s[6], key=f"ra_{uk}"); m2.text_input("Steer", "13.0", key=f"st_{uk}")

with t[4]: # Dampers
    
    d1, d2 = st.columns(2)
    d1.text_input("Bump", s[9], key=f"bp_{uk}"); d2.text_input("Rebound", s[10], key=f"rb_{uk}")

with t[5]: # Aero
    a1, a2 = st.columns(2)
    a1.text_input("Wing", s[1], key=f"wi_{uk}"); a2.text_input("RH Front", "48", key=f"hf_{uk}")

# 5. OPSLAG
st.divider()
if st.button("💾 Sla Setup op"):
    st.session_state['history'].append({"Auto": auto, "Circ": circuit, "BB": s[2], "Wing": s[1]})
    st.success("Opgeslagen!")

if st.session_state['history']:
    st.table(pd.DataFrame(st.session_state['history']))
