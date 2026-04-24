import streamlit as st
import pandas as pd
import os
import matplotlib.pyplot as plt

st.set_page_config(page_title="Seismic Vulnerability Records", layout="wide")

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
df.columns = df.columns.astype(str).str.strip().str.upper()

required_cols = ["MUNICIPALITY", "BARANGAY HALL", "VULNERABILITY", "RVS SCORE"]
missing = [col for col in required_cols if col not in df.columns]

if missing:
    st.error(f"Missing required columns: {missing}")
    st.write("Available columns:", list(df.columns))
    st.stop()

df["MUNICIPALITY"] = df["MUNICIPALITY"].astype(str).str.strip().str.upper()
df["BARANGAY HALL"] = df["BARANGAY HALL"].astype(str).str.strip()
df["VULNERABILITY"] = df["VULNERABILITY"].astype(str).str.strip()
df["RVS SCORE"] = pd.to_numeric(df["RVS SCORE"], errors="coerce")

if "RANK" in df.columns:
    df["RANK"] = pd.to_numeric(df["RANK"], errors="coerce")

# -----------------------------
# HELPERS
# -----------------------------
def get_value(row, col_name):
    return row[col_name] if col_name in row.index else "N/A"

def get_image_path(folder_path, barangay_name):
    if not os.path.isdir(folder_path):
        return None

    barangay_clean = str(barangay_name).strip().lower()

    for file in os.listdir(folder_path):
        name, ext = os.path.splitext(file)
        if ext.lower() in [".jpg", ".jpeg", ".png"]:
            if name.strip().lower() == barangay_clean:
                return os.path.join(folder_path, file)

    return None

def horizontal_bar_chart(data, title, xlabel):
    fig, ax = plt.subplots(figsize=(9, 5))
    data.plot(kind="barh", ax=ax)
    ax.set_title(title, fontsize=14)
    ax.set_xlabel(xlabel)
    ax.set_ylabel("")
    ax.bar_label(ax.containers[0], padding=3)
    ax.grid(axis="x", linestyle="--", alpha=0.4)
    plt.tight_layout()
    st.pyplot(fig)

# -----------------------------
# SIDEBAR
# -----------------------------
st.sidebar.header("Navigation")

st.sidebar.markdown("---")
st.sidebar.markdown("### 📌 Thesis Information")
st.sidebar.markdown("""
**DATABASE DEVELOPMENT ON SEISMIC VULNERABILITY OF  
BARANGAY HALLS IN L.I.S.T.T. AREA**

This system stores, organizes, searches, and visualizes seismic vulnerability records of barangay halls using Rapid Visual Screening (RVS).

**Coverage Area:**
- La Trinidad
- Itogon
- Sablan
- Tuba
- Tublay
""")

page = st.sidebar.radio(
    "Go to",
    ["🔍 Search Barangay", "📊 Dashboard", "ℹ️ About"]
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
                selected_barangay = str(row["BARANGAY HALL"]).strip()

                photo_folder = f"images/{selected_municipality} PICS"
                sketch_folder = f"images/{selected_municipality} SKETCHES"

                photo_path = get_image_path(photo_folder, selected_barangay)
                sketch_path = get_image_path(sketch_folder, selected_barangay)

                st.markdown('<div class="card">', unsafe_allow_html=True)
                c1, c2, c3 = st.columns(3)

                c1.metric("RVS Score", get_value(row, "RVS SCORE"))
                c2.metric("Damage Grade", get_value(row, "GRADE OF DAMAGEABILITY"))
                c3.metric("Rank", get_value(row, "RANK"))

                st.markdown("</div>", unsafe_allow_html=True)

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

                st.markdown('<div class="card">', unsafe_allow_html=True)
                st.subheader("Hazards and Irregularities")

                st.write("**Geologic Hazards:**", get_value(row, "GEOLOGIC HAZARD (GEOANALYTICS PH & HAZARD HUNTER PH)"))
                st.write("**Adjacency:**", get_value(row, "ADJACENCY"))
                st.write("**Exterior Falling Hazards:**", get_value(row, "EXTERIOR FALLING HAZARDS"))
                st.write("**Vertical Irregularity:**", get_value(row, "VERTICAL IRREGULARITY"))
                st.write("**Plan Irregularity:**", get_value(row, "PLAN IRREGULARITY"))

                st.markdown("</div>", unsafe_allow_html=True)

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

                st.markdown('<div class="card">', unsafe_allow_html=True)
                st.subheader("Code Classification")

                st.write("**Pre-Code Before 1972:**", get_value(row, "PRE-CODE (BEFORE 1972)"))
                st.write("**Post-Benchmark After 1972:**", get_value(row, "POST-BENCHMARK (AFTER 1972)"))

                st.markdown("</div>", unsafe_allow_html=True)

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
    st.caption("Panel-friendly summary of seismic vulnerability results")

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

    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.subheader("Vulnerability Distribution")

    vulnerability_counts = dashboard_df["VULNERABILITY"].value_counts().sort_values()
    horizontal_bar_chart(
        vulnerability_counts,
        "Number of Barangay Halls per Vulnerability Level",
        "Number of Barangay Halls"
    )

    st.markdown("</div>", unsafe_allow_html=True)

    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.subheader("Average RVS Score by Municipality")

    avg_scores = dashboard_df.groupby("MUNICIPALITY")["RVS SCORE"].mean().sort_values()
    horizontal_bar_chart(
        avg_scores,
        "Average RVS Score by Municipality",
        "Average RVS Score"
    )

    st.markdown("</div>", unsafe_allow_html=True)

    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.subheader("RVS Score per Barangay")

    score_chart = dashboard_df[["BARANGAY HALL", "RVS SCORE"]].dropna()
    score_chart = score_chart.sort_values("RVS SCORE")

    fig, ax = plt.subplots(figsize=(10, max(5, len(score_chart) * 0.35)))
    ax.barh(score_chart["BARANGAY HALL"], score_chart["RVS SCORE"])
    ax.set_title("RVS Score per Barangay Hall", fontsize=14)
    ax.set_xlabel("RVS Score")
    ax.set_ylabel("Barangay Hall")
    ax.bar_label(ax.containers[0], padding=3)
    ax.grid(axis="x", linestyle="--", alpha=0.4)
    plt.tight_layout()
    st.pyplot(fig)

    st.markdown("</div>", unsafe_allow_html=True)

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

# ==================================================
# PAGE 3: ABOUT
# ==================================================
elif page == "ℹ️ About":

    st.title("About the System")

    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.subheader("Thesis Title")

    st.write("""
    **DATABASE DEVELOPMENT ON SEISMIC VULNERABILITY OF BARANGAY HALLS IN L.I.S.T.T.  
    (LA TRINIDAD, ITOGON, SABLAN, TUBA, TUBLAY) AREA USING RAPID VISUAL SCREENING**
    """)

    st.markdown("</div>", unsafe_allow_html=True)

    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.subheader("System Description")

    st.write("""
    This web-based system is designed to store, manage, search, and visualize seismic vulnerability
    records of barangay halls within the L.I.S.T.T. area. It uses Rapid Visual Screening (RVS)
    data to provide users with structured information about each barangay hall, including building
    characteristics, hazards, irregularities, RVS scores, vulnerability classification, photos,
    and structural sketches.
    """)

    st.markdown("</div>", unsafe_allow_html=True)

    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.subheader("Main Features")

    st.write("""
    - Search barangay hall records by municipality and barangay
    - View structural and hazard-related information
    - Display photos and sketches of barangay hall structures
    - Analyze vulnerability distribution through readable graphs
    - Filter dashboard results by municipality
    - Identify high-vulnerability barangay halls
    """)

    st.markdown("</div>", unsafe_allow_html=True)

    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.subheader("Coverage Area")

    st.write("""
    The system covers barangay halls located in:
    - La Trinidad
    - Itogon
    - Sablan
    - Tuba
    - Tublay
    """)

    st.markdown("</div>", unsafe_allow_html=True)
