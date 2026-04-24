# -----------------------------
# RESULT
# -----------------------------
if search:

    if municipality == "Select" or barangay == "Select":
        st.warning("Please complete all fields.")
    else:
        row = df[
            (df["MUNICIPALITY"] == municipality) &
            (df["BARANGAY HALL"] == barangay)
        ].iloc[0]

        # -----------------------------
        # SUMMARY HEADER (NEW 🔥)
        # -----------------------------
        st.markdown('<div class="card fade-in">', unsafe_allow_html=True)

        col1, col2, col3 = st.columns(3)

        col1.metric("RVS Score", row.get("RVS SCORE", "N/A"))
        col2.metric("Damage Grade", row.get("GRADE OF DAMAGEABILITY", "N/A"))
        col3.metric("Rank", row.get("RANK", "N/A"))

        st.markdown('</div>', unsafe_allow_html=True)

        # -----------------------------
        # GENERAL INFO
        # -----------------------------
        st.markdown('<div class="card fade-in">', unsafe_allow_html=True)
        st.markdown('<div class="section-title">📌 General Information</div>', unsafe_allow_html=True)

        col1, col2 = st.columns(2)

        with col1:
            st.write("**Barangay:**", row.get("BARANGAY HALL", "N/A"))
            st.write("**Municipality:**", row.get("MUNICIPALITY", "N/A"))
            st.write("**Year Built:**", row.get("YEAR BUILT", "N/A"))
            st.write("**Floor Area (sq ft):**", row.get("TOTAL FLOOR AREA (sq. ft.)", "N/A"))

        with col2:
            st.write("**Stories Above:**", row.get("NO. OF STORIES ABOVE GRADE", "N/A"))
            st.write("**Stories Below:**", row.get("NO. OF STORIES BELOW GRADE", "N/A"))
            st.write("**Soil Type:**", row.get("SOIL TYPE", "N/A"))
            st.write("**Building Type:**", row.get("BUILDING TYPE", "N/A"))

        st.markdown('</div>', unsafe_allow_html=True)

        # -----------------------------
        # HAZARDS
        # -----------------------------
        st.markdown('<div class="card fade-in">', unsafe_allow_html=True)
        st.markdown('<div class="section-title">⚠️ Hazards & Irregularities</div>', unsafe_allow_html=True)

        st.write("**Geologic Hazards:**", row.get("GEOLOGIC HAZARD (Geoanalytics PH & Hazard Hunter PH)", "N/A"))
        st.write("**Exterior Hazards:**", row.get("EXTERIOR FALLING HAZARDS", "N/A"))
        st.write("**Plan Irregularities:**", row.get("PLAN IRREGULARITY", "N/A"))
        st.write("**Vertical Irregularities:**", row.get("VERTICAL IRREGULARITY", "N/A"))
        st.write("**Adjacency:**", row.get("ADJACENCY", "N/A"))

        st.markdown('</div>', unsafe_allow_html=True)

        # -----------------------------
        # RISK LEVEL (ENHANCED 🔥)
        # -----------------------------
        st.markdown('<div class="card fade-in">', unsafe_allow_html=True)
        st.markdown('<div class="section-title">📊 Assessment Result</div>', unsafe_allow_html=True)

        interpretation = row.get("VULNERABILITY", "N/A")

        if interpretation == "Low Vulnerability":
            st.success(f"🟢 {interpretation}")
        elif interpretation == "Moderate Vulnerability":
            st.warning(f"🟡 {interpretation}")
        elif "High" in str(interpretation):
            st.error(f"🔴 {interpretation}")
        else:
            st.write(interpretation)

        st.markdown('</div>', unsafe_allow_html=True)
