import streamlit as st
import pandas as pd

# 1. Pagina Configuratie
st.set_page_config(page_title="ACC Setup Master v9.9", layout="wide")

# 2. DATABASE: Volledige geometrie en basiswaarden per auto
cars_db = {
    "Ferrari 296 GT3": {"bb": 54.2, "diff": 80, "steer": 13.0, "wr_f": 160, "wr_r": 130, "f_cam": -3.5, "r_cam": -3.0, "f_toe": 0.06, "r_toe": 0.12, "caster": 12.5, "tips": "Focus op aero-rake."},
    "Porsche 911 GT3 R (992)": {"bb": 50.2, "diff": 120, "steer": 12.0, "wr_f": 190, "wr_r": 150, "f_cam": -3.8, "r_cam": -3.2, "f_toe": -0.04, "r_toe": 0.20, "caster": 13.2, "tips": "Motor achterin, wees voorzichtig."},
    "BMW M4 GT3": {"bb": 57.5, "diff": 40, "steer": 14.0, "wr_f": 150, "wr_r": 120, "f_cam": -3.2, "r_cam": -2.8, "f_toe": 0.05, "r_toe": 0.10, "caster": 11.8, "tips": "Stabiel over curbs."},
    "Lamborghini EVO2": {"bb": 55.2, "diff": 90, "steer": 13.0, "wr_f": 165, "wr_r": 135, "f_cam": -3.6, "r_cam": -3.1, "f_toe": 0.06, "r_toe": 0.14, "caster": 12.8, "tips": "Veel rotatie."},
    "McLaren 720S EVO": {"bb": 53.2, "diff": 70, "steer": 13.0, "wr_f": 155, "wr_r": 125, "f_cam": -3.5, "r_cam": -3.0, "f_toe": 0.06, "r_toe": 0.10, "caster": 12.0, "tips": "Aero gevoelig."},
    "Mercedes AMG EVO": {"bb": 56.8, "diff": 65, "steer": 14.0, "wr_f": 170, "wr_r": 140, "f_cam": "-3.4", "r_cam": -2.9, "f_toe": 0.07, "r_toe": 0.12, "caster": 13.5, "tips": "Focus op tractie."},
    "Audi R8 EVO II": {"bb": 54.0, "diff": 110, "steer": 13.0, "wr_f": 160, "wr_r": 130, "f_cam": "-3.7", "r_cam": -3.1, "f_toe": 0.06, "r_toe": 0.11, "caster": 12.4, "tips": "Nerveus bij remmen."},
    "Aston Martin EVO": {"bb": 56.2, "diff": 55, "steer": 14.0, "wr_f": 155, "wr_r": 125, "f_cam": "-3.3", "r_cam": -2.8, "f_toe": 0.06, "r_toe": 0.10, "caster": 12.2, "tips": "Stabiel platform."},
    "Ford Mustang GT3": {"bb": 57.0, "diff": 50, "steer": 14.0, "wr_f": 160, "wr_r": 130, "f_cam": "-3.5", "r_cam": -3.0, "f_toe": 0.06, "r_toe": 0.13, "caster": 12.0, "tips": "Veel koppel."},
    "Corvette Z06 GT3.R": {"bb": 54.8, "diff": 75, "steer": 13.0, "wr_f": 160, "wr_r": 130, "f_cam": "-3.5", "r_cam": -3.0, "f_toe": 0.06, "r_toe": 0.12, "caster": 12.6, "tips": "Goede balans."}
}

circuits_db = {
    "High Downforce": ["Spa-Francorchamps", "Zandvoort", "Kyalami", "Barcelona", "Hungaroring", "Suzuka", "Donington Park", "Oulton Park", "Misano", "Valencia", "Nürburgring"],
    "Low Downforce": ["Monza", "Paul Ricard", "Bathurst", "Silverstone", "Indianapolis", "Jeddah"],
    "Street/Bumpy": ["Zolder", "Mount Panorama", "Laguna Seca", "Imola", "Snetterton", "Watkins Glen", "Red Bull Ring", "Magny-Cours"]
}

if 'history' not in st.session_state:
    st.session_state['history'] = []

# 3. SELECTIE
st.title("🏎️ ACC Setup Master v9.9")
col_a, col_c = st.columns(2)
with col_a:
    auto = st.selectbox("🚗 Kies Auto:", list(cars_db.keys()))
with col_c:
    all_circuits = sorted([c for sub in circuits_db.values() for c in sub])
    circuit = st.selectbox("📍 Kies Circuit:", all_circuits)

# ENGINEER LOGICA
car = cars_db[auto]
ctype = next((k for k, v in circuits_db.items() if circuit in v), "High Downforce")

if ctype == "Low Downforce":
    psi, wing, bb_mod, arb_f, arb_r = "26.2", "2", 1.5, "5", "1"
    damp, rh_f, rh_r, spl = ["4", "9", "7", "11"], "45", "62", "0"
elif ctype == "Street/Bumpy":
    psi, wing, bb_mod, arb_f, arb_r = "26.6", "8", -0.5, "3", "2"
    damp, rh_f, rh_r, spl = ["8", "15", "6", "10"], "52", "75", "2"
