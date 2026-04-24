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
    max-width: 1100px;
    padding-top: 2rem;
}

h1, h2, h3 {
    color: #f8fafc;
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

# Clean column names
df.columns = (
    df.columns
    .astype(str)
    .str.strip()
    .str.upper()
)

# Safety check
required_cols = ["MUNICIPALITY", "BARANGAY HALL", "VULNERABILITY", "RVS SCORE"]

missing = [col for col in required_cols if col not in df.columns]

if missing:
    st.error(f"Missing required columns: {missing}")
    st.write("Available columns:", list(df.columns))
    st.stop()

# Clean data values
df["MUNICIPALITY"] = df["MUNICIPALITY"].astype(str).str.strip().str.upper()
df["BARANGAY HALL"] = df["BARANGAY HALL"].astype(str).str.strip().str.upper()
df["VULNERABILITY"] = df["VULNERABILITY"].astype(str).str.strip()

df["RVS SCORE"] = pd.to_numeric(df["RVS SCORE"], errors="coerce")

if "RANK" in df.columns:
    df["RANK"] = pd.to_numeric(df["RANK"], errors="coerce")

# -----------------------------
# HELPER FUNCTIONS
# -----------------------------
def get_value(row, col_name):
    return row[col_name] if col_name in row.index else "N/A"

def get_image_path(base_path):
    for ext in [".jpg", ".jpeg", ".png"]:
        path = base_path + ext
        if os.path.exists(path):
            return path
    return None

# -----------------------------
# SIDEBAR NAVIGATION
# -----------------------------
st.sidebar.title("Navigation")

page = st.sidebar.radio(
    "Go to",
    ["🔍 Search Barangay", "📊 Dashboard"]
)

# ==================================================
# PAGE 1: SEARCH BARANGAY
# ==================================================
if page == "🔍 Search Barangay":

    st.title("Seismic Vulnerability Records")
    st.caption("Barangay Hall Assessment System")

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

    st.markdown("</div>", unsafe_allow_html=True)

    if search:

        if municipality == "Select" or barangay == "Select":
            st.warning("Please select both Municipality and Barangay.")
        else:
            result = df[
                (df["MUNICIPALITY"] == municipality) &
                (df["BARANGAY HALL"] == barangay)
            ]

            if result.empty:
                st.error("No record found.")
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

                c1, c2, c3 = st.columns(3)

                c1.metric("RVS Score", get_value(row, "RVS SCORE"))
                c2.metric("Damage Grade", get_value(row, "GRADE OF DAMAGEABILITY"))
                c3.metric("Rank", get_value(row, "RANK"))

                st.markdown("</div>", unsafe_allow_html=True)

                # GENERAL INFORMATION
                st.markdown('<div class="card">', unsafe_allow_html=True)
                st.subheader("General Information")

                col1, col2 = st.columns(2)

                with col1:
                    st.write("**Code:**", get_value(row, "CODE"))
                    st.write("**Barangay Hall:**", get_value(row, "BARANGAY HALL"))
                    st.write("**Municipality:**", get_value(row, "MUNICIPALITY"))
                    st.write("**Year Built:**", get_value(row, "YEAR BUILT"))
                    st.write("**Occupancy:**", get_value(row, "OCCUPANCY"))

                with col2:
                    st.write("**Above Grade Stories:**", get_value(row, "ABOVE GRADE"))
                    st.write("**Below Grade Stories:**", get_value(row, "BELOW GRADE"))
                    st.write("**Total Floor Area:**", get_value(row, "TOTAL FLOOR AREA (SQ. FT.)"))
                    st.write("**Soil Type:**", get_value(row, "SOIL TYPE"))
                    st.write("**Building Type:**", get_value(row, "BUILDING TYPE"))

                st.markdown("</div>", unsafe_allow_html=True)

                # HAZARDS
                st.markdown('<div class="card">', unsafe_allow_html=True)
                st.subheader("Hazards and Irregularities")

                st.write(
                    "**Geologic Hazards:**",
                    get_value(row, "GEOLOGIC HAZARD (GEOANALYTICS PH & HAZARD HUNTER PH)")
                )
                st.write("**Adjacency:**", get_value(row, "ADJACENCY"))
                st.write("**Exterior Falling Hazards:**", get_value(row, "EXTERIOR FALLING HAZARDS"))
                st.write("**Vertical Irregularity:**", get_value(row, "VERTICAL IRREGULARITY"))
                st.write("**Plan Irregularity:**", get_value(row, "PLAN IRREGULARITY"))

                st.markdown("</div>", unsafe_allow_html=True)

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

                st.markdown("</div>", unsafe_allow_html=True)

                # CODE CLASSIFICATION
                st.markdown('<div class="card">', unsafe_allow_html=True)
                st.subheader("Code Classification")

                st.write("**Pre-Code Before 1972:**", get_value(row, "PRE-CODE (BEFORE 1972)"))
                st.write("**Post-Benchmark After 1972:**", get_value(row, "POST-BENCHMARK (AFTER 1972)"))

                st.markdown("</div>", unsafe_allow_html=True)

                # RVS RESULT
                st.markdown('<div class="card">', unsafe_allow_html=True)
                st.subheader("Rapid Visual Screening Result")

                vulnerability = str(get_value(row, "VULNERABILITY")).strip()

                st.write("**Score:**", get_value(row, "RVS SCORE"))
                st.write("**Vulnerability:**", vulnerability)
                st.write("**Interpretation:**", get_value(row, "INTERPRETATION"))
                st.write("**Grade of Damageability:**", get_value(row, "GRADE OF DAMAGEABILITY"))

                if "LOW" in vulnerability.upper():
                    st.success(f"🟢 {vulnerability}")
                elif "MODERATE" in vulnerability.upper():
                    st.warning(f"🟡 {vulnerability}")
                elif "HIGH" in vulnerability.upper():
                    st.error(f"🔴 {vulnerability}")
                else:
                    st.info(vulnerability)

                st.markdown("</div>", unsafe_allow_html=True)

# ==================================================
# PAGE 2: DASHBOARD
# ==================================================
elif page == "📊 Dashboard":

    st.title("Vulnerability Dashboard")
    st.caption("Overall vulnerability analysis of barangay halls")

    st.markdown('<div class="card">', unsafe_allow_html=True)

    selected_municipality = st.selectbox(
        "Filter by Municipality",
        ["All"] + sorted(df["MUNICIPALITY"].dropna().unique())
    )

    if selected_municipality != "All":
        dashboard_df = df[df["MUNICIPALITY"] == selected_municipality]
    else:
        dashboard_df = df.copy()

    c1, c2, c3 = st.columns(3)

    c1.metric("Total Barangays", len(dashboard_df))
    c2.metric("Average RVS Score", round(dashboard_df["RVS SCORE"].mean(), 2))

    high_count = dashboard_df[
        dashboard_df["VULNERABILITY"].str.contains("High", case=False, na=False)
    ].shape[0]

    c3.metric("High Vulnerability", high_count)

    st.markdown("</div>", unsafe_allow_html=True)

    # GRAPH 1
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.subheader("Vulnerability Distribution")

    vulnerability_counts = dashboard_df["VULNERABILITY"].value_counts()
    st.bar_chart(vulnerability_counts)

    st.markdown("</div>", unsafe_allow_html=True)

    # GRAPH 2
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.subheader("RVS Score per Barangay")

    score_chart = dashboard_df[["BARANGAY HALL", "RVS SCORE"]].dropna()
    score_chart = score_chart.set_index("BARANGAY HALL")

    st.bar_chart(score_chart)

    st.markdown("</div>", unsafe_allow_html=True)

    # GRAPH 3
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.subheader("Vulnerability by Municipality")

    grouped = (
        dashboard_df
        .groupby(["MUNICIPALITY", "VULNERABILITY"])
        .size()
        .unstack(fill_value=0)
    )

    st.bar_chart(grouped)

    st.markdown("</div>", unsafe_allow_html=True)

    # HIGH RISK TABLE
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.subheader("High Vulnerability Barangays")

    high_risk = dashboard_df[
        dashboard_df["VULNERABILITY"].str.contains("High", case=False, na=False)
    ]

    if not high_risk.empty:
        columns_to_show = [
            col for col in [
                "BARANGAY HALL",
                "MUNICIPALITY",
                "RVS SCORE",
                "VULNERABILITY",
                "GRADE OF DAMAGEABILITY",
                "RANK"
            ] if col in high_risk.columns
        ]

        st.dataframe(
            high_risk[columns_to_show].sort_values(by="RANK", na_position="last"),
            use_container_width=True
        )
    else:
        st.info("No high vulnerability barangays found.")

    st.markdown("</div>", unsafe_allow_html=True)
