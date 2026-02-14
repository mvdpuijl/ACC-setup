import streamlit as st
import pandas as pd
import io

# 1. Pagina Configuratie & Styling
st.set_page_config(page_title="ACC Setup Master v9.53", layout="wide")
st.markdown("""<style>
    .stApp { background-color: #000000 !important; color: #FFFFFF !important; }
    [data-testid="stSidebar"] { background-color: #0A0C10 !important; }
    .stTabs [aria-selected="true"] { background-color: #333333 !important; color: #FFFFFF !important; border-bottom: 2px solid #FFFFFF !important; }
    input { background-color: #111111 !important; color: #FFFFFF !important; border: 1px solid #333 !important; }
    .stButton>button { border: 1px solid #444; background-color: #000; color: #fff; width: 100%; }
</style>""", unsafe_allow_html=True)

# 2. FULL SETUP MATRIX
# Kolom index: 0:PSI, 1:Wing, 2:BB, 3:Toe, 4:Cam, 5:F-ARB, 6:R-ARB, 7:TC, 8:ABS, 9:Bump, 10:Rebound
matrix = {
    "Ferrari 296 GT3": {
        "High": ["26.8", "11", "54.2", "0.06", "-3.5", "4", "3", "3", "3", "5", "10"],
        "Low":  ["26.2", "2",  "56.0", "0.02", "-3.2", "5", "1", "2", "2", "4", "11"],
        "Bumpy":["26.5", "8",  "53.8", "0.08", "-3.7", "3", "2", "4", "4", "8", "7"]
    },
    "Porsche 911 GT3 R (992)": {
        "High": ["26.7", "12", "50.2", "-0.04", "-3.8", "3", "4", "4", "3", "4", "12"],
        "Low":  ["26.1", "3",  "52.5", "-0.08", "-3.5", "4", "2", "3", "2", "3", "13"],
        "Bumpy":["26.6", "10", "49.5", "0.00", "-4.0", "2", "3", "5", "4", "7", "9"]
    },
    "BMW M4 GT3": {
        "High": ["26.9", "10", "57.5", "0.05", "-3.2", "5", "3", "2", "3", "6", "9"],
        "Low":  ["26.3", "1",  "59.2", "0.01", "-2.9", "6", "1", "1", "2", "5", "10"],
        "Bumpy":["26.7", "9",  "56.8", "0.07", "-3.4", "4", "2", "3", "4", "9", "6"]
    }
}

circ_db = {
    "High": ["Spa-Francorchamps", "Zandvoort", "Suzuka", "Barcelona", "Nürburgring"],
    "Low": ["Monza", "Paul Ricard", "Silverstone", "Indianapolis"],
    "Bumpy": ["Zolder", "Imola", "Mount Panorama", "Laguna Seca"]
}

# 3. INTERFACE
st.title("ACC Master v9.53")
ca, cc = st.columns(2)
with ca: auto = st.selectbox("🚗 Auto:", list(matrix.keys()))
with cc: 
    alist = sorted([c for sub in circ_db.values() for c in sub])
    circuit = st.selectbox("📍 Circuit:", alist)

ctype = next((k for k, v in circ_db.items() if circuit in v), "High")
s = matrix[auto][ctype]
uk = f"{auto}_{circuit}".replace(" ", "")

# SIDEBAR EXPORT
st.sidebar.header("📊 Master Database")
if st.sidebar.button("Genereer Volledige Excel"):
    rows = []
    for ct, cl in circ_db.items():
        for cn in cl:
            for an in matrix.keys():
                v = matrix[an][ct]
                rows.append({
                    "Auto": an, "Circuit": cn, "Type": ct, "PSI": v[0], "Wing": v[1], 
                    "BB": v[2], "Toe": v[3], "Cam": v[4], "F-ARB": v[5], "R-ARB": v[6],
                    "TC": v[7], "ABS": v[8], "Bump": v[9], "Rebound": v[10]
                })
    df = pd.DataFrame(rows)
    buf = io.BytesIO()
    with pd.ExcelWriter(buf, engine='xlsxwriter') as wr: df.to_excel(wr, index=False)
    st.sidebar.download_button("📥 Download Master Setup List", data=buf.getvalue(), file_name="ACC_Full_Database.xlsx")

# 4. TABS
t = st.tabs(["🛞 Tyres", "⚡ Electronics", "⚙️ Mechanical", "☁️ Dampers", "✈️ Aero"])

with t[0]: # Tyres
    c1, c2 = st.columns(2)
    c1.text_input("LF PSI", s[0], key=f"lp_{uk}"); c1.text_input("F-Toe", s[3], key=f"ft_{uk}")
    c2.text_input("F-Cam", s[4], key=f"fc_{uk}"); c2.text_input("Caster", "12.5", key=f"cs_{uk}")

with t[1]: # Electronics
    e1, e2 = st.columns(2)
    e1.text_input("TC 1", s[7], key=f"t1_{uk}"); e2.text_input("ABS", s[8], key=f"ab_{uk}")

with t[2]: # Mechanical
    m1, m2 = st.columns(2)
    m1.text_input("F-ARB", s[5], key=f"fa_{uk}"); m1.text_input("BB", s[2], key=f"bb_{uk}")
    m2.text_input("R-ARB", s[6], key=f"ra_{uk}"); m2.text_input("Steer Ratio", "13.0", key=f"sr_{uk}")

with t[3]: # Dampers
    
    d1, d2 = st.columns(2)
    d1.text_input("Bump (All)", s[9], key=f"bp_{uk}"); d2.text_input("Rebound (All)", s[10], key=f"rb_{uk}")

with t[4]: # Aero
    a1, a2 = st.columns(2)
    a1.text_input("Wing", s[1], key=f"wi_{uk}"); a2.text_input("RH Front", "48", key=f"hf_{uk}")

st.info(f"Geoptimaliseerd profiel geladen voor {auto} op {circuit}.")
