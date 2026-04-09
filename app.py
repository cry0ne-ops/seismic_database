import streamlit as st
import pandas as pd

# -----------------------------
# PAGE CONFIG
# -----------------------------
st.set_page_config(
    page_title="Barangay Seismic Records",
    layout="wide"
)

# -----------------------------
# MINIMAL CSS
# -----------------------------
st.markdown("""
<style>
body {
    background-color: #ffffff;
}

h1 {
    color: #1f4e79;
    text-align: center;
}

h2 {
    color: #1f4e79;
    border-bottom: 2px solid #ddd;
    padding-bottom: 5px;
}

.section {
    padding: 15px 0;
}

</style>
""", unsafe_allow_html=True)

# -----------------------------
# LOAD DATA
# -----------------------------
df = pd.read_excel("cleaned_full_seismic_dataset.xlsx")
df["RVS SCORE"] = pd.to_numeric(df["RVS SCORE"], errors='coerce')
df["PROVINCE"] = "Benguet"

# -----------------------------
# HEADER
# -----------------------------
st.title("Barangay Seismic Vulnerability Records System")
st.caption("Province of Benguet | LISTT Area")

st.divider()

# -----------------------------
# SEARCH SECTION
# -----------------------------
st.markdown("## 🔍 Search Barangay Record")

col1, col2, col3 = st.columns(3)

with col1:
    province = st.selectbox("Province", ["Benguet"])

with col2:
    municipalities = sorted(df["MUNICIPALITY"].dropna().unique())
    municipality = st.selectbox("Municipality", ["Select"] + municipalities)

with col3:
    if municipality != "Select":
        barangays = df[df["MUNICIPALITY"] == municipality]["BARANGAY HALL"].dropna().unique()
    else:
        barangays = []

    barangay = st.selectbox("Barangay", ["Select"] + sorted(barangays))

search = st.button("Search")

st.divider()

# -----------------------------
# RESULT
# -----------------------------
if search:

    if municipality == "Select" or barangay == "Select":
        st.warning("Please select Municipality and Barangay.")
    else:
        row = df[
            (df["MUNICIPALITY"] == municipality) &
            (df["BARANGAY HALL"] == barangay)
        ].iloc[0]

        # -----------------------------
        # GENERAL INFORMATION
        # -----------------------------
        st.markdown("## General Information")

        col1, col2 = st.columns(2)

        with col1:
            st.write("**Barangay Hall:**", row.get("BARANGAY HALL", "N/A"))
            st.write("**Municipality:**", row.get("MUNICIPALITY", "N/A"))
            st.write("**Year Built:**", row.get("YEAR BUILT", "N/A"))
            st.write("**Occupancy:**", row.get("OCCUPANCY", "N/A"))
            st.write("**Soil Type:**", row.get("SOIL TYPE", "N/A"))

        with col2:
            st.write("**Stories Above Grade:**", row.get("NO. OF STORIES ABOVE GRADE", "N/A"))
            st.write("**Stories Below Grade:**", row.get("NO. OF STORIES BELOW GRADE", "N/A"))
            st.write("**Floor Area:**", row.get("TOTAL FLOOR AREA", "N/A"))
            st.write("**Building Type:**", row.get("BUILDING TYPE", "N/A"))

        st.divider()

        # -----------------------------
        # HAZARDS
        # -----------------------------
        st.markdown("## Hazards and Irregularities")

        st.write("**Geologic Hazards:**", row.get("GEOLOGIC HAZARD", "N/A"))
        st.write("**Exterior Falling Hazards:**", row.get("EXTERIOR FALLING HAZARDS", "N/A"))
        st.write("**Plan Irregularities:**", row.get("PLAN IRREGULARITY", "N/A"))
        st.write("**Vertical Irregularities:**", row.get("VERTICAL IRREGULARITY", "N/A"))
        st.write("**Adjacency:**", row.get("ADJACENCY", "N/A"))

        st.divider()

        # -----------------------------
        # RVS RESULT
        # -----------------------------
        st.markdown("## RVS Result")

        score = row.get("RVS SCORE", "N/A")
        interpretation = row.get("INTERPRETATION", "N/A")

        st.write("**Score:**", score)

        if interpretation == "Low Vulnerability":
            st.success(interpretation)
        elif interpretation == "Moderate Vulnerability":
            st.warning(interpretation)
        elif interpretation == "High Vulnerability":
            st.error(interpretation)
        else:
            st.write(interpretation)
