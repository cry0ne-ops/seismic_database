import streamlit as st
import pandas as pd

# -----------------------------
# PAGE CONFIG
# -----------------------------
st.set_page_config(
    page_title="Seismic Vulnerability Records",
    layout="wide"
)

# -----------------------------
# CSS STYLE
# -----------------------------
st.markdown("""
<style>
.block-container {
    max-width: 900px;
    padding-top: 2rem;
}

html, body, [class*="css"] {
    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
}

.fade-in {
    animation: fadeIn 0.6s ease-in-out;
}

@keyframes fadeIn {
    from {opacity: 0; transform: translateY(12px);}
    to {opacity: 1; transform: translateY(0);}
}

h1 {
    font-size: 2.3rem;
    font-weight: 700;
    text-align: center;
    margin-bottom: 0.2em;
}

.subtitle {
    text-align: center;
    color: #666;
    margin-bottom: 2rem;
}

.search-box, .card {
    background: #ffffff;
    padding: 22px;
    border-radius: 16px;
    border: 1px solid #e5e7eb;
    margin-bottom: 18px;
    transition: all 0.2s ease;
}

.search-box:hover, .card:hover {
    box-shadow: 0px 10px 25px rgba(0,0,0,0.06);
}

.section-title {
    font-size: 1.2rem;
    font-weight: 700;
    margin-bottom: 12px;
}
</style>
""", unsafe_allow_html=True)

# -----------------------------
# LOAD DATA
# -----------------------------
df = pd.read_excel("cleaned_full_seismic_dataset.xlsx")

# Clean column names
df.columns = df.columns.str.strip()

# Convert numeric values
df["RVS SCORE"] = pd.to_numeric(df["RVS SCORE"], errors="coerce")

# -----------------------------
# HEADER
# -----------------------------
st.markdown('<div class="fade-in">', unsafe_allow_html=True)
st.markdown("<h1>📊 Seismic Vulnerability Records</h1>", unsafe_allow_html=True)
st.markdown(
    '<div class="subtitle">Search and view barangay hall seismic assessment records</div>',
    unsafe_allow_html=True
)
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
# SEARCH RESULT
# -----------------------------
if search:

    if municipality == "Select" or barangay == "Select":
        st.warning("⚠️ Please select both Municipality and Barangay.")
    else:
        result = df[
            (df["MUNICIPALITY"] == municipality) &
            (df["BARANGAY HALL"] == barangay)
        ]

        if result.empty:
            st.error("No record found.")
        else:
            row = result.iloc[0]

            # -----------------------------
            # SUMMARY METRICS
            # -----------------------------
            st.markdown('<div class="card fade-in">', unsafe_allow_html=True)

            col1, col2, col3 = st.columns(3)

            col1.metric("RVS Score", row.get("RVS SCORE", "N/A"))
            col2.metric("Damage Grade", row.get("GRADE OF DAMAGEABILITY", "N/A"))
            col3.metric("Rank", row.get("RANK", "N/A"))

            st.markdown('</div>', unsafe_allow_html=True)

            # -----------------------------
            # GENERAL INFORMATION
            # -----------------------------
            st.markdown('<div class="card fade-in">', unsafe_allow_html=True)
            st.markdown('<div class="section-title">📌 General Information</div>', unsafe_allow_html=True)

            col1, col2 = st.columns(2)

            with col1:
                st.write("**Name of Barangay Hall:**", row.get("BARANGAY HALL", "N/A"))
                st.write("**Municipality:**", row.get("MUNICIPALITY", "N/A"))
                st.write("**Year Built:**", row.get("YEAR BUILT", "N/A"))
                st.write("**Total Floor Area:**", row.get("TOTAL FLOOR AREA (sq. ft.)", "N/A"))
                st.write("**Occupancy:**", row.get("OCCUPANCY", "N/A"))

            with col2:
                st.write("**Above Grade Stories:**", row.get("ABOVE GRADE", "N/A"))
                st.write("**Below Grade Stories:**", row.get("BELOW GRADE", "N/A"))
                st.write("**Soil Type:**", row.get("SOIL TYPE", "N/A"))
                st.write("**FEMA Building Type:**", row.get("BUILDING TYPE", "N/A"))
                st.write("**Code:**", row.get("CODE", "N/A"))

            st.markdown('</div>', unsafe_allow_html=True)

            # -----------------------------
            # CODE YEAR
            # -----------------------------
            st.markdown('<div class="card fade-in">', unsafe_allow_html=True)
            st.markdown('<div class="section-title">🏗️ Code Classification</div>', unsafe_allow_html=True)

            st.write("**Pre-Code Before 1972:**", row.get("PRE-CODE (Before 1972)", "N/A"))
            st.write("**Post-Benchmark After 1972:**", row.get("POST-BENCHMARK (after 1972)", "N/A"))

            st.markdown('</div>', unsafe_allow_html=True)

            # -----------------------------
            # HAZARDS AND IRREGULARITIES
            # -----------------------------
            st.markdown('<div class="card fade-in">', unsafe_allow_html=True)
            st.markdown('<div class="section-title">⚠️ Hazards and Irregularities</div>', unsafe_allow_html=True)

            st.write(
                "**Geologic Hazards:**",
                row.get("GEOLOGIC HAZARD (Geoanalytics PH & Hazard Hunter PH)", "N/A")
            )
            st.write("**Exterior Falling Hazards:**", row.get("EXTERIOR FALLING HAZARDS", "N/A"))
            st.write("**Plan Irregularities:**", row.get("PLAN IRREGULARITY", "N/A"))
            st.write("**Vertical Irregularities:**", row.get("VERTICAL IRREGULARITY", "N/A"))
            st.write("**Adjacency:**", row.get("ADJACENCY", "N/A"))

            st.markdown('</div>', unsafe_allow_html=True)

            # -----------------------------
            # PHOTO AND SKETCH
            # -----------------------------
            st.markdown('<div class="card fade-in">', unsafe_allow_html=True)
            st.markdown('<div class="section-title">🖼️ Photo and Sketch of the Structure</div>', unsafe_allow_html=True)

            st.info("Photo and sketch section can be added once image files are available.")

            st.markdown('</div>', unsafe_allow_html=True)

            # -----------------------------
            # RVS RESULT
            # -----------------------------
            st.markdown('<div class="card fade-in">', unsafe_allow_html=True)
            st.markdown('<div class="section-title">📊 Rapid Visual Screening Result</div>', unsafe_allow_html=True)

            vulnerability = str(row.get("VULNERABILITY", "N/A")).strip()
            interpretation = row.get("INTERPRETATION", "N/A")

            st.write("**Score:**", row.get("RVS SCORE", "N/A"))
            st.write("**Interpretation:**", interpretation)
            st.write("**Grade of Damageability:**", row.get("GRADE OF DAMAGEABILITY", "N/A"))

            if vulnerability == "Low Vulnerability":
                st.success(f"🟢 {vulnerability}")
            elif vulnerability == "Moderate Vulnerability":
                st.warning(f"🟡 {vulnerability}")
            elif "High" in vulnerability:
                st.error(f"🔴 {vulnerability}")
            else:
                st.write(vulnerability)

            st.markdown('</div>', unsafe_allow_html=True)
