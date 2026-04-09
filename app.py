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
# CENTERED FILTER PANEL
# -----------------------------
st.markdown("### 🔍 Data Selection Panel")

col1, col2, col3 = st.columns(3)

with col1:
    show_all = st.checkbox("Show All Data")

with col2:
    municipalities = ["All"] + sorted(df["MUNICIPALITY"].dropna().unique())
    municipality = st.selectbox("Select Municipality", municipalities)

with col3:
    if municipality != "All":
        barangays = df[df["MUNICIPALITY"] == municipality]["BARANGAY HALL"].dropna().unique()
    else:
        barangays = df["BARANGAY HALL"].dropna().unique()

    barangay = st.selectbox("Select Barangay", ["All"] + sorted(barangays))

# -----------------------------
# FILTER LOGIC
# -----------------------------
if show_all:
    filtered_df = df.copy()

else:
    if municipality == "All" and barangay == "All":
        st.info("👆 Please select a Municipality or enable 'Show All Data'")
        st.stop()

    filtered_df = df.copy()

    if municipality != "All":
        filtered_df = filtered_df[filtered_df["MUNICIPALITY"] == municipality]

    if barangay != "All":
        filtered_df = filtered_df[filtered_df["BARANGAY HALL"] == barangay]

# -----------------------------
# METRICS
# -----------------------------
st.subheader("📊 Overview")

col1, col2, col3 = st.columns(3)

col1.metric("Total Records", len(filtered_df))

avg_score = filtered_df["RVS SCORE"].mean()
col2.metric("Average RVS Score", round(avg_score, 2) if pd.notnull(avg_score) else "N/A")

col3.metric("Municipalities", filtered_df["MUNICIPALITY"].nunique())

# -----------------------------
# TABLE
# -----------------------------
st.subheader("📋 Data Table")
st.dataframe(filtered_df, use_container_width=True)

# -----------------------------
# CHART
# -----------------------------
st.subheader("📊 Risk Distribution")
st.bar_chart(filtered_df["INTERPRETATION"].value_counts())

# -----------------------------
# DETAIL VIEW (IF SINGLE)
# -----------------------------
if len(filtered_df) == 1:
    st.subheader("📍 Detailed Information")

    row = filtered_df.iloc[0]

    st.write(f"**Barangay:** {row['BARANGAY HALL']}")
    st.write(f"**Municipality:** {row['MUNICIPALITY']}")
    st.write(f"**RVS Score:** {row['RVS SCORE']}")
    st.write(f"**Risk Level:** {row['INTERPRETATION']}")
    st.write(f"**Building Type:** {row['BUILDING TYPE']}")
