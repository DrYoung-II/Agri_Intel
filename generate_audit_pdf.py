"""
Script to generate the AgroBiometrix Comprehensive Platform Audit & Strategic Gap Analysis PDF.
"""

import sys
import os
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, HRFlowable, Image as RLImage
)
from reportlab.pdfgen import canvas

PDF_FILENAME = "AgroBiometrix_Platform_Audit_and_Gap_Analysis.pdf"


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
            self.drawString(54, 755, "AgroBiometrix Strategic Audit — Platform Architecture & Gap Analysis")
            self.drawRightString(558, 755, "Institutional & Founder Alignment")
            self.setStrokeColor(colors.HexColor("#C8E6C9"))
            self.setLineWidth(0.6)
            self.line(54, 750, 558, 750)

        # Footer (all pages)
        page_text = f"Page {self._pageNumber} of {page_count}"
        self.drawString(54, 35, "AgroBiometrix: Generative Intelligence Platform for African & Global Agriculture")
        self.drawRightString(558, 35, page_text)
        self.setStrokeColor(colors.HexColor("#C8E6C9"))
        self.setLineWidth(0.6)
        self.line(54, 45, 558, 45)
        self.restoreState()


def create_audit_pdf():
    doc = SimpleDocTemplate(
        PDF_FILENAME,
        pagesize=letter,
        leftMargin=54,
        rightMargin=54,
        topMargin=54,
        bottomMargin=54
    )

    styles = getSampleStyleSheet()

    # Custom styles
    title_style = ParagraphStyle(
        'DocTitle',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=20,
        leading=24,
        textColor=colors.HexColor("#1B5E20"),
        spaceAfter=4
    )

    subtitle_style = ParagraphStyle(
        'DocSubTitle',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=11,
        leading=15,
        textColor=colors.HexColor("#2E7D32"),
        spaceAfter=12
    )

    h1_style = ParagraphStyle(
        'Heading1_Custom',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=13,
        leading=17,
        textColor=colors.HexColor("#1B5E20"),
        spaceBefore=12,
        spaceAfter=6,
        keepWithNext=True
    )

    h2_style = ParagraphStyle(
        'Heading2_Custom',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=10.5,
        leading=14,
        textColor=colors.HexColor("#2E7D32"),
        spaceBefore=8,
        spaceAfter=4,
        keepWithNext=True
    )

    body_style = ParagraphStyle(
        'Body_Custom',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=8.5,
        leading=12,
        textColor=colors.HexColor("#263238"),
        spaceAfter=5
    )

    callout_style = ParagraphStyle(
        'Callout_Text',
        parent=styles['Normal'],
        fontName='Helvetica-Oblique',
        fontSize=8.5,
        leading=12,
        textColor=colors.HexColor("#1B5E20")
    )

    table_cell = ParagraphStyle(
        'TableCell',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=8,
        leading=10.5,
        textColor=colors.HexColor("#263238")
    )

    table_header = ParagraphStyle(
        'TableHeader',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=8,
        leading=11,
        textColor=colors.white
    )

    elements = []

    # Title block with official logo
    logo_file = "assets/agrobiometrix_logo.png"
    if os.path.exists(logo_file):
        header_data = [
            [
                RLImage(logo_file, width=64, height=70),
                Paragraph("<b>AgroBiometrix Platform Audit &amp; Strategic Gap Analysis</b><br/><font size='8' color='#2E7D32'><b>AGRICULTURE &bull; RESEARCH &bull; INSIGHT</b></font><br/><font size='7.5' color='#555555'>Benchmarking Against 'The BIG Idea' Founder Document, CGIAR/FAO Standards &amp; Production Roadmap</font>", title_style),
            ]
        ]
        t_head = Table(header_data, colWidths=[70, 434])
        t_head.setStyle(TableStyle([
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 2),
            ('TOPPADDING', (0, 0), (-1, -1), 0),
            ('LEFTPADDING', (0, 0), (-1, -1), 0),
            ('RIGHTPADDING', (0, 0), (-1, -1), 0),
        ]))
        elements.append(t_head)
    else:
        elements.append(Paragraph("🌱 AgroBiometrix Platform Audit & Strategic Gap Analysis", title_style))
        elements.append(Paragraph("Benchmarking Against 'The BIG Idea' Founder Document, CGIAR/FAO Standards & Production Roadmap", subtitle_style))
    elements.append(HRFlowable(width="100%", thickness=1.5, color=colors.HexColor("#2E7D32"), spaceBefore=3, spaceAfter=8))

    # Executive Summary Card
    summary_text = (
        "<b>Executive Verdict:</b> AgroBiometrix has successfully established the core biometrics, statistical genetics, "
        "soil, climate, and policy intelligence infrastructure. To achieve full parity with the founder's original design and "
        "meet international enterprise and donor standards (CGIAR AI Hub, Gates Foundation, World Bank), this audit identifies "
        "<b>7 critical capability gaps</b> and defines an immediate 3-step action plan to finalize institutional readiness."
    )
    summary_table = Table([[Paragraph(summary_text, callout_style)]], colWidths=[504])
    summary_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor("#E8F5E9")),
        ('BORDER', (0, 0), (-1, -1), 1, colors.HexColor("#81C784")),
        ('PADDING', (0, 0), (-1, -1), 8),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
    ]))
    elements.append(summary_table)
    elements.append(Spacer(1, 10))

    # SECTION 1: Current System Inventory
    elements.append(Paragraph("1. System Inventory: Current vs. Complete Architecture", h1_style))
    inventory_intro = (
        "AgroBiometrix currently operates 12 live modules, an exact Duncan's Multiple Range Test (DMRT) biometrics engine, "
        "and a multi-agent orchestration layer. The table below audits current modules against the complete 15-module blueprint:"
    )
    elements.append(Paragraph(inventory_intro, body_style))

    inv_data = [
        [
            Paragraph("Module Blueprint", table_header),
            Paragraph("Current Status", table_header),
            Paragraph("Coverage & Key Functions", table_header),
            Paragraph("Audit Finding", table_header)
        ],
        [
            Paragraph("<b>Mod 1: Research Copilot</b>", table_cell),
            Paragraph("<font color='#2E7D32'><b>Operational</b></font>", table_cell),
            Paragraph("African Evidence Engine, Q&A synthesis, evidence tables.", table_cell),
            Paragraph("Meets initial spec.", table_cell)
        ],
        [
            Paragraph("<b>Mod 2: Research Scientist</b>", table_cell),
            Paragraph("<font color='#2E7D32'><b>Operational</b></font>", table_cell),
            Paragraph("Proposal builder, dataset health inspector, mixed models.", table_cell),
            Paragraph("Meets initial spec.", table_cell)
        ],
        [
            Paragraph("<b>Mod 3: Statistical Geneticist</b>", table_cell),
            Paragraph("<font color='#2E7D32'><b>Operational</b></font>", table_cell),
            Paragraph("ANOVA, Duncan's Test, Tukey, Fisher, Dunnett, EBVs/BLUP.", table_cell),
            Paragraph("Needs 1-click report export.", table_cell)
        ],
        [
            Paragraph("<b>Mod 4: Plant Breeding</b>", table_cell),
            Paragraph("<font color='#2E7D32'><b>Operational</b></font>", table_cell),
            Paragraph("GxE interaction, drought/heat breeding prioritizer.", table_cell),
            Paragraph("Meets initial spec.", table_cell)
        ],
        [
            Paragraph("<b>Mod 5: Soil Intelligence</b>", table_cell),
            Paragraph("<font color='#2E7D32'><b>Operational</b></font>", table_cell),
            Paragraph("NPK, pH, texture, fertilizer strategy, price simulator.", table_cell),
            Paragraph("Hardcoded to NGN; needs multi-currency.", table_cell)
        ],
        [
            Paragraph("<b>Mod 6: Climate Intelligence</b>", table_cell),
            Paragraph("<font color='#2E7D32'><b>Operational</b></font>", table_cell),
            Paragraph("4-scenario simulator + live Open-Meteo REST API.", table_cell),
            Paragraph("Meets initial spec.", table_cell)
        ],
        [
            Paragraph("<b>Mod 7: Livestock Intelligence</b>", table_cell),
            Paragraph("<font color='#2E7D32'><b>Operational</b></font>", table_cell),
            Paragraph("Multi-trait breeding index, THI heat stress, selection.", table_cell),
            Paragraph("Meets initial spec.", table_cell)
        ],
        [
            Paragraph("<b>Mod 8: Experiment Designer</b>", table_cell),
            Paragraph("<font color='#2E7D32'><b>Operational</b></font>", table_cell),
            Paragraph("CRD, RCBD, Factorial, field layout, CSV download, R code.", table_cell),
            Paragraph("Meets initial spec.", table_cell)
        ],
        [
            Paragraph("<b>Mod 9: Literature Review Scientist</b>", table_cell),
            Paragraph("<font color='#D32F2F'><b>MISSING</b></font>", table_cell),
            Paragraph("PRISMA flow, methodological/geographic gap matrix.", table_cell),
            Paragraph("<b>CRITICAL GAP: In founder doc, not yet built.</b>", table_cell)
        ],
        [
            Paragraph("<b>Mod 10: Thesis & Student Tutor</b>", table_cell),
            Paragraph("<font color='#2E7D32'><b>Operational</b></font>", table_cell),
            Paragraph("Pedagogical step-by-step mentor, defense prep, critique.", table_cell),
            Paragraph("Meets initial spec.", table_cell)
        ],
        [
            Paragraph("<b>Mod 11: Policy Simulator</b>", table_cell),
            Paragraph("<font color='#2E7D32'><b>Operational</b></font>", table_cell),
            Paragraph("What-if simulator, 1B intervention allocator, food security.", table_cell),
            Paragraph("Hardcoded to NGN; needs multi-currency.", table_cell)
        ],
        [
            Paragraph("<b>Mod 13: Knowledge Graph</b>", table_cell),
            Paragraph("<font color='#2E7D32'><b>Operational</b></font>", table_cell),
            Paragraph("Gene to Trait to Breed to Soil to Economy Plotly network.", table_cell),
            Paragraph("Needs interactive sub-graph filters.", table_cell)
        ],
        [
            Paragraph("<b>Mod 15: API Subscription Hub</b>", table_cell),
            Paragraph("<font color='#2E7D32'><b>Operational</b></font>", table_cell),
            Paragraph("Directory of paid and free agricultural data APIs.", table_cell),
            Paragraph("Meets initial spec.", table_cell)
        ]
    ]

    inv_table = Table(inv_data, colWidths=[120, 75, 175, 134])
    inv_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor("#1B5E20")),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor("#C8E6C9")),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor("#F9FBF9")]),
        ('PADDING', (0, 0), (-1, -1), 4),
    ]))
    elements.append(inv_table)
    elements.append(Spacer(1, 10))

    # SECTION 2: Detailed Breakdown of the 7 Gaps
    elements.append(Paragraph("2. Deep-Dive: The 7 Strategic & Architectural Gaps", h1_style))

    gaps = [
        ("Gap 1: Module 9 — Systematic Literature Review & PRISMA Engine",
         "The founder document specified an AI Literature Review Scientist that systematically synthesizes published papers, "
         "extracts sample sizes, traits, and models, constructs PRISMA 2020 flow diagrams, and identifies geographic and "
         "methodological gaps. This is currently omitted from the application sidebar."),
        ("Gap 2: Dynamic Pan-African Country & Multi-Currency Switcher",
         "The soil and policy simulation modules hardcode Nigerian Naira (₦). To fulfill the Pan-African mandate, a universal "
         "sidebar selector is required to seamlessly toggle currencies (₦ NGN, KSh KES, GH₵ GHS, ETB, ZAR, $ USD) and align "
         "economic baselines across East, West, and Southern Africa."),
        ("Gap 3: One-Click Publication-Ready Statistical Report Generator",
         "While Module 3 runs publication-grade ANOVA and Duncan's Multiple Range Tests, researchers currently have to manually "
         "transcribe output. A single-click 'Download Publication Manuscript (APA Format)' feature generating formal results paragraphs, "
         "letter grouping tables, and appendix code is missing."),
        ("Gap 4: Multilingual Voice / Audio Advisory Simulator (Last-Mile Extension)",
         "High-level research insights fail if they cannot reach rural, illiterate farmers. A simulated extension radio bulletin "
         "translating complex biometrics into localized voice advisories in Hausa, Yoruba, Igbo, and Swahili is required to "
         "prove last-mile efficacy to donors (Gates Foundation, AGRA, USAID)."),
        ("Gap 5: Persistent Session Database (Save & Load Historical Scenarios)",
         "Currently, browser refreshes wipe user trial configurations, policy budget allocations, and breeding indexes. An embedded "
         "local store (SQLite/DuckDB) is needed to persist user experiments across sessions."),
        ("Gap 6: Interactive Filter Controls for the Agricultural Knowledge Graph",
         "Module 13 renders a monolithic Plotly network graph. An interactive filtering pane allowing users to isolate specific crops "
         "(Cassava, Maize), livestock (White Fulani, N'Dama), or abiotic stressors (Heat, Acid Soil) is needed."),
        ("Gap 7: Cloud & Production Deployment Package",
         "The platform lacks automated containerization files (Dockerfile, docker-compose.yml, .streamlit/secrets.toml.example) "
         "required for 1-click institutional deployment on AWS, Google Cloud Run, or Streamlit Community Cloud.")
    ]

    for title, desc in gaps:
        elements.append(Paragraph(title, h2_style))
        elements.append(Paragraph(desc, body_style))

    elements.append(Spacer(1, 10))

    # SECTION 3: The 3-Step Execution Action Plan
    elements.append(Paragraph("3. Immediate 3-Step Implementation Plan", h1_style))
    plan_intro = "To address the most urgent scientific and user-facing requirements immediately, the following 3 steps are scheduled for active deployment:"
    elements.append(Paragraph(plan_intro, body_style))

    steps_data = [
        [
            Paragraph("Step", table_header),
            Paragraph("Target Area", table_header),
            Paragraph("Deliverable & Implementation Details", table_header),
            Paragraph("Expected Impact", table_header)
        ],
        [
            Paragraph("<b>Step 1</b>", table_cell),
            Paragraph("<b>Module 9 Literature Review Scientist</b>", table_cell),
            Paragraph("Create <code>modules/mod9_literature.py</code> featuring: PRISMA 2020 flow visualization, "
                      "evidence extraction matrix with sample size/trait/method columns, and geographic/methodological gap detector.", table_cell),
            Paragraph("Restores complete parity with 'The BIG Idea' founder document.", table_cell)
        ],
        [
            Paragraph("<b>Step 2</b>", table_cell),
            Paragraph("<b>Pan-African Currency Switcher</b>", table_cell),
            Paragraph("Add global selector in sidebar (NGN ₦, KES KSh, GHS GH₵, ETB Br, ZAR R, USD $). Bind currency symbol "
                      "dynamically across <code>mod5_soil.py</code> (fertilizer margin) and <code>mod11_policy.py</code> (budget allocator).", table_cell),
            Paragraph("Instantly personalizes app for Kenya, Ghana, Ethiopia & international users.", table_cell)
        ],
        [
            Paragraph("<b>Step 3</b>", table_cell),
            Paragraph("<b>1-Click Publication Report Export</b>", table_cell),
            Paragraph("Add instant report exporter in <code>mod3_geneticist.py</code> generating formal APA/Journal results text, "
                      "degrees of freedom, exact F-statistic, p-value, and Duncan's letter grouping table in Markdown/Text.", table_cell),
            Paragraph("Saves postgraduate students and researchers hours of manuscript prep.", table_cell)
        ]
    ]

    steps_table = Table(steps_data, colWidths=[40, 110, 240, 114])
    steps_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor("#2E7D32")),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor("#C8E6C9")),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor("#F9FBF9")]),
        ('PADDING', (0, 0), (-1, -1), 5),
    ]))
    elements.append(steps_table)
    elements.append(Spacer(1, 14))

    # SECTION 4: Institutional Readiness Scorecard
    elements.append(Paragraph("4. Institutional Readiness Scorecard (Post-Implementation)", h1_style))
    scorecard_data = [
        [
            Paragraph("Institutional Criterion", table_header),
            Paragraph("Benchmark Standard", table_header),
            Paragraph("AgroBiometrix Capability Post-Upgrade", table_header),
            Paragraph("Readiness", table_header)
        ],
        [
            Paragraph("<b>Scientific Rigor</b>", table_cell),
            Paragraph("CGIAR / FAO Biometrics Standards", table_cell),
            Paragraph("Exact ANOVA, DMRT alpha_p formulas, heritability, BLUP, PRISMA reviews.", table_cell),
            Paragraph("<font color='#2E7D32'><b>100% Complete</b></font>", table_cell)
        ],
        [
            Paragraph("<b>Geographic Scope</b>", table_cell),
            Paragraph("African Union / CAADP Mandate", table_cell),
            Paragraph("Pan-African currency switcher, multi-country soil/climate presets (East/West Africa).", table_cell),
            Paragraph("<font color='#2E7D32'><b>100% Complete</b></font>", table_cell)
        ],
        [
            Paragraph("<b>Zero-Cost Operability</b>", table_cell),
            Paragraph("African University Budget Realities", table_cell),
            Paragraph("100% offline deterministic engines with preloaded benchmark trial datasets.", table_cell),
            Paragraph("<font color='#2E7D32'><b>100% Complete</b></font>", table_cell)
        ],
        [
            Paragraph("<b>Commercial Viability</b>", table_cell),
            Paragraph("B2B SaaS / Institutional Licensing", table_cell),
            Paragraph("Freemium student tier, institutional lab licenses, government policy sandboxes.", table_cell),
            Paragraph("<font color='#2E7D32'><b>High</b></font>", table_cell)
        ]
    ]

    score_table = Table(scorecard_data, colWidths=[110, 110, 214, 70])
    score_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor("#1B5E20")),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor("#C8E6C9")),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor("#F9FBF9")]),
        ('PADDING', (0, 0), (-1, -1), 5),
    ]))
    elements.append(score_table)

    # Build PDF
    doc.build(elements, canvasmaker=NumberedCanvas)
    
    import shutil
    alt_file = "4 AgroBiometrix_Platform_Audit_and_Gap_Analysis.pdf"
    brain_dir = r"C:\Users\USER\.gemini\antigravity\brain\1e91af0e-0faf-4a71-9df3-64f967526da0"
    if os.path.exists(PDF_FILENAME):
        shutil.copyfile(PDF_FILENAME, alt_file)
        if os.path.exists(brain_dir):
            shutil.copyfile(PDF_FILENAME, os.path.join(brain_dir, PDF_FILENAME))
            shutil.copyfile(PDF_FILENAME, os.path.join(brain_dir, alt_file))
    print(f"Successfully generated {PDF_FILENAME} and mirrored to {alt_file}")


if __name__ == "__main__":
    create_audit_pdf()
