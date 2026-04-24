import streamlit as st
import pandas as pd
import os

# -----------------------------
# PAGE CONFIG
# -----------------------------
st.set_page_config(page_title="Seismic System", layout="wide")

# -----------------------------
# DARK MODE
# -----------------------------
st.markdown("""
<style>
.stApp {background: #0f172a; color: #e5e7eb;}
.block-container {max-width: 1050px;}
.card {
    background: #111827;
    padding: 20px;
    border-radius: 12px;
    border: 1px solid #334155;
    margin-bottom: 15px;
}
.stButton button {
    background: #2563eb;
    color: white;
    border-radius: 8px;
}
</style>
""", unsafe_allow_html=True)

# -----------------------------
# LOAD DATA
# -----------------------------
df = pd.read_excel("final_dataset.xlsx")
df.columns = df.columns.str.strip().str.upper()

df["MUNICIPALITY"] = df["MUNICIPALITY"].str.strip().str.upper()
df["BARANGAY HALL"] = df["BARANGAY HALL"].str.strip().str.upper()
df["VULNERABILITY"] = df["VULNERABILITY"].astype(str)

df["RVS SCORE"] = pd.to_numeric(df["RVS SCORE"], errors="coerce")
df["RANK"] = pd.to_numeric(df["RANK"], errors="coerce")

# -----------------------------
# IMAGE FUNCTION
# -----------------------------
def get_image_path(base):
    for ext in [".jpg", ".png"]:
        if os.path.exists(base + ext):
            return base + ext
    return None

# -----------------------------
# SIDEBAR NAVIGATION
# -----------------------------
st.sidebar.title("Navigation")

page = st.sidebar.radio(
    "Go to",
    ["🔍 Search Barangay", "📊 Dashboard"]
)

# =============================
# PAGE 1: SEARCH
# =============================
if page == "🔍 Search Barangay":

    st.title("Seismic Vulnerability Records")
    st.caption("Barangay Hall Assessment System")

    st.markdown('<div class="card">', unsafe_allow_html=True)

    col1, col2, col3 = st.columns(3)

    with col1:
        municipalities = sorted(df["MUNICIPALITY"].unique())
        municipality = st.selectbox("Municipality", ["Select"] + municipalities)

    with col2:
        if municipality != "Select":
            barangays = df[df["MUNICIPALITY"] == municipality]["BARANGAY HALL"].unique()
        else:
            barangays = []

        barangay = st.selectbox("Barangay", ["Select"] + list(barangays))

    with col3:
        st.markdown("<br>", unsafe_allow_html=True)
        search = st.button("Search", use_container_width=True)

    st.markdown('</div>', unsafe_allow_html=True)

    if search:

        if municipality == "Select" or barangay == "Select":
            st.warning("Select both fields")
        else:
            row = df[
                (df["MUNICIPALITY"] == municipality) &
                (df["BARANGAY HALL"] == barangay)
            ].iloc[0]

            muni = row["MUNICIPALITY"]
            brgy = row["BARANGAY HALL"]

            photo = get_image_path(f"images/{muni} Pics/{brgy}")
            sketch = get_image_path(f"images/{muni} Sketch/{brgy}")

            # SUMMARY
            st.markdown('<div class="card">', unsafe_allow_html=True)

            c1, c2, c3 = st.columns(3)
            c1.metric("RVS Score", row["RVS SCORE"])
            c2.metric("Damage Grade", row["GRADE OF DAMAGEABILITY"])
            c3.metric("Rank", row["RANK"])

            st.markdown('</div>', unsafe_allow_html=True)

            # IMAGES
            st.markdown('<div class="card">', unsafe_allow_html=True)
            st.subheader("Photo & Sketch")

            col1, col2 = st.columns(2)

            if photo:
                col1.image(photo)
            else:
                col1.info("No photo")

            if sketch:
                col2.image(sketch)
            else:
                col2.info("No sketch")

            st.markdown('</div>', unsafe_allow_html=True)

# =============================
# PAGE 2: DASHBOARD
# =============================
elif page == "📊 Dashboard":

    st.title("Vulnerability Dashboard")

    st.markdown('<div class="card">', unsafe_allow_html=True)

    # FILTER
    selected_muni = st.selectbox(
        "Filter by Municipality",
        ["All"] + sorted(df["MUNICIPALITY"].unique())
    )

    if selected_muni != "All":
        data = df[df["MUNICIPALITY"] == selected_muni]
    else:
        data = df.copy()

    # METRICS
    c1, c2, c3 = st.columns(3)
    c1.metric("Total Barangays", len(data))
    c2.metric("Avg RVS", round(data["RVS SCORE"].mean(), 2))
    c3.metric("High Risk", len(data[data["VULNERABILITY"].str.contains("High")]))

    # GRAPH 1
    st.subheader("Vulnerability Distribution")
    st.bar_chart(data["VULNERABILITY"].value_counts())

    # GRAPH 2
    st.subheader("RVS Score per Barangay")
    chart = data.set_index("BARANGAY HALL")["RVS SCORE"]
    st.bar_chart(chart)

    # GRAPH 3
    st.subheader("By Municipality")
    grouped = data.groupby(["MUNICIPALITY", "VULNERABILITY"]).size().unstack(fill_value=0)
    st.bar_chart(grouped)

    st.markdown('</div>', unsafe_allow_html=True)
