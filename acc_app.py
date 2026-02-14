import streamlit as st
import pandas as pd
import io

# 1. Pagina Configuratie
st.set_page_config(page_title="ACC Setup Master v9.43", layout="wide")

# Styling
st.markdown("""<style>.stTabs [aria-selected="true"] { background-color: #ff4b4b !important; }</style>""", unsafe_allow_html=True)

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
    "Low": ["Monza", "Paul Ricard", "Bathurst", "Silverstone", "Indianapolis"],
    "Bumpy": ["Zolder", "Mount Panorama", "Laguna Seca", "Imola", "Watkins Glen"]
}

# 3. MASTER GENERATOR LOGICA
def generate_full_master():
    rows = []
    for c_type, c_list in circ_db.items():
        for c_name in c_list:
            for a_name, a_data in cars_db.items():
                # Bereken circuit-specifieke mods
                if c_type == "Low":
                    p, w, bm, af, ar, d = "26.2", "2", 1.5, "5", "1", "Soft"
                    hf, hr, sp = "45", "62", "0"
                elif c_type == "Bumpy":
                    p, w, bm, af, ar, d = "26.6", "8", -0.5, "3", "2", "Very Soft"
                    hf, hr, sp = "52", "75", "2"
                else: # High
                    p, w, bm, af, ar, d = "26.8", "11", 0.0, "4", "3", "Medium"
                    hf, hr, sp = "48", "68", "0"
                
                rows.append({
                    "Auto": a_name, "Circuit": c_name, "Track Type": c_type,
                    "PSI": p, "Wing": w, "Splitter": sp, "RH Front": hf, "RH Rear": hr,
                    "Brake Bias": a_data["bb"] + bm, "Steer Ratio": a_data["steer"],
                    "F-ARB": af, "R-ARB": ar, "Diff Preload": a_data["bb"], # Proxy voor diff
                    "F-Camber": a_data["f_cam"], "R-Camber": a_data["r_cam"],
                    "F-Toe": a_data["f_toe"], "R-Toe": a_data["r_toe"], "Caster": a_data["caster"],
                    "Damper Preset": d, "TC1": "3", "TC2": "3", "ABS": "3", "ECU Map": "1"
                })
    return pd.DataFrame(rows)

# 4. SIDEBAR - DE MASTER KNOP
st.sidebar.header("📊 Master Database")
if st.sidebar.button("Genereer Alle Combinaties"):
    df_master = generate_full_master()
    buf = io.BytesIO()
    with pd.ExcelWriter(buf, engine='xlsxwriter') as wr:
        df_master.to_excel(wr, index=False, sheet_name='ACC_Master_Setups')
    
    st.sidebar.download_button(
        label="📥 Download Master Excel",
        data=buf.getvalue(),
        file_name="ACC_Master_Database_Full.xlsx",
        mime="application/vnd.ms-excel"
    )
    st.sidebar.success(f"Gereed: {len(df_master)} setups gegenereerd!")

# 5. REGULIERE INTERFACE (Individuele Selectie)
st.title("🏎️ ACC Setup Master v9.43")
col_a, col_c = st.columns(2)
with col_a: auto = st.selectbox("🚗 Kies Auto:", list(cars_db.keys()))
with col_c: 
    all_c = sorted([c for sub in circ_db.values() for c in sub])
    circuit = st.selectbox("📍 Kies Circuit:", all_c)

# (De rest van de interface voor handmatige aanpassingen blijft zoals in v9.41/9.42)
st.info("Gebruik de sidebar om de volledige database in één keer te downloaden.")
