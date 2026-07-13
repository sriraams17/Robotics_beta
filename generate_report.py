import json
import pandas as pd
from datetime import datetime
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors

def create_pdf_report(json_file, output_pdf):
    # 1. Read mock telemetry data
    with open(json_file, 'r') as f:
        raw_data = json.load(f)
    df = pd.DataFrame(raw_data)
    
    # Split into Pass and Fail groups for the bottom categories
    failures = df[df['status'] == 'FAIL']
    passes = df[df['status'] == 'PASS']
    
    # 2. Setup PDF Page Geometry
    doc = SimpleDocTemplate(
        output_pdf, 
        pagesize=letter, 
        leftMargin=36, rightMargin=36, 
        topMargin=36, bottomMargin=36
    )
    story = []
    styles = getSampleStyleSheet()
    
    # Color Definition matching your Excel sheet template
    NAVY_BANNER = colors.HexColor("#1F4E79") # Deep Blue Header Banner
    LIGHT_BLUE_BG = colors.HexColor("#DDEBF7") # Padded section label background
    BORDER_GRAY = colors.HexColor("#D9D9D9")
    TEXT_DARK = colors.HexColor("#000000")
    RED_TEXT = colors.HexColor("#C00000")
    GREEN_TEXT = colors.HexColor("#385723")

    # Typography / Styles
    banner_style = ParagraphStyle('BannerText', fontName='Helvetica-Bold', fontSize=14, textColor=colors.white, alignment=1)
    section_title = ParagraphStyle('SecTitle', fontName='Helvetica-Bold', fontSize=10, textColor=TEXT_DARK, alignment=0)
    label_style = ParagraphStyle('Label', fontName='Helvetica-Bold', fontSize=9, textColor=TEXT_DARK)
    value_style = ParagraphStyle('Value', fontName='Helvetica', fontSize=9, textColor=TEXT_DARK)
    category_heading = ParagraphStyle('CatHead', fontName='Helvetica-Bold', fontSize=11, textColor=NAVY_BANNER, spaceBefore=14, spaceAfter=6)
    
    table_hdr_style = ParagraphStyle('TableHdr', fontName='Helvetica-Bold', fontSize=9, textColor=TEXT_DARK)
    table_cell_style = ParagraphStyle('TableCell', fontName='Helvetica', fontSize=9, textColor=TEXT_DARK)

    # ----------------------------------------------------
    # BLOCK 1: MAIN REPORT HEADER BANNER
    # ----------------------------------------------------
    banner_data = [[Paragraph("QUALITY, HEALTH, SAFETY & ENVIRONMENT REPORT", banner_style)]]
    banner_table = Table(banner_data, colWidths=[540])
    banner_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), NAVY_BANNER),
        ('ALIGN', (0,0), (-1,-1), 'CENTER'),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('TOPPADDING', (0,0), (-1,-1), 8),
        ('BOTTOMPADDING', (0,0), (-1,-1), 8),
    ]))
    story.append(banner_table)
    story.append(Spacer(1, 2))

    # ----------------------------------------------------
    # BLOCK 2: DOCUMENT SECTIONS META-INFO
    # ----------------------------------------------------
    doc_sec_data = [[Paragraph("DOCUMENT SECTIONS", section_title)]]
    doc_sec_table = Table(doc_sec_data, colWidths=[540])
    doc_sec_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), LIGHT_BLUE_BG),
        ('BOX', (0,0), (-1,-1), 1, BORDER_GRAY),
        ('TOPPADDING', (0,0), (-1,-1), 4),
        ('BOTTOMPADDING', (0,0), (-1,-1), 4),
        ('LEFTPADDING', (0,0), (-1,-1), 6),
    ]))
    story.append(doc_sec_table)
    story.append(Spacer(1, 1))

    # Meta-Data Fields Grid
    current_date = datetime.now().strftime("%Y-%m-%d")
    meta_grid_data = [
        [Paragraph("Doc ID:", label_style), Paragraph("QHSE-ROB-001", value_style), Paragraph("Location:", label_style), Paragraph("Logistics Zone Alpha", value_style)],
        [Paragraph("Version:", label_style), Paragraph("V1.0 Beta", value_style), Paragraph("Date:", label_style), Paragraph(current_date, value_style)],
        [Paragraph("Conducted By:", label_style), Paragraph("Autonomous Unit 01", value_style), Paragraph("", label_style), Paragraph("", value_style)]
    ]
    meta_grid_table = Table(meta_grid_data, colWidths=[90, 180, 90, 180])
    meta_grid_table.setStyle(TableStyle([
        ('BOX', (0,0), (-1,-1), 1, BORDER_GRAY),
        ('INNERGRID', (0,0), (-1,-1), 0.5, BORDER_GRAY),
        ('TOPPADDING', (0,0), (-1,-1), 5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 5),
        ('LEFTPADDING', (0,0), (-1,-1), 6),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
    ]))
    story.append(meta_grid_table)
    story.append(Spacer(1, 10))

    # Helper function to generate clean data tables matching the template grid
    def build_styled_grid(dataframe, status_color):
        grid_rows = [[
            Paragraph("Timestamp", table_hdr_style), 
            Paragraph("Zone", table_hdr_style), 
            Paragraph("Metric Inspected", table_hdr_style), 
            Paragraph("Risk Severity", table_hdr_style)
        ]]
        
        for _, row in dataframe.iterrows():
            grid_rows.append([
                Paragraph(row['timestamp'], table_cell_style),
                Paragraph(row['zone'], table_cell_style),
                Paragraph(row['metric'], table_cell_style),
                Paragraph(f"<font color='{status_color}'><b>{row['severity']}</b></font>", table_cell_style)
            ])
            
        t = Table(grid_rows, colWidths=[120, 110, 220, 90])
        t.setStyle(TableStyle([
            ('BACKGROUND', (0,0), (-1,0), LIGHT_BLUE_BG),
            ('BOX', (0,0), (-1,-1), 1, BORDER_GRAY),
            ('INNERGRID', (0,0), (-1,-1), 0.5, BORDER_GRAY),
            ('TOPPADDING', (0,0), (-1,-1), 6),
            ('BOTTOMPADDING', (0,0), (-1,-1), 6),
            ('LEFTPADDING', (0,0), (-1,-1), 6),
            ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ]))
        return t

    # ----------------------------------------------------
    # BLOCK 3: CATEGORIES AT THE END (FAILED VS PASSED)
    # ----------------------------------------------------
    # Category A: Non-Compliance Action Items (FAIL)
    story.append(Paragraph("❌ Detected Non-Compliance Action Items (FAIL)", category_heading))
    if not failures.empty:
        story.append(build_styled_grid(failures, RED_TEXT))
    else:
        story.append(Paragraph("All evaluated metrics conformed perfectly to workplace safety standards.", table_cell_style))
        
    story.append(Spacer(1, 10))
    
    # Category B: Confirmed Operational Passes (PASS)
    story.append(Paragraph("✅ Confirmed Operational Passes (PASS)", category_heading))
    if not passes.empty:
        story.append(build_styled_grid(passes, GREEN_TEXT))
    else:
        story.append(Paragraph("No checking criteria returned an explicit passing status.", table_cell_style))

    # Build the document layout structure
    doc.build(story)

if __name__ == "__main__":
    create_pdf_report('mock_robot_telemetry.json', 'QHSE_Audit_Report.pdf')