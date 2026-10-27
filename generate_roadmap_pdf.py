"""
Generates the executive PDF: AgriIntel Strategic Roadmap and Next Steps.
"""

from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, HRFlowable
)
from reportlab.pdfgen import canvas

PDF_FILENAME = "AgriIntel_Strategic_Roadmap_and_Next_Steps.pdf"


class NumberedCanvas(canvas.Canvas):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._saved_page_states = []

    def showPage(self):
        self._saved_page_states.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        num_pages = len(self._saved_page_states)
        for state in self._saved_page_states:
            self.__dict__.update(state)
            self.draw_header_footer(num_pages)
            super().showPage()
        super().save()

    def draw_header_footer(self, page_count):
        self.saveState()
        self.setFont("Helvetica", 8)
        self.setFillColor(colors.HexColor("#2E7D32"))
        
        # Header (pages > 1)
        if self._pageNumber > 1:
            self.drawString(54, 755, "AgriIntel Strategic Roadmap — Execution, Funding & Monetization Plan")
            self.drawRightString(558, 755, "Africa-First, Globally Relevant")
            self.setStrokeColor(colors.HexColor("#C8E6C9"))
            self.setLineWidth(0.6)
            self.line(54, 750, 558, 750)
            
        # Footer
        page_text = f"Page {self._pageNumber} of {page_count}"
        self.drawString(54, 35, "AgriIntel Commercial Strategy — Confidential Executive Brief")
        self.drawRightString(558, 35, page_text)
        self.setStrokeColor(colors.HexColor("#C8E6C9"))
        self.setLineWidth(0.6)
        self.line(54, 45, 558, 45)
        self.restoreState()


