import streamlit as st
import pandas as pd

# -----------------------------
# LOAD DATA
# -----------------------------
df = pd.read_excel("cleaned_full_seismic_dataset.xlsx")
df["RVS SCORE"] = pd.to_numeric(df["RVS SCORE"], errors='coerce')

# Add Province (since dataset is LISTT only)
df["PROVINCE"] = "Benguet"

# -----------------------------
# PAGE CONFIG
# -----------------------------
st.set_page_config(page_title="Barangay Seismic Records System", layout="wide")

st.title("📄 Barangay Seismic Records Search System")
st.markdown("Official database of seismic vulnerability of barangay halls in LISTT area.")

# -----------------------------
# SEARCH PANEL
# -----------------------------
st.markdown("## 🔍 Search Records")

col1, col2, col3 = st.columns(3)

# Province
with col1:
    provinces = sorted(df["PROVINCE"].unique())
    province = st.selectbox("Select Province", ["Select Province"] + provinces)

# Municipality
with col2:
    if province != "Select Province":
        municipalities = df[df["PROVINCE"] == province]["MUNICIPALITY"].dropna().unique()
    else:
        municipalities = []

    municipality = st.selectbox("Select Municipality", ["Select Municipality"] + sorted(municipalities))

# Barangay
with col3:
    if municipality != "Select Municipality":
        barangays = df[df["MUNICIPALITY"] == municipality]["BARANGAY HALL"].dropna().unique()
    else:
        barangays = []

    barangay = st.selectbox("Select Barangay", ["Select Barangay"] + sorted(barangays))

# Search Button
search = st.button("🔎 Search")

# -----------------------------
# SEARCH RESULT
# -----------------------------
if search:

    if province == "Select Province" or municipality == "Select Municipality" or barangay == "Select Barangay":
        st.error("⚠️ Please complete all selections before searching.")
    else:
        filtered_df = df[
            (df["PROVINCE"] == province) &
            (df["MUNICIPALITY"] == municipality) &
            (df["BARANGAY HALL"] == barangay)
        ]

        if len(filtered_df) == 0:
            st.warning("No data found.")
        else:
            row = filtered_df.iloc[0]

            st.success(f"📄 Record for {barangay}, {municipality}, {province}")

            # -----------------------------
            # GENERAL INFORMATION
            # -----------------------------
            st.markdown("## 📌 GENERAL INFORMATION")

            st.write(f"**Name of Barangay Hall:** {row.get('BARANGAY HALL', 'N/A')}")
            st.write(f"**Municipality:** {row.get('MUNICIPALITY', 'N/A')}")
            st.write(f"**Zip Code:** N/A")
            st.write(f"**Longitude and Latitude:** N/A")
            st.write(f"**SS and S1:** N/A")

            st.write("**No. of Stories:**")
            st.write(f"• Above Grade: {row.get('NO. OF STORIES ABOVE GRADE', 'N/A')}")
            st.write(f"• Below Grade: {row.get('NO. OF STORIES BELOW GRADE', 'N/A')}")

            st.write(f"**Year Built:** {row.get('YEAR BUILT', 'N/A')}")
            st.write(f"**Code Year:** {'Pre-Code' if row.get('PRE-CODE') == 'Yes' else 'Post-Benchmark'}")
            st.write(f"**Total Floor Area:** {row.get('TOTAL FLOOR AREA', 'N/A')}")
            st.write(f"**Occupancy:** {row.get('OCCUPANCY', 'N/A')}")
            st.write(f"**Soil Type:** {row.get('SOIL TYPE', 'N/A')}")
            st.write(f"**FEMA Building Type:** {row.get('BUILDING TYPE', 'N/A')}")

            # -----------------------------
            # HAZARDS
            # -----------------------------
            st.markdown("## ⚠️ HAZARDS AND IRREGULARITIES")

            st.write(f"**Geologic Hazards:** {row.get('GEOLOGIC HAZARD', 'N/A')}")
            st.write(f"**Exterior Falling Hazards:** {row.get('EXTERIOR FALLING HAZARDS', 'N/A')}")
            st.write(f"**Plan Irregularities:** {row.get('PLAN IRREGULARITY', 'N/A')}")
            st.write(f"**Vertical Irregularities:** {row.get('VERTICAL IRREGULARITY', 'N/A')}")
            st.write(f"**Adjacency:** {row.get('ADJACENCY', 'N/A')}")

            # -----------------------------
            # PHOTO SECTION
            # -----------------------------
            st.markdown("## 🖼️ PHOTO AND SKETCH OF THE STRUCTURE")

            st.info("📌 Image integration can be added here (future enhancement)")

            # -----------------------------
            # RVS RESULT
            # -----------------------------
            st.markdown("## 📊 RAPID VISUAL SCREENING RESULT")

            score = row.get("RVS SCORE", "N/A")
            interpretation = row.get("INTERPRETATION", "N/A")

            st.write(f"**Score:** {score}")

            if interpretation == "Low Vulnerability":
                st.success(f"🟢 {interpretation}")
            elif interpretation == "Moderate Vulnerability":
                st.warning(f"🟡 {interpretation}")
            elif interpretation == "High Vulnerability":
                st.error(f"🔴 {interpretation}")
            else:
                st.write(interpretation)
