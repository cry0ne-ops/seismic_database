import streamlit as st
import pandas as pd
import sqlite3

# -----------------------------
# LOAD DATA FROM DATABASE
# -----------------------------
conn = sqlite3.connect("seismic.db")
df = pd.read_sql("SELECT * FROM barangay_data", conn)
conn.close()

# -----------------------------
# PAGE CONFIG
# -----------------------------
st.set_page_config(page_title="Seismic System", layout="wide")

# -----------------------------
# CLEAN UI STYLE
# -----------------------------
st.markdown("""
<style>
.block-container {
    max-width: 900px;
    padding-top: 2rem;
}

h1 {
    text-align: center;
    font-weight: 600;
}

.subtitle {
    text-align: center;
    color: gray;
    margin-bottom: 2rem;
}

.card {
    background: white;
    padding: 20px;
    border-radius: 12px;
    border: 1px solid #e5e7eb;
    margin-bottom: 15px;
}
</style>
""", unsafe_allow_html=True)

# -----------------------------
# HEADER
# -----------------------------
st.title("Seismic Vulnerability Records")
st.markdown('<div class="subtitle">Barangay Hall Assessment System</div>', unsafe_allow_html=True)

# -----------------------------
# SEARCH SECTION
# -----------------------------
col1, col2, col3 = st.columns(3)

with col1:
    municipalities = sorted(df["MUNICIPALITY"].unique())
    municipality = st.selectbox("Municipality", ["Select"] + municipalities)

with col2:
    if municipality != "Select":
        barangays = df[df["MUNICIPALITY"] == municipality]["BARANGAY HALL"].unique()
    else:
        barangays = []

    barangay = st.selectbox("Barangay", ["Select"] + list(barangays))

with col3:
    st.markdown("<br>", unsafe_allow_html=True)
    search = st.button("Search", use_container_width=True)

# -----------------------------
# RESULT
# -----------------------------
if search:

    if municipality == "Select" or barangay == "Select":
        st.warning("Please select both Municipality and Barangay.")
    else:
        result = df[
            (df["MUNICIPALITY"] == municipality) &
            (df["BARANGAY HALL"] == barangay)
        ]

        if result.empty:
            st.error("No data found.")
        else:
            row = result.iloc[0]

            # SUMMARY
            st.markdown('<div class="card">', unsafe_allow_html=True)

            col1, col2, col3 = st.columns(3)

            col1.metric("RVS Score", row["RVS SCORE"])
            col2.metric("Damage Grade", row["GRADE OF DAMAGEABILITY"])
            col3.metric("Rank", row["RANK"])

            st.markdown('</div>', unsafe_allow_html=True)

            # GENERAL INFO
            st.markdown('<div class="card">', unsafe_allow_html=True)
            st.subheader("General Information")

            st.write("Barangay:", row["BARANGAY HALL"])
            st.write("Municipality:", row["MUNICIPALITY"])
            st.write("Year Built:", row["YEAR BUILT"])
            st.write("Floor Area:", row["TOTAL FLOOR AREA (SQ. FT.)"])
            st.write("Occupancy:", row["OCCUPANCY"])

            st.markdown('</div>', unsafe_allow_html=True)

            # HAZARDS
            st.markdown('<div class="card">', unsafe_allow_html=True)
            st.subheader("Hazards and Irregularities")

            st.write("Geologic Hazard:", row["GEOLOGIC HAZARD (GEOANALYTICS PH & HAZARD HUNTER PH)"])
            st.write("Plan Irregularity:", row["PLAN IRREGULARITY"])
            st.write("Vertical Irregularity:", row["VERTICAL IRREGULARITY"])

            st.markdown('</div>', unsafe_allow_html=True)

            # RESULT
            st.markdown('<div class="card">', unsafe_allow_html=True)
            st.subheader("Assessment Result")

            vulnerability = row["VULNERABILITY"]

            if "Low" in vulnerability:
                st.success(vulnerability)
            elif "Moderate" in vulnerability:
                st.warning(vulnerability)
            else:
                st.error(vulnerability)

            st.markdown('</div>', unsafe_allow_html=True)
