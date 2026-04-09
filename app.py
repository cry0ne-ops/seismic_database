import streamlit as st
import pandas as pd

# -----------------------------
# PAGE CONFIG
# -----------------------------
st.set_page_config(
    page_title="Barangay Seismic Records System",
    layout="wide"
)

# -----------------------------
# CUSTOM CSS (GOVERNMENT STYLE)
# -----------------------------
st.markdown("""
<style>
.main {
    background-color: #f5f7fa;
}

h1, h2, h3 {
    color: #1f4e79;
}

.section {
    background-color: white;
    padding: 20px;
    border-radius: 10px;
    box-shadow: 0px 2px 6px rgba(0,0,0,0.1);
    margin-bottom: 20px;
}

.header {
    text-align: center;
    padding: 10px;
}

.subheader {
    color: #444;
    text-align: center;
    margin-bottom: 30px;
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
st.markdown('<div class="header">', unsafe_allow_html=True)
st.title("Republic of the Philippines")
st.subheader("Barangay Seismic Vulnerability Records System")
st.markdown("Province of Benguet | LISTT Area")
st.markdown('</div>', unsafe_allow_html=True)

# -----------------------------
# SEARCH PANEL
# -----------------------------
st.markdown('<div class="section">', unsafe_allow_html=True)
st.markdown("### 🔍 Search Barangay Records")

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

search = st.button("🔎 Search Record")

st.markdown('</div>', unsafe_allow_html=True)

# -----------------------------
# RESULT
# -----------------------------
if search:

    if municipality == "Select" or barangay == "Select":
        st.error("⚠️ Please select Municipality and Barangay.")
    else:
        row = df[
            (df["MUNICIPALITY"] == municipality) &
            (df["BARANGAY HALL"] == barangay)
        ].iloc[0]

        # -----------------------------
        # GENERAL INFO
        # -----------------------------
        st.markdown('<div class="section">', unsafe_allow_html=True)
        st.markdown("## 📌 General Information")

        col1, col2 = st.columns(2)

        with col1:
            st.write(f"**Barangay Hall:** {row.get('BARANGAY HALL', 'N/A')}")
            st.write(f"**Municipality:** {row.get('MUNICIPALITY', 'N/A')}")
            st.write(f"**Year Built:** {row.get('YEAR BUILT', 'N/A')}")
            st.write(f"**Occupancy:** {row.get('OCCUPANCY', 'N/A')}")
            st.write(f"**Soil Type:** {row.get('SOIL TYPE', 'N/A')}")

        with col2:
            st.write(f"**Stories Above Grade:** {row.get('NO. OF STORIES ABOVE GRADE', 'N/A')}")
            st.write(f"**Stories Below Grade:** {row.get('NO. OF STORIES BELOW GRADE', 'N/A')}")
            st.write(f"**Floor Area:** {row.get('TOTAL FLOOR AREA', 'N/A')}")
            st.write(f"**Building Type:** {row.get('BUILDING TYPE', 'N/A')}")

        st.markdown('</div>', unsafe_allow_html=True)

        # -----------------------------
        # HAZARDS
        # -----------------------------
        st.markdown('<div class="section">', unsafe_allow_html=True)
        st.markdown("## ⚠️ Hazards and Irregularities")

        st.write(f"**Geologic Hazards:** {row.get('GEOLOGIC HAZARD', 'N/A')}")
        st.write(f"**Exterior Hazards:** {row.get('EXTERIOR FALLING HAZARDS', 'N/A')}")
        st.write(f"**Plan Irregularities:** {row.get('PLAN IRREGULARITY', 'N/A')}")
        st.write(f"**Vertical Irregularities:** {row.get('VERTICAL IRREGULARITY', 'N/A')}")
        st.write(f"**Adjacency:** {row.get('ADJACENCY', 'N/A')}")

        st.markdown('</div>', unsafe_allow_html=True)

        # -----------------------------
        # PHOTO
        # -----------------------------
        st.markdown('<div class="section">', unsafe_allow_html=True)
        st.markdown("## 🖼️ Structure Image")

        st.info("📌 Add barangay images here (future improvement)")

        st.markdown('</div>', unsafe_allow_html=True)

        # -----------------------------
        # RVS RESULT
        # -----------------------------
        st.markdown('<div class="section">', unsafe_allow_html=True)
        st.markdown("## 📊 RVS Assessment Result")

        score = row.get("RVS SCORE", "N/A")
        interpretation = row.get("INTERPRETATION", "N/A")

        st.write(f"**RVS Score:** {score}")

        if interpretation == "Low Vulnerability":
            st.success(f"🟢 {interpretation}")
        elif interpretation == "Moderate Vulnerability":
            st.warning(f"🟡 {interpretation}")
        elif interpretation == "High Vulnerability":
            st.error(f"🔴 {interpretation}")
        else:
            st.write(interpretation)

        st.markdown('</div>', unsafe_allow_html=True)
