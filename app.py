import streamlit as st
import os
import base64
from process_vision import analyze_inspection_image
from generate_report import create_pdf_report

st.set_page_config(layout="wide")

st.title("🤖 QHSE Robot Telemetry & Report Center")
st.write("Upload an inspection snapshot captured by the robot sensor payload.")

# File uploader widget inside the dashboard
uploaded_file = st.file_uploader("Choose a snapshot image...", type=["jpg", "jpeg", "png"])

json_path = "mock_robot_telemetry.json"
pdf_output = "QHSE_Audit_Report.pdf"

if uploaded_file is not None:
    # Save the file locally so our backend script can read it
    with open("temp_inspection.jpg", "wb") as f:
        f.write(uploaded_file.getbuffer())
        
    st.image("temp_inspection.jpg", caption="Uploaded Payload Frame", use_container_width=True)
    
    if st.button("Analyze Image & Compile Report"):
        with st.spinner("Executing Computer Vision models and structuring data fields..."):
            # 1. Run the AI vision pipeline to build the telemetry JSON
            analyze_inspection_image("temp_inspection.jpg", json_path)
            
            # 2. Compile the PDF using the updated JSON data
            create_pdf_report(json_path, pdf_output)
            
        if os.path.exists(pdf_output):
            st.success("✅ Analytics complete! Document generated.")
            
            # Read and encode PDF for display
            with open(pdf_output, "rb") as f:
                pdf_bytes = f.read()
            base64_pdf = base64.b64encode(pdf_bytes).decode('utf-8')
            pdf_display = f'<iframe src="data:application/pdf;base64,{base64_pdf}" width="100%" height="700" type="application/pdf"></iframe>'
            
            st.subheader("📋 Document Preview")
            st.markdown(pdf_display, unsafe_allow_html=True)
            
            st.write("---")
            st.download_button(
                label="📥 Download Official PDF Report",
                data=pdf_bytes,
                file_name="QHSE_Inspection_Report.pdf",
                mime="application/pdf"
            )