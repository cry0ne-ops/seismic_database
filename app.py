import streamlit as st
import pandas as pd

# Load Excel instead of DB
df = pd.read_excel("cleaned_full_seismic_dataset.xlsx")

st.set_page_config(page_title="Seismic Vulnerability Dashboard", layout="wide")

st.title("🏢 Seismic Vulnerability Dashboard (LISTT Area)")

# Sidebar filters
st.sidebar.header("Filter Options")

municipality = st.sidebar.selectbox(
    "Select Municipality",
    ["All"] + list(df["MUNICIPALITY"].dropna().unique())
)

risk = st.sidebar.selectbox(
    "Select Risk Level",
    ["All"] + list(df["INTERPRETATION"].dropna().unique())
)

# Filtering
filtered_df = df.copy()

if municipality != "All":
    filtered_df = filtered_df[filtered_df["MUNICIPALITY"] == municipality]

if risk != "All":
    filtered_df = filtered_df[filtered_df["INTERPRETATION"] == risk]

# Metrics
st.subheader("📊 Overview")

col1, col2, col3 = st.columns(3)

col1.metric("Total Barangays", len(filtered_df))
col2.metric("Average RVS Score", round(pd.to_numeric(filtered_df["RVS SCORE"], errors='coerce').mean(), 2))
col3.metric("Municipalities", filtered_df["MUNICIPALITY"].nunique())

# Table
st.subheader("📋 Data Table")
st.dataframe(filtered_df)

# Chart
st.subheader("📊 Risk Distribution")
st.bar_chart(filtered_df["INTERPRETATION"].value_counts())
