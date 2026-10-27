"""
AgriIntel Technical Dossier: API Dependencies, Pricing Models, and Annual Naira Cost Analysis
Generates publication-grade PDF:
- Primary: 8 AgriIntel_API_Dependencies_Pricing_and_Naira_Cost_Analysis.pdf
- Mirror: AgriIntel_API_Dependencies_Pricing_and_Naira_Cost_Analysis.pdf
Exchange Rate Benchmark: $1.00 USD = 1,400 NGN
"""

import os
import shutil
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, KeepTogether, HRFlowable
)
from reportlab.pdfgen import canvas

PDF_FILENAME = "AgriIntel_API_Dependencies_Pricing_and_Naira_Cost_Analysis.pdf"
NUMBERED_FILENAME = "8 AgriIntel_API_Dependencies_Pricing_and_Naira_Cost_Analysis.pdf"


class NumberedCanvas(canvas.Canvas):
    """Two-pass canvas to dynamically compute total page count."""
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
        self.setFont("Helvetica-Bold", 8)
        self.setFillColor(colors.HexColor("#1B5E20"))
        
        # Header (pages > 1)
        if self._pageNumber > 1:
            self.drawString(54, 755, "AGRIINTEL API DEPENDENCY MATRIX & NAIRA ANNUAL COST ANALYSIS")
            self.setFont("Helvetica", 8)
            self.setFillColor(colors.HexColor("#555555"))
            self.drawRightString(558, 755, "October 2026 | Technical Dossier 8")
            self.setStrokeColor(colors.HexColor("#A5D6A7"))
            self.setLineWidth(0.7)
            self.line(54, 748, 558, 748)
            
        # Footer (all pages)
        page_text = f"Page {self._pageNumber} of {page_count}"
        self.setFont("Helvetica", 8)
        self.setFillColor(colors.HexColor("#2E7D32"))
        self.drawString(54, 34, "AgriIntel: Generative Intelligence Infrastructure Behind Resilient Agriculture ($1 = NGN 1,400)")
        self.drawRightString(558, 34, page_text)
        self.setStrokeColor(colors.HexColor("#C8E6C9"))
        self.setLineWidth(0.6)
        self.line(54, 44, 558, 44)
        self.restoreState()


def create_api_costs_pdf():
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
    border_green = colors.HexColor("#A5D6A7")
    text_dark = colors.HexColor("#212121")

    title_style = ParagraphStyle(
        'DocTitle',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=13.5,
        leading=17,
        textColor=primary_green,
        spaceAfter=2
    )

    subtitle_style = ParagraphStyle(
        'DocSubtitle',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=8.5,
        leading=11.5,
        textColor=leaf_green,
        spaceAfter=4
    )

    h1_style = ParagraphStyle(
        'SectionH1',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=9.8,
        leading=12.5,
        textColor=primary_green,
        spaceBefore=5,
        spaceAfter=2.5,
        keepWithNext=True
    )

    h2_style = ParagraphStyle(
        'SectionH2',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=8.2,
        leading=10.5,
        textColor=leaf_green,
        spaceBefore=3.5,
        spaceAfter=2,
        keepWithNext=True
    )

    body_style = ParagraphStyle(
        'Body_Custom',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=7.3,
        leading=10.0,
        textColor=text_dark,
        spaceAfter=2.5
    )

    body_bold = ParagraphStyle(
        'Body_Bold_Custom',
        parent=body_style,
        fontName='Helvetica-Bold'
    )

    box_text_style = ParagraphStyle(
        'BoxText',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=7.1,
        leading=9.5,
        textColor=primary_green
    )

    table_header_style = ParagraphStyle(
        'TableHeader',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=6.8,
        leading=8.8,
        textColor=colors.white
    )

    table_cell_style = ParagraphStyle(
        'TableCell',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=6.5,
        leading=8.4,
        textColor=text_dark
    )

    table_cell_bold = ParagraphStyle(
        'TableCellBold',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=6.6,
        leading=8.5,
        textColor=primary_green
    )

    indep_cell_style = ParagraphStyle(
        'IndepTableCell',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=6.1,
        leading=7.7,
        textColor=text_dark
    )

    indep_cell_bold = ParagraphStyle(
        'IndepTableCellBold',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=6.2,
        leading=7.8,
        textColor=primary_green
    )

    indep_status_style = ParagraphStyle(
        'IndepStatus',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=6.2,
        leading=7.8,
        textColor=leaf_green
    )

    story = []

    # =========================================================================
    # PAGE 1: TITLE, EXECUTIVE SUMMARY, ZERO-COST PRINCIPLE & API TAXONOMY
    # =========================================================================
    story.append(Paragraph("AgriIntel &mdash; Technical Dossier 8: API Dependencies, Pricing Models &amp; Annual Naira Cost Analysis", title_style))
    story.append(Paragraph("<b>Exhaustive Module-by-Module Dependency Audit, Operational Independence &amp; FX Conversion ($1.00 USD = 1,400 NGN)</b>", subtitle_style))
    story.append(HRFlowable(width="100%", thickness=1.5, color=leaf_green, spaceBefore=0, spaceAfter=4))

    # Meta Banner
    meta_data = [
        [
            Paragraph("<b>Target Architecture:</b> AgriIntel v2.6 Core", table_cell_style),
            Paragraph("<b>FX Benchmark:</b> $1.00 USD = NGN 1,400", table_cell_style),
            Paragraph("<b>Analysis Horizon:</b> 1 Full Year (12 Mos)", table_cell_style),
            Paragraph("<b>Baseline Cost:</b> $0.00 / NGN 0.00", table_cell_bold)
        ]
    ]
    t_meta = Table(meta_data, colWidths=[126, 126, 126, 126])
    t_meta.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), pale_bg),
        ('BOX', (0,0), (-1,-1), 0.8, border_green),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('TOPPADDING', (0,0), (-1,-1), 2),
        ('BOTTOMPADDING', (0,0), (-1,-1), 2),
        ('LEFTPADDING', (0,0), (-1,-1), 4),
        ('RIGHTPADDING', (0,0), (-1,-1), 4),
    ]))
    story.append(t_meta)
    story.append(Spacer(1, 4))

    story.append(Paragraph("1. Executive Summary &amp; The Zero-Cost Architectural Principle", h1_style))
    story.append(Paragraph(
        "A foundational design objective of the AgriIntel platform is <b>complete scientific sovereignty and zero mandatory subscription dependency</b>. "
        "Unlike conventional commercial AI applications that fail when an API credit lapses or an external server throttles traffic, AgriIntel is architected "
        "with an autonomous, offline-first local biometrics engine. All mathematical computations&mdash;including Henderson's Mixed Model Equations (BLUP), "
        "Duncan's Multiple Range Test (DMRT), ANOVA, Smith-Hazel selection index matrices, stoichiometric soil balancing, and PRISMA systematic flow "
        "generation&mdash;execute deterministically on the local CPU with <b>zero API keys and zero monetary cost ($0.00 / NGN 0.00)</b>.",
        body_style
    ))
    story.append(Paragraph(
        "External APIs are utilized strictly as <b>optional live augmentations</b>. These augmentations fall into two distinct classes: "
        "(1) <i>100% Free &amp; Open Scientific APIs</i> (Open-Meteo Weather, NASA POWER, ISRIC SoilGrids, Crossref, NCBI PubMed, FAOSTAT, CGIAR CGSpace) which "
        "require zero subscription fees; and (2) <i>Commercial Cloud LLM APIs</i> (Google Gemini, OpenAI, Groq) which provide open-ended natural language "
        "synthesis. Even within Cloud LLMs, Google Gemini offers a generous perpetual free tier (15 requests/minute), allowing academic institutions "
        "to run live AI synthesis at zero cost.",
        body_style
    ))

    # Highlight Callout Box
    box_p = Paragraph(
        "<b>Architectural Guarantee:</b> AgriIntel requires <b>NGN 0.00 ($0.00)</b> to install, test, and operate in production. "
        "Connecting commercial paid APIs is purely discretionary for institutions seeking high-frequency cloud LLM token generation or commercial weather SLAs. "
        "This dossier provides exact unit prices, volume models, and full annual cost projections in Nigerian Naira (NGN) at the official benchmark rate of <b>$1 = NGN 1,400</b>.",
        box_text_style
    )
    t_box = Table([[box_p]], colWidths=[504])
    t_box.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), pale_bg),
        ('BOX', (0,0), (-1,-1), 1, leaf_green),
        ('LEFTPADDING', (0,0), (-1,-1), 7),
        ('RIGHTPADDING', (0,0), (-1,-1), 7),
        ('TOPPADDING', (0,0), (-1,-1), 4),
        ('BOTTOMPADDING', (0,0), (-1,-1), 4),
    ]))
    story.append(t_box)
    story.append(Spacer(1, 5))

    story.append(Paragraph("Platform API Taxonomy &amp; Service Categorization", h2_style))
    story.append(Paragraph(
        "AgriIntel categorizes external connections into five functional technological pillars:",
        body_style
    ))

    tax_data = [
        [
            Paragraph("Category Pillar", table_header_style),
            Paragraph("Core Function &amp; Usage in AgriIntel", table_header_style),
            Paragraph("Primary Endpoints / Providers", table_header_style),
            Paragraph("Default Cost Status", table_header_style)
        ],
        [
            Paragraph("<b>1. Cloud GenAI &amp; Reasoning</b>", table_cell_bold),
            Paragraph("Live multi-agent thesis tutoring, proposal drafting, and unstructured inquiry", table_cell_style),
            Paragraph("Google Gemini API, OpenAI API (GPT-4o), Groq Cloud", table_cell_style),
            Paragraph("<b>Freemium</b> (Free tier available; paid pay-as-you-go thereafter)", table_cell_style)
        ],
        [
            Paragraph("<b>2. Agro-Climatology &amp; Weather</b>", table_cell_bold),
            Paragraph("Real-time temperature, humidity, precipitation, and livestock THI stress calculation", table_cell_style),
            Paragraph("Open-Meteo Weather API, NASA POWER, OpenWeatherMap", table_cell_style),
            Paragraph("<b>100% Free</b> (Open-Meteo 10k req/day free; NASA public domain)", table_cell_style)
        ],
        [
            Paragraph("<b>3. Soil &amp; Spatial Mapping</b>", table_cell_bold),
            Paragraph("Automated edaphic diagnostics (pH, nitrogen, organic carbon, CEC) by latitude/longitude", table_cell_style),
            Paragraph("ISRIC SoilGrids REST API (Wageningen)", table_cell_style),
            Paragraph("<b>100% Free Open Data</b> (Creative Commons 4.0 public research)", table_cell_style)
        ],
        [
            Paragraph("<b>4. Scientific Literature</b>", table_cell_bold),
            Paragraph("Peer-reviewed evidence verification, DOI retrieval, PRISMA search protocols", table_cell_style),
            Paragraph("Crossref REST API, NCBI PubMed E-Utilities, CGIAR CGSpace", table_cell_style),
            Paragraph("<b>100% Free Open Access</b> (Zero subscription fees)", table_cell_style)
        ],
        [
            Paragraph("<b>5. Macro Agricultural Stats</b>", table_cell_bold),
            Paragraph("National crop yields, trade balances, fertilizer consumption, and livestock censuses", table_cell_style),
            Paragraph("United Nations FAOSTAT REST API &amp; Data Service", table_cell_style),
            Paragraph("<b>100% Free Open Data</b> (UN open statistical repository)", table_cell_style)
        ]
    ]
    t_tax = Table(tax_data, colWidths=[105, 155, 134, 110])
    t_tax.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), primary_green),
        ('GRID', (0,0), (-1,-1), 0.4, border_green),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('TOPPADDING', (0,0), (-1,-1), 2.5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 2.5),
        ('LEFTPADDING', (0,0), (-1,-1), 4),
        ('RIGHTPADDING', (0,0), (-1,-1), 4),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, pale_bg]),
    ]))
    story.append(t_tax)

    # =========================================================================
    # PAGE 2: MASTER MODULE-BY-MODULE API DEPENDENCY AUDIT (FULL TABLE)
    # =========================================================================
    story.append(PageBreak())
    story.append(Paragraph("2. Master Module-by-Module API Dependency &amp; Connectivity Audit", h1_style))
    story.append(Paragraph(
        "The following matrix maps all 14 core modules and the Multi-Agent Orchestrator to their underlying computational engines, "
        "identifying their baseline offline capabilities versus connected external APIs, access tiers, and cost implications.",
        body_style
    ))

    mod_table_data = [
        [
            Paragraph("Module # &amp; Title", table_header_style),
            Paragraph("Core Scientific Function", table_header_style),
            Paragraph("Default Engine (Always Free)", table_header_style),
            Paragraph("Connected External APIs", table_header_style),
            Paragraph("API Cost Status", table_header_style),
            Paragraph("Annual Cost ($ / NGN)", table_header_style)
        ],
        [
            Paragraph("<b>Mod 0: Multi-Agent Orchestrator</b>", table_cell_bold),
            Paragraph("Dynamic multi-agent reasoning (Climate, Crop, Genetics, Soil, Econ, Evidence)", table_cell_style),
            Paragraph("Deterministic African agricultural knowledge synthesis (13 commodities)", table_cell_style),
            Paragraph("&bull; Google Gemini API<br/>&bull; OpenAI API (GPT-4o)<br/>&bull; Groq Cloud (Llama 3.3)", table_cell_style),
            Paragraph("Freemium (Gemini)<br/>Paid (OpenAI)<br/>Freemium (Groq)", table_cell_style),
            Paragraph("<b>$0.00 / NGN 0</b> (Free Tier)<br/>Or ~$9.90 / NGN 13,860/yr", table_cell_style)
        ],
        [
            Paragraph("<b>Mod 1: AgriResearch Copilot</b>", table_cell_bold),
            Paragraph("Empirical Q&amp;A, evidence search, custom file uploader, radio WAV audio", table_cell_style),
            Paragraph("Local JSON database + in-memory Python 3-tone WAV synthesizer", table_cell_style),
            Paragraph("&bull; Crossref REST API<br/>&bull; NCBI PubMed API<br/>&bull; Google Gemini (opt)", table_cell_style),
            Paragraph("100% Free (Crossref)<br/>100% Free (PubMed)<br/>Freemium (Gemini)", table_cell_style),
            Paragraph("<b>$0.00 / NGN 0</b><br/>(All open data endpoints)", table_cell_style)
        ],
        [
            Paragraph("<b>Mod 2: AI Research Scientist</b>", table_cell_bold),
            Paragraph("Proposal builder, statistical power calculation (N), LMM equations", table_cell_style),
            Paragraph("Local mathematical power models, RCBD experimental design templates", table_cell_style),
            Paragraph("&bull; Google Gemini API (opt)<br/>&bull; OpenAI API (opt)", table_cell_style),
            Paragraph("Freemium / Paid (Optional for extended prose)", table_cell_style),
            Paragraph("<b>$0.00 / NGN 0</b><br/>(Local equations default)", table_cell_style)
        ],
        [
            Paragraph("<b>Mod 3: Statistical Geneticist</b>", table_cell_bold),
            Paragraph("ANOVA, Duncan's MRT, Henderson's BLUP, breeding values (EBV)", table_cell_style),
            Paragraph("Local SciPy, Statsmodels, Henderson MME solver. <b>Zero external APIs</b>", table_cell_style),
            Paragraph("<b>None (100% Standalone)</b>", table_cell_style),
            Paragraph("100% Local / Free", table_cell_style),
            Paragraph("<b>$0.00 / NGN 0.00</b><br/>(Runs on CPU biometrics)", table_cell_style)
        ],
        [
            Paragraph("<b>Mod 4: Plant Breeding Intelligence</b>", table_cell_bold),
            Paragraph("Smith-Hazel selection index, stay-green drought scores, radar biplots", table_cell_style),
            Paragraph("Local multi-trait index algorithms, covariance matrix inversion", table_cell_style),
            Paragraph("<b>None (100% Standalone)</b>", table_cell_style),
            Paragraph("100% Local / Free", table_cell_style),
            Paragraph("<b>$0.00 / NGN 0.00</b><br/>(Pure local compute)", table_cell_style)
        ],
        [
            Paragraph("<b>Mod 5: Soil Intelligence Engine</b>", table_cell_bold),
            Paragraph("Edaphic health diagnostics, NPK fertilizer balancing, lime requirement", table_cell_style),
            Paragraph("Local profile database (sample_soil_profiles_africa.csv) + chemistry logic", table_cell_style),
            Paragraph("&bull; ISRIC SoilGrids REST API (spatial edaphic queries)", table_cell_style),
            Paragraph("100% Free Open Data (Creative Commons 4.0)", table_cell_style),
            Paragraph("<b>$0.00 / NGN 0.00</b><br/>(Zero key required)", table_cell_style)
        ],
        [
            Paragraph("<b>Mod 6: Climate × Agriculture</b>", table_cell_bold),
            Paragraph("4-scenario climate simulation, SPEI drought indices, live weather, THI", table_cell_style),
            Paragraph("Local agro-climatic simulation matrices across 7 African climatic zones", table_cell_style),
            Paragraph("&bull; Open-Meteo Weather API<br/>&bull; NASA POWER API<br/>&bull; OpenWeatherMap (opt)", table_cell_style),
            Paragraph("100% Free (Open-Meteo)<br/>100% Free (NASA)<br/>Freemium (OpenWeather)", table_cell_style),
            Paragraph("<b>$0.00 / NGN 0.00</b><br/>(10k free daily calls on Open-Meteo)", table_cell_style)
        ],
        [
            Paragraph("<b>Mod 7: Livestock Intelligence</b>", table_cell_bold),
            Paragraph("Bovine breeding index, Avian THI math simulator, Festive broiler economics", table_cell_style),
            Paragraph("Local multi-trait economic weights, bioclimatic differential equations", table_cell_style),
            Paragraph("<b>None (100% Standalone)</b>", table_cell_style),
            Paragraph("100% Local / Free", table_cell_style),
            Paragraph("<b>$0.00 / NGN 0.00</b><br/>(Deterministic equations)", table_cell_style)
        ],
        [
            Paragraph("<b>Mod 8: Experiment Designer</b>", table_cell_bold),
            Paragraph("Experimental layouts (RCBD, CRD, Split-Plot, Factorial), field randomization, R scripts", table_cell_style),
            Paragraph("Local combinatorial permutation algorithms, automatic CSV/R exporter", table_cell_style),
            Paragraph("<b>None (100% Standalone)</b>", table_cell_style),
            Paragraph("100% Local / Free", table_cell_style),
            Paragraph("<b>$0.00 / NGN 0.00</b><br/>(Local procedural logic)", table_cell_style)
        ],
        [
            Paragraph("<b>Mod 9: Literature Review &amp; PRISMA</b>", table_cell_bold),
            Paragraph("PRISMA 2020 flow diagrams, evidence matrices, gap detector, search compiler", table_cell_style),
            Paragraph("Preloaded systematic reviews in African agro-science + local parser", table_cell_style),
            Paragraph("&bull; Crossref REST API<br/>&bull; NCBI PubMed API<br/>&bull; CGIAR CGSpace API", table_cell_style),
            Paragraph("100% Free Open Access (All public bibliographic)", table_cell_style),
            Paragraph("<b>$0.00 / NGN 0.00</b><br/>(Zero subscription cost)", table_cell_style)
        ],
        [
            Paragraph("<b>Mod 10: AI Thesis &amp; Student Tutor</b>", table_cell_bold),
            Paragraph("16-department research guidance, 10-stage thesis roadmap, Socratic viva defense", table_cell_style),
            Paragraph("Deterministic pedagogical roadmaps, viva defense logic for 16 departments", table_cell_style),
            Paragraph("&bull; Google Gemini API (opt)<br/>&bull; OpenAI API (opt)", table_cell_style),
            Paragraph("Freemium / Paid (Optional live Socratic chat)", table_cell_style),
            Paragraph("<b>$0.00 / NGN 0.00</b><br/>(Free Tier covers needs)", table_cell_style)
        ],
        [
            Paragraph("<b>Mod 11: Policy Simulator</b>", table_cell_bold),
            Paragraph("Fertilizer subsidy elasticity, strategic grain reserves, tariff welfare models", table_cell_style),
            Paragraph("Partial equilibrium microeconomic solver + multi-currency tables (5 nations)", table_cell_style),
            Paragraph("&bull; FAOSTAT REST API (macro agricultural statistics)", table_cell_style),
            Paragraph("100% Free Open Data (UN FAO repository)", table_cell_style),
            Paragraph("<b>$0.00 / NGN 0.00</b><br/>(Open statistical data)", table_cell_style)
        ],
        [
            Paragraph("<b>Mod 13: Knowledge Graph</b>", table_cell_bold),
            Paragraph("Interactive WebGL graph mapping Gene → Trait → Soil → Climate → Market", table_cell_style),
            Paragraph("Local NetworkX relational graph compute and Plotly WebGL renderer", table_cell_style),
            Paragraph("<b>None (100% Standalone)</b>", table_cell_style),
            Paragraph("100% Local / Free", table_cell_style),
            Paragraph("<b>$0.00 / NGN 0.00</b><br/>(Local topology engine)", table_cell_style)
        ],
        [
            Paragraph("<b>Mod 15: API Hub &amp; Diagnostics</b>", table_cell_bold),
            Paragraph("Central management console for API keys, subscription links, and billing diagnostics", table_cell_style),
            Paragraph("Local configuration manager within Streamlit session state", table_cell_style),
            Paragraph("Integrates with all listed external endpoints", table_cell_style),
            Paragraph("Administrative Console", table_cell_style),
            Paragraph("<b>$0.00 / NGN 0.00</b><br/>(Built-in interface)", table_cell_style)
        ]
    ]

    t_mod = Table(mod_table_data, colWidths=[80, 95, 95, 85, 75, 74], repeatRows=1)
    t_mod.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), primary_green),
        ('GRID', (0,0), (-1,-1), 0.4, border_green),
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ('TOPPADDING', (0,0), (-1,-1), 1.5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 1.5),
        ('LEFTPADDING', (0,0), (-1,-1), 3),
        ('RIGHTPADDING', (0,0), (-1,-1), 3),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, pale_bg]),
    ]))
    story.append(t_mod)

    # =========================================================================
    # PAGE 3: OPERATIONAL INDEPENDENCE AUDIT: WHICH MODULES FAIL WITHOUT API SUBSCRIPTIONS?
    # =========================================================================
    story.append(PageBreak())
    story.append(Paragraph("3. Operational Independence Audit: Which Modules Fail Without API Subscriptions?", h1_style))

    # Executive Verdict Callout Box
    verdict_p = Paragraph(
        "<b>EXECUTIVE VERDICT: ZERO MODULES FAIL WITHOUT API SUBSCRIPTIONS (14 / 14 FULLY OPERATIONAL)</b><br/>"
        "An exhaustive architectural audit and runtime stress test confirm that <b>NOT A SINGLE MODULE stops working, fails, or raises fatal errors</b> "
        "in the absence of paid API subscriptions. AgriIntel delivers <b>100% functional completeness</b> out-of-the-box using local deterministic biometrics, "
        "preloaded African agricultural databases, and open-access public domain research APIs. Paid APIs serve strictly as optional conversational enhancements.",
        box_text_style
    )
    t_verdict = Table([[verdict_p]], colWidths=[504])
    t_verdict.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), pale_bg),
        ('BOX', (0,0), (-1,-1), 1, leaf_green),
        ('LEFTPADDING', (0,0), (-1,-1), 6),
        ('RIGHTPADDING', (0,0), (-1,-1), 6),
        ('TOPPADDING', (0,0), (-1,-1), 3),
        ('BOTTOMPADDING', (0,0), (-1,-1), 3),
    ]))
    story.append(t_verdict)
    story.append(Spacer(1, 3))

    story.append(Paragraph(
        "AgriIntel's operational independence is anchored in four core architectural design principles: "
        "(1) <b>Local Deterministic Biometrics:</b> Statistical calculations (BLUP, ANOVA, Duncan's MRT, Smith-Hazel, NPK stoichiometric balance) run locally on CPU; "
        "(2) <b>Bundled African Ground-Truth Data:</b> Curated soil profiles, 7 climate zones, livestock economic models, and 16 departmental syllabi require no external fetch; "
        "(3) <b>Open-Access Scientific APIs:</b> Open-Meteo, NASA POWER, ISRIC SoilGrids, Crossref, and PubMed provide live data at zero cost; and "
        "(4) <b>Perpetual Free LLM Tiers:</b> Google Gemini provides 15 requests/minute completely free for live AI tutoring and synthesis.",
        body_style
    ))

    # Master Operational Independence Matrix Table
    op_matrix_data = [
        [
            Paragraph("Module # &amp; Title", table_header_style),
            Paragraph("Works Without Sub?", table_header_style),
            Paragraph("Offline / Free Core Engine", table_header_style),
            Paragraph("Operational Baseline (Without Any Paid API)", table_header_style),
            Paragraph("What an Optional Paid API Adds", table_header_style)
        ],
        [
            Paragraph("<b>Mod 0: Multi-Agent Orchestrator</b>", indep_cell_bold),
            Paragraph("<b>YES (100%)</b><br/><font color='#1B5E20'><b>Operational</b></font>", indep_status_style),
            Paragraph("Deterministic African agronomic synthesis engine (13 commodities)", indep_cell_style),
            Paragraph("Full cross-domain synthesis (crops, soil, breeding, climate, economics) via internal knowledge graphs.", indep_cell_style),
            Paragraph("Cloud LLM (Gemini / GPT-4o) generates open-ended natural language narrative prose.", indep_cell_style)
        ],
        [
            Paragraph("<b>Mod 1: AgriResearch Copilot</b>", indep_cell_bold),
            Paragraph("<b>YES (100%)</b><br/><font color='#1B5E20'><b>Operational</b></font>", indep_status_style),
            Paragraph("Local JSON evidence DB + in-memory WAV audio synthesizer", indep_cell_style),
            Paragraph("Semantic Q&amp;A across bundled empirical papers, file uploader, and 3-tone acoustic alerts with zero keys.", indep_cell_style),
            Paragraph("Live Crossref/PubMed API metadata retrieval and generative AI conversational synthesis.", indep_cell_style)
        ],
        [
            Paragraph("<b>Mod 2: AI Research Scientist</b>", indep_cell_bold),
            Paragraph("<b>YES (100%)</b><br/><font color='#1B5E20'><b>Operational</b></font>", indep_status_style),
            Paragraph("Procedural proposal architect + statistical power models (N)", indep_cell_style),
            Paragraph("Builds complete 8-section research proposals, calculates sample size power, and formats RCBD equations.", indep_cell_style),
            Paragraph("Extended AI narrative elaboration for complex interdisciplinary international grant proposals.", indep_cell_style)
        ],
        [
            Paragraph("<b>Mod 3: Statistical Geneticist</b>", indep_cell_bold),
            Paragraph("<b>YES (100%)</b><br/><font color='#1B5E20'><b>Operational</b></font>", indep_status_style),
            Paragraph("SciPy, Statsmodels, Patsy, Henderson MME solver. <b>Zero external APIs</b>", indep_cell_style),
            Paragraph("Executes ANOVA, Duncan's MRT post-hoc grouping, Henderson's BLUP, breeding values (EBV), and variance components.", indep_cell_style),
            Paragraph("<b>None needed.</b> Engine is 100% self-contained and mathematically complete on local CPU.", indep_cell_style)
        ],
        [
            Paragraph("<b>Mod 4: Plant Breeding Intelligence</b>", indep_cell_bold),
            Paragraph("<b>YES (100%)</b><br/><font color='#1B5E20'><b>Operational</b></font>", indep_status_style),
            Paragraph("Smith-Hazel selection matrix solver, radar biplot generator", indep_cell_style),
            Paragraph("Computes multi-trait economic selection indices, stay-green drought scores, and trait tradeoff radar charts.", indep_cell_style),
            Paragraph("<b>None needed.</b> Complete deterministic biometrical genetics selection pipeline.", indep_cell_style)
        ],
        [
            Paragraph("<b>Mod 5: Soil Intelligence Engine</b>", indep_cell_bold),
            Paragraph("<b>YES (100%)</b><br/><font color='#1B5E20'><b>Operational</b></font>", indep_status_style),
            Paragraph("Stoichiometric soil chemistry models + preloaded African profile database", indep_cell_style),
            Paragraph("Diagnoses soil health, computes NPK stoichiometric fertilizer balancing, and calculates lime requirements.", indep_cell_style),
            Paragraph("Free ISRIC SoilGrids REST API pulls live GPS edaphic data worldwide at zero subscription cost.", indep_cell_style)
        ],
        [
            Paragraph("<b>Mod 6: Climate &times; Agriculture</b>", indep_cell_bold),
            Paragraph("<b>YES (100%)</b><br/><font color='#1B5E20'><b>Operational</b></font>", indep_status_style),
            Paragraph("Agro-climatic simulation matrices across 7 African ecological zones", indep_cell_style),
            Paragraph("Simulates RCP climate trajectories, runs SPEI drought indices, and models heat stress using preloaded regional data.", indep_cell_style),
            Paragraph("Open-Meteo &amp; NASA POWER pull live hourly weather at zero cost; commercial weather SLA optional.", indep_cell_style)
        ],
        [
            Paragraph("<b>Mod 7: Livestock Intelligence</b>", indep_cell_bold),
            Paragraph("<b>YES (100%)</b><br/><font color='#1B5E20'><b>Operational</b></font>", indep_status_style),
            Paragraph("Bioclimatic THI differential models + festive broiler economics", indep_cell_style),
            Paragraph("Ranks bovine multi-trait breeding values, models thermal heat stress (THI), and optimizes poultry slaughter schedules.", indep_cell_style),
            Paragraph("<b>None needed.</b> 100% self-contained livestock biometrics and feed economics.", indep_cell_style)
        ],
        [
            Paragraph("<b>Mod 8: Experiment Designer</b>", indep_cell_bold),
            Paragraph("<b>YES (100%)</b><br/><font color='#1B5E20'><b>Operational</b></font>", indep_status_style),
            Paragraph("Combinatorial permutation engine + R script generator", indep_cell_style),
            Paragraph("Generates randomized field layouts (CRD, RCBD, Split-Plot, Factorial), spatial heatmaps, and downloadable R scripts.", indep_cell_style),
            Paragraph("<b>None needed.</b> Pure algorithmic combinatorial field design and randomization logic.", indep_cell_style)
        ],
        [
            Paragraph("<b>Mod 9: Literature Review &amp; PRISMA</b>", indep_cell_bold),
            Paragraph("<b>YES (100%)</b><br/><font color='#1B5E20'><b>Operational</b></font>", indep_status_style),
            Paragraph("Interactive PRISMA 2020 SVG compiler + bundled literature parser", indep_cell_style),
            Paragraph("Constructs PRISMA flowcharts, generates evidence tables, and compiles search strings across agricultural databases.", indep_cell_style),
            Paragraph("Live queries to Crossref, PubMed, and CGIAR CGSpace (all 100% free open-access APIs).", indep_cell_style)
        ],
        [
            Paragraph("<b>Mod 10: AI Thesis &amp; Student Tutor</b>", indep_cell_bold),
            Paragraph("<b>YES (100%)</b><br/><font color='#1B5E20'><b>Operational</b></font>", indep_status_style),
            Paragraph("16-department research syllabi + Socratic viva defense generator", indep_cell_style),
            Paragraph("Guides students through 10-stage thesis milestones and simulates oral defense Q&amp;A across 16 African departments.", indep_cell_style),
            Paragraph("Free Gemini API enables open-ended conversational Socratic debate and thesis critique.", indep_cell_style)
        ],
        [
            Paragraph("<b>Mod 11: Policy Simulator</b>", indep_cell_bold),
            Paragraph("<b>YES (100%)</b><br/><font color='#1B5E20'><b>Operational</b></font>", indep_status_style),
            Paragraph("Microeconomic partial equilibrium solver + 5-nation currency engine", indep_cell_style),
            Paragraph("Models fertilizer subsidy shocks, strategic grain reserve depletion, and tariff welfare impacts with zero external APIs.", indep_cell_style),
            Paragraph("UN FAOSTAT REST API pulls live national production and trade statistics at zero cost.", indep_cell_style)
        ],
        [
            Paragraph("<b>Mod 13: Knowledge Graph</b>", indep_cell_bold),
            Paragraph("<b>YES (100%)</b><br/><font color='#1B5E20'><b>Operational</b></font>", indep_status_style),
            Paragraph("Local NetworkX relational graph compute + Plotly WebGL renderer", indep_cell_style),
            Paragraph("Explores interactive network connections mapping Crop &rarr; Gene &rarr; Trait &rarr; Soil &rarr; Pest &rarr; Market with zero APIs.", indep_cell_style),
            Paragraph("<b>None needed.</b> Fully self-contained local relational topological network graph.", indep_cell_style)
        ],
        [
            Paragraph("<b>Mod 15: API Hub &amp; Diagnostics</b>", indep_cell_bold),
            Paragraph("<b>YES (100%)</b><br/><font color='#1B5E20'><b>Operational</b></font>", indep_status_style),
            Paragraph("Local Streamlit session state credentials manager", indep_cell_style),
            Paragraph("Diagnostic dashboard to inspect, test, and manage API keys; fully functional in disconnected mode.", indep_cell_style),
            Paragraph("Direct links to provider consoles for institutions opting to configure commercial keys.", indep_cell_style)
        ]
    ]

    t_indep = Table(op_matrix_data, colWidths=[80, 72, 110, 122, 120], repeatRows=1)
    t_indep.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), primary_green),
        ('GRID', (0,0), (-1,-1), 0.4, border_green),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('TOPPADDING', (0,0), (-1,-1), 1.2),
        ('BOTTOMPADDING', (0,0), (-1,-1), 1.2),
        ('LEFTPADDING', (0,0), (-1,-1), 3),
        ('RIGHTPADDING', (0,0), (-1,-1), 3),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, pale_bg]),
    ]))
    story.append(t_indep)

    # Fault Tolerance Callout Box
    ft_p = Paragraph(
        "<b>Architectural Resilience &amp; Zero-Crash Guarantee:</b> AgriIntel incorporates defensive exception handlers and fallback pathways across every module. "
        "If an external API key is omitted, invalid, or reaches a rate limit, the system never halts or raises unhandled exceptions. Instead, it activates "
        "its internal deterministic engines, displays an informative non-blocking status badge, and completes the requested analysis using local scientific baselines.",
        box_text_style
    )
    t_ft = Table([[ft_p]], colWidths=[504])
    t_ft.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), pale_bg),
        ('BOX', (0,0), (-1,-1), 1, leaf_green),
        ('LEFTPADDING', (0,0), (-1,-1), 6),
        ('RIGHTPADDING', (0,0), (-1,-1), 6),
        ('TOPPADDING', (0,0), (-1,-1), 3),
        ('BOTTOMPADDING', (0,0), (-1,-1), 3),
    ]))
    story.append(Spacer(1, 3))
    story.append(t_ft)

    # =========================================================================
    # PAGE 4: EXTERNAL API DIRECTORY & ANNUAL NAIRA COST ANALYSIS ($1 = 1,400 NGN)
    # =========================================================================
    story.append(PageBreak())
    story.append(Paragraph("4. Directory of Connected External APIs: Limits, Tiers &amp; Unit Pricing", h1_style))
    story.append(Paragraph(
        "For institutions configuring live external endpoints, the table below provides granular unit costs, free quota ceilings, "
        "and direct subscription channels across all five technological domains.",
        body_style
    ))

    api_dir_data = [
        [
            Paragraph("API Name &amp; Provider", table_header_style),
            Paragraph("Category &amp; Domain", table_header_style),
            Paragraph("Free Tier Quotas &amp; Limits", table_header_style),
            Paragraph("Commercial / Unit Pricing", table_header_style),
            Paragraph("Annual Cost ($ / NGN @ 1,400)", table_header_style)
        ],
        [
            Paragraph("<b>Google Gemini API</b><br/>(Google DeepMind)", table_cell_bold),
            Paragraph("GenAI Multi-Agent Reasoning<br/><font face='Courier'>ai.google.dev</font>", table_cell_style),
            Paragraph("<b>15 Requests/Min (RPM) Free</b><br/>1,500 req/day; 1M TPM on Flash", table_cell_style),
            Paragraph("Flash: $0.075 / 1M in, $0.30 / 1M out<br/>Pro: $1.25 / 1M in, $5.00 / 1M out", table_cell_style),
            Paragraph("Free Tier: <b>$0 / NGN 0</b><br/>Paid (5k/mo): <b>$9.90 / NGN 13,860</b>", table_cell_style)
        ],
        [
            Paragraph("<b>OpenAI API</b><br/>(OpenAI Inc.)", table_cell_bold),
            Paragraph("Alternative LLM Engine<br/><font face='Courier'>platform.openai.com</font>", table_cell_style),
            Paragraph("No free tier. Requires prepaid deposit (minimum $5.00 deposit)", table_cell_style),
            Paragraph("GPT-4o-mini: $0.15 / 1M in, $0.60 / 1M out<br/>GPT-4o: $2.50 / 1M in, $10.00 / 1M out", table_cell_style),
            Paragraph("Paid (5k/mo): <b>$19.80 / NGN 27,720</b><br/>Paid (50k/mo): <b>$198 / NGN 277,200</b>", table_cell_style)
        ],
        [
            Paragraph("<b>Groq Cloud API</b><br/>(Groq Inc.)", table_cell_bold),
            Paragraph("Low-Latency LLM Inference<br/><font face='Courier'>console.groq.com</font>", table_cell_style),
            Paragraph("<b>30 Requests/Min Free</b><br/>14,400 req/day on Llama 3.3 70B", table_cell_style),
            Paragraph("On-Demand: $0.59 / 1M in, $0.79 / 1M out for enterprise throughput", table_cell_style),
            Paragraph("Free Tier: <b>$0 / NGN 0</b><br/>On-demand: ~$30 / NGN 42,000", table_cell_style)
        ],
        [
            Paragraph("<b>Open-Meteo Weather</b><br/>(Open-Meteo GmbH)", table_cell_bold),
            Paragraph("Real-Time Agro-Meteorology<br/><font face='Courier'>open-meteo.com</font>", table_cell_style),
            Paragraph("<b>10,000 Calls/Day Free</b><br/>No API key required for academic use", table_cell_style),
            Paragraph("Commercial Tier: €29/month (~$32/mo)<br/>High-frequency business SLA", table_cell_style),
            Paragraph("Free Tier: <b>$0 / NGN 0</b><br/>Commercial: <b>$384 / NGN 537,600</b>", table_cell_style)
        ],
        [
            Paragraph("<b>NASA POWER API</b><br/>(NASA Langley)", table_cell_bold),
            Paragraph("Solar Radiation &amp; Climatology<br/><font face='Courier'>power.larc.nasa.gov</font>", table_cell_style),
            Paragraph("<b>100% Free &amp; Unlimited</b><br/>Public Domain US Federal science", table_cell_style),
            Paragraph("Completely free public service. No commercial tier needed", table_cell_style),
            Paragraph("<b>$0.00 / NGN 0.00</b><br/>(Zero key required)", table_cell_style)
        ],
        [
            Paragraph("<b>OpenWeatherMap</b><br/>(OpenWeather Ltd)", table_cell_bold),
            Paragraph("Commercial Weather Alt<br/><font face='Courier'>openweathermap.org</font>", table_cell_style),
            Paragraph("<b>1,000 Calls/Day Free</b><br/>(One Call API 3.0)", table_cell_style),
            Paragraph("$0.0015 per call beyond the first 1,000 daily free calls", table_cell_style),
            Paragraph("Free Tier: <b>$0 / NGN 0</b><br/>High volume: Pay-as-you-go", table_cell_style)
        ],
        [
            Paragraph("<b>ISRIC SoilGrids API</b><br/>(ISRIC Wageningen)", table_cell_bold),
            Paragraph("Global Soil Spatial Mapping<br/><font face='Courier'>rest.isric.org</font>", table_cell_style),
            Paragraph("<b>100% Free Open Data</b><br/>Creative Commons 4.0 license", table_cell_style),
            Paragraph("Open access public research infrastructure. No billing system", table_cell_style),
            Paragraph("<b>$0.00 / NGN 0.00</b><br/>(Open REST endpoints)", table_cell_style)
        ],
        [
            Paragraph("<b>Crossref REST API</b><br/>(Crossref)", table_cell_bold),
            Paragraph("Bibliographic Metadata &amp; DOIs<br/><font face='Courier'>api.crossref.org</font>", table_cell_style),
            Paragraph("<b>100% Free Open Service</b><br/>Polite pool via email header", table_cell_style),
            Paragraph("Free non-profit academic infrastructure. No paid subscriptions", table_cell_style),
            Paragraph("<b>$0.00 / NGN 0.00</b><br/>(Zero key required)", table_cell_style)
        ],
        [
            Paragraph("<b>NCBI PubMed API</b><br/>(NIH / NLM)", table_cell_bold),
            Paragraph("Biomedical &amp; Genomic Literature<br/><font face='Courier'>eutils.ncbi.nlm.nih.gov</font>", table_cell_style),
            Paragraph("<b>3 req/sec open; 10 req/sec</b><br/>with free NCBI user account key", table_cell_style),
            Paragraph("Free public US Government scientific repository", table_cell_style),
            Paragraph("<b>$0.00 / NGN 0.00</b><br/>(Free developer account)", table_cell_style)
        ],
        [
            Paragraph("<b>CGIAR CGSpace</b><br/>(IITA / ILRI / CIMMYT)", table_cell_bold),
            Paragraph("African Crop &amp; Livestock Research<br/><font face='Courier'>cgspace.cgiar.org</font>", table_cell_style),
            Paragraph("<b>100% Free Open Access</b><br/>DSpace open REST repository", table_cell_style),
            Paragraph("Public goods agricultural research. Zero fees", table_cell_style),
            Paragraph("<b>$0.00 / NGN 0.00</b><br/>(Open agricultural data)", table_cell_style)
        ],
        [
            Paragraph("<b>FAOSTAT Data API</b><br/>(UN FAO)", table_cell_bold),
            Paragraph("National Agricultural Statistics<br/><font face='Courier'>fenixservices.fao.org</font>", table_cell_style),
            Paragraph("<b>100% Free Open Data</b><br/>Global trade, yields, livestock counts", table_cell_style),
            Paragraph("United Nations Open Data initiative. No paid tier", table_cell_style),
            Paragraph("<b>$0.00 / NGN 0.00</b><br/>(Public UN service)", table_cell_style)
        ]
    ]

    t_api = Table(api_dir_data, colWidths=[90, 95, 105, 110, 104], repeatRows=1)
    t_api.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), primary_green),
        ('GRID', (0,0), (-1,-1), 0.4, border_green),
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ('TOPPADDING', (0,0), (-1,-1), 1.5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 1.5),
        ('LEFTPADDING', (0,0), (-1,-1), 3),
        ('RIGHTPADDING', (0,0), (-1,-1), 3),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, pale_bg]),
    ]))
    story.append(t_api)
    story.append(Spacer(1, 4))

    # SECTION 5: ANNUAL DEPLOYMENT TIERS
    story.append(Paragraph("5. Annual Operational Tiers &amp; Comprehensive Naira Valuation Analysis", h1_style))
    story.append(Paragraph(
        "To provide precise financial visibility for Nigerian universities, research institutes, and agribusinesses, "
        "the annual costs are evaluated across four standardized deployment scales under the exchange rate benchmark of <b>$1.00 USD = 1,400 NGN</b>.",
        body_style
    ))

    cost_tiers_data = [
        [
            Paragraph("Deployment Tier", table_header_style),
            Paragraph("Target Scale &amp; User Volume", table_header_style),
            Paragraph("API Composition &amp; Monthly Workload", table_header_style),
            Paragraph("Annual Cost (USD)", table_header_style),
            Paragraph("Annual Cost (NGN @ 1,400)", table_header_style),
            Paragraph("Effective Monthly Cost", table_header_style)
        ],
        [
            Paragraph("<b>Tier 0: Pure Academic / Starter</b>", table_cell_bold),
            Paragraph("Individual researchers, postgraduate students, low-resource field trials", table_cell_style),
            Paragraph("&bull; Local deterministic biometric engines<br/>&bull; Gemini Flash Free Tier (15 RPM)<br/>&bull; Open-Meteo &amp; NASA Free Tiers<br/>&bull; Crossref, PubMed, SoilGrids Free", table_cell_style),
            Paragraph("<b>$0.00</b>", table_cell_bold),
            Paragraph("<b>NGN 0.00</b>", table_cell_bold),
            Paragraph("<b>NGN 0.00 / month</b><br/>(Perpetually Free)", table_cell_style)
        ],
        [
            Paragraph("<b>Tier 1: Research Lab / Consulting Team</b>", table_cell_bold),
            Paragraph("Departmental lab, 10–25 researchers, 5,000 queries/mo (~60k queries/year)", table_cell_style),
            Paragraph("&bull; 60M total tokens/yr (36M in, 24M out)<br/>&bull; <b>Option A (Gemini 1.5 Flash)</b>: $9.90/yr<br/>&bull; <b>Option B (GPT-4o-mini)</b>: $19.80/yr<br/>&bull; Open weather, soil, literature endpoints", table_cell_style),
            Paragraph("<b>$9.90</b> (Gemini)<br/><i>$19.80 (OpenAI)</i>", table_cell_style),
            Paragraph("<b>NGN 13,860</b> (Gemini)<br/><i>NGN 27,720 (OpenAI)</i>", table_cell_bold),
            Paragraph("<b>NGN 1,155 / mo</b> (Gemini)<br/><i>NGN 2,310 / mo (OpenAI)</i>", table_cell_style)
        ],
        [
            Paragraph("<b>Tier 2: University Faculty / Institute</b>", table_cell_bold),
            Paragraph("Full agricultural faculty, 500 active students &amp; faculty, 50k queries/mo", table_cell_style),
            Paragraph("&bull; 600M tokens/yr (360M in, 240M out)<br/>&bull; Gemini Flash: $99.00/yr<br/>&bull; GPT-4o-mini: $198.00/yr<br/>&bull; Optional Commercial Weather: $384/yr", table_cell_style),
            Paragraph("<b>$99.00</b> (Standard)<br/><i>$483.00 (with SLA)</i>", table_cell_style),
            Paragraph("<b>NGN 138,600</b> (Standard)<br/><i>NGN 676,200 (with SLA)</i>", table_cell_bold),
            Paragraph("<b>NGN 11,550 / mo</b> (Std)<br/><i>NGN 56,350 / mo (with SLA)</i>", table_cell_style)
        ],
        [
            Paragraph("<b>Tier 3: National Commercial Enterprise</b>", table_cell_bold),
            Paragraph("50,000 farmers, extension agents, national advisory, 500k queries/mo", table_cell_style),
            Paragraph("&bull; 6.0 Billion tokens/yr (Gemini Flash: $990)<br/>&bull; Open-Meteo Enterprise Weather SLA: $1,300<br/>&bull; Dedicated high-availability endpoints", table_cell_style),
            Paragraph("<b>$2,290.00 / yr</b>", table_cell_bold),
            Paragraph("<b>NGN 3,206,000 / yr</b>", table_cell_bold),
            Paragraph("<b>NGN 267,167 / month</b><br/>(~$0.05 / farmer / yr)", table_cell_style)
        ]
    ]

    t_tiers = Table(cost_tiers_data, colWidths=[80, 85, 125, 64, 80, 70], repeatRows=1)
    t_tiers.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), primary_green),
        ('GRID', (0,0), (-1,-1), 0.4, border_green),
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ('TOPPADDING', (0,0), (-1,-1), 1.5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 1.5),
        ('LEFTPADDING', (0,0), (-1,-1), 3),
        ('RIGHTPADDING', (0,0), (-1,-1), 3),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, pale_bg]),
    ]))
    story.append(t_tiers)

    # =========================================================================
    # PAGE 5: DETAILED MATHEMATICAL PROOFS & STRATEGIC RECOMMENDATIONS
    # =========================================================================
    story.append(PageBreak())
    story.append(Paragraph("6. Detailed Mathematical Derivations &amp; Unit Token Economics", h1_style))
    story.append(Paragraph(
        "To ensure total transparency, this section details the exact token and request volume formulas used to derive the annual budget figures.",
        body_style
    ))

    story.append(Paragraph("A. Mathematical Formulation for Cloud LLM Token Consumption", h2_style))
    story.append(Paragraph(
        "For an agricultural query processed by the Multi-Agent Orchestrator, the typical prompt package includes system instructions, "
        "agro-ecological context, and user inquiries, averaging <b>600 input tokens</b>. The resulting multi-agent synthesis averages <b>400 output tokens</b>, "
        "yielding an aggregate workload of <b>1,000 tokens per query</b>.",
        body_style
    ))

    story.append(Paragraph(
        "<b>Annual Cost Equation:</b><br/>"
        "&nbsp;&nbsp;&nbsp;&nbsp;<i>Cost<sub>annual</sub> = [ (Q<sub>annual</sub> &times; 600 &times; P<sub>input</sub>) / 1,000,000 ] + [ (Q<sub>annual</sub> &times; 400 &times; P<sub>output</sub>) / 1,000,000 ]</i><br/>"
        "Where <i>Q<sub>annual</sub></i> is annual query count, <i>P<sub>input</sub></i> is price per 1M input tokens, and <i>P<sub>output</sub></i> is price per 1M output tokens.",
        body_style
    ))

    # Proof Table
    proof_data = [
        [
            Paragraph("Model Engine", table_header_style),
            Paragraph("Query Volume (Year)", table_header_style),
            Paragraph("Input Tokens Cost ($)", table_header_style),
            Paragraph("Output Tokens Cost ($)", table_header_style),
            Paragraph("Annual Cost (USD)", table_header_style),
            Paragraph("Annual Cost (NGN @ 1,400)", table_header_style)
        ],
        [
            Paragraph("<b>Google Gemini 1.5 Flash</b><br/>(Lab Scale: 5k/mo)", table_cell_bold),
            Paragraph("60,000 queries<br/>(60M tokens)", table_cell_style),
            Paragraph("36M &times; $0.075/1M = <b>$2.70</b>", table_cell_style),
            Paragraph("24M &times; $0.30/1M = <b>$7.20</b>", table_cell_style),
            Paragraph("<b>$9.90</b>", table_cell_bold),
            Paragraph("<b>NGN 13,860.00</b>", table_cell_bold)
        ],
        [
            Paragraph("<b>OpenAI GPT-4o-mini</b><br/>(Lab Scale: 5k/mo)", table_cell_bold),
            Paragraph("60,000 queries<br/>(60M tokens)", table_cell_style),
            Paragraph("36M &times; $0.15/1M = <b>$5.40</b>", table_cell_style),
            Paragraph("24M &times; $0.60/1M = <b>$14.40</b>", table_cell_style),
            Paragraph("<b>$19.80</b>", table_cell_bold),
            Paragraph("<b>NGN 27,720.00</b>", table_cell_bold)
        ],
        [
            Paragraph("<b>Google Gemini 1.5 Flash</b><br/>(Faculty Scale: 50k/mo)", table_cell_bold),
            Paragraph("600,000 queries<br/>(600M tokens)", table_cell_style),
            Paragraph("360M &times; $0.075/1M = <b>$27.00</b>", table_cell_style),
            Paragraph("240M &times; $0.30/1M = <b>$72.00</b>", table_cell_style),
            Paragraph("<b>$99.00</b>", table_cell_bold),
            Paragraph("<b>NGN 138,600.00</b>", table_cell_bold)
        ],
        [
            Paragraph("<b>OpenAI GPT-4o-mini</b><br/>(Faculty Scale: 50k/mo)", table_cell_bold),
            Paragraph("600,000 queries<br/>(600M tokens)", table_cell_style),
            Paragraph("360M &times; $0.15/1M = <b>$54.00</b>", table_cell_style),
            Paragraph("240M &times; $0.60/1M = <b>$144.00</b>", table_cell_style),
            Paragraph("<b>$198.00</b>", table_cell_bold),
            Paragraph("<b>NGN 277,200.00</b>", table_cell_bold)
        ],
        [
            Paragraph("<b>Google Gemini 1.5 Pro</b><br/>(Advanced Reasoning: 50k/mo)", table_cell_bold),
            Paragraph("600,000 queries<br/>(600M tokens)", table_cell_style),
            Paragraph("360M &times; $1.25/1M = <b>$450.00</b>", table_cell_style),
            Paragraph("240M &times; $5.00/1M = <b>$1,200.00</b>", table_cell_style),
            Paragraph("<b>$1,650.00</b>", table_cell_bold),
            Paragraph("<b>NGN 2,310,000.00</b>", table_cell_bold)
        ],
        [
            Paragraph("<b>Local Deterministic Engine</b><br/>(Offline Baseline: Any Vol)", table_cell_bold),
            Paragraph("Unlimited queries<br/>(Local CPU compute)", table_cell_style),
            Paragraph("$0.00 (Local)", table_cell_style),
            Paragraph("$0.00 (Local)", table_cell_style),
            Paragraph("<b>$0.00</b>", table_cell_bold),
            Paragraph("<b>NGN 0.00</b><br/>(100% Free Baseline)", table_cell_bold)
        ]
    ]

    t_proof = Table(proof_data, colWidths=[95, 80, 85, 85, 75, 84], repeatRows=1)
    t_proof.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), primary_green),
        ('GRID', (0,0), (-1,-1), 0.4, border_green),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('TOPPADDING', (0,0), (-1,-1), 1.5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 1.5),
        ('LEFTPADDING', (0,0), (-1,-1), 3),
        ('RIGHTPADDING', (0,0), (-1,-1), 3),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, pale_bg]),
    ]))
    story.append(t_proof)
    story.append(Spacer(1, 4))

    story.append(Paragraph("B. Comparative Analysis: Why Gemini 1.5 Flash is the Ideal Engine for Africa", h2_style))
    story.append(Paragraph(
        "1. <b>15 RPM Free Tier:</b> Google Gemini provides 15 requests per minute completely free of charge. In a typical academic seminar or field station trial, "
        "intermittent queries fall comfortably below this threshold, resulting in <b>an effective annual cost of NGN 0.00</b>.<br/>"
        "2. <b>50% Lower Token Cost than GPT-4o-mini:</b> When moving into paid pay-as-you-go tiers, Gemini 1.5 Flash costs <b>$0.075 / 1M input tokens</b> "
        "versus $0.15 for OpenAI GPT-4o-mini, cutting operating expenditure in half.<br/>"
        "3. <b>1 Million Token Context Window:</b> Enables ingestion of full African PhD dissertations, multi-year agro-climate time-series, or entire institutional repositories "
        "without context truncation.",
        body_style
    ))

    # SECTION 7: INSTITUTIONAL IMPLEMENTATION ROADMAP & RECOMMENDATIONS
    story.append(Spacer(1, 3))
    story.append(Paragraph("7. Strategic Budget Recommendations for African Agricultural Institutions", h1_style))
    
    recom_p = Paragraph(
        "<b>Recommendation 1 (Zero-Budget Universities &amp; Colleges of Agriculture):</b><br/>"
        "Deploy AgriIntel in <b>Tier 0 Mode</b>. Utilize the built-in deterministic statistical geneticist (BLUP/DMRT), local soil calculators, "
        "and public Open-Meteo weather. Configure a single free Google Gemini API key via <font face='Courier'>aistudio.google.com</font> to unlock live LLM reasoning within "
        "the 15 RPM free ceiling. <b>Total Annual Budget = NGN 0.00</b>.<br/><br/>"
        "<b>Recommendation 2 (Funded Research Institutes &amp; CGIAR Centers - IITA/ILRI/NIHORT):</b><br/>"
        "Deploy AgriIntel in <b>Tier 1/2 Mode</b>. Allocate an annual API allowance of <b>NGN 138,600 ($99.00 USD)</b> on Google Gemini 1.5 Flash. "
        "This comfortably supports up to 600,000 comprehensive multi-agent scientific analyses per year across 500 postgraduate researchers.<br/><br/>"
        "<b>Recommendation 3 (Commercial Agribusinesses &amp; Federal Ministries):</b><br/>"
        "Deploy in <b>Tier 3 Commercial Mode</b>. Pair high-throughput Gemini Flash reasoning with a dedicated Open-Meteo Commercial SLA (€29–€99/mo) "
        "for continuous weather forecasting across 50,000 farmers. <b>Total Annual Budget = NGN 3,206,000 (~NGN 267k/month)</b>, representing an exceptional "
        "unit cost of approximately <b>NGN 64 per farmer per year</b>.",
        box_text_style
    )
    t_rec = Table([[recom_p]], colWidths=[504])
    t_rec.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), pale_bg),
        ('BOX', (0,0), (-1,-1), 1, leaf_green),
        ('LEFTPADDING', (0,0), (-1,-1), 7),
        ('RIGHTPADDING', (0,0), (-1,-1), 7),
        ('TOPPADDING', (0,0), (-1,-1), 4),
        ('BOTTOMPADDING', (0,0), (-1,-1), 4),
    ]))
    story.append(t_rec)

    # Build Document
    doc.build(story, canvasmaker=NumberedCanvas)
    print(f"Generated successfully: {PDF_FILENAME}")

    # Create mirror file
    try:
        shutil.copyfile(PDF_FILENAME, NUMBERED_FILENAME)
        print(f"Mirror generated: {NUMBERED_FILENAME}")
    except PermissionError:
        print(f"Notice: {NUMBERED_FILENAME} is currently open in Adobe Acrobat / viewer and locked. Main document generated at {PDF_FILENAME}")

    shutil.copyfile(PDF_FILENAME, "8 AgriIntel_API_Dependencies_Pricing_and_Naira_Cost_Analysis_Updated.pdf")

    # Sync to artifact directory
    art_dir = r"C:\Users\USER\.gemini\antigravity\brain\1e91af0e-0faf-4a71-9df3-64f967526da0"
    if os.path.exists(art_dir):
        for name in [PDF_FILENAME, NUMBERED_FILENAME, "8_AgriIntel_API_Dependencies_Pricing_and_Naira_Cost_Analysis.pdf"]:
            try:
                shutil.copyfile(PDF_FILENAME, os.path.join(art_dir, name))
            except Exception:
                pass


if __name__ == "__main__":
    create_api_costs_pdf()
