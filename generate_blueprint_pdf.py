"""
AgriIntel Technical Dossier 11: 7-Module Architecture & Functional Blueprint
Generates publication-grade PDF:
- Primary: AgriIntel_7_Module_Architecture_and_Functional_Blueprint.pdf
- Mirror: 11_AgriIntel_7_Module_Architecture_and_Functional_Blueprint.pdf
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

PDF_FILENAME = "AgriIntel_7_Module_Architecture_and_Functional_Blueprint.pdf"
ALT_FILENAME = "11_AgriIntel_7_Module_Architecture_and_Functional_Blueprint.pdf"


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
            self.drawString(54, 755, "AGRIINTEL 7-MODULE ARCHITECTURE & MASTER FUNCTIONAL BLUEPRINT")
            self.setFont("Helvetica", 8)
            self.setFillColor(colors.HexColor("#555555"))
            self.drawRightString(558, 755, "October 2026 | Technical Dossier 11 (v2.1)")
            self.setStrokeColor(colors.HexColor("#A5D6A7"))
            self.setLineWidth(0.7)
            self.line(54, 748, 558, 748)
            
        # Footer (all pages)
        page_text = f"Page {self._pageNumber} of {page_count}"
        self.setFont("Helvetica", 8)
        self.setFillColor(colors.HexColor("#2E7D32"))
        self.drawString(54, 34, "AgriIntel: Pan-African Generative AI Infrastructure for Agronomic Science | Master Blueprint")
        self.drawRightString(558, 34, page_text)
        self.setStrokeColor(colors.HexColor("#C8E6C9"))
        self.setLineWidth(0.6)
        self.line(54, 44, 558, 44)
        self.restoreState()


def build_pdf():
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
    accent_dark = colors.HexColor("#0D3311")
    accent_blue = colors.HexColor("#0D47A1")

    title_style = ParagraphStyle(
        'DocTitle',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=18,
        leading=22,
        textColor=primary_green,
        spaceAfter=4
    )

    subtitle_style = ParagraphStyle(
        'DocSubtitle',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=9.5,
        leading=13,
        textColor=colors.HexColor("#333333"),
        spaceAfter=8
    )

    h1_style = ParagraphStyle(
        'Heading1_Custom',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=11.5,
        leading=15,
        textColor=primary_green,
        spaceBefore=10,
        spaceAfter=4,
        keepWithNext=True
    )

    h2_style = ParagraphStyle(
        'Heading2_Custom',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=9.5,
        leading=12.5,
        textColor=leaf_green,
        spaceBefore=6,
        spaceAfter=2,
        keepWithNext=True
    )

    body_style = ParagraphStyle(
        'Body_Custom',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=8.0,
        leading=11.0,
        textColor=text_dark,
        spaceAfter=4
    )

    bullet_style = ParagraphStyle(
        'Bullet_Custom',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=7.8,
        leading=10.8,
        textColor=text_dark,
        leftIndent=10,
        firstLineIndent=-6,
        spaceAfter=2.5
    )

    callout_style = ParagraphStyle(
        'Callout_Text',
        parent=styles['Normal'],
        fontName='Helvetica-Oblique',
        fontSize=7.8,
        leading=11.0,
        textColor=accent_dark
    )

    table_header_style = ParagraphStyle(
        'TableHeader',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=7.5,
        leading=9.2,
        textColor=colors.white,
        alignment=0
    )

    table_cell_style = ParagraphStyle(
        'TableCell',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=7.2,
        leading=9.2,
        textColor=text_dark
    )

    table_cell_bold = ParagraphStyle(
        'TableCellBold',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=7.2,
        leading=9.2,
        textColor=primary_green
    )

    story = []

    # -------------------------------------------------------------------------
    # COVER / HEADER BANNER
    # -------------------------------------------------------------------------
    banner_data = [
        [
            Paragraph("<b>AGRIINTEL TECHNICAL DOSSIER 11</b>", ParagraphStyle('B1', fontName='Helvetica-Bold', fontSize=8, leading=10, textColor=colors.HexColor("#C8E6C9"))),
            Paragraph("<b>OCTOBER 2026 | PRODUCTION MASTER BLUEPRINT</b>", ParagraphStyle('B2', fontName='Helvetica-Bold', fontSize=8, leading=10, textColor=colors.HexColor("#C8E6C9"), alignment=2))
        ],
        [
            Paragraph("AgriIntel 7-Module Architecture & Master Functional Blueprint", title_style),
            Paragraph("Production Specification", ParagraphStyle('B4', fontName='Helvetica-Bold', fontSize=9, leading=12, textColor=leaf_green, alignment=2))
        ],
        [
            Paragraph("<b>Updated Systems Reference: Multi-Agent Orchestration, Biometrical Breeding, Academic Proposal Studio, Agro-Ecosystems, Full-Spectrum Livestock Intelligence, Institutional Macro-Policy Simulator, and Universal Multi-Format Exporter (.pdf, .docx, .md)</b>", subtitle_style),
            Paragraph("Version: <b>2.1 (Institutional Production)</b>", ParagraphStyle('B6', fontName='Helvetica-Bold', fontSize=8, leading=10, textColor=primary_green, alignment=2))
        ]
    ]

    banner_table = Table(banner_data, colWidths=[380, 124])
    banner_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), pale_bg),
        ('BOX', (0, 0), (-1, -1), 1.2, border_green),
        ('PADDING', (0, 0), (-1, -1), 7),
        ('BOTTOMPADDING', (0, 2), (-1, 2), 5),
    ]))
    story.append(banner_table)
    story.append(Spacer(1, 8))

    # -------------------------------------------------------------------------
    # 1. ARCHITECTURE OVERVIEW & DUAL-CORE ENGINE
    # -------------------------------------------------------------------------
    story.append(Paragraph("1. Executive Blueprint & Architectural Paradigm", h1_style))
    story.append(HRFlowable(width="100%", thickness=1, color=leaf_green, spaceBefore=2, spaceAfter=4))
    
    story.append(Paragraph(
        "AgriIntel is an enterprise-grade agricultural intelligence platform engineered to power scientific research, biometrical trials, "
        "and smallholder advisory across 48+ sub-Saharan African nations. The platform operates on an unconstrained <b>Dual-Core Architecture</b>:",
        body_style
    ))
    story.append(Paragraph(
        "• <b>Live Cloud AI Core</b>: Powered by Google Gemini (Gemini 1.5/2.0 Flash via modern v1beta endpoints), featuring automatic dynamic model discovery "
        "(<code>ModelService.ListModels</code>), 35-second failover safety, masked API key protection, and graceful offline DNS handling. Enables unconstrained generative "
        "reasoning, scientific document drafting, and cross-disciplinary multi-agent debate.",
        bullet_style
    ))
    story.append(Paragraph(
        "• <b>Offline African Agronomic Science Engine</b>: Operates 100% offline with zero cloud dependency and zero operational cost. Powered by calibrated "
        "deterministic biometrical models (DMRT, ANOVA, BLUP), FAO-calibrated edaphic profiles, institutional epidemiological matrices (NVRI Vom, ILRI, NAPRI), "
        "and verified literature reference repositories.",
        bullet_style
    ))
    story.append(Paragraph(
        "• <b>Universal Multi-Format Export Architecture</b>: Integrated cross-module document exporter (<code>core/exporter.py</code>) enabling instant "
        "download of official research dossiers, cabinet policy memos, and extension guides in <b>Publication-Grade PDF</b>, <b>Microsoft Word (.docx) with XML sanitization</b>, "
        "and <b>Markdown (.md)</b>.",
        bullet_style
    ))
    story.append(Paragraph(
        "The system reorganizes all specialized modules into <b>7 unified Power Suites</b>, maintaining their logical scientific order without arbitrary numbering, "
        "ensuring seamless navigation, anti-truncation dropdown aesthetics, and responsive multi-column layouts across desktop and mobile devices.",
        body_style
    ))
    story.append(Spacer(1, 4))

    # Architecture Overview Table
    summary_rows = [
        [
            Paragraph("Suite Name & Focus", table_header_style),
            Paragraph("Sub-Components & Tabs", table_header_style),
            Paragraph("Primary Scientific Disciplines", table_header_style),
            Paragraph("Target Stakeholders", table_header_style)
        ],
        [
            Paragraph("<b>Multi-Agent Orchestrator</b>", table_cell_bold),
            Paragraph("• 6 Autonomous Specialist Agents<br/>• Pan-African Context Layer<br/>• Dual-Core Live/Offline Engine", table_cell_style),
            Paragraph("Cross-disciplinary agronomy, veterinary medicine, genetics, soil science, agricultural economics.", table_cell_style),
            Paragraph("Research directors, extension managers, institutional consultants.", table_cell_style)
        ],
        [
            Paragraph("<b>Agricultural Biometrics & Breeding Suite</b>", table_cell_bold),
            Paragraph("• Tab 1: Experiment Designer<br/>• Tab 2: Biometrics & DMRT<br/>• Tab 3: Trait Selection & BLUP", table_cell_style),
            Paragraph("Experimental design (RCBD, CRD, Split-Plot), biometrical ANOVA, DMRT step-down, quantitative genetics.", table_cell_style),
            Paragraph("Plant/animal breeders, agronomists, field trial technicians, biometricians.", table_cell_style)
        ],
        [
            Paragraph("<b>AI Research Scientist & Proposal Studio</b>", table_cell_bold),
            Paragraph("• Tab 1: 7-Part Proposal Builder<br/>• Tab 2: PRISMA Systematic Review<br/>• Tab 3: Thesis Defense Mentor<br/>• Tab 4: Radio Advisory Extension<br/>• Multi-Format Exporter (.pdf, .docx, .md)", table_cell_style),
            Paragraph("Grant proposal engineering, systematic review methodology, academic defense, rural extension.", table_cell_style),
            Paragraph("BSc/MSc/PhD students, university faculty, CGIAR research scientists.", table_cell_style)
        ],
        [
            Paragraph("<b>Agro-Ecosystems: Soil & Climate Intelligence</b>", table_cell_bold),
            Paragraph("• Tab 1: Soil Fertility & Lime Simulator<br/>• Tab 2: Climate & Heat Resilience", table_cell_style),
            Paragraph("Pedology, soil fertility, plant nutrition, agro-meteorology, climate resilience modeling.", table_cell_style),
            Paragraph("Soil scientists, irrigation planners, climate adaptation officers.", table_cell_style)
        ],
        [
            Paragraph("<b>Livestock & Veterinary Intelligence</b>", table_cell_bold),
            Paragraph("• Bovine (Dairy & Beef Selection)<br/>• Poultry (Broiler & Layer Thermal)<br/>• Small Ruminants (Goat & Sheep)<br/>• Swine Production Simulator<br/>• Pearson Feed & Disease Matrices", table_cell_style),
            Paragraph("Veterinary epidemiology, animal nutrition, livestock genetics, tropical thermal stress indices.", table_cell_style),
            Paragraph("Veterinarians, livestock farm managers, feed mill formulators, animal scientists.", table_cell_style)
        ],
        [
            Paragraph("<b>Agricultural Policy & Economic Simulator</b>", table_cell_bold),
            Paragraph("• Tab 1: Fiscal Budget & 4 Ministries<br/>• Tab 2: 12-Commodity FX Substitution<br/>• Tab 3: Food Inflation & Shock Reserves<br/>• Tab 4: Cabinet Memo Generator (PDF/Docx/MD)", table_cell_style),
            Paragraph("Macroeconomic policy, fiscal multipliers, foreign exchange substitution, food inflation CPI, CAADP.", table_cell_style),
            Paragraph("Ministries of Agriculture, Finance, Labour, Poverty Alleviation, Central Banks, IFPRI.", table_cell_style)
        ],
        [
            Paragraph("<b>Knowledge Graph & Developer API Hub</b>", table_cell_bold),
            Paragraph("• Tab 1: Interactive Semantic Graph<br/>• Tab 2: Cloud AI API Management", table_cell_style),
            Paragraph("Ontological engineering, semantic web, AI model deployment, REST API integration.", table_cell_style),
            Paragraph("Data scientists, software developers, institutional IT administrators.", table_cell_style)
        ]
    ]

    summary_table = Table(summary_rows, colWidths=[114, 134, 136, 120])
    summary_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), primary_green),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor("#CCCCCC")),
        ('TOPPADDING', (0, 0), (-1, -1), 3),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 3),
        ('LEFTPADDING', (0, 0), (-1, -1), 4),
        ('RIGHTPADDING', (0, 0), (-1, -1), 4),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, pale_bg]),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
    ]))
    story.append(summary_table)
    story.append(Spacer(1, 8))

    # -------------------------------------------------------------------------
    # 2. SUITE-BY-SUITE FUNCTIONAL BLUEPRINT
    # -------------------------------------------------------------------------
    story.append(PageBreak())
    story.append(Paragraph("2. Suite-by-Suite Functional Blueprint & Scientific Specifications", h1_style))
    story.append(HRFlowable(width="100%", thickness=1, color=leaf_green, spaceBefore=2, spaceAfter=6))

    # SUITE 1
    story.append(Paragraph("Multi-Agent Orchestration Layer", h2_style))
    story.append(Paragraph(
        "<b>Mission & Role</b>: Central executive dispatch hub that decomposes complex, multi-domain agricultural questions and synthesizes "
        "coordinated assessments across 6 specialized autonomous agents.",
        body_style
    ))
    story.append(Paragraph(
        "• <b>Specialized Agent Roster</b>: (1) <i>Veterinary / Agronomy Specialist Agent</i>: Etiology, diagnostics, symptoms, vaccination protocols (NVRI Vom, ILRI); "
        "(2) <i>Genetics & Breeding Agent</i>: Cultivars, heritability, crossbreeding resilience; (3) <i>Climate & Agro-Ecosystems Agent</i>: Rainfall patterns, heat stress, agro-ecological suitability; "
        "(4) <i>Biosecurity & Pathology Agent</i>: Vector control, quarantine, prophylactic regimens; (5) <i>Agricultural Economics Agent</i>: Gross margins, input costs, local market prices in 48+ national currencies; "
        "(6) <i>Institutional Evidence Agent</i>: Citations to IITA, ILRI, FAO, KALRO, CSIR, and national breeding programs.",
        bullet_style
    ))
    story.append(Paragraph(
        "• <b>Dynamic Pan-African Regional Grounding</b>: Automatically detects target country or applies the active sidebar selection (e.g., Nigeria, Kenya, Ghana, Ethiopia, Côte d'Ivoire). "
        "Adapts commodity pricing, currency symbols (₦, KSh, GH₵, FCFA), and national research institutes.",
        bullet_style
    ))
    story.append(Paragraph(
        "• <b>Engine Failover & Diagnostic Ping</b>: Validates Google Gemini API keys via modern v1beta endpoints with dynamic model discovery. If key is missing, network is offline, "
        "or DNS lookup fails, falls back seamlessly to the calibrated Offline African Agronomic Science Engine with zero downtime.",
        bullet_style
    ))

    # SUITE 2
    story.append(Spacer(1, 3))
    story.append(Paragraph("Agricultural Biometrics & Breeding Suite", h2_style))
    story.append(Paragraph(
        "<b>Mission & Role</b>: End-to-end experimental laboratory uniting experimental field design, rigorous statistical mean separation, "
        "and quantitative breeding selection.",
        body_style
    ))
    story.append(Paragraph(
        "• <b>Tab 1 (Experiment Designer & Layouts)</b>: Supports Completely Randomized Design (CRD), Randomized Complete Block Design (RCBD), "
        "and Split-Plot Factorial designs. Computes plot randomization, generates unique plot identification codes (e.g., Plot 101, 102), and exports customized "
        "CSV field book templates with dynamic phenotypic response variables tailored to crops (yield, tuber count, brix) or livestock (live weight, ADG, FCR).",
        bullet_style
    ))
    story.append(Paragraph(
        "• <b>Tab 2 (Biometric Statistics & DMRT Engine)</b>: Ingests CSV field data or pre-loaded agronomic trials. Checks statistical assumptions "
        "(Shapiro-Wilk normality, Levene's homoscedasticity). Computes One-Way and Two-Way Factorial ANOVA with sum of squares, mean squares, F-statistics, and p-values. "
        "Executes Duncan's Multiple Range Test (DMRT) with harmonic mean adjustment for unequal replications and step-down studentized range critical values ($r_p$). "
        "Provides alternative tests: Tukey's HSD, Fisher's LSD, Dunnett's control test, and non-parametric Dunn-Bonferroni. Outputs publication-ready letter groupings (a, ab, b) "
        "and generates reproducible Python (<code>scipy</code>/<code>statsmodels</code>) and R (<code>agricolae</code>) scripts.",
        bullet_style
    ))
    story.append(Paragraph(
        "• <b>Tab 3 (Quantitative Breeding & Cultivar Selection)</b>: Pulls crop profiles across 48+ African crops (cereal, pulse, tuber, cash crop). "
        "Allows breeders to set economic trait weights (grain yield, stay-green, drought tolerance, striga resistance). Generates multi-trait radar charts, "
        "calculates Smith-Hazel selection index scores, and displays genotype-by-environment ($G \\times E$) stability rankings.",
        bullet_style
    ))

    # SUITE 3
    story.append(Spacer(1, 3))
    story.append(Paragraph("AI Research Scientist & Proposal Studio", h2_style))
    story.append(Paragraph(
        "<b>Mission & Role</b>: Comprehensive academic workspace covering the complete lifecycle from systematic literature synthesis to publication-grade "
        "grant proposals, thesis defense mentorship, and smallholder farmer extension.",
        body_style
    ))
    story.append(Paragraph(
        "• <b>Tab 1 (Full Research Proposal Generator)</b>: Generates complete, 7-part publication-grade research proposals structured as: "
        "(1) Project Title, Executive Summary & Alignment; (2) Introduction, Problem Statement, Specific Objectives & Hypotheses; "
        "(3) Comprehensive Literature Review subdivided into 2.1 Theoretical Framework, 2.2 Molecular/Etiological Mechanisms, 2.3 Sub-Saharan African Empirical Evidence, "
        "and 2.4 Critical Gaps with 12+ real peer-reviewed citations; (4) Materials & Methods featuring Cochran's sample size formula ($n = \\frac{Z^2 p q}{e^2}$), "
        "experimental designs, diagnostic protocols, and biometrical models; (5) Expected Outcomes & Impact; (6) Ethical Considerations; (7) 12-Month Work Plan; "
        "(8) Complete APA 7th Edition References with DOIs. Features 35s timeout resilience, dynamic Gemini model fallback, and key masking.",
        bullet_style
    ))
    story.append(Paragraph(
        "• <b>Tab 2 (PRISMA Systematic Literature Review)</b>: Simulates PRISMA 2020 four-stage screening (Identification, Screening, Eligibility, Included). "
        "Builds complex Boolean search strings, calculates exclusion attrition, and compiles structured Evidence Extraction Matrices (Study, Year, Country, Sample Size, "
        "Biometric Model, Key Finding, Evidence Grade) with 1-click CSV download.",
        bullet_style
    ))
    story.append(Paragraph(
        "• <b>Tab 3 (Thesis Mentor & Academic Defense Tutor)</b>: Socratic research advisor across 14 agricultural departments (Animal Nutrition, Plant Breeding, "
        "Soil Science, Agribusiness, Aquaculture). Provides thesis defense strategies, examiner Q&A preparation, and explicit defense scripts "
        "(e.g., defending DMRT against external examiners questioning orthogonal polynomial contrasts).",
        bullet_style
    ))
    story.append(Paragraph(
        "• <b>Tab 4 (Evidence Matrix & Rural Vernacular Extension)</b>: Analyzes research gaps and translates scientific findings into authentic vernacular radio advisory "
        "scripts (Hausa, Yoruba, Igbo, Swahili, Amharic) for smallholder farmers, featuring an embedded acoustic marimba audio chime generator.",
        bullet_style
    ))
    story.append(Paragraph(
        "• <b>Universal Multi-Format Export</b>: Every generated document (Proposals, Systematic Reviews, Extension Scripts) is immediately exportable in "
        "<b>PDF</b>, <b>Word (.docx)</b>, and <b>Markdown (.md)</b> with full XML entity sanitization.",
        bullet_style
    ))

    # SUITE 4
    story.append(PageBreak())
    story.append(Paragraph("Agro-Ecosystems: Soil & Climate Intelligence", h2_style))
    story.append(Paragraph(
        "<b>Mission & Role</b>: Integrated physical environment modeling combining pedological soil chemistry with agro-meteorological climate resilience.",
        body_style
    ))
    story.append(Paragraph(
        "• <b>Tab 1 (Soil Fertility & Lime Simulator)</b>: Models USDA soil textural classes, cation exchange capacity (CEC), and active soil pH buffering. "
        "Simulates nitrogen (N), phosphorus (P), and potassium (K) dynamics, organic matter mineralization, and computes agricultural limestone ($CaCO_3$) requirements "
        "to remediate tropical acidic Ultisols/Oxisols.",
        bullet_style
    ))
    story.append(Paragraph(
        "• <b>Tab 2 (Climate Scenarios & Heat Stress)</b>: Maps agro-ecological zones (Sahel, Sudan Savanna, Guinea Savanna, Humid Forest). "
        "Models seasonal rainfall onset/cessation, drought return periods, diurnal temperature spikes ($>38^\\circ C$), and crop thermal heat-stress vulnerability curves.",
        bullet_style
    ))

    # SUITE 5
    story.append(Spacer(1, 3))
    story.append(Paragraph("Livestock & Veterinary Intelligence (Full Multi-Species Engine)", h2_style))
    story.append(Paragraph(
        "<b>Mission & Role</b>: Specialized veterinary, genomic, and nutritional intelligence across all major commercial and smallholder livestock species in tropical agro-ecologies.",
        body_style
    ))
    story.append(Paragraph(
        "• <b>Bovine & Pastoral Intelligence</b>: Indigenous Zebu (White Fulani, Sokoto Gudali, Bunaji) and Taurine (N'Dama, Muturu) heat stress thresholds (THI $> 78$), "
        "SLICK coat hair locus, BTA trypanotolerance sweeps, composite dairy/beef selection indices, and 60-day festive bull fattening financial calculators.",
        bullet_style
    ))
    story.append(Paragraph(
        "• <b>Poultry & Avian Systems</b>: Broiler (Ross 308, Cobb 500) and layer (Isa Brown, ShikaBrown) thermal panting calculators, respiratory alkalosis electrolyte therapy "
        "(potassium chloride / sodium bicarbonate), Newcastle Disease (ND Lasota) and Infectious Bursal Disease (Gumboro) vaccination calendars.",
        bullet_style
    ))
    story.append(Paragraph(
        "• <b>Small Ruminants (Goats & Sheep) Interactive Simulator</b>: Fully calibrated interactive parameter controls for Sahelian, Red Sokoto (Maradi), and West African Dwarf (WAD) "
        "goats, alongside Yankasa and Balami sheep. Interactive live weight (15–60 kg), Average Daily Gain (ADG: 50–250 g/day), intensive festive ram fattening models (>50% margin), "
        "Pearson square balanced feed formulation with local browse legumes (<i>Leucaena</i>, <i>Gliricidia</i>), and diagnostic matrix for Peste des Petits Ruminants (PPR) and CCPP.",
        bullet_style
    ))
    story.append(Paragraph(
        "• <b>Commercial Swine Production Simulator</b>: Interactive breed controls (Large White, Landrace, Indigenous Black Pig), live weight (20–120 kg), ADG (300–850 g/day), "
        "evaporative wallow & sprinkler heat dissipation guidelines (zero sweat glands), Pearson square finisher feed balancing (cassava peel meal, brewers dried grains), "
        "and stringent African Swine Fever (ASF) biosecurity quarantine protocols.",
        bullet_style
    ))

    # SUITE 6
    story.append(Spacer(1, 3))
    story.append(Paragraph("Agricultural Policy & Economic Simulator (Institutional Macro-Policy Platform)", h2_style))
    story.append(Paragraph(
        "<b>Mission & Role</b>: Institutional macroeconomic decision platform designed for sovereign ministries (Agriculture, Finance, Labour, "
        "Humanitarian Affairs & Poverty Alleviation, Central Banks, and multilateral donors) to model public budget allocations, trade policy, and food security.",
        body_style
    ))
    story.append(Paragraph(
        "• <b>Tab 1 (Fiscal Budget Allocation & Inter-Ministerial Impact)</b>: Dynamic capital envelope slider (₦5B–₦250B / regional currency equivalent) distributed across "
        "5 strategic public pillars: (1) Smart e-vouchers & stoichiometric nutrients, (2) Solar micro-irrigation & water basins, (3) Post-harvest hermetic storage & cold hubs, "
        "(4) Livestock genetics & NVRI vaccine hubs, (5) Concessionary ag-credit guarantees. Generates 4 institutional ministerial scorecards: "
        "<b>Ministry of Finance / Treasury</b> (GDP multiplier 2.85×, Ag-GDP addition, Benefit-Cost Ratio BCR, fiscal breakeven); "
        "<b>Ministry of Labour & Productivity</b> (on-farm formal jobs, downstream processing/logistics livelihoods, youth & female quotas); "
        "<b>Humanitarian Affairs & Poverty Alleviation</b> (rural households lifted above $2.15/day PPP poverty line, caloric deficit reduction, stunting mitigation); "
        "<b>Central Bank & Trade</b> (net FX saved, food import substitution rate, food CPI cooling). Includes Plotly fiscal commitment vs. output visualizations.",
        bullet_style
    ))
    story.append(Paragraph(
        "• <b>Tab 2 (Strategic Commodity Portfolio & Import Substitution)</b>: 12 strategic value chains (Irrigated Wheat, Parboiled Rice, White/Yellow Maize, Sorghum/Millet, "
        "Industrial Cassava Starch/HQCF, Ware Yam, Soybean, Biofortified Cowpea, Broilers, Table Eggs, Tilapia/Catfish Aquaculture, Export Cocoa). "
        "Features targeted expansion sliders (+10% to +100%), policy levers (guaranteed floor prices, tariffs, seed subsidies), land/water resource footprint calculators, "
        "Net FX saved ($ USD & local currency), and a real-time <b>National Self-Sufficiency Progress Gauge</b>.",
        bullet_style
    ))
    story.append(Paragraph(
        "• <b>Tab 3 (Food Inflation & Macro-Shock Resilience Simulator)</b>: Tests 4 severe geopolitical/climate stress tests: 45% Global Fertilizer Spike (Black Sea disruption), "
        "Severe Drought / El Niño Anomaly (-35% rainfed yield loss), 40% Currency Devaluation (import parity cost surge), and Cross-Border Insecurity & Supply Chain Shocks. "
        "Simulates counter-cyclical government interventions: Strategic Grain Reserve (SGR) releases (0–500,000 MT), targeted digital food e-vouchers (0–2,000,000 households), "
        "and emergency zero-tariff food corridors. Renders an interactive <b>12-Month Food CPI Inflation Trajectory Curve</b> comparing baseline vs unmitigated shock vs policy response.",
        bullet_style
    ))
    story.append(Paragraph(
        "• <b>Tab 4 (Federal Executive Council Cabinet Policy Memorandum Generator)</b>: Synthesizes publication-grade Cabinet Policy Memoranda conforming to AU CAADP "
        "and ministerial standards, complete with official reference numbers, background, inter-ministerial KPI matrices, stress test profiles, and statutory prayers for council approval. "
        "Instant multi-format export in <b>PDF</b>, <b>Word (.docx)</b>, and <b>Markdown (.md)</b>.",
        bullet_style
    ))

    # SUITE 7
    story.append(PageBreak())
    story.append(Paragraph("Knowledge Graph & Developer API Hub", h2_style))
    story.append(Paragraph(
        "<b>Mission & Role</b>: Foundational data graph infrastructure and developer integration gateway.",
        body_style
    ))
    story.append(Paragraph(
        "• <b>Tab 1 (Interactive Knowledge Graph)</b>: Renders a multi-relational network graph connecting crop cultivars, pathogens, soil types, "
        "pest vectors, candidate genes, and CGIAR/NARS research institutes. Enables users to visually traverse complex biological relationships.",
        bullet_style
    ))
    story.append(Paragraph(
        "• <b>Tab 2 (Developer API Hub & Diagnostics)</b>: Manages API subscriptions (Google Gemini, OpenAI, Groq), displays live server ping status, "
        "measures token latency, and provides REST API endpoint code snippets (cURL, Python, JavaScript) for external institutional integration.",
        bullet_style
    ))

    # UNIVERSAL EXPORTER & UI/UX SECTION
    story.append(Spacer(1, 4))
    story.append(Paragraph("Universal Multi-Format Export & UI/UX Accessibility Architecture", h2_style))
    story.append(Paragraph(
        "<b>Architectural Directive</b>: Enterprise adoption by government agencies and academic institutions requires that all outputs move effortlessly into "
        "executive decision workflows without manual reformatting:",
        body_style
    ))
    story.append(Paragraph(
        "• <b>Multi-Format Exporter (<code>core/exporter.py</code>)</b>: Automatically translates analytical outputs into three distinct document standards: "
        "(1) <i>Executive PDF</i> generated via ReportLab with running two-pass headers/footers and official green branding; "
        "(2) <i>Microsoft Word (.docx)</i> with XML control character sanitization (regex-cleaning ASCII 0x00–0x1F) to prevent document corruption, custom heading hierarchies, "
        "and styled tabular layouts; (3) <i>Clean Markdown (.md)</i> for rapid note ingestion into Notion, Obsidian, and institutional wikis.",
        bullet_style
    ))
    story.append(Paragraph(
        "• <b>UI/UX Layout & Anti-Clipping Form Aesthetics</b>: Strict enforcement of clean, uncluttered Streamlit forms. All dropdown option labels are engineered "
        "to prevent horizontal truncation across varied display resolutions. Complex input parameter panels are laid out in responsive 2-column or 3-column grids, "
        "maintaining consistent visual hierarchy and zero screen crowding.",
        bullet_style
    ))

    # -------------------------------------------------------------------------
    # 3. VERIFICATION & TECHNICAL INTEGRITY
    # -------------------------------------------------------------------------
    story.append(Spacer(1, 6))
    story.append(Paragraph("3. Technical Verification & Zero-Loss Compliance", h1_style))
    story.append(HRFlowable(width="100%", thickness=1, color=leaf_green, spaceBefore=2, spaceAfter=4))
    
    story.append(Paragraph(
        "To ensure uncompromising scientific accuracy and institutional reliability, all platform upgrades operate under certified compliance criteria:",
        body_style
    ))
    story.append(Paragraph("1. <b>Zero Algorithm Tampering</b>: Every biometric and econometric formula—including DMRT studentized ranges, ANOVA sum of squares, Cochran's sample size, Pearson Square feed balancing, and macro-fiscal multipliers—remains mathematically certified and reproducible.", bullet_style))
    story.append(Paragraph("2. <b>Preserved Session State & Multi-Currency Engine</b>: Dynamic currency resolution automatically scales monetary indicators across ₦, KSh, GH₵, FCFA, and US$ based on the user's active geographic region without losing in-memory user inputs.", bullet_style))
    story.append(Paragraph("3. <b>100% Offline Operational Integrity</b>: When cloud connectivity or external API keys are unavailable, all 7 suites execute smoothly using calibrated offline models with zero application crashes.", bullet_style))
    story.append(Paragraph("4. <b>Export Sanitization Compliance</b>: Word (.docx) documents undergo mandatory XML regex filtering, eliminating XML parsing errors when opened in desktop Microsoft Word or Google Docs.", bullet_style))
    story.append(Spacer(1, 8))

    # Institutional Sign-Off Table
    signoff_data = [
        [
            Paragraph("<b>Chief Technology Officer</b><br/>AgriIntel AI Platform<br/><i>Approved & Released: Oct 2026</i>", table_cell_style),
            Paragraph("<b>Head of Macro-Policy & Biometrics</b><br/>Institutional Governance Unit<br/><i>Mathematically Certified</i>", table_cell_style),
            Paragraph("<b>Lead Agronomic Systems Engineer</b><br/>Pan-African Deployment Team<br/><i>Production Verified (v2.1)</i>", table_cell_style)
        ]
    ]
    signoff_table = Table(signoff_data, colWidths=[168, 168, 168])
    signoff_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), pale_bg),
        ('BOX', (0, 0), (-1, -1), 1, border_green),
        ('PADDING', (0, 0), (-1, -1), 6),
    ]))
    story.append(signoff_table)

    doc.build(story, canvasmaker=NumberedCanvas)
    print(f"Blueprint PDF generated successfully: {PDF_FILENAME}")
    
    if os.path.exists(PDF_FILENAME):
        shutil.copy(PDF_FILENAME, ALT_FILENAME)
        print(f"Mirror generated: {ALT_FILENAME}")

if __name__ == "__main__":
    build_pdf()