else: # High Downforce
    psi, wing, bb_mod, arb_f, arb_r = "26.8", "11", 0.0, "4", "3"
    damp, rh_f, rh_r, spl = ["5", "10", "8", "12"], "48", "68", "0"

ukey = f"v99_{auto}_{circuit}".replace(" ", "_").replace("-", "")

# 4. SIDEBAR DOKTER
st.sidebar.header("🩺 De Setup Dokter")
klacht = st.sidebar.selectbox("Klacht?", ["Geen", "Onderstuur", "Overstuur"], key=f"dr_{ukey}")
if klacht != "Geen":
    st.sidebar.warning("Advies: Wijzig de ARB of vleugelstand.")
st.sidebar.divider()
st.sidebar.info(f"💡 **Tip voor {auto}:**\n{car['tips']}")

# 5. TABS
tabs = st.tabs(["🛞 Tyres", "⚡ Electronics", "⛽ Fuel", "⚙️ Mechanical Grip", "☁️ Dampers", "✈️ Aero"])

with tabs[0]: # TYRES
    tc1, tc2 = st.columns(2)
    with tc1:
        st.write("**Front**")
        st.text_input("LF PSI", psi, key=f"lf_p_{ukey}")
        st.text_input("RF PSI", psi, key=f"rf_p_{ukey}")
        st.text_input("Front Toe", str(car["f_toe"]), key=f"f_t_{ukey}")
        st.text_input("Front Camber", str(car["f_cam"]), key=f"f_c_{ukey}")
        st.text_input("Front Caster", str(car["caster"]), key=f"f_cas_{ukey}")
    with tc2:
        st.write("**Rear**")
        st.text_input("LR PSI", psi, key=f"lr_p_{ukey}")
        st.text_input("RR PSI", psi, key=f"rr_p_{ukey}")
        st.text_input("Rear Toe", str(car["r_toe"]), key=f"r_t_{ukey}")
        st.text_input("Rear Camber", str(car["r_cam"]), key=f"r_c_{ukey}")

with tabs[1]: # ELECTRONICS
    st.text_input("TC1", "3", key=f"tc1_{ukey}")
    st.text_input("ABS", "3", key=f"abs_{ukey}")

with tabs[3]: # MECHANICAL GRIP
    mc1, mc2 = st.columns(2)
    with mc1:
        st.text_input("Front ARB", arb_f, key=f"farb_{ukey}")
        st.text_input("Brake Bias (%)", str(car["bb"] + bb_mod), key=f"bb_{ukey}")
        st.text_input("Wheel Rate LF", str(car["wr_f"]), key=f"wlf_{ukey}")
    with mc2:
        st.text_input("Rear ARB", arb_r, key=f"rarb_{ukey}")
        st.text_input("Preload Diff", str(car["diff"]), key=f"diff_{ukey}")

with tabs[4]: # DAMPERS
    dc1, dc2 = st.columns(2)
    with dc1:
        st.write("**Front**")
        st.text_input("Bump LF", damp[0], key=f"blf_{ukey}")
        st.text_input("Fast Bump LF", damp[1], key=f"fblf_{ukey}")
    with dc2:
        st.write("**Rear**")
        st.text_input("Rebound LR", damp[2], key=f"rlr_{ukey}")
        st.text_input("Fast Rebound LR", damp[3], key=f"frlr_{ukey}")

with tabs[5]: # AERO (NU MET SPLITTER)
    ac1, ac2 = st.columns(2)
    with ac1:
        st.write("**Front Aero**")
        st.text_input("Ride Height Front", rh_f, key=f"rhf_{ukey}")
        st.text_input("Splitter", spl, key=f"spl_{ukey}")
    with ac2:
        st.write("**Rear Aero**")
        st.text_input("Ride Height Rear", rh_r, key=f"rhr_{ukey}")
        st.text_input("Rear Wing", wing, key=f"wing_{ukey}")

# 6. OPSLAG & VOLLEDIGE EXPORT
st.divider()
if st.button("💾 Sla Setup op"):
    new_setup = {
        "Auto": auto, "Circuit": circuit, "PSI": psi, "Wing": wing, "Splitter": spl,
        "BB": car["bb"] + bb_mod, "F_Cam": car["f_cam"], "R_Cam": car["r_cam"],
        "F_Toe": car["f_toe"], "R_Toe": car["r_toe"], "Caster": car["caster"],
        "F_ARB": arb_f, "R_ARB": arb_r, "Diff": car["diff"], "RH_F": rh_f, "RH_R": rh_r
    }
    st.session_state['history'].append(new_setup)
    st.success(f"Setup voor {auto} op {circuit} toegevoegd!")

if st.session_state['history']:
    st.subheader("📋 Opgeslagen Setup Database")
    df = pd.DataFrame(st.session_state['history'])
    st.table(df) 
    csv = df.to_csv(index=False).encode('utf-8')
    st.download_button(label="📥 Download Database (CSV)", data=csv, file_name='acc_setups_v99.csv', mime='text/csv')
