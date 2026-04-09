import streamlit as st
import pandas as pd

# -----------------------------
# LOAD DATA
# -----------------------------
df = pd.read_excel("cleaned_full_seismic_dataset.xlsx")

# Clean numeric column (important)
df["RVS SCORE"] = pd.to_numeric(df["RVS SCORE"], errors='coerce')

# -----------------------------
# PAGE CONFIG
# -----------------------------
st.set_page_config(page_title="Seismic Vulnerability Dashboard", layout="wide")

st.title("🏢 Seismic Vulnerability Dashboard (LISTT Area)")

# -----------------------------
# SIDEBAR FILTERS
# -----------------------------
st.sidebar.header("Filter Options")

# MUNICIPALITY
municipalities = ["All"] + sorted(df["MUNICIPALITY"].dropna().unique())
municipality = st.sidebar.selectbox("Select Municipality", municipalities)

# BARANGAY (DYNAMIC)
if municipality != "All":
    barangays = df[df["MUNICIPALITY"] == municipality]["BARANGAY HALL"].dropna().unique()
else:
    barangays = df["BARANGAY HALL"].dropna().unique()

barangay = st.sidebar.selectbox(
    "Select Barangay",
    ["All"] + sorted(barangays)
)

# CODE (DYNAMIC)
if barangay != "All":
    codes = df[df["BARANGAY HALL"] == barangay]["CODE"].dropna().unique()
else:
    codes = df["CODE"].dropna().unique()

code = st.sidebar.selectbox(
    "Select Barangay Code",
    ["All"] + list(codes)
)

# RISK LEVEL
risk = st.sidebar.selectbox(
    "Select Risk Level",
    ["All"] + list(df["INTERPRETATION"].dropna().unique())
)

# -----------------------------
# FILTERING LOGIC
# -----------------------------
filtered_df = df.copy()

if municipality != "All":
    filtered_df = filtered_df[filtered_df["MUNICIPALITY"] == municipality]

if barangay != "All":
    filtered_df = filtered_df[filtered_df["BARANGAY HALL"] == barangay]

if code != "All":
    filtered_df = filtered_df[filtered_df["CODE"] == code]

if risk != "All":
    filtered_df = filtered_df[filtered_df["INTERPRETATION"] == risk]

# -----------------------------
# DASHBOARD METRICS
# -----------------------------
st.subheader("📊 Overview")

col1, col2, col3 = st.columns(3)

col1.metric("Total Barangays", len(filtered_df))

avg_score = filtered_df["RVS SCORE"].mean()
col2.metric("Average RVS Score", round(avg_score, 2) if pd.notnull(avg_score) else "N/A")

col3.metric("Municipalities", filtered_df["MUNICIPALITY"].nunique())

# -----------------------------
# DATA TABLE
# -----------------------------
st.subheader("📋 Data Table")
st.dataframe(filtered_df, use_container_width=True)

# -----------------------------
# CHART
# -----------------------------
st.subheader("📊 Risk Distribution")
st.bar_chart(filtered_df["INTERPRETATION"].value_counts())

# -----------------------------
# OPTIONAL: SELECTED DETAILS (BONUS 🔥)
# -----------------------------
if len(filtered_df) == 1:
    st.subheader("📍 Selected Barangay Details")

    row = filtered_df.iloc[0]

    st.write(f"**Barangay:** {row['BARANGAY HALL']}")
    st.write(f"**Municipality:** {row['MUNICIPALITY']}")
    st.write(f"**RVS Score:** {row['RVS SCORE']}")
    st.write(f"**Risk Level:** {row['INTERPRETATION']}")
    st.write(f"**Building Type:** {row['BUILDING TYPE']}")
