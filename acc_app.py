import streamlit as st
import pandas as pd

# 1. Pagina Configuratie
st.set_page_config(page_title="ACC Setup Master v9.20", layout="wide")

# HIGH-CONTRAST THEME CSS (Volledig Stealth)
st.markdown("""
    <style>
    /* Hoofdscherm en Sidebar naar gitzwart */
    .stApp, [data-testid="stSidebar"], .stAppHeader {
        background-color: #000000 !important;
        color: #FFFFFF !important;
    }
    
    /* Alle teksten spierwit */
    label, p, span, h1, h2, h3, .stMarkdown, [data-testid="stWidgetLabel"] p {
        color: #FFFFFF !important;
        font-weight: 600 !important;
    }

    /* Sidebar Midnight Black en uitlijning */
    [data-testid="stSidebar"] {
        background-color: #0A0C10 !important;
        border-right: 1px solid #1E1E1E;
    }
    [data-testid="stSidebar"] .stSelectbox {
        margin-top: 52px; 
    }

    /* Focus Rand Rood */
    .stSelectbox div[data-baseweb="select"]:focus-within {
        border: 2px solid #FF4B4B !important;
        box-shadow: 0 0 10px #FF4B4B;
    }

    /* Knoppen: Zwart op Wit/Blauw */
    .stButton button {
        background-color: #FFFFFF !important;
        color: #000000 !important;
        font-weight: bold !important;
        width: 100%;
    }
    .stDownloadButton button {
        background-color: #58A6FF !important;
        color: #000000 !important;
        font-weight: bold !important;
        width: 100%;
    }

    /* Input velden */
    .stTextInput input {
        background-color: #161B22 !important;
        color: #FFFFFF !important;
        border: 1px solid #58A6FF !important;
    }

    /* Tabel styling */
    .stTable, table {
        background-color: #000000 !important;
        color: #FFFFFF !important;
        border: 1px solid #30363D !important;
    }
    thead th {
        background-color: #161B22 !important;
        color: #FF4B4B !important;
    }

    /* Diagnose kaders */
    .advice-box {
        padding: 15px;
        border-radius: 5px;
        background-color: #000000;
        margin-top: 10px;
        border-left: 5px solid;
    }
    </style>
    """, unsafe_allow_html=True)

# 2. DATABASE
cars_db = {
    "Ferrari 296 GT3": {"bb": 54.2, "diff": 80, "steer": 13.0, "tips": "Focus op aero-rake."},
    "Porsche 911 GT3 R (992)": {"bb": 50.2, "diff": 120, "steer": 12.0, "tips": "Motor achterin; beheer lift-off."},
    "BMW M4 GT3": {"bb": 57.5, "diff": 40, "steer": 14.0, "tips": "Sterk over curbs."},
    "Lamborghini EVO2": {"bb": 55.2, "diff": 90, "steer": 13.0, "tips": "Veel mechanische grip."},
    "McLaren 720S EVO": {"bb": 53.2, "diff": 70, "steer": 13.0, "tips": "Aero-gevoelig platform."},
    "Mercedes AMG EVO": {"bb": 56.8, "diff": 65, "steer": 14.0, "tips": "Focus op tractie."},
    "Audi R8 EVO II": {"bb": 54.0, "diff": 110, "steer": 13.0, "tips": "Nerveus bij remmen."},
    "Aston Martin EVO": {"bb": 56.2, "diff": 55, "steer": 14.0, "tips": "Zeer stabiel platform."},
    "Ford Mustang GT3": {"bb": 57.0, "diff": 50, "steer": 14.0, "tips": "Veel koppel; beheer banden."},
    "Corvette Z06 GT3.R": {"bb": 54.8, "diff": 75, "steer": 13.0, "tips": "Goede balans."}
}

circuits_db = {
    "High Downforce": ["Spa-Francorchamps", "Zandvoort", "Kyalami", "Barcelona", "Hungaroring", "Suzuka", "Donington Park", "Oulton Park", "Misano", "Valencia", "Nürburgring"],
    "Low Downforce": ["Monza", "Paul Ricard", "Bathurst", "Silverstone", "Indianapolis", "Jeddah"],
    "Street/Bumpy": ["Zolder", "Mount Panorama", "Laguna Seca", "Imola", "Snetterton", "Watkins Glen", "Red Bull Ring", "Magny-Cours"]
}

if 'history' not in st.session_state:
    st.session_state['history'] = []

# 3. SELECTIE HEADER
st.title("🏎️ :red[ACC] Setup Master v9.20")
col_a, col_c = st.columns(2)
with col_a:
    auto = st.selectbox("🚗 Kies Auto:", list(cars_db.keys()))
with col_c:
    all_circuits = sorted([c for sub in circuits_db.values() for c in sub])
    circuit = st.selectbox("📍 Kies Circuit:", all_circuits)

# ENGINEER LOGICA (Gecorrigeerd voor Syntax)
car = cars_db[auto]
ctype = next((k for k, v in circuits_db.items() if circuit in v), "High Downforce")

