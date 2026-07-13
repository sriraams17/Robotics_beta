import streamlit as st
import os
import base64
from generate_report import create_pdf_report

st.set_page_config(layout="wide") # Sets a wide layout so the PDF preview has plenty of room

st.title("🤖 QHSE Robot Telemetry & Report Center")
st.write("Generate and preview your audit-ready compliance reports below.")

# Define static paths
json_path = "mock_robot_telemetry.json"
pdf_output = "QHSE_Audit_Report.pdf"

# Button to trigger compilation
if st.button("Generate Inspection Report"):
    with st.spinner("Compiling report with corporate layout structures..."):
        # 1. Run the backend generation script
        create_pdf_report(json_path, pdf_output)
        
    # Check if the file was created successfully
    if os.path.exists(pdf_output):
        st.success("✅ Report successfully generated!")
        
        # 2. Read PDF file and convert it to Base64 to embed it in HTML
        with open(pdf_output, "rb") as f:
            pdf_bytes = f.read()
        base64_pdf = base64.b64encode(pdf_bytes).decode('utf-8')
        
        # 3. Create the HTML iframe code for the live preview layout
        # We use standard PDF data URI parameters to display it neatly
        pdf_display = f'<iframe src="data:application/pdf;base64,{base64_pdf}" width="100%" height="700" type="application/pdf"></iframe>'
        
        # 4. Render the preview window inside the app browser
        st.subheader("📋 Document Preview")
        st.markdown(pdf_display, unsafe_allow_html=True)
        
        st.write("---")
        
        # 5. Provide the dedicated download option below the viewer
        st.download_button(
            label="📥 Download Official PDF Report",
            data=pdf_bytes,
            file_name="QHSE_Inspection_Report.pdf",
            mime="application/pdf"
        )
    else:
        st.error("Could not find the generated PDF file. Please verify generate_report.py works.")