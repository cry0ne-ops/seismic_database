import streamlit as st
import pandas as pd
import os
import matplotlib.pyplot as plt
from io import BytesIO
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas

# ==================================================
# PAGE CONFIG
# ==================================================
st.set_page_config(
    page_title="Seismic Vulnerability Records",
    layout="wide"
)

# ==================================================
# DARK MODE + ANIMATIONS
# ==================================================
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

.subtitle {
    color: #94a3b8;
    font-size: 1rem;
    margin-bottom: 2rem;
}

.card {
    background: #111827;
    padding: 24px;
    border-radius: 16px;
    border: 1px solid #334155;
    margin-bottom: 18px;
    box-shadow: 0 10px 25px rgba(0,0,0,0.25);
    animation: fadeIn 0.6s ease-in-out;
}

.small-muted {
    color: #cbd5e1;
    font-size: 0.95rem;
    line-height: 1.6;
    margin-top: 15px;
}

@keyframes fadeIn {
    from {
        opacity: 0;
        transform: translateY(12px);
    }
    to {
        opacity: 1;
        transform: translateY(0);
    }
}

.stButton button {
    background: #2563eb;
    color: white;
    border-radius: 10px;
    border: none;
    font-weight: 600;
    padding: 0.65rem 1rem;
}

.stButton button:hover {
    background: #1d4ed8;
    color: white;
}

div[data-testid="stMetric"] {
    background: #1e293b;
    padding: 14px;
    border-radius: 12px;
    border: 1px solid #334155;
}
</style>
""", unsafe_allow_html=True)

# ==================================================
# LOAD DATA
# ==================================================
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

# ==================================================
# SESSION STATE
# ==================================================
if "page" not in st.session_state:
    st.session_state.page = "About"

# ==================================================
# HELPER FUNCTIONS
# ==================================================
def get_value(row, col_name):
    if col_name not in row.index:
        return "No Data Recorded"

    value = row[col_name]

    if pd.isna(value):
        return "No Data Recorded"

    value_str = str(value).strip()

    if value_str.lower() in ["nan", "none", "null", "n/a", "na", ""]:
        return "No Data Recorded"

    if isinstance(value, float) and value.is_integer():
        return int(value)

    return value


def get_metric_value(row, col_name):
    value = get_value(row, col_name)
    return "—" if value == "No Data Recorded" else value


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

    if len(ax.containers) > 0:
        ax.bar_label(ax.containers[0], padding=3)

    ax.grid(axis="x", linestyle="--", alpha=0.4)
    plt.tight_layout()
    st.pyplot(fig)


from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image
from reportlab.lib.styles import getSampleStyleSheet

def generate_pdf(row, photo_path=None, sketch_path=None):

    buffer = BytesIO()

    doc = SimpleDocTemplate(buffer, pagesize=A4)
    styles = getSampleStyleSheet()

    elements = []

    # TITLE
    elements.append(Paragraph(
        "<b>Seismic Vulnerability Barangay Hall Report</b>",
        styles['Title']
    ))
    elements.append(Spacer(1, 12))

    # BASIC INFO
    elements.append(Paragraph(
        f"<b>Barangay Hall:</b> {get_value(row, 'BARANGAY HALL')}",
        styles['Normal']
    ))
    elements.append(Paragraph(
        f"<b>Municipality:</b> {get_value(row, 'MUNICIPALITY')}",
        styles['Normal']
    ))
    elements.append(Spacer(1, 10))

    # RVS RESULT
    elements.append(Paragraph(
        f"<b>RVS Score:</b> {get_value(row, 'RVS SCORE')}",
        styles['Normal']
    ))
    elements.append(Paragraph(
        f"<b>Vulnerability:</b> {get_value(row, 'VULNERABILITY')}",
        styles['Normal']
    ))
    elements.append(Paragraph(
        f"<b>Damage Grade:</b> {get_value(row, 'GRADE OF DAMAGEABILITY')}",
        styles['Normal']
    ))
    elements.append(Spacer(1, 12))

    # HAZARDS
    elements.append(Paragraph("<b>Hazards and Irregularities</b>", styles['Heading2']))
    elements.append(Paragraph(
        f"Geologic Hazard: {get_value(row, 'GEOLOGIC HAZARD (GEOANALYTICS PH & HAZARD HUNTER PH)')}",
        styles['Normal']
    ))
    elements.append(Paragraph(
        f"Exterior Falling Hazards: {get_value(row, 'EXTERIOR FALLING HAZARDS')}",
        styles['Normal']
    ))
    elements.append(Spacer(1, 12))

    # -----------------------------
    # ADD PHOTO
    # -----------------------------
    if photo_path and os.path.exists(photo_path):
        elements.append(Paragraph("<b>Photo</b>", styles['Heading3']))
        img = Image(photo_path, width=250, height=180)
        elements.append(img)
        elements.append(Spacer(1, 12))

    # -----------------------------
    # ADD SKETCH
    # -----------------------------
    if sketch_path and os.path.exists(sketch_path):
        elements.append(Paragraph("<b>Sketch</b>", styles['Heading3']))
        img2 = Image(sketch_path, width=250, height=180)
        elements.append(img2)
        elements.append(Spacer(1, 12))

    # BUILD PDF
    doc.build(elements)

    buffer.seek(0)
    return buffer
# ==================================================
# SIDEBAR
# ==================================================
st.sidebar.title("Navigation")

st.sidebar.markdown("---")
st.sidebar.markdown("### 📌 System Description")
st.sidebar.markdown("""
Seismic Vulnerability Records are organized data used to assess how susceptible barangay halls are to earthquake damage.

Using Rapid Visual Screening (RVS), each structure is evaluated based on physical characteristics, hazards, and site conditions to support risk assessment and disaster preparedness.
""")

st.sidebar.markdown("---")

if st.sidebar.button("🏠 About System", use_container_width=True):
    st.session_state.page = "About"
    st.rerun()

if st.sidebar.button("🔍 Search Barangay", use_container_width=True):
    st.session_state.page = "Search"
    st.rerun()

if st.sidebar.button("📊 Dashboard", use_container_width=True):
    st.session_state.page = "Dashboard"
    st.rerun()

# ==================================================
# PAGE 1: ABOUT
# ==================================================
if st.session_state.page == "About":

    st.title("Seismic Vulnerability Records System")
    st.markdown(
        '<div class="subtitle">Database Development on Seismic Vulnerability of Barangay Halls in L.I.S.T.T. Area</div>',
        unsafe_allow_html=True
    )

    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.subheader("Thesis Title")
    st.write("""
    **DATABASE DEVELOPMENT ON SEISMIC VULNERABILITY OF BARANGAY HALLS IN L.I.S.T.T.  
    (LA TRINIDAD, ITOGON, SABLAN, TUBA, TUBLAY) AREA USING RAPID VISUAL SCREENING**
    """)
    st.markdown("</div>", unsafe_allow_html=True)

    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.subheader("About the System")
    st.write("""
    This web-based system stores, organizes, searches, and visualizes seismic vulnerability records
    of barangay halls within the L.I.S.T.T. area. It uses Rapid Visual Screening data to help identify
    structural vulnerability levels, hazards, irregularities, and the need for further structural evaluation.
    """)
    st.markdown("</div>", unsafe_allow_html=True)

    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.subheader("Main Features")
    st.write("""
    - Search barangay hall records by municipality and barangay  
    - View structural and hazard-related information  
    - Display photos and structural sketches  
    - Analyze vulnerability data through charts  
    - Export barangay record as PDF report  
    """)
    st.markdown("</div>", unsafe_allow_html=True)

    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.subheader("Go to")

    col1, col2 = st.columns(2)

    with col1:
        if st.button("🔍 Search Barangay Records", use_container_width=True):
            st.session_state.page = "Search"
            st.rerun()

    with col2:
        if st.button("📊 View Dashboard", use_container_width=True):
            st.session_state.page = "Dashboard"
            st.rerun()

    st.markdown("</div>", unsafe_allow_html=True)

# ==================================================
# PAGE 2: SEARCH
# ==================================================
elif st.session_state.page == "Search":

    st.title("Search Barangay Record")
    st.caption("View detailed seismic vulnerability information per barangay hall")

    if st.button("⬅ Back to About System"):
        st.session_state.page = "About"
        st.rerun()

    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.subheader("Search")

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

                # -----------------------------
                # METRICS
                # -----------------------------
                st.markdown('<div class="card">', unsafe_allow_html=True)

                col1, col2, col3 = st.columns(3)
                col1.metric("RVS Score", get_metric_value(row, "RVS SCORE"))
                col2.metric("Damage Grade", get_metric_value(row, "GRADE OF DAMAGEABILITY"))
                col3.metric("Rank", get_metric_value(row, "RANK"))

                st.markdown("""
                <div class="small-muted">
                <b>What do these mean?</b><br><br>
                • <b>RVS Score</b> – A numerical value obtained from Rapid Visual Screening. Lower scores indicate higher seismic vulnerability.<br>
                • <b>Damage Grade</b> – Indicates the expected level of structural damage during an earthquake. Higher grades mean more severe damage.<br>
                • <b>Rank</b> – Priority level based on vulnerability. Lower rank numbers indicate higher priority for inspection or intervention.
                </div>
                """, unsafe_allow_html=True)

                st.markdown("</div>", unsafe_allow_html=True)

                # -----------------------------
                # INFORMATION
                # -----------------------------
                st.markdown('<div class="card">', unsafe_allow_html=True)
                st.subheader("INFORMATION")

                st.write(f"• **Name of Barangay Hall:** {get_value(row, 'BARANGAY HALL')}")
                st.write(f"• **Municipality:** {get_value(row, 'MUNICIPALITY')}")

                st.write("• **No. of Stories:**")
                st.write(f"  - Above Grade: {get_value(row, 'ABOVE GRADE')}")
                st.write(f"  - Below Grade: {get_value(row, 'BELOW GRADE')}")

                st.write(f"• **Year Built:** {get_value(row, 'YEAR BUILT')}")
                st.write(f"• **Total Floor Area (SQ. FT.):** {get_value(row, 'TOTAL FLOOR AREA (SQ. FT.)')}")
                st.write(f"• **Occupancy:** {get_value(row, 'OCCUPANCY')}")
                st.write(f"• **Soil Type:** {get_value(row, 'SOIL TYPE')}")
                st.write(f"• **FEMA Building Type:** {get_value(row, 'BUILDING TYPE')}")

                st.markdown("</div>", unsafe_allow_html=True)

                # -----------------------------
                # HAZARDS AND IRREGULARITIES
                # -----------------------------
                st.markdown('<div class="card">', unsafe_allow_html=True)
                st.subheader("HAZARDS AND IRREGULARITIES")

                st.write(f"• **Geologic Hazards:** {get_value(row, 'GEOLOGIC HAZARD (GEOANALYTICS PH & HAZARD HUNTER PH)')}")
                st.write(f"• **Exterior Falling Hazards:** {get_value(row, 'EXTERIOR FALLING HAZARDS')}")
                st.write(f"• **Plan Irregularities:** {get_value(row, 'PLAN IRREGULARITY')}")
                st.write(f"• **Vertical Irregularities:** {get_value(row, 'VERTICAL IRREGULARITY')}")
                st.write(f"• **Adjacency:** {get_value(row, 'ADJACENCY')}")

                st.markdown("</div>", unsafe_allow_html=True)

                # -----------------------------
                # PHOTO AND SKETCH
                # -----------------------------
                st.markdown('<div class="card">', unsafe_allow_html=True)
                st.subheader("PHOTO AND SKETCH OF THE STRUCTURE")

                col1, col2 = st.columns(2)

                with col1:
                    st.markdown("**Photo**")
                    if photo_path:
                        st.image(photo_path, use_container_width=True)
                    else:
                        st.info("No photo uploaded for this barangay hall.")

                with col2:
                    st.markdown("**Sketch**")
                    if sketch_path:
                        st.image(sketch_path, use_container_width=True)
                    else:
                        st.info("No structural sketch uploaded for this barangay hall.")

                st.markdown("</div>", unsafe_allow_html=True)

                # -----------------------------
                # RVS RESULT
                # -----------------------------
                st.markdown('<div class="card">', unsafe_allow_html=True)
                st.subheader("RAPID VISUAL SCREENING RESULT")

                barangay_name = get_value(row, "BARANGAY HALL")
                municipality_name = get_value(row, "MUNICIPALITY")
                rvs_score = get_value(row, "RVS SCORE")
                vulnerability = str(get_value(row, "VULNERABILITY")).strip()
                damage_grade = get_value(row, "GRADE OF DAMAGEABILITY")
                rank = get_value(row, "RANK")

                geologic_hazard = get_value(row, "GEOLOGIC HAZARD (GEOANALYTICS PH & HAZARD HUNTER PH)")
                exterior_hazard = get_value(row, "EXTERIOR FALLING HAZARDS")
                plan_irregularity = get_value(row, "PLAN IRREGULARITY")
                vertical_irregularity = get_value(row, "VERTICAL IRREGULARITY")
                adjacency = get_value(row, "ADJACENCY")

                st.write("**Score:**", rvs_score)
                st.write("**Vulnerability:**", vulnerability)
                st.write("**Interpretation:**", get_value(row, "INTERPRETATION"))
                st.write("**Grade of Damageability:**", damage_grade)

                if "LOW" in vulnerability.upper():
                    st.success(f"🟢 {vulnerability}")
                elif "MODERATE" in vulnerability.upper():
                    st.warning(f"🟡 {vulnerability}")
                elif "HIGH" in vulnerability.upper():
                    st.error(f"🔴 {vulnerability}")
                else:
                    st.info(vulnerability)

                st.markdown("</div>", unsafe_allow_html=True)

                # -----------------------------
                # OVERALL RESULT SUMMARY
                # -----------------------------
                st.markdown('<div class="card">', unsafe_allow_html=True)
                st.subheader("Overall Result Summary")

                st.write(
                    f"The **{barangay_name} Barangay Hall** located in **{municipality_name}** "
                    f"was assessed using Rapid Visual Screening (RVS). "
                    f"The structure obtained an **RVS Score of {rvs_score}**, classified as "
                    f"**{vulnerability}**, with a **{damage_grade}** damageability rating and "
                    f"a priority rank of **{rank}**."
                )

                st.write(
                    f"Based on the recorded hazards and irregularities, the structure is associated with "
                    f"the following conditions: **Geologic Hazard:** {geologic_hazard}, "
                    f"**Exterior Falling Hazards:** {exterior_hazard}, "
                    f"**Plan Irregularity:** {plan_irregularity}, "
                    f"**Vertical Irregularity:** {vertical_irregularity}, and "
                    f"**Adjacency:** {adjacency}."
                )

                if "LOW" in vulnerability.upper():
                    st.success(
                        "Overall, this barangay hall shows relatively low seismic vulnerability. "
                        "Detailed structural evaluation may not be immediately required, but regular monitoring is recommended."
                    )
                elif "MODERATE" in vulnerability.upper():
                    st.warning(
                        "Overall, this barangay hall shows moderate seismic vulnerability. "
                        "Further structural evaluation is recommended to verify safety and determine strengthening measures."
                    )
                elif "HIGH" in vulnerability.upper():
                    st.error(
                        "Overall, this barangay hall shows high seismic vulnerability. "
                        "It should be prioritized for urgent detailed structural evaluation and possible intervention."
                    )
                else:
                    st.info(
                        "The vulnerability classification requires further review due to incomplete or unavailable recorded information."
                    )

                st.markdown("</div>", unsafe_allow_html=True)

# ------------------------
# EXPORT REPORT
# -----------------------
                st.markdown('<div class="card">', unsafe_allow_html=True)
                st.subheader("EXPORT REPORT")

                pdf_file = generate_pdf(row, photo_path, sketch_path)
                st.download_button(
                        label="📄 Export Full PDF Report (with Images)",
                        data=pdf_file,
                        file_name=f"{get_value(row, 'BARANGAY HALL')}_FULL_REPORT.pdf",
                        mime="application/pdf",
                        use_container_width=True
                    )
                st.markdown("</div>", unsafe_allow_html=True)

# ==================================================
# PAGE 3: DASHBOARD
# ==================================================
elif st.session_state.page == "Dashboard":

    st.title("Vulnerability Dashboard")
    st.caption("Panel-friendly summary of seismic vulnerability results")

    if st.button("⬅ Back to About System"):
        st.session_state.page = "About"
        st.rerun()

    st.markdown('<div class="card">', unsafe_allow_html=True)

    selected_municipality = st.selectbox(
        "Filter by Municipality",
        ["All"] + sorted(df["MUNICIPALITY"].dropna().unique())
    )

    if selected_municipality != "All":
        dashboard_df = df[df["MUNICIPALITY"] == selected_municipality]
    else:
        dashboard_df = df.copy()

    col1, col2, col3 = st.columns(3)

    col1.metric("Total Barangays", len(dashboard_df))

    avg_rvs = dashboard_df["RVS SCORE"].mean()
    col2.metric("Average RVS Score", "—" if pd.isna(avg_rvs) else round(avg_rvs, 2))

    high_count = dashboard_df[
        dashboard_df["VULNERABILITY"].str.contains("High", case=False, na=False)
    ].shape[0]

    col3.metric("High Vulnerability", high_count)

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

    if score_chart.empty:
        st.info("No RVS score data available for this selection.")
    else:
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
