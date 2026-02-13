import streamlit as st
import pandas as pd

# 1. Pagina Configuratie
st.set_page_config(page_title="ACC Setup Master v9.17", layout="wide")

# COMBINED HIGH-CONTRAST THEME CSS
st.markdown("""
    <style>
    /* Algemene achtergrond naar gitzwart */
    .stApp, [data-testid="stSidebar"], .stAppHeader {
        background-color: #000000 !important;
        color: #FFFFFF !important;
    }
    
    /* Alle tekst naar spierwit */
    label, p, span, h1, h2, h3, .stMarkdown, [data-testid="stWidgetLabel"] p {
        color: #FFFFFF !important;
        font-weight: 600 !important;
    }

    /* Selectbox Focus Rand (Rood) */
    .stSelectbox div[data-baseweb="select"] {
        border: 1px solid #30363D;
        background-color: #161B22 !important;
    }
    .stSelectbox div[data-baseweb="select"]:focus-within {
        border: 2px solid #FF4B4B !important;
        box-shadow: 0 0 10px #FF4B4B;
    }

    /* Knoppen: Zwarte tekst op heldere achtergrond */
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

    /* Input velden styling */
    .stTextInput input {
        background-color: #161B22 !important;
        color: #FFFFFF !important;
        border: 1px solid #58A6FF !important;
    }

    /* Tabs styling */
    .stTabs [data-baseweb="tab-list"] { background-color: #161B22; border-radius: 5px; }
    .stTabs [data-baseweb="tab"] { color: #FFFFFF !important; }
    .stTabs [aria-selected="true"] { background-color: #FF4B4B !important; border-radius: 5px; }

    /* Alert/Dokter styling */
    .stAlert {
        background-color: #000000 !important;
        color: #FFFFFF !important;
        border: 2px solid #FF4B4B !important;
    }
    
    /* Sidebar Tip blok */
    [data-testid="stSidebar"] .stInfo {
        background-color: #161B22 !important;
        border-left: 5px solid #58A6FF !important;
    }
    </style>
    """, unsafe_allow_html=True)

# 2. DATABASE (Volledige v9.11-v9.14 data)
cars_db = {
    "Ferrari 296 GT3": {"bb": 54.2, "diff": 80, "steer": 13.0, "wr_f": 160, "wr_r": 130, "f_cam": -3.5, "r_cam": -3.0, "f_toe": 0.06, "r_toe": 0.12, "caster": 12.5, "tips": "Focus op aero-rake."},
    "Porsche 911 GT3 R (992)": {"bb": 50.2, "diff": 120, "steer": 12.0, "wr_f": 190, "wr_r": 150, "f_cam": -3.8, "r_cam": -3.2, "f_toe": -0.04, "r_toe": 0.20, "caster": 13.2, "tips": "Motor achterin; pas op voor lift-off oversteer."},
    "BMW M4 GT3": {"bb": 57.5, "diff": 40, "steer": 14.0, "wr_f": 150, "wr_r": 120, "f_cam": -3.2, "r_cam": -2.8, "f_toe": 0.05, "r_toe": 0.10, "caster": 11.8, "tips": "Stabiel over curbs."},
    "Lamborghini EVO2": {"bb": 55.2, "diff": 90, "steer": 13.0, "wr_f": 165, "wr_r": 135, "f_cam": -3.6, "r_cam": -3.1, "f_toe": 0.06, "r_toe": 0.14, "caster": 12.8, "tips": "Veel mechanische grip."},
    "McLaren 720S EVO": {"bb": 53.2, "diff": 70, "steer": 13.0, "wr_f": 155, "wr_r": 125, "f_cam": -3.5, "r_cam": -3.0, "f_toe": 0.06, "r_toe": 0.10, "caster": 12.0, "tips": "Aero-gevoelig platform."},
    "Mercedes AMG EVO": {"bb": 56.8, "diff": 65, "steer": 14.0, "wr_f": 170, "wr_r": 140, "f_cam": -3.4, "r_cam": -2.9, "f_toe": 0.07, "r_toe": 0.12, "caster": 13.5, "tips": "Focus op tractie."},
    "Audi R8 EVO II": {"bb": 54.0, "diff": 110, "steer": 13.0, "wr_f": 160, "wr_r": 130, "f_cam": -3.7, "r_cam": -3.1, "f_toe": 0.06, "r_toe": 0.11, "caster": 12.4, "tips": "Nerveus bij remmen."},
    "Aston Martin EVO": {"bb": 56.2, "diff": 55, "steer": 14.0, "wr_f": 155, "wr_r": 125, "f_cam": -3.3, "r_cam": -2.8, "f_toe": 0.06, "r_toe": 0.10, "caster": 12.2, "tips": "Zeer stabiel platform."},
    "Ford Mustang GT3": {"bb": 57.0, "diff": 50, "steer": 14.0, "wr_f": 160, "wr_r": 130, "f_cam": -3.5, "r_cam": -3.0, "f_toe": 0.06, "r_toe": 0.13, "caster": 12.0, "tips": "Veel koppel; beheer banden."},
    "Corvette Z06 GT3.R": {"bb": 54.8, "diff": 75, "steer": 13.0, "wr_f": 160, "wr_r": 130, "f_cam": -3.5, "r_cam": -3.0, "f_toe": 0.06, "r_toe": 0.12, "caster": 12.6, "tips": "Goede balans."}
}

circuits_db = {
    "High Downforce": ["Spa-Francorchamps", "Zandvoort", "Kyalami", "Barcelona", "Hungaroring", "Suzuka", "Donington Park", "Oulton Park", "Misano", "Valencia", "Nürburgring"],
    "Low Downforce": ["Monza", "Paul Ricard", "Bathurst", "Silverstone", "Indianapolis", "Jeddah"],
    "Street/Bumpy": ["Zolder", "Mount Panorama", "Laguna Seca", "Imola", "Snetterton", "Watkins Glen", "Red Bull Ring", "Magny-Cours"]
}

if 'history' not in st.session_state:
    st.session_state['history'] = []

# 3. SELECTIE
st.title("🏎️ :red[ACC] Setup Master v9.17")
col_a, col_c = st.columns(2)
with col_a:
    auto = st.selectbox("🚗 Selecteer Auto:", list(cars_db.keys()))
with col_c:
    all_circuits = sorted([c for sub in circuits_db.values() for c in sub])
    circuit = st.selectbox("📍 Selecteer Circuit:", all_circuits)

# ENGINEER LOGICA
car = cars_db[auto]
ctype = next((k for k, v in circuits_db.items() if circuit in v), "High Downforce")

if ctype == "Low Downforce":
    psi, wing, bb_mod, arb_f, arb_r = "26.2", "2", 1.5, "5", "1"
    damp, rh_f, rh_r, spl, bduct = ["4", "9", "7", "11"], "45", "62", "0", "1"
elif ctype == "Street/Bumpy":
    psi, wing, bb_mod, arb_f, arb_r = "26.6", "8", -0.5, "3", "2"
    damp, rh_f, rh_r, spl, bduct = ["8", "15", "6", "10"], "52", "75", "2", "3"
else:
    psi, wing, bb_mod, arb_f, arb_r = "26.8", "11", 0.0, "4", "3"
    damp, rh_f, rh_r, spl, bduct = ["5", "10", "8", "12"], "48", "68", "0", "2"

ukey = f"v917_{auto}_{circuit}".replace(" ", "_").replace("-", "")

# 4. SIDEBAR - SETUP DOKTER
st.sidebar.header("🩺 De Setup Dokter")
klacht = st.sidebar.selectbox("Klacht?", ["Geen", "Onderstuur", "Overstuur"], key=f"dr_{ukey}")
if klacht != "Geen":
    st.sidebar.warning(f"Advies: Wijzig ARB voor {klacht}")
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
        st.text_input("F-Camber", str(car['f_cam']), key=f"fc_{ukey}")
    with c2:
        st.text_input("LR PSI", psi, key=f"lr_{ukey}")
        st.text_input("RR PSI", psi, key=f"rr_{ukey}")
        st.text_input("R-Camber", str(car['r_cam']), key=f"rc_{ukey}")

with tabs[2]:
    st.text_input("Fuel", "62", key=f"fuel_{ukey}")
    st.text_input("Brake Duct Front", bduct, key=f"bdf_{ukey}")
    st.text_input("Brake Duct Rear", bduct, key=f"bdr_{ukey}")

with tabs[3]:
    mc1, mc2 = st.columns(2)
    with mc1:
        st.text_input("Front ARB", arb_f, key=f"farb_{ukey}")
        st.text_input("Brake Bias (%)", str(car["bb"] + bb_mod), key=f"bb_{ukey}")
        st.text_input("Steer Ratio", str(car["steer"]), key=f"str_{ukey}")
    with mc2:
        st.text_input("Rear ARB", arb_r, key=f"rarb_{ukey}")
        st.text_input("Preload Diff", str(car["diff"]), key=f"diff_{ukey}")

with tabs[5]:
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
with col_btn1:
    save_btn = st.button("💾 Sla Setup op")

if save_btn:
    new_setup = {
        "Auto": auto, "Circuit": circuit, "PSI": psi, "Wing": wing, "Splitter": spl,
        "BB": car["bb"] + bb_mod, "Brake_Duct": bduct, "Steer": car["steer"],
        "RH_F": rh_f, "RH_R": rh_r
    }
    st.session_state['history'].append(new_setup)
    st.success("Opgeslagen!")

if st.session_state['history']:
    df = pd.DataFrame(st.session_state['history'])
    csv = df.to_csv(index=False).encode('utf-8')
    with col_btn2:
        st.download_button(label="📥 Download Database (CSV)", data=csv, file_name='acc_setups.csv', mime='text/csv')
    st.table(df)
