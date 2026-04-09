import streamlit as st
import pandas as pd
import sqlite3

# Connect to database
conn = sqlite3.connect("seismic_database.db")

# Load data
df = pd.read_sql("SELECT * FROM barangay_halls", conn)

st.set_page_config(page_title="Seismic Vulnerability Dashboard", layout="wide")

st.title("🏢 Seismic Vulnerability Dashboard (LISTT Area)")

# Sidebar filters
st.sidebar.header("Filter Options")

municipality = st.sidebar.selectbox(
    "Select Municipality",
    ["All"] + list(df["municipality"].dropna().unique())
)

risk = st.sidebar.selectbox(
    "Select Risk Level",
    ["All"] + list(df["interpretation"].dropna().unique())
)

# Apply filters
filtered_df = df.copy()

if municipality != "All":
    filtered_df = filtered_df[filtered_df["municipality"] == municipality]

if risk != "All":
    filtered_df = filtered_df[filtered_df["interpretation"] == risk]

# Show metrics
st.subheader("📊 Overview")

col1, col2, col3 = st.columns(3)

col1.metric("Total Barangays", len(filtered_df))
col2.metric("Average RVS Score", round(filtered_df["rvs_score"].mean(), 2))
col3.metric("Municipalities", filtered_df["municipality"].nunique())

# Show table
st.subheader("📋 Data Table")
st.dataframe(filtered_df)

# Chart
st.subheader("📊 Risk Distribution")
st.bar_chart(filtered_df["interpretation"].value_counts())

conn.close()