def create_roadmap_pdf():
    doc = SimpleDocTemplate(
        PDF_FILENAME,
        pagesize=letter,
        leftMargin=54,
        rightMargin=54,
        topMargin=54,
        bottomMargin=54
    )

    styles = getSampleStyleSheet()
    
    primary_green = colors.HexColor("#1B5E20")
    leaf_green = colors.HexColor("#2E7D32")
    pale_bg = colors.HexColor("#F1F8F2")
    border_green = colors.HexColor("#C8E6C9")
    text_dark = colors.HexColor("#1B3B1D")

    title_style = ParagraphStyle(
        'DocTitle',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=20,
        leading=24,
        textColor=primary_green,
        spaceAfter=4
    )

    subtitle_style = ParagraphStyle(
        'DocSubtitle',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=11,
        leading=15,
        textColor=leaf_green,
        spaceAfter=10
    )

    h1_style = ParagraphStyle(
        'Heading1_Custom',
        parent=styles['Heading1'],
        fontName='Helvetica-Bold',
        fontSize=12.5,
        leading=16,
        textColor=primary_green,
        spaceBefore=11,
        spaceAfter=4,
        keepWithNext=True
    )

    body_style = ParagraphStyle(
        'Body_Custom',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=8.8,
        leading=12.5,
        textColor=text_dark,
        spaceAfter=5
    )

    body_bold = ParagraphStyle(
        'Body_Bold_Custom',
        parent=body_style,
        fontName='Helvetica-Bold'
    )

    quote_style = ParagraphStyle(
        'Quote_Custom',
        parent=styles['Normal'],
        fontName='Helvetica-Oblique',
        fontSize=9,
        leading=13,
        textColor=primary_green
    )

    table_header_style = ParagraphStyle(
        'TableHeader',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=8.5,
        leading=11,
        textColor=colors.white
    )

    table_cell_style = ParagraphStyle(
        'TableCell',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=8,
        leading=10.5,
        textColor=text_dark
    )

    story = []

    # Title & Banner
    story.append(Paragraph("AgriIntel: What Next? Strategic Execution Plan", title_style))
    story.append(Paragraph("<b>The 4-Horizon Roadmap: Deployment, Grant Funding, Planetary APIs & Commercial Scale</b>", subtitle_style))
    story.append(HRFlowable(width="100%", thickness=1.5, color=leaf_green, spaceBefore=0, spaceAfter=8))

    # Executive Overview Callout Box
    overview_box = [
        [Paragraph("<b>STRATEGIC OBJECTIVE: MOVING FROM MVP TO VENTURE/INSTITUTIONAL SCALE</b>", body_bold)],
        [Paragraph(
            "<i>\"With the core AgriIntel engine running live—complete with the publication-grade Duncan Multiple Range Test (DMRT) biometrics, "
            "the 14 specialized intelligence modules, and the Leaf Green design system—the critical objective is now to execute a structured "
            "commercial and institutional transition: moving from a local prototype to a deployed cloud platform, securing non-dilutive grant funding "
            "(CGIAR AI Hub / Gates Foundation), and scaling toward multi-tiered monetization.\"</i>",
            quote_style
        )]
    ]
    t_overview = Table(overview_box, colWidths=[504])
    t_overview.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), pale_bg),
        ('BOX', (0, 0), (-1, -1), 1.2, leaf_green),
        ('PADDING', (0, 0), (-1, -1), 7),
    ]))
    story.append(t_overview)
    story.append(Spacer(1, 6))

    # HORIZON 1
    story.append(Paragraph("Horizon 1: Immediate Cloud Deployment & Pilot User Testing (Days 1 – 30)", h1_style))
    story.append(Paragraph(
        "<b>Goal</b>: Make AgriIntel accessible via a single URL so researchers, students, and extension officers can test it on mobile phones and laptops without touching a terminal.",
        body_style
    ))
    story.append(Paragraph(
        "• <b>One-Click Cloud Deployment</b>: Host AgriIntel on <b>Streamlit Community Cloud</b> (free public tier) or <b>Hugging Face Spaces</b>, connected to a custom domain (e.g. <code>agriintel.ai</code> or <code>agriintel.africa</code>).<br/>"
        "• <b>Closed Beta Pilot with 3 Target Cohorts</b>:<br/>"
        "&nbsp;&nbsp;&nbsp;&nbsp;1. <i>Cohort A (Postgraduate Students & Lecturers)</i>: Validate the <b>AI Statistical Geneticist (DMRT/ANOVA)</b> and <b>Thesis Tutor</b> against historical SPSS/SAS/R datasets.<br/>"
        "&nbsp;&nbsp;&nbsp;&nbsp;2. <i>Cohort B (Breeders & Agronomists at IITA/NAPRI/Universities)</i>: Test the <b>Maize Trait Prioritizer</b> and <b>Agricultural Experiment Designer (RCBD layouts)</b>.<br/>"
        "&nbsp;&nbsp;&nbsp;&nbsp;3. <i>Cohort C (Commercial Farm Managers & Extension Officers)</i>: Test the <b>Soil & Climate What-If Scenario Simulators</b> under economic and rainfall stress.<br/>"
        "• <b>Quantitative Case Studies</b>: Document time saved (e.g., <i>'Reduced trial biometric analysis and post-hoc Duncan testing time from 4 days in SAS to 4 minutes in AgriIntel'</i>).",
        body_style
    ))

    # HORIZON 2
    story.append(Paragraph("Horizon 2: Non-Dilutive Grant Funding & CGIAR Alignment (Months 1 – 3)", h1_style))
    story.append(Paragraph(
        "<b>Goal</b>: Secure non-dilutive capital and institutional backing without sacrificing equity by leveraging the founder's unique triple-intersection background (genetics + data science + agriculture):",
        body_style
    ))

    grant_data = [
        ("CGIAR AI Hub (2025/2026)", "CGIAR launched its AI Hub specifically around turning agricultural science into practical AI products.", "Position AgriIntel as the <i>operational intelligence delivery infrastructure</i> for CGIAR Dataverse and regional breeding programs."),
        ("Bill & Melinda Gates Foundation (BMGF)", "Digital Agricultural Public Infrastructure & Climate Adaptation Grants.", "Pitch AgriIntel's genomic thermotolerance and drought-escape breeding tools as smallholder resilience infrastructure."),
        ("IFPRI / AFAAS Generative AI Pilots", "AFAAS is piloting GenAI extension services across Nigeria, Kenya, Uganda, and Liberia.", "Integrate AgriIntel as the verified evidence-grounded backend, eliminating hallucinations in extension advisory."),
        ("AfDB TAAT & Agri-Pitch", "African Development Bank Technologies for African Agricultural Transformation.", "Demonstrate macro-policy decision support and seed-system intervention optimization.")
    ]
    g_rows = [[Paragraph(f"<b>{g[0]}</b>", table_cell_style), Paragraph(g[1], table_cell_style), Paragraph(g[2], table_cell_style)] for g in grant_data]
    g_table = Table([[Paragraph("<b>Target Institution / Grant</b>", table_header_style), Paragraph("<b>Strategic Mandate</b>", table_header_style), Paragraph("<b>AgriIntel Value Proposition</b>", table_header_style)]] + g_rows, colWidths=[120, 180, 204])
    g_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), primary_green),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('GRID', (0, 0), (-1, -1), 0.5, border_green),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, pale_bg]),
        ('PADDING', (0, 0), (-1, -1), 4),
    ]))
    story.append(g_table)
    story.append(Spacer(1, 6))

    # HORIZON 3
    story.append(PageBreak())
    story.append(Paragraph("Horizon 3: Data Ingestion & Live Planetary APIs (Months 3 – 6)", h1_style))
    story.append(Paragraph(
        "<b>Goal</b>: Connect dynamic global data pipelines so that any user typing a GPS coordinate receives live real-time analysis.",
        body_style
    ))
    story.append(Paragraph(
        "• <b>Live NASA POWER & Open-Meteo Integration</b>: Query live solar radiation, rainfall anomalies, and 7-day agro-weather forecasts automatically based on user farm coordinates.<br/>"
        "• <b>Automated ISRIC SoilGrids REST Queries</b>: Retrieve high-resolution soil pH, organic carbon, texture, and CEC directly from the global 250m soil grid without manual data entry.<br/>"
        "• <b>Multi-Country & Currency Switcher</b>: Introduce a sidebar selector toggling between <b>Nigeria (&#8358;)</b>, <b>Kenya (KSh)</b>, <b>Ghana (GH&#8373;)</b>, <b>Ethiopia (ETB)</b>, and <b>Global ($ USD)</b>, automatically adjusting input costs, commodity benchmarks, and regional agro-ecological zones.",
        body_style
    ))

    # HORIZON 4
    story.append(Paragraph("Horizon 4: Commercial Monetization & Enterprise Scale (Months 6 – 12)", h1_style))
    story.append(Paragraph(
        "<b>Goal</b>: Convert active community engagement into a robust, diversified revenue model across academia, agribusiness, and governments:",
        body_style
    ))

    pricing_data = [
        ("Free Community Tier", "$0 / Free Forever", "Students, smallholders, extension workers", "Basic ANOVA/DMRT, research topic tutor, public evidence matrices, pre-loaded benchmark datasets."),
        ("Researcher / Lab Pro", "$9 – $29 / month", "MSc/PhD candidates, university lecturers, trial agronomists", "Unlimited Mixed-Model BLUP runs, automated thesis review exports, custom R/Python script downloads, private CSV storage."),
        ("Agribusiness & Commercial", "$199 – $499 / month", "Seed companies, feedmills, agro-dealers, commercial farms", "Crop variety matching, multi-farm soil batch diagnostics, breeding candidate rankings, proprietary trial ingestion."),
        ("National Government & CGIAR", "$25k – $100k+ / year", "Ministries of Agriculture, CGIAR centers, FAO, World Bank", "Custom national policy simulation instances, national census data integration, food security budget optimization.")
    ]
    p_rows = [[Paragraph(f"<b>{p[0]}</b>", table_cell_style), Paragraph(f"<b>{p[1]}</b>", table_cell_style), Paragraph(p[2], table_cell_style), Paragraph(p[3], table_cell_style)] for p in pricing_data]
    p_table = Table([[Paragraph("<b>Tier</b>", table_header_style), Paragraph("<b>Target Pricing</b>", table_header_style), Paragraph("<b>Target Audience</b>", table_header_style), Paragraph("<b>Key Features & Value Unlock</b>", table_header_style)]] + p_rows, colWidths=[100, 85, 130, 189])
    p_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), primary_green),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('GRID', (0, 0), (-1, -1), 0.5, border_green),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, pale_bg]),
        ('PADDING', (0, 0), (-1, -1), 4),
    ]))
    story.append(p_table)
    story.append(Spacer(1, 8))

    story.append(Paragraph(
        "<b>Payment Architecture</b>: Integrated with <b>Paystack & Flutterwave</b> for African local debit cards and mobile money (M-Pesa, bank transfers), alongside <b>Stripe</b> for international institutional subscriptions.",
        body_style
    ))

    # IMMEDIATE NEXT ACTIONS
    story.append(Paragraph("Actionable Next Steps Matrix", h1_style))
    
    actions_data = [
        ("1. Cloud Deployment Setup", "Configure Streamlit Community Cloud repository, requirements freeze, and custom domain routing.", "Immediate (Week 1)"),
        ("2. Multi-Country Sidebar Toggle", "Add instant country & currency switcher (Nigeria, Kenya, Ghana, Ethiopia, Global).", "Week 1 – 2"),
        ("3. 2-Page CGIAR Concept Note", "Draft an institutional pitch brief tailored to the CGIAR AI Hub and Gates Foundation guidelines.", "Week 2 – 3"),
        ("4. Live NASA/SoilGrids APIs", "Connect live REST endpoints for automated meteorological and soil profile fetching.", "Week 3 – 4")
    ]
    act_rows = [[Paragraph(f"<b>{a[0]}</b>", table_cell_style), Paragraph(a[1], table_cell_style), Paragraph(f"<b>{a[2]}</b>", table_cell_style)] for a in actions_data]
    act_table = Table([[Paragraph("<b>Workstream</b>", table_header_style), Paragraph("<b>Action Items</b>", table_header_style), Paragraph("<b>Timeline</b>", table_header_style)]] + act_rows, colWidths=[130, 264, 110])
    act_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), primary_green),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('GRID', (0, 0), (-1, -1), 0.5, border_green),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, pale_bg]),
        ('PADDING', (0, 0), (-1, -1), 4),
    ]))
    story.append(act_table)
    story.append(Spacer(1, 10))

    story.append(Paragraph(
        "<b>Summary Conclusion:</b> AgriIntel is positioned at the exact historical moment when agricultural research centers and international funders are actively demanding agentic AI products. Following this 4-horizon roadmap ensures that AgriIntel transitions from an inspiring concept into an enduring, venture-scale agricultural intelligence institution.",
        body_bold
    ))

    doc.build(story, canvasmaker=NumberedCanvas)
    print(f"Generated {PDF_FILENAME} successfully!")


if __name__ == "__main__":
    create_roadmap_pdf()
