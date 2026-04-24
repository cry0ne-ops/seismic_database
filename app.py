import streamlit as st
import pandas as pd

# -----------------------------
# LOAD DATA (SAFE FOR CLOUD)
# -----------------------------
df = pd.read_excel("final_dataset.xlsx")

# Fix column names (VERY IMPORTANT)
df.columns = df.columns.str.strip().str.upper()

# Convert numeric safely
df["RVS SCORE"] = pd.to_numeric(df["RVS SCORE"], errors="coerce")

# -----------------------------
# PAGE CONFIG
# -----------------------------
st.set_page_config(page_title="Seismic System", layout="wide")

# -----------------------------
# SIMPLE CLEAN UI
# -----------------------------
st.markdown("""
<style>
.stApp {
    background: #0f172a;
    color: #e5e7eb;
}

.block-container {
    max-width: 900px;
    padding-top: 2rem;
}

h1, h2, h3 {
    color: #f8fafc;
}

h1 {
    text-align: center;
    font-weight: 700;
}

.subtitle {
    text-align: center;
    color: #94a3b8;
    margin-bottom: 2rem;
}

.card {
    background: #111827;
    padding: 22px;
    border-radius: 14px;
    border: 1px solid #334155;
    margin-bottom: 16px;
    box-shadow: 0 10px 25px rgba(0,0,0,0.25);
}

div[data-testid="stMetric"] {
    background: #1e293b;
    padding: 16px;
    border-radius: 12px;
    border: 1px solid #334155;
}

div[data-testid="stMetricLabel"] {
    color: #94a3b8;
}

div[data-testid="stMetricValue"] {
    color: #f8fafc;
}

.stSelectbox label {
    color: #e5e7eb !important;
}

.stButton button {
    background: #2563eb;
    color: white;
    border-radius: 10px;
    border: none;
    padding: 0.6rem 1rem;
    font-weight: 600;
}

.stButton button:hover {
    background: #1d4ed8;
    color: white;
}

[data-testid="stMarkdownContainer"] {
    color: #e5e7eb;
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
    municipalities = sorted(df["MUNICIPALITY"].dropna().unique())
    municipality = st.selectbox("Municipality", ["Select"] + municipalities)

with col2:
    if municipality != "Select":
        barangays = df[df["MUNICIPALITY"] == municipality]["BARANGAY HALL"].dropna().unique()
    else:
        barangays = []

    barangay = st.selectbox("Barangay", ["Select"] + list(barangays))

with col3:
    st.markdown("<br>", unsafe_allow_html=True)
    search = st.button("Search", use_container_width=True)

# -----------------------------
# RESULT SECTION
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
            st.error("No data found.")
        else:
            row = result.iloc[0]

            # -----------------------------
            # SUMMARY
            # -----------------------------
            st.markdown('<div class="card">', unsafe_allow_html=True)

            col1, col2, col3 = st.columns(3)

            col1.metric("RVS Score", row.get("RVS SCORE", "N/A"))
            col2.metric("Damage Grade", row.get("GRADE OF DAMAGEABILITY", "N/A"))
            col3.metric("Rank", row.get("RANK", "N/A"))

            st.markdown('</div>', unsafe_allow_html=True)

            # -----------------------------
            # GENERAL INFO
            # -----------------------------
            st.markdown('<div class="card">', unsafe_allow_html=True)
            st.subheader("General Information")

            st.write("**Barangay Hall:**", row.get("BARANGAY HALL", "N/A"))
            st.write("**Municipality:**", row.get("MUNICIPALITY", "N/A"))
            st.write("**Year Built:**", row.get("YEAR BUILT", "N/A"))
            st.write("**Total Floor Area:**", row.get("TOTAL FLOOR AREA (SQ. FT.)", "N/A"))
            st.write("**Occupancy:**", row.get("OCCUPANCY", "N/A"))

            st.markdown('</div>', unsafe_allow_html=True)

            # -----------------------------
            # STRUCTURAL INFO
            # -----------------------------
            st.markdown('<div class="card">', unsafe_allow_html=True)
            st.subheader("Structural Information")

            st.write("**Stories Above Grade:**", row.get("ABOVE GRADE", "N/A"))
            st.write("**Stories Below Grade:**", row.get("BELOW GRADE", "N/A"))
            st.write("**Soil Type:**", row.get("SOIL TYPE", "N/A"))
            st.write("**Building Type:**", row.get("BUILDING TYPE", "N/A"))

            st.markdown('</div>', unsafe_allow_html=True)

            # -----------------------------
            # HAZARDS
            # -----------------------------
            st.markdown('<div class="card">', unsafe_allow_html=True)
            st.subheader("Hazards and Irregularities")

            st.write("**Geologic Hazards:**", row.get("GEOLOGIC HAZARD (GEOANALYTICS PH & HAZARD HUNTER PH)", "N/A"))
            st.write("**Exterior Falling Hazards:**", row.get("EXTERIOR FALLING HAZARDS", "N/A"))
            st.write("**Plan Irregularity:**", row.get("PLAN IRREGULARITY", "N/A"))
            st.write("**Vertical Irregularity:**", row.get("VERTICAL IRREGULARITY", "N/A"))
            st.write("**Adjacency:**", row.get("ADJACENCY", "N/A"))

            st.markdown('</div>', unsafe_allow_html=True)

            # -----------------------------
            # CODE CLASSIFICATION
            # -----------------------------
            st.markdown('<div class="card">', unsafe_allow_html=True)
            st.subheader("Code Classification")

            st.write("**Pre-Code (Before 1972):**", row.get("PRE-CODE (BEFORE 1972)", "N/A"))
            st.write("**Post-Benchmark (After 1972):**", row.get("POST-BENCHMARK (AFTER 1972)", "N/A"))

            st.markdown('</div>', unsafe_allow_html=True)

            # -----------------------------
            # RVS RESULT
            # -----------------------------
            st.markdown('<div class="card">', unsafe_allow_html=True)
            st.subheader("Assessment Result")

            vulnerability = str(row.get("VULNERABILITY", "N/A"))

            st.write("**Interpretation:**", row.get("INTERPRETATION", "N/A"))
            st.write("**Damageability Grade:**", row.get("GRADE OF DAMAGEABILITY", "N/A"))

            if "Low" in vulnerability:
                st.success(f"🟢 {vulnerability}")
            elif "Moderate" in vulnerability:
                st.warning(f"🟡 {vulnerability}")
            else:
                st.error(f"🔴 {vulnerability}")

            st.markdown('</div>', unsafe_allow_html=True)
