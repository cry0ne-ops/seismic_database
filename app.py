import streamlit as st
import pandas as pd

# -----------------------------
# LOAD DATA
# -----------------------------
df = pd.read_excel("cleaned_full_seismic_dataset.xlsx")
df["RVS SCORE"] = pd.to_numeric(df["RVS SCORE"], errors='coerce')

# ADD PROVINCE COLUMN
df["PROVINCE"] = "Benguet"

# -----------------------------
# PAGE CONFIG
# -----------------------------
st.set_page_config(page_title="Barangay Records Search System", layout="wide")

st.title("📄 Barangay Seismic Records Search System")
st.markdown("Search official records of barangay halls in LISTT area.")

# -----------------------------
# SEARCH PANEL (CENTERED)
# -----------------------------
st.markdown("### 🔍 Search Records")

col1, col2, col3 = st.columns(3)

with col1:
    provinces = sorted(df["PROVINCE"].unique())
    province = st.selectbox("Select Province", ["Select Province"] + provinces)

with col2:
    if province != "Select Province":
        municipalities = df[df["PROVINCE"] == province]["MUNICIPALITY"].dropna().unique()
    else:
        municipalities = []

    municipality = st.selectbox("Select Municipality", ["Select Municipality"] + sorted(municipalities))

with col3:
    if municipality != "Select Municipality":
        barangays = df[df["MUNICIPALITY"] == municipality]["BARANGAY HALL"].dropna().unique()
    else:
        barangays = []

    barangay = st.selectbox("Select Barangay", ["Select Barangay"] + sorted(barangays))

# SEARCH BUTTON
search = st.button("🔎 Search")

# -----------------------------
# SEARCH LOGIC
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

        st.success(f"Showing results for {barangay}, {municipality}, {province}")

        # -----------------------------
        # METRICS
        # -----------------------------
        st.subheader("📊 Summary")

        col1, col2, col3 = st.columns(3)

        col1.metric("Records Found", len(filtered_df))

        avg_score = filtered_df["RVS SCORE"].mean()
        col2.metric("RVS Score", round(avg_score, 2) if pd.notnull(avg_score) else "N/A")

        col3.metric("Risk Level", filtered_df["INTERPRETATION"].iloc[0])

        # -----------------------------
        # DETAILS
        # -----------------------------
        st.subheader("📋 Record Details")

        st.dataframe(filtered_df, use_container_width=True)

        # -----------------------------
        # DETAILED VIEW
        # -----------------------------
        if len(filtered_df) > 0:
            row = filtered_df.iloc[0]

            st.subheader("📍 Detailed Information")

            st.write(f"**Barangay:** {row['BARANGAY HALL']}")
            st.write(f"**Municipality:** {row['MUNICIPALITY']}")
            st.write(f"**Province:** {row['PROVINCE']}")
            st.write(f"**RVS Score:** {row['RVS SCORE']}")
            st.write(f"**Risk Level:** {row['INTERPRETATION']}")
            st.write(f"**Building Type:** {row['BUILDING TYPE']}")
            st.write(f"**Year Built:** {row['YEAR BUILT']}")
