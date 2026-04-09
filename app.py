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
# CUSTOM CSS (CLEAN + MODERN)
# -----------------------------
st.markdown("""
<style>
/* Center content */
.block-container {
    max-width: 900px;
    padding-top: 2rem;
}

/* Typography */
h1 {
    color: #1f4e79;
    text-align: center;
    font-weight: 600;
}

h2 {
    color: #1f4e79;
    margin-top: 1.5rem;
    margin-bottom: 0.5rem;
}

/* Cards */
.card {
    background-color: #ffffff;
    padding: 20px;
    border-radius: 10px;
    border: 1px solid #e5e7eb;
    margin-bottom: 15px;
}

/* Search box */
.search-box {
    background-color: #f9fafb;
    padding: 20px;
    border-radius: 10px;
    border: 1px solid #e5e7eb;
    margin-bottom: 20px;
}

/* Labels */
label {
    font-weight: 500 !important;
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
st.markdown("### Republic of the Philippines")
st.title("Barangay Seismic Vulnerability Records System")
st.caption("Province of Benguet | LISTT Area")

st.markdown("---")

# -----------------------------
# SEARCH PANEL
# -----------------------------
st.markdown('<div class="search-box">', unsafe_allow_html=True)
st.markdown("### 🔍 Search Barangay Record")

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

search = st.button("Search", use_container_width=True)

st.markdown('</div>', unsafe_allow_html=True)

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
        # GENERAL INFO CARD
        # -----------------------------
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.markdown("## General Information")

        col1, col2 = st.columns(2)

        with col1:
            st.write("**Barangay Hall:**", row.get("BARANGAY HALL", "N/A"))
            st.write("**Municipality:**", row.get("MUNICIPALITY", "N/A"))
            st.write("**Year Built:**", row.get("YEAR BUILT", "N/A"))
            st.write("**Occupancy:**", row.get("OCCUPANCY", "N/A"))

        with col2:
            st.write("**Stories Above Grade:**", row.get("NO. OF STORIES ABOVE GRADE", "N/A"))
            st.write("**Stories Below Grade:**", row.get("NO. OF STORIES BELOW GRADE", "N/A"))
            st.write("**Soil Type:**", row.get("SOIL TYPE", "N/A"))
            st.write("**Building Type:**", row.get("BUILDING TYPE", "N/A"))

        st.markdown('</div>', unsafe_allow_html=True)

        # -----------------------------
        # HAZARDS CARD
        # -----------------------------
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.markdown("## Hazards and Irregularities")

        st.write("**Geologic Hazards:**", row.get("GEOLOGIC HAZARD", "N/A"))
        st.write("**Exterior Falling Hazards:**", row.get("EXTERIOR FALLING HAZARDS", "N/A"))
        st.write("**Plan Irregularities:**", row.get("PLAN IRREGULARITY", "N/A"))
        st.write("**Vertical Irregularities:**", row.get("VERTICAL IRREGULARITY", "N/A"))
        st.write("**Adjacency:**", row.get("ADJACENCY", "N/A"))

        st.markdown('</div>', unsafe_allow_html=True)

        # -----------------------------
        # RVS CARD
        # -----------------------------
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.markdown("## RVS Assessment")

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

        st.markdown('</div>', unsafe_allow_html=True)
