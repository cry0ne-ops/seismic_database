import streamlit as st
import pandas as pd

# -----------------------------
# LOAD DATA
# -----------------------------
df = pd.read_excel("cleaned_full_seismic_dataset.xlsx")
df["RVS SCORE"] = pd.to_numeric(df["RVS SCORE"], errors='coerce')

# -----------------------------
# PAGE CONFIG
# -----------------------------
st.set_page_config(page_title="Seismic Vulnerability Dashboard", layout="wide")

st.title("🏢 Seismic Vulnerability Dashboard (LISTT Area)")

# -----------------------------
# SIDEBAR
# -----------------------------
st.sidebar.header("Selection Panel")

# STEP 1: Municipality (REQUIRED)
municipalities = sorted(df["MUNICIPALITY"].dropna().unique())
municipality = st.sidebar.selectbox(
    "Step 1: Select Municipality",
    ["Select Municipality"] + municipalities
)

# STOP if not selected
if municipality == "Select Municipality":
    st.warning("⚠️ Please select a Municipality to proceed.")
    st.stop()

# STEP 2: Barangay (based on municipality)
barangays = df[df["MUNICIPALITY"] == municipality]["BARANGAY HALL"].dropna().unique()

barangay = st.sidebar.selectbox(
    "Step 2: Select Barangay",
    ["Select Barangay"] + sorted(barangays)
)

# STOP if not selected
if barangay == "Select Barangay":
    st.warning("⚠️ Please select a Barangay to view data.")
    st.stop()

# STEP 3: Code (optional but automatic)
codes = df[df["BARANGAY HALL"] == barangay]["CODE"].dropna().unique()

code = st.sidebar.selectbox(
    "Step 3: Select Barangay Code (Optional)",
    ["All"] + list(codes)
)

# -----------------------------
# FILTERING
# -----------------------------
filtered_df = df[
    (df["MUNICIPALITY"] == municipality) &
    (df["BARANGAY HALL"] == barangay)
]

if code != "All":
    filtered_df = filtered_df[filtered_df["CODE"] == code]

# -----------------------------
# DISPLAY
# -----------------------------
st.success(f"Showing data for {barangay}, {municipality}")

# METRICS
st.subheader("📊 Overview")

col1, col2, col3 = st.columns(3)

col1.metric("Total Records", len(filtered_df))

avg_score = filtered_df["RVS SCORE"].mean()
col2.metric("Average RVS Score", round(avg_score, 2) if pd.notnull(avg_score) else "N/A")

col3.metric("Risk Level", filtered_df["INTERPRETATION"].iloc[0] if len(filtered_df) > 0 else "N/A")

# TABLE
st.subheader("📋 Data Table")
st.dataframe(filtered_df, use_container_width=True)

# CHART
st.subheader("📊 Risk Distribution")
st.bar_chart(filtered_df["INTERPRETATION"].value_counts())

# -----------------------------
# DETAILED VIEW
# -----------------------------
if len(filtered_df) > 0:
    st.subheader("📍 Detailed Information")

    row = filtered_df.iloc[0]

    st.write(f"**Barangay:** {row['BARANGAY HALL']}")
    st.write(f"**Municipality:** {row['MUNICIPALITY']}")
    st.write(f"**RVS Score:** {row['RVS SCORE']}")
    st.write(f"**Risk Level:** {row['INTERPRETATION']}")
    st.write(f"**Building Type:** {row['BUILDING TYPE']}")
    st.write(f"**Year Built:** {row['YEAR BUILT']}")
