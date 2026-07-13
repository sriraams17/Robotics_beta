import pandas as pd
import json
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib import colors

def create_pdf_report(json_path, pdf_path):
    # 1. Load the structured JSON data
    with open(json_path, 'r') as f:
        raw_data = json.load(f)
    
    # 2. Extract metadata and findings separately
    metadata = raw_data.get("metadata", {})
    findings = raw_data.get("findings", [])
    
    # 3. Target the 'findings' array to build your table rows
    df = pd.DataFrame(findings)
    
    # Check if we actually found anything; if empty, create a dummy row so the PDF doesn't break
    if df.empty:
        df = pd.DataFrame([{
            "element": "No hazards detected",
            "confidence_score": 0.0,
            "risk_assessment": "Low",
            "corrective_action": "None"
        }])

    # 4. Build the PDF Document
    doc = SimpleDocTemplate(pdf_path, pagesize=letter)
    styles = getSampleStyleSheet()
    story = []
    
    # Title & Metadata Header
    story.append(Paragraph(f"<b>QHSE Inspection Report</b>", styles['Title']))
    story.append(Spacer(1, 12))
    story.append(Paragraph(f"<b>Robot ID:</b> {metadata.get('robot_id', 'Unknown')}", styles['Normal']))
    story.append(Paragraph(f"<b>Timestamp:</b> {metadata.get('timestamp', 'N/A')}", styles['Normal']))
    story.append(Paragraph(f"<b>Inspection Status:</b> {metadata.get('overall_status', 'UNKNOWN')}", styles['Normal']))
    story.append(Paragraph(f"<b>Max Risk Level Flagged:</b> {metadata.get('max_risk_level', 'Low')}", styles['Normal']))
    story.append(Spacer(1, 20))
    
    # 5. Convert DataFrame to a ReportLab printable matrix
    # Table columns: Element, Confidence, Risk, Corrective Action
    table_data = [df.columns.tolist()] + df.values.tolist()
    
    # Style the table layout
    t = Table(table_data, colWidths=[150, 80, 100, 180])
    t.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.grey),
        ('TEXTCOLOR', (0,0), (-1,0), colors.whitesmoke),
        ('ALIGN', (0,0), (-1,-1), 'CENTER'),
        ('BOTTOMPADDING', (0,0), (-1,0), 8),
        ('BACKGROUND', (0,1), (-1,-1), colors.beige),
        ('GRID', (0,0), (-1,-1), 1, colors.black),
    ]))
    
    story.append(t)
    doc.build(story)