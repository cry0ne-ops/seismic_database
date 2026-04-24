import streamlit as st
import pandas as pd
import os

# -----------------------------
# PAGE CONFIG
# -----------------------------
st.set_page_config(
    page_title="Seismic Vulnerability Records",
    layout="wide"
)

# -----------------------------
# DARK MODE CSS
# -----------------------------
st.markdown("""
<style>
.stApp {
    background: #0f172a;
    color: #e5e7eb;
}

.block-container {
    max-width: 1050px;
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

.stButton button {
    background: #2563eb;
    color: white;
    border-radius: 10px;
    border: none;
    font-weight: 600;
}

.stButton button:hover {
    background: #1d4ed8;
    color: white;
}
</style>
""", unsafe_allow_html=True)

# -----------------------------
# LOAD DATA
# -----------------------------
df = pd.read_excel("final_dataset.xlsx")

df.columns = df.columns.str.strip().str.upper()

df["MUNICIPALITY"] = df["MUNICIPALITY"].astype(str).str.strip().str.upper()
df["BARANGAY HALL"] = df["BARANGAY HALL"].astype(str).str.strip().str.upper()
df["VULNERABILITY"] = df["VULNERABILITY"].astype(str).str.strip()

df["RVS SCORE"] = pd.to_numeric(df["RVS SCORE"], errors="coerce")
df["RANK"] = pd.to_numeric(df["RANK"], errors="coerce")

# -----------------------------
# IMAGE DETECTION FUNCTION
# -----------------------------
def get_image_path(base_path):
    for ext in [".jpg", ".png", ".jpeg"]:
        path = base_path + ext
        if os.path.exists(path):
            return path
    return None

# -----------------------------
# HEADER
# -----------------------------
st.title("Seismic Vulnerability Records")
st.markdown(
    '<div class="subtitle">Barangay Hall Assessment System</div>',
    unsafe_allow_html=True
)

# -----------------------------
# SEARCH SECTION
# -----------------------------
st.markdown('<div class="card">', unsafe_allow_html=True)
st.subheader("Search Barangay Record")

col1, col2, col3 = st.columns(3)

with col1:
    municipalities = sorted(df["MUNICIPALITY"].dropna().unique())
    municipality = st.selectbox("Municipality", ["Select"] + municipalities)

with col2:
    if municipality != "Select":
        barangays = df[df["MUNICIPALITY"] == municipality]["BARANGAY HALL"].dropna().unique()
    else:
        barangays = []

    barangay = st.selectbox("Barangay", ["Select"] + sorted(barangays))

with col3:
    st.markdown("<br>", unsafe_allow_html=True)
    search = st.button("Search", use_container_width=True)

st.markdown('</div>', unsafe_allow_html=True)

# -----------------------------
# VULNERABILITY ANALYSIS DASHBOARD
# -----------------------------
st.markdown('<div class="card">', unsafe_allow_html=True)
st.subheader("Vulnerability Overview Dashboard")

graph_municipality = st.selectbox(
    "Filter Graphs by Municipality",
    ["All"] + sorted(df["MUNICIPALITY"].dropna().unique())
)

if graph_municipality != "All":
    graph_df = df[df["MUNICIPALITY"] == graph_municipality]
else:
    graph_df = df.copy()

col1, col2, col3 = st.columns(3)

col1.metric("Total Barangays", len(graph_df))
col2.metric("Average RVS Score", round(graph_df["RVS SCORE"].mean(), 2))
col3.metric("Municipalities Covered", graph_df["MUNICIPALITY"].nunique())

st.markdown("### Overall Vulnerability Distribution")
vuln_counts = graph_df["VULNERABILITY"].value_counts()
st.bar_chart(vuln_counts)

st.markdown("### RVS Score per Barangay")
score_chart = graph_df[["BARANGAY HALL", "RVS SCORE"]].dropna()
score_chart = score_chart.set_index("BARANGAY HALL")
st.bar_chart(score_chart)

st.markdown("### Vulnerability by Municipality")
grouped = graph_df.groupby(["MUNICIPALITY", "VULNERABILITY"]).size().unstack(fill_value=0)
st.bar_chart(grouped)

st.markdown("### High Vulnerability Barangays")
high_risk = graph_df[graph_df["VULNERABILITY"].str.contains("High", case=False, na=False)]

if not high_risk.empty:
    st.dataframe(
        high_risk[[
            "BARANGAY HALL",
            "MUNICIPALITY",
            "RVS SCORE",
            "VULNERABILITY",
            "GRADE OF DAMAGEABILITY",
            "RANK"
        ]].sort_values(by="RANK"),
        use_container_width=True
    )
else:
    st.info("No high vulnerability barangays found.")

st.markdown('</div>', unsafe_allow_html=True)

# -----------------------------
# RESULT SECTION
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

            selected_municipality = str(row["MUNICIPALITY"]).strip().upper()
            selected_barangay = str(row["BARANGAY HALL"]).strip().upper()

            photo_path = get_image_path(
                f"images/{selected_municipality} Pics/{selected_barangay}"
            )

            sketch_path = get_image_path(
                f"images/{selected_municipality} Sketch/{selected_barangay}"
            )

            # SUMMARY
            st.markdown('<div class="card">', unsafe_allow_html=True)

            col1, col2, col3 = st.columns(3)

            col1.metric("RVS Score", row.get("RVS SCORE", "N/A"))
            col2.metric("Damage Grade", row.get("GRADE OF DAMAGEABILITY", "N/A"))
            col3.metric("Rank", row.get("RANK", "N/A"))

            st.markdown('</div>', unsafe_allow_html=True)

            # GENERAL INFORMATION
            st.markdown('<div class="card">', unsafe_allow_html=True)
            st.subheader("General Information")

            col1, col2 = st.columns(2)

            with col1:
                st.write("**Code:**", row.get("CODE", "N/A"))
                st.write("**Barangay Hall:**", row.get("BARANGAY HALL", "N/A"))
                st.write("**Municipality:**", row.get("MUNICIPALITY", "N/A"))
                st.write("**Year Built:**", row.get("YEAR BUILT", "N/A"))
                st.write("**Occupancy:**", row.get("OCCUPANCY", "N/A"))

            with col2:
                st.write("**Above Grade Stories:**", row.get("ABOVE GRADE", "N/A"))
                st.write("**Below Grade Stories:**", row.get("BELOW GRADE", "N/A"))
                st.write("**Total Floor Area:**", row.get("TOTAL FLOOR AREA (SQ. FT.)", "N/A"))
                st.write("**Soil Type:**", row.get("SOIL TYPE", "N/A"))
                st.write("**Building Type:**", row.get("BUILDING TYPE", "N/A"))

            st.markdown('</div>', unsafe_allow_html=True)

            # HAZARDS
            st.markdown('<div class="card">', unsafe_allow_html=True)
            st.subheader("Hazards and Irregularities")

            st.write(
                "**Geologic Hazards:**",
                row.get("GEOLOGIC HAZARD (GEOANALYTICS PH & HAZARD HUNTER PH)", "N/A")
            )
            st.write("**Adjacency:**", row.get("ADJACENCY", "N/A"))
            st.write("**Exterior Falling Hazards:**", row.get("EXTERIOR FALLING HAZARDS", "N/A"))
            st.write("**Vertical Irregularity:**", row.get("VERTICAL IRREGULARITY", "N/A"))
            st.write("**Plan Irregularity:**", row.get("PLAN IRREGULARITY", "N/A"))

            st.markdown('</div>', unsafe_allow_html=True)

            # PHOTO AND SKETCH
            st.markdown('<div class="card">', unsafe_allow_html=True)
            st.subheader("Photo and Sketch of the Structure")

            col1, col2 = st.columns(2)

            with col1:
                st.markdown("**Photo**")
                if photo_path:
                    st.image(photo_path, use_container_width=True)
                else:
                    st.info("No photo available.")

            with col2:
                st.markdown("**Sketch**")
                if sketch_path:
                    st.image(sketch_path, use_container_width=True)
                else:
                    st.info("No sketch available.")

            st.markdown('</div>', unsafe_allow_html=True)

            # CODE CLASSIFICATION
            st.markdown('<div class="card">', unsafe_allow_html=True)
            st.subheader("Code Classification")

            st.write("**Pre-Code Before 1972:**", row.get("PRE-CODE (BEFORE 1972)", "N/A"))
            st.write("**Post-Benchmark After 1972:**", row.get("POST-BENCHMARK (AFTER 1972)", "N/A"))

            st.markdown('</div>', unsafe_allow_html=True)

            # RVS RESULT
            st.markdown('<div class="card">', unsafe_allow_html=True)
            st.subheader("Rapid Visual Screening Result")

            vulnerability = str(row.get("VULNERABILITY", "N/A")).strip()

            st.write("**Score:**", row.get("RVS SCORE", "N/A"))
            st.write("**Vulnerability:**", vulnerability)
            st.write("**Interpretation:**", row.get("INTERPRETATION", "N/A"))
            st.write("**Grade of Damageability:**", row.get("GRADE OF DAMAGEABILITY", "N/A"))

            if "Low" in vulnerability:
                st.success(f"🟢 {vulnerability}")
            elif "Moderate" in vulnerability:
                st.warning(f"🟡 {vulnerability}")
            elif "High" in vulnerability:
                st.error(f"🔴 {vulnerability}")
            else:
                st.info(vulnerability)

            st.markdown('</div>', unsafe_allow_html=True)