if ctype == "Low Downforce":
    psi, wing, bb_mod, arb_f, arb_r, bduct = "26.2", "2", 1.5, "5", "1", "1"
    rh_f, rh_r, spl = "45", "62", "0"
elif ctype == "Street/Bumpy":
    psi, wing, bb_mod, arb_f, arb_r, bduct = "26.6", "8", -0.5, "3", "2", "3"
    rh_f, rh_r, spl = "52", "75", "2"
else: # High Downforce
    psi, wing, bb_mod, arb_f, arb_r, bduct = "26.8", "11", 0.0, "4", "3", "2"
    rh_f, rh_r, spl = "48", "68", "0"

ukey = f"v920_{auto}_{circuit}".replace(" ", "_")

# 4. SIDEBAR - DYNAMISCHE DOKTER
st.sidebar.header("🩺 De Setup Dokter")
klacht = st.sidebar.selectbox("Klacht?", ["Geen", "Onderstuur (Entry)", "Onderstuur (Exit)", "Overstuur (Entry)", "Overstuur (Exit)", "Onrustig over curbs"], key=f"dr_{ukey}")

if klacht != "Geen":
    advice = ""
    color = "#FFFFFF"
    if "Onderstuur" in klacht:
        val = int(arb_f) - 1
        advice = f"Advies voor {auto}: Verlaag **Front ARB** van **{arb_f}** naar **{val}**."
        color = "#FFA500"
    elif "Overstuur" in klacht:
        val = int(arb_r) - 1
        advice = f"Advies voor {auto}: Verlaag **Rear ARB** van **{arb_r}** naar **{val}**."
        color = "#FF4B4B"
    elif "curbs" in klacht:
        advice = f"Advies voor {auto}: Verhoog de **Rijhoogte** met **2mm** en verzacht de bumpers."
        color = "#58A6FF"
    
    st.sidebar.markdown(f"""<div class='advice-box' style='border-color: {color}'>{advice}</div>""", unsafe_allow_html=True)

st.sidebar.divider()
st.sidebar.info(f"💡 Tip: {car['tips']}")

# 5. TABS
tabs = st.tabs(["🛞 Tyres", "⚡ Electronics", "⛽ Fuel", "⚙️ Mechanical", "☁️ Dampers", "✈️ Aero"])

with tabs[0]:
    st.write("### :blue[Tyre Alignment]")
    c1, c2 = st.columns(2)
    with c1:
        st.text_input("LF PSI", psi, key=f"lf_{ukey}")
        st.text_input("RF PSI", psi, key=f"rf_{ukey}")
    with c2:
        st.text_input("LR PSI", psi, key=f"lr_{ukey}")
        st.text_input("RR PSI", psi, key=f"rr_{ukey}")

with tabs[1]: # ELECTRONICS UITGEBREID
    st.write("### :orange[Electronics & Assist]")
    e1, e2 = st.columns(2)
    with e1:
        tc1 = st.text_input("TC1", "3", key=f"tc1_{ukey}")
        tc2 = st.text_input("TC2 (Cut)", "3", key=f"tc2_{ukey}")
    with e2:
        abs_v = st.text_input("ABS", "3", key=f"abs_{ukey}")
        ecumap = st.text_input("ECU Map", "1", key=f"ecu_{ukey}")

with tabs[3]: # MECHANICAL
    mc1, mc2 = st.columns(2)
    with mc1:
        st.text_input("Front ARB", arb_f, key=f"farb_{ukey}")
        st.text_input("Brake Bias (%)", str(car["bb"] + bb_mod), key=f"bb_{ukey}")
    with mc2:
        st.text_input("Rear ARB", arb_r, key=f"rarb_{ukey}")
        st.text_input("Steer Ratio", str(car["steer"]), key=f"str_{ukey}")

with tabs[5]: # AERO
    ac1, ac2 = st.columns(2)
    with ac1:
        st.text_input("Splitter", spl, key=f"spl_{ukey}")
        st.text_input("RH Front", rh_f, key=f"rhf_{ukey}")
    with ac2:
        st.text_input("Wing", wing, key=f"wing_{ukey}")
        st.text_input("RH Rear", rh_r, key=f"rhr_{ukey}")

# 6. OPSLAG & EXPORT
st.divider()
col_btn1, col_btn2 = st.columns([1, 4])
if col_btn1.button("💾 Sla Setup op"):
    new_setup = {
        "Auto": auto, "Circuit": circuit, "TC1": tc1, "TC2": tc2, "ECU": ecumap, "ABS": abs_v,
        "Wing": wing, "Splitter": spl, "Brake_Duct": bduct, "Steer": car["steer"]
    }
    st.session_state['history'].append(new_setup)
    st.success("Opgeslagen!")

if st.session_state['history']:
    df = pd.DataFrame(st.session_state['history'])
    csv_data = df.to_csv(index=False).encode('utf-8')
    col_btn2.download_button("📥 Download CSV", data=csv_data, file_name='acc_setups.csv', mime='text/csv')
    st.subheader("📋 Opgeslagen Setup Database")
    st.table(df)
