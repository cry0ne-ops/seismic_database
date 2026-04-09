# -----------------------------
# SEARCH RESULT DISPLAY
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

            st.success(f"📄 Record for {barangay}, {municipality}")

            # -----------------------------
            # GENERAL INFORMATION
            # -----------------------------
            st.markdown("## 📌 GENERAL INFORMATION")

            st.write(f"**Name of Barangay Hall:** {row.get('BARANGAY HALL', 'N/A')}")
            st.write(f"**Municipality:** {row.get('MUNICIPALITY', 'N/A')}")
            st.write(f"**Zip Code:** N/A")
            st.write(f"**Longitude and Latitude:** N/A")
            st.write(f"**SS and S1:** N/A")

            st.write(f"**No. of Stories:**")
            st.write(f"• Above Grade: {row.get('NO. OF STORIES ABOVE GRADE', 'N/A')}")
            st.write(f"• Below Grade: {row.get('NO. OF STORIES BELOW GRADE', 'N/A')}")

            st.write(f"**Year Built:** {row.get('YEAR BUILT', 'N/A')}")
            st.write(f"**Code Year:** {'Pre-Code' if row.get('PRE-CODE') == 'Yes' else 'Post-Benchmark'}")
            st.write(f"**Total Floor Area:** {row.get('TOTAL FLOOR AREA', 'N/A')}")
            st.write(f"**Occupancy:** {row.get('OCCUPANCY', 'N/A')}")
            st.write(f"**Soil Type:** {row.get('SOIL TYPE', 'N/A')}")
            st.write(f"**FEMA Building Type:** {row.get('BUILDING TYPE', 'N/A')}")

            # -----------------------------
            # HAZARDS AND IRREGULARITIES
            # -----------------------------
            st.markdown("## ⚠️ HAZARDS AND IRREGULARITIES")

            st.write(f"**Geologic Hazards:** {row.get('GEOLOGIC HAZARD', 'N/A')}")
            st.write(f"**Exterior Falling Hazards:** {row.get('EXTERIOR FALLING HAZARDS', 'N/A')}")
            st.write(f"**Plan Irregularities:** {row.get('PLAN IRREGULARITY', 'N/A')}")
            st.write(f"**Vertical Irregularities:** {row.get('VERTICAL IRREGULARITY', 'N/A')}")
            st.write(f"**Adjacency:** {row.get('ADJACENCY', 'N/A')}")

            # -----------------------------
            # PHOTO & SKETCH
            # -----------------------------
            st.markdown("## 🖼️ PHOTO AND SKETCH OF THE STRUCTURE")

            st.info("📌 Upload or link images here (to be added later)")

            # Example (future)
            # st.image("images/sample.jpg")

            # -----------------------------
            # RVS RESULT
            # -----------------------------
            st.markdown("## 📊 RAPID VISUAL SCREENING RESULT")

            score = row.get("RVS SCORE", "N/A")
            interpretation = row.get("INTERPRETATION", "N/A")

            st.write(f"**Score:** {score}")

            # Highlight interpretation
            if interpretation == "Low Vulnerability":
                st.success(f"🟢 {interpretation}")
            elif interpretation == "Moderate Vulnerability":
                st.warning(f"🟡 {interpretation}")
            elif interpretation == "High Vulnerability":
                st.error(f"🔴 {interpretation}")
            else:
                st.write(interpretation)
