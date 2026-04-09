import streamlit as st
import pandas as pd

# -----------------------------
# PAGE CONFIG
# -----------------------------
st.set_page_config(
    page_title="Seismic Vulnerability System",
    layout="wide"
)

# -----------------------------
# MODERN CSS + ANIMATIONS
# -----------------------------
st.markdown("""
<style>
/* Center content */
.block-container {
    max-width: 850px;
    padding-top: 2rem;
}

/* Font */
html, body, [class*="css"] {
    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
}

/* Fade animation */
.fade-in {
    animation: fadeIn 0.6s ease-in-out;
}

@keyframes fadeIn {
    from {opacity: 0; transform: translateY(10px);}
    to {opacity: 1; transform: translateY(0);}
}

/* Header */
h1 {
    font-size: 2.2rem;
    font-weight: 600;
    text-align: center;
    margin-bottom: 0.2em;
}

.subtitle {
    text-align: center;
    color: #666;
    margin-bottom: 2rem;
}

/* Search box */
.search-box {
    background: #ffffff;
    padding: 22px;
    border-radius: 14px;
    border: 1px solid #e5e7eb;
    margin-bottom: 20px;
    transition: all 0.2s ease;
}

.search-box:hover {
    box-shadow: 0px 8px 20px rgba(0,0,0,0.06);
}

/* Cards */
.card {
    background: #ffffff;
    padding: 20px;
    border-radius: 14px;
    border: 1px solid #e5e7eb;
    margin-bottom: 15px;
    transition: all 0.2s ease;
}

.card:hover {
    box-shadow: 0px 8px 20px rgba(0,0,0,0.06);
}

/* Section titles */
.section-title {
    font-size: 1.15rem;
    font-weight: 600;
    margin-bottom: 10px;
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

# -----------------------------
# HEADER
# -----------------------------
st.markdown('<div class="fade-in">', unsafe_allow_html=True)
st.markdown("<h1>📊 Seismic Vulnerability Records</h1>", unsafe_allow_html=True)
st.markdown('<div class="subtitle">Search and explore barangay structural assessment data</div>', unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)

# -----------------------------
# SEARCH PANEL
# -----------------------------
st.markdown('<div class="search-box fade-in">', unsafe_allow_html=True)

col1, col2, col3 = st.columns(3)

with col1:
    municipalities = sorted(df["MUNICIPALITY"].dropna().unique())
    municipality = st.selectbox("📍 Municipality", ["Select"] + municipalities)

with col2:
    if municipality != "Select":
        barangays = df[df["MUNICIPALITY"] == municipality]["BARANGAY HALL"].dropna().unique()
    else:
        barangays = []

    barangay = st.selectbox("🏘️ Barangay", ["Select"] + sorted(barangays))

with col3:
    st.markdown("<br>", unsafe_allow_html=True)
    search = st.button("🔍 Search", use_container_width=True)

st.markdown('</div>', unsafe_allow_html=True)

# -----------------------------
# RESULT
# -----------------------------
if search:

    if municipality == "Select" or barangay == "Select":
        st.warning("⚠️ Please complete all fields.")
    else:
        row = df[
            (df["MUNICIPALITY"] == municipality) &
            (df["BARANGAY HALL"] == barangay)
        ].iloc[0]

        # -----------------------------
        # GENERAL INFO
        # -----------------------------
        st.markdown('<div class="card fade-in">', unsafe_allow_html=True)
        st.markdown('<div class="section-title">📌 General Information</div>', unsafe_allow_html=True)

        col1, col2 = st.columns(2)

        with col1:
            st.write("**Barangay:**", row.get("BARANGAY HALL", "N/A"))
            st.write("**Municipality:**", row.get("MUNICIPALITY", "N/A"))
            st.write("**Year Built:**", row.get("YEAR BUILT", "N/A"))
            st.write("**Occupancy:**", row.get("OCCUPANCY", "N/A"))

        with col2:
            st.write("**Stories Above:**", row.get("NO. OF STORIES ABOVE GRADE", "N/A"))
            st.write("**Stories Below:**", row.get("NO. OF STORIES BELOW GRADE", "N/A"))
            st.write("**Soil Type:**", row.get("SOIL TYPE", "N/A"))
            st.write("**Building Type:**", row.get("BUILDING TYPE", "N/A"))

        st.markdown('</div>', unsafe_allow_html=True)

        # -----------------------------
        # HAZARDS
        # -----------------------------
        st.markdown('<div class="card fade-in">', unsafe_allow_html=True)
        st.markdown('<div class="section-title">⚠️ Hazards & Irregularities</div>', unsafe_allow_html=True)

        st.write("**Geologic Hazards:**", row.get("GEOLOGIC HAZARD", "N/A"))
        st.write("**Exterior Hazards:**", row.get("EXTERIOR FALLING HAZARDS", "N/A"))
        st.write("**Plan Irregularities:**", row.get("PLAN IRREGULARITY", "N/A"))
        st.write("**Vertical Irregularities:**", row.get("VERTICAL IRREGULARITY", "N/A"))
        st.write("**Adjacency:**", row.get("ADJACENCY", "N/A"))

        st.markdown('</div>', unsafe_allow_html=True)

        # -----------------------------
        # RVS RESULT
        # -----------------------------
        st.markdown('<div class="card fade-in">', unsafe_allow_html=True)
        st.markdown('<div class="section-title">📊 Assessment Result</div>', unsafe_allow_html=True)

        score = row.get("RVS SCORE", "N/A")
        interpretation = row.get("INTERPRETATION", "N/A")

        st.metric("RVS Score", score)

        if interpretation == "Low Vulnerability":
            st.success(f"🟢 {interpretation}")
        elif interpretation == "Moderate Vulnerability":
            st.warning(f"🟡 {interpretation}")
        elif interpretation == "High Vulnerability":
            st.error(f"🔴 {interpretation}")
        else:
            st.write(interpretation)

        st.markdown('</div>', unsafe_allow_html=True)
