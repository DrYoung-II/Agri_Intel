"""
Script to generate AgroBiometrix Global Dominance & Pitch Mastery PDF.
"""

from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, HRFlowable
)
from reportlab.pdfgen import canvas

PDF_FILENAME = "AgroBiometrix_Global_Dominance_and_Pitch_Mastery.pdf"


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
            self.drawString(54, 755, "AgroBiometrix Global Blueprint — Pitch Mastery & Commercial Dominance")
            self.drawRightString(558, 755, "Africa-First, Globally Scalable")
            self.setStrokeColor(colors.HexColor("#C8E6C9"))
            self.setLineWidth(0.6)
            self.line(54, 750, 558, 750)

        # Footer (all pages)
        page_text = f"Page {self._pageNumber} of {page_count}"
        self.drawString(54, 35, "AgroBiometrix: The Generative Intelligence Platform for Agriculture")
        self.drawRightString(558, 35, page_text)
        self.setStrokeColor(colors.HexColor("#C8E6C9"))
        self.setLineWidth(0.6)
        self.line(54, 45, 558, 45)
        self.restoreState()


def create_pitch_pdf():
    doc = SimpleDocTemplate(
        PDF_FILENAME,
        pagesize=letter,
        leftMargin=54,
        rightMargin=54,
        topMargin=54,
        bottomMargin=54
    )

    styles = getSampleStyleSheet()

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

    pitch_quote_style = ParagraphStyle(
        'PitchQuote',
        parent=styles['Normal'],
        fontName='Helvetica-Oblique',
        fontSize=9,
        leading=13.5,
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

    # Title & Banner
    elements.append(Paragraph("🚀 AgroBiometrix: Global Dominance & Pitch Mastery Blueprint", title_style))
    elements.append(Paragraph("Executive Investor Script, 10-Slide Pitch Deck Framework, and Institutional Defense Strategy", subtitle_style))
    elements.append(HRFlowable(width="100%", thickness=1.5, color=colors.HexColor("#2E7D32"), spaceBefore=2, spaceAfter=8))

    # Executive Verdict Banner
    banner_text = (
        "<b>The Global Position:</b> AgroBiometrix is in the top 1% of agricultural AI architectures worldwide. While competitors build "
        "shallow leaf-photo classifiers or generic ChatGPT wrappers, AgroBiometrix connects quantitative genetics, exact biometrics (DMRT), "
        "PRISMA systematic reviews, real-time climate telemetry, and macroeconomic policy sovereignty. This document provides the "
        "exact words, pitch structure, and defensive strategies to dominate grant competitions and venture capital meetings."
    )
    banner_table = Table([[Paragraph(banner_text, pitch_quote_style)]], colWidths=[504])
    banner_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor("#E8F5E9")),
        ('BORDER', (0, 0), (-1, -1), 1, colors.HexColor("#81C784")),
        ('PADDING', (0, 0), (-1, -1), 8),
    ]))
    elements.append(banner_table)
    elements.append(Spacer(1, 10))

    # SECTION 1: The 3-Minute World-Class Pitch Script
    elements.append(Paragraph("1. The 3-Minute World-Class Pitch Script", h1_style))
    elements.append(Paragraph("Deliver this opening monologue verbatim to investors, CGIAR leadership, or grant juries:", body_style))

    script_box = (
        "<i>\"Africa holds 60% of the world's remaining uncultivated arable land, yet our continent spends $50 billion every year "
        "importing food. The problem is NOT that agricultural science is missing—it is that our knowledge is completely fragmented. "
        "It sits locked in academic theses at Ahmadu Bello University, isolated CIMMYT trial spreadsheets, inaccessible soil maps, "
        "and uncoordinated government ministry files.<br/><br/>"
        "Generic Silicon Valley AI cannot solve this because it hallucinates, lacks African biological ground truth, and doesn't understand "
        "pastoral zebu cattle or tropical ultisol soils. Meanwhile, existing African agricultural apps merely say: 'Upload a picture of your "
        "leaf and I will identify the pest.' Useful, but narrow.<br/><br/>"
        "We built <b>AgroBiometrix</b>: the generative intelligence infrastructure behind African agriculture. Give AgroBiometrix a crop, an indigenous "
        "animal breed, a GPS coordinate, a soil profile, a climate scenario, or a policy goal—and it unites scientific research, runs exact "
        "biometrics like Duncan's Multiple Range Test, simulates climate shocks via live satellite APIs, and translates findings into "
        "multilingual voice advisories in Hausa, Yoruba, and Swahili for the rural farmer.<br/><br/>"
        "From the university research lab to the smallholder field, and straight to the Minister of Agriculture's desk: AgroBiometrix connects "
        "agricultural intelligence at continental scale.\"</i>"
    )
    script_table = Table([[Paragraph(script_box, pitch_quote_style)]], colWidths=[504])
    script_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor("#F1F8F2")),
        ('BORDER', (0, 0), (-1, -1), 1, colors.HexColor("#A5D6A7")),
        ('PADDING', (0, 0), (-1, -1), 9),
    ]))
    elements.append(script_table)
    elements.append(Spacer(1, 12))

    # SECTION 2: Competitive Positioning Matrix
    elements.append(Paragraph("2. Competitive Moat: AgroBiometrix vs. Market Alternatives", h1_style))
    matrix_data = [
        [
            Paragraph("Capability Dimension", table_header),
            Paragraph("Generic LLMs (ChatGPT/Claude)", table_header),
            Paragraph("Farmer Diagnostic Apps (Plantix)", table_header),
            Paragraph("AgroBiometrix Platform", table_header)
        ],
        [
            Paragraph("<b>Statistical Biometrics</b>", table_cell),
            Paragraph("Hallucinates formulas; cannot calculate exact studentized ranges.", table_cell),
            Paragraph("None (Visual image classification only).", table_cell),
            Paragraph("<font color='#2E7D32'><b>Exact ANOVA, DMRT alpha_p, Tukey, Fisher, GBLUP</b></font>", table_cell)
        ],
        [
            Paragraph("<b>African Grounding</b>", table_cell),
            Paragraph("Trained on US/European temperate agricultural data.", table_cell),
            Paragraph("Limited to common cosmopolitan pest libraries.", table_cell),
            Paragraph("<font color='#2E7D32'><b>Native Zebu/Taurine breeds, Savanna soils, CGIAR/IITA evidence</b></font>", table_cell)
        ],
        [
            Paragraph("<b>Scientific Citations</b>", table_cell),
            Paragraph("Fabricates non-existent DOIs and author citations.", table_cell),
            Paragraph("Proprietary internal diagnosis without literature linkage.", table_cell),
            Paragraph("<font color='#2E7D32'><b>PRISMA 2020 systematic review matrices with verified DOIs</b></font>", table_cell)
        ],
        [
            Paragraph("<b>Macroeconomic Policy</b>", table_cell),
            Paragraph("Generic conversational policy essays.", table_cell),
            Paragraph("Zero macroeconomic or policy simulation capability.", table_cell),
            Paragraph("<font color='#2E7D32'><b>Treasury subsidy cost-benefit, forex savings, 1B intervention model</b></font>", table_cell)
        ],
        [
            Paragraph("<b>Last-Mile Delivery</b>", table_cell),
            Paragraph("Text-only English prompts; unusable by illiterate farmers.", table_cell),
            Paragraph("Smartphone camera required; high data consumption.", table_cell),
            Paragraph("<font color='#2E7D32'><b>Simulated multilingual voice bulletins (Hausa, Yoruba, Swahili)</b></font>", table_cell)
        ]
    ]

    matrix_table = Table(matrix_data, colWidths=[90, 135, 135, 144])
    matrix_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor("#1B5E20")),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor("#C8E6C9")),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor("#F9FBF9")]),
        ('PADDING', (0, 0), (-1, -1), 4.5),
    ]))
    elements.append(matrix_table)
    elements.append(Spacer(1, 12))

    # SECTION 3: The 10-Slide Pitch Deck Structure
    elements.append(Paragraph("3. The 10-Slide Pitch Deck Framework (Institutional / VC)", h1_style))
    deck_intro = "Use this proven 10-slide narrative when presenting to institutional investors, accelerators, and foundation partners:"
    elements.append(Paragraph(deck_intro, body_style))

    deck_slides = [
        ("Slide 1: Title & The Bold Vision", "AgroBiometrix: The Generative Intelligence Infrastructure Behind African & Global Agriculture. Africa-first, globally relevant."),
        ("Slide 2: The Continental Paradox", "$50B spent importing food while 60% of global arable land lies uncultivated due to knowledge fragmentation."),
        ("Slide 3: The Critical Problem", "Agricultural research exists in silos: breeding data, satellite weather, soil maps, and farm decisions never talk to each other."),
        ("Slide 4: The AgroBiometrix Solution", "One unified intelligence layer with specialized agents: Climate, Genetics, Biometrics, Soil, Policy, and Evidence."),
        ("Slide 5: Live Product Demonstration", "Walk through Module 3 (exact DMRT report generation) and Module 11 (national policy budget simulator in local currency)."),
        ("Slide 6: The Last-Mile Bridge", "Multilingual voice synthesis (Hausa, Swahili, Yoruba) connecting PhD genetic discoveries directly to rural extension radio."),
        ("Slide 7: Total Addressable Market (TAM)", "$45B African AgTech & digital extension opportunity; 50M smallholders, 400 universities, 54 ministries of agriculture."),
        ("Slide 8: Business Model & Monetization", "3-Tier Revenue Engine: Free/freemium student thesis tier, Institutional Lab SaaS licenses, and Government Policy Sandboxes."),
        ("Slide 9: Founder Advantage ('Why Us')", "Unique cross-disciplinary founder background: Animal Genetics + Agricultural Biometrics + Advanced Artificial Intelligence."),
        ("Slide 10: The Ask & 18-Month Milestones", "$1.5M Seed / Grant to onboard 5 national agricultural research institutes (NARIs), 100k farmers, and deploy across 6 African nations.")
    ]

    deck_data = [[Paragraph(f"<b>{s[0]}</b>", table_cell), Paragraph(s[1], table_cell)] for s in deck_slides]
    deck_table = Table([[Paragraph("Slide Title", table_header), Paragraph("Key Content & Narrative Focus", table_header)]] + deck_data, colWidths=[160, 344])
    deck_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor("#2E7D32")),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor("#C8E6C9")),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor("#F9FBF9")]),
        ('PADDING', (0, 0), (-1, -1), 4),
    ]))
    elements.append(deck_table)
    elements.append(Spacer(1, 12))

    # SECTION 4: Defensive FAQ
    elements.append(Paragraph("4. Defensive FAQ: Handling Tough Pitch Questions", h1_style))
    faqs = [
        ("Q: 'Why won't OpenAI or Google just build this?'",
         "A: Foundation model companies build horizontal, generic models. Agriculture is deeply local, biological, and non-linear. "
         "Genomic BLUP, tropical soil acidity interactions, and African indigenous livestock breeds require domain-specific biometric "
         "pipelines and localized evidence bases that horizontal tech giants cannot curate or maintain."),
        ("Q: 'How do you handle rural connectivity and cost?'",
         "A: AgroBiometrix is designed from African realities outward. All core biometric and simulation engines operate 100% offline "
         "with zero API fees. For field deployment, our voice advisory engine compresses advisories into ultra-low-bandwidth audio "
         "compatible with 2G Interactive Voice Response (IVR) and community radio broadcasts."),
        ("Q: 'How do you monetize when farmers have little money?'",
         "A: Farmers do NOT pay directly. AgroBiometrix monetizes via B2B institutional lab subscriptions (universities, seed companies, "
         "livestock breeding conglomerates) and B2G government policy modeling licenses. Farmers receive subsidized extension delivery "
         "funded by donor programs and agribusiness outgrower schemes.")
    ]

    for q, a in faqs:
        elements.append(Paragraph(f"<b>{q}</b>", h2_style))
        elements.append(Paragraph(a, body_style))

    # Build PDF
    doc.build(elements, canvasmaker=NumberedCanvas)
    print(f"Successfully generated {PDF_FILENAME}")


if __name__ == "__main__":
    create_pitch_pdf()
