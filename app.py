import streamlit as st
import os
from generate_report import create_pdf_report

st.set_page_config(page_title="Robot Inspection Center", page_icon="🤖", layout="centered")

st.title("🤖 QHSE Robot Control Center")
st.subheader("Proof of Concept: Autonomous Data-to-Audit Pipeline")

st.markdown("""
This dashboard simulates an operator's interface. The software parses real-time telemetry 
emitted from an active robotic unit, filters compliance failures, and constructs an official audit document.
""")

st.info("💡 **Current Status:** Robot simulation path complete. Telemetry log parsed successfully.")

# Button to trigger the backend compliance processing pipeline
if st.button("🚨 Process Telemetry & Generate Audit Report", type="primary"):
    json_path = "mock_robot_telemetry.json"
    pdf_output = "QHSE_Robot_Audit_Report.pdf"
    
    with st.spinner("Processing telemetry logs..."):
        # Call your report generator logic
        create_pdf_report(json_path, pdf_output)
        
    if os.path.exists(pdf_output):
        st.success("✅ Audit Report Compiled Successfully!")
        
        # Provide download button directly in the browser UI
        with open(pdf_output, "rb") as pdf_file:
            st.download_button(
                label="📥 Download Audit-Ready PDF",
                data=pdf_file,
                file_name="QHSE_Robot_Audit_Report.pdf",
                mime="application/pdf"
            )