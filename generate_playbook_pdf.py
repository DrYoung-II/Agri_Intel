"""
Script to generate AgroBiometrix Institutional Pitch & Live Demo Playbook PDF.
A comprehensive, publication-grade executive field manual for pitching and demonstrating
AgroBiometrix to CGIAR Centers, NARS Institutes, Universities, and Ministries.
"""

import os
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, HRFlowable, KeepTogether
)
from reportlab.pdfgen import canvas

PDF_FILENAME = "AgroBiometrix_Institutional_Pitch_and_Live_Demo_Playbook.pdf"


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
        self.setFont("Helvetica-Bold", 8)
        self.setFillColor(colors.HexColor("#1B5E20"))

        # Header (pages > 1)
        if self._pageNumber > 1:
            self.drawString(54, 755, "AgroBiometrix: Institutional Pitch & Live Demo Playbook")
            self.setFont("Helvetica", 8)
            self.setFillColor(colors.HexColor("#2E7D32"))
            self.drawRightString(558, 755, "Executive Field Manual • Africa-First Infrastructure")
            self.setStrokeColor(colors.HexColor("#C8E6C9"))
            self.setLineWidth(0.6)
            self.line(54, 748, 558, 748)

        # Footer (all pages)
        self.setFont("Helvetica", 8)
        self.setFillColor(colors.HexColor("#546E7A"))
        page_text = f"Page {self._pageNumber} of {page_count}"
        self.drawString(54, 34, "AgroBiometrix: The Generative Intelligence Platform for Resilient Agriculture (agrobiometrix.streamlit.app)")
        self.drawRightString(558, 34, page_text)
        self.setStrokeColor(colors.HexColor("#C8E6C9"))
        self.setLineWidth(0.6)
        self.line(54, 44, 558, 44)
        self.restoreState()


def build_playbook_pdf():
    doc = SimpleDocTemplate(
        PDF_FILENAME,
        pagesize=letter,
        leftMargin=54,
        rightMargin=54,
        topMargin=54,
        bottomMargin=54
    )

    styles = getSampleStyleSheet()

    # Custom Typography Styles
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
        fontName='Helvetica-Bold',
        fontSize=10.5,
        leading=14.5,
        textColor=colors.HexColor("#2E7D32"),
        spaceAfter=10
    )

    h1_style = ParagraphStyle(
        'Heading1_Custom',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=13,
        leading=17,
        textColor=colors.HexColor("#1B5E20"),
        spaceBefore=14,
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
        spaceBefore=9,
        spaceAfter=4,
        keepWithNext=True
    )

    body_style = ParagraphStyle(
        'Body_Custom',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=8.5,
        leading=12.2,
        textColor=colors.HexColor("#263238"),
        spaceAfter=5
    )

    body_bold = ParagraphStyle(
        'Body_Bold',
        parent=body_style,
        fontName='Helvetica-Bold'
    )

    quote_style = ParagraphStyle(
        'PitchQuote',
        parent=styles['Normal'],
        fontName='Helvetica-Oblique',
        fontSize=9,
        leading=13.5,
        textColor=colors.HexColor("#1B5E20")
    )

    callout_style = ParagraphStyle(
        'CalloutText',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=8.5,
        leading=12.5,
        textColor=colors.HexColor("#1B3B1D")
    )

    table_cell = ParagraphStyle(
        'TableCell',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=7.8,
        leading=10.5,
        textColor=colors.HexColor("#263238")
    )

    table_cell_bold = ParagraphStyle(
        'TableCellBold',
        parent=table_cell,
        fontName='Helvetica-Bold',
        textColor=colors.HexColor("#1B5E20")
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

    # =========================================================
    # TITLE & EXECUTIVE BANNER
    # =========================================================
    elements.append(Paragraph("AgroBiometrix: Institutional Pitch & Live Demo Playbook", title_style))
    elements.append(Paragraph("Executive Field Manual for Demonstrating & Pitching AgroBiometrix to CGIAR Centers, NARS Institutes, University Agriculture Faculties, and Pan-African Ministries", subtitle_style))
    elements.append(HRFlowable(width="100%", thickness=1.5, color=colors.HexColor("#1B5E20"), spaceBefore=2, spaceAfter=8))

    banner_text = (
        "<b>Executive Purpose:</b> This playbook equips AgroBiometrix founders, scientists, and presentation teams with a rigorous, "
        "step-by-step master strategy to engage high-level agricultural stakeholders. It provides the exact 90-second spoken opening hook, "
        "a scripted 7-minute live web application walkthrough, an institutional stakeholder mapping matrix, defensive answers to tough "
        "technical critiques (hallucinations, rural connectivity, mathematical rigor), and a concrete 90-day pilot proposal closing structure."
    )
    banner_table = Table([[Paragraph(banner_text, callout_style)]], colWidths=[504])
    banner_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor("#E8F5E9")),
        ('BORDER', (0, 0), (-1, -1), 1, colors.HexColor("#81C784")),
        ('PADDING', (0, 0), (-1, -1), 8),
    ]))
    elements.append(banner_table)
    elements.append(Spacer(1, 10))

    # =========================================================
    # SECTION 1: MASTER STAKEHOLDER MAPPING MATRIX
    # =========================================================
    elements.append(Paragraph("1. Master Stakeholder Mapping Matrix", h1_style))
    elements.append(Paragraph(
        "Institutional decision-makers have fundamentally divergent mandates. Never deliver a generic presentation; customize your emphasis based on this strategic alignment matrix:",
        body_style
    ))

    matrix_data = [
        [
            Paragraph("Stakeholder Segment", table_header),
            Paragraph("Key Decision Makers", table_header),
            Paragraph("Core Motivations & Pain Points", table_header),
            Paragraph("AgroBiometrix Hook & Proof Point", table_header)
        ],
        [
            Paragraph("<b>CGIAR Centers</b><br/>(IITA, ILRI, AfricaRice, ICRISAT, CIMMYT, IFPRI)", table_cell),
            Paragraph("Director General, Director of R4D, Regional Directors, AI Hub Leads", table_cell),
            Paragraph("Pan-African scale, breeding trial analytics, multi-location trials, zero hallucinations, bilingual French/English adoption.", table_cell),
            Paragraph("Dual-engine architecture; automated ANOVA & Duncan's post-hoc; native 1-click bilingual switch; IITA/ILRI QTL evidence grounding.", table_cell)
        ],
        [
            Paragraph("<b>NARS Institutes</b><br/>(ARCN, NIHORT, NCRI, NVRI, CSIR, KALRO, ISRA)", table_cell),
            Paragraph("Executive Directors, Heads of Division, Senior Breeders, Chief Agronomists", table_cell),
            Paragraph("Researchers lose weeks on complex SPSS/SAS/R software; lack of specialized tropical biometrical tools; budget constraints.", table_cell),
            Paragraph("Instant RCBD/Split-plot trial generator; downloadable CSV field books; reproducible R/Python scripts generated in 3 seconds.", table_cell)
        ],
        [
            Paragraph("<b>University Faculties</b><br/>(FUNAAB, UI, ABU, UNN, KNUST, Makerere)", table_cell),
            Paragraph("Vice-Chancellors, Deans of Agriculture, HODs, Postgraduate Supervisors", table_cell),
            Paragraph("Postgraduate dissertation bottlenecks, low faculty grant win-rates (TETFUND/NIH), oral defense preparation.", table_cell),
            Paragraph("Socratic AI Thesis Defense Mentor across 14 departments; Cochran sample sizing; publication-grade Word (.docx) grant proposals.", table_cell)
        ],
        [
            Paragraph("<b>Federal Ministries & AU</b><br/>(FMAFS Nigeria, MINADER, AU-CAADP)", table_cell),
            Paragraph("Ministers, Permanent Secretaries, Directors of Planning & Policy Analysis", table_cell),
            Paragraph("Food inflation crises, volatile fertilizer import expenditure, strategic grain reserves, cabinet memo drafting.", table_cell),
            Paragraph("₦5B–₦250B fiscal budget allocator; 12 strategic commodity balance sheets; macro-shock resilience simulators; AU CAADP memos.", table_cell)
        ],
        [
            Paragraph("<b>Donors & Development</b><br/>(Gates Fdn, AGRA, AfDB TAAT, FAO, FARA)", table_cell),
            Paragraph("Agricultural Program Directors, Investment Officers, Extension Leaders", table_cell),
            Paragraph("Return on public investment, smallholder climate resilience, women/youth inclusion, bridging lab-to-last-mile farmer gap.", table_cell),
            Paragraph("Last-Mile Vernacular Radio Synthesizer (Hausa, Yoruba, Swahili, French); climate thermal spike alerts; open digital public good.", table_cell)
        ],
    ]

    matrix_table = Table(matrix_data, colWidths=[95, 95, 154, 160])
    matrix_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor("#1B5E20")),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor("#C8E6C9")),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('PADDING', (0, 0), (-1, -1), 4.5),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor("#F9FBF9")]),
    ]))
    elements.append(matrix_table)
    elements.append(Spacer(1, 10))

    # =========================================================
    # SECTION 2: THE 90-SECOND OPENING MONOLOGUE
    # =========================================================
    elements.append(Paragraph("2. The 90-Second Opening Monologue (Verbatim Spoken Script)", h1_style))
    elements.append(Paragraph(
        "Deliver this monologue verbatim at the start of any meeting, boardroom presentation, or conference pitch before displaying your screen. "
        "It hooks attention by identifying the real enemy (fragmentation and shallow diagnostics) and positions AgroBiometrix as essential infrastructure:",
        body_style
    ))

    script_box = (
        "<i>\"Africa holds 60% of the world's remaining uncultivated arable land, yet our continent spends over $50 billion every year "
        "importing food.<br/><br/>"
        "The problem is NOT that agricultural science is missing. The problem is that our knowledge is completely fragmented. "
        "It sits locked in university theses at Ahmadu Bello and Ibadan, isolated CGIAR trial spreadsheets, inaccessible soil maps, "
        "and uncoordinated government ministry files.<br/><br/>"
        "Most agricultural AI deployed in Africa today simply says: 'Upload a picture of your tomato leaf, and I will identify the pest.' "
        "While helpful, that only diagnoses symptoms. It fails researchers, it fails breeders, and it fails policymakers.<br/><br/>"
        "We built <b>AgroBiometrix</b>: the generative biometrics and intelligence infrastructure behind African agriculture. "
        "Give AgroBiometrix an agro-ecological coordinate, a crop variety, an indigenous livestock breed, a soil chemistry profile, "
        "or a macroeconomic policy objective—and it unites scientific research, runs exact statistical biometrics like Duncan's Multiple "
        "Range Test, and translates findings all the way from a Minister's policy brief down to a vernacular radio broadcast for a rural farmer.<br/><br/>"
        "Let me show you how it works in real-time.\"</i>"
    )
    script_table = Table([[Paragraph(script_box, quote_style)]], colWidths=[504])
    script_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor("#F1F8F2")),
        ('BORDER', (0, 0), (-1, -1), 1, colors.HexColor("#81C784")),
        ('PADDING', (0, 0), (-1, -1), 8),
    ]))
    elements.append(script_table)
    elements.append(Spacer(1, 6))

    elements.append(Paragraph("<b>Delivery Coaching Points:</b>", body_bold))
    elements.append(Paragraph("• <b>First 15 Seconds:</b> Speak slowly on '$50 billion every year importing food.' Let the economic weight sink in.", body_style))
    elements.append(Paragraph("• <b>The Contrast:</b> Emphasize 'shallow leaf-photo diagnostics' dismissively to differentiate yourself from consumer apps.", body_style))
    elements.append(Paragraph("• <b>The Transition:</b> Transition smoothly into screen-sharing at the words 'Let me show you how it works in real-time.'", body_style))
    elements.append(Spacer(1, 10))

    elements.append(PageBreak())

    # =========================================================
    # SECTION 3: THE 7-MINUTE LIVE DEMO CLICK PATH
    # =========================================================
    elements.append(Paragraph("3. The 7-Minute Live Screen Walkthrough (Step-by-Step Click Path)", h1_style))
    elements.append(Paragraph(
        "Open <b>https://agrobiometrix.streamlit.app</b> in a clean browser window before the presentation. Follow this structured 6-step click path to systematically demonstrate technical superiority:",
        body_style
    ))

    demo_steps = [
        ("Step 1: The Pan-African Bilingual Hook (60 seconds)",
         "<b>Action:</b> Start on the home screen. Point to the sidebar and toggle the language radio button from <code>English GB</code> to <code>Français FR</code>.<br/>"
         "<b>Spoken Line:</b> <i>'Notice that AgroBiometrix is natively bilingual. Over 25 African countries are French-speaking. With one click, the entire scientific interface, biometrical models, and agent prompts switch seamlessly between English and French.'</i>"),
        
        ("Step 2: Multi-Agent Orchestration Swarm (90 seconds)",
         "<b>Action:</b> Navigate to <code>🌟 Multi-Agent Orchestrator</code>. Select the preset inquiry: <i>'Which maize varieties should Northern Nigerian farmers plant under increasing heat stress?'</i> Click 'Run Multi-Agent Synthesis'.<br/>"
         "<b>Spoken Line:</b> <i>'This is not generic ChatGPT. An agronomic inquiry requires multiple specialized intelligences. Watch as AgroBiometrix deploys our Climate Agent to analyze thermal spikes, Crop Physiology Agent for drought tolerance, Soil Agent for NPK buffering, and Evidence Agent for verified CGIAR literature citations—with zero hallucinations.'</i>"),
        
        ("Step 3: Quantitative Biometrics & Breeding Suite (90 seconds)",
         "<b>Action:</b> Navigate to <code>🧬 Agricultural Biometrics & Breeding</code> ➔ <code>Tab 2: Biometrical Analysis & DMRT</code>. Click 'Execute ANOVA & Post-Hoc Engine'.<br/>"
         "<b>Spoken Line:</b> <i>'African crop breeders and university postgraduates spend weeks wrestling with SPSS, SAS, or writing custom R scripts. AgroBiometrix executes Two-Way Factorial ANOVA and Duncan's Multiple Range Test with distinct letter separation in under three seconds, generating downloadable trial field books and reproducible R scripts.'</i>"),
        
        ("Step 4: AI Research Scientist & Grant Proposal Studio (90 seconds)",
         "<b>Action:</b> Navigate to <code>🔬 AI Research Scientist & Proposal Studio</code> ➔ <code>Tab 1: Grant Proposal Architect</code>. Show the 7-part proposal, Cochran's sample sizing equation, and download buttons.<br/>"
         "<b>Spoken Line:</b> <i>'Our Research Studio automates PRISMA 2020 systematic literature matrices and synthesizes 7-part funding proposals complete with Cochran sample size calculations, real peer-reviewed APA citations, and direct export into clean, uncorrupted Microsoft Word (.docx) and PDF documents.'</i>"),
        
        ("Step 5: Last-Mile Vernacular Extension Radio (90 seconds)",
         "<b>Action:</b> Click <code>Tab 4: Evidence Matrix & Vernacular Radio</code>. Select the <i>'Kaduna/Kano Maize Heat Wave'</i> scenario. Choose <b>Hausa</b>, <b>Swahili</b>, <b>French</b>, or <b>Yoruba</b>. Play the Marimba station chime and trigger the voice broadcast player.<br/>"
         "<b>Spoken Line:</b> <i>'Science that remains trapped in academic journals does not feed nations. AgroBiometrix translates complex biometric findings into vernacular audio broadcast bulletins voiced in Hausa, Yoruba, Swahili, and French for rural community radio and extension WhatsApp dispatches.'</i>"),
        
        ("Step 6: Institutional Macro-Policy Platform (60 seconds)",
         "<b>Action:</b> Navigate to <code>🏛️ Agricultural Policy & Economic Simulator</code>. Adjust the ₦50B budget allocation slider across Treasury Ag-GDP, Labour jobs, and FX savings scorecards.<br/>"
         "<b>Spoken Line:</b> <i>'For agricultural ministries and the African Union CAADP, AgroBiometrix models import substitution across 12 strategic value chains, stress-tests food inflation against fertilizer price shocks, and drafts Federal Executive Council policy briefs.'</i>")
    ]

    for step_title, step_desc in demo_steps:
        s_table = Table([[Paragraph(f"<b>{step_title}</b>", table_header)],
                         [Paragraph(step_desc, body_style)]], colWidths=[504])
        s_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor("#2E7D32")),
            ('BACKGROUND', (0, 1), (-1, 1), colors.HexColor("#F9FBF9")),
            ('BOX', (0, 0), (-1, -1), 0.8, colors.HexColor("#81C784")),
            ('PADDING', (0, 0), (-1, -1), 6),
        ]))
        elements.append(s_table)
        elements.append(Spacer(1, 5))

    elements.append(PageBreak())

    # =========================================================
    # SECTION 4: INSTITUTIONAL DEFENSE PLAYBOOK (TOUGH Q&A)
    # =========================================================
    elements.append(Paragraph("4. Institutional Defense Playbook (Tough Stakeholder Q&A)", h1_style))
    elements.append(Paragraph(
        "Senior scientists, directors general, and software evaluators will probe your claims. Deliver these authoritative, mathematically grounded answers:",
        body_style
    ))

    defense_qa = [
        ("Q1: 'How do you prevent generative AI hallucinations in critical biological and agronomic research?'",
         "<b>The Power Answer:</b> 'AgroBiometrix employs a dual-engine architecture. All mathematical and biometrical computations—ANOVA, Duncan's Multiple Range Test, BLUP breeding values, USDA soil physics, and Cochran sample sizing—run entirely on deterministic, local Python mathematical libraries (SciPy, Statsmodels, NumPy). They do NOT use LLM generative approximations. For literature retrieval, our Evidence Agent is strictly constrained to indexed CGIAR, FAO, Crossref, and PubMed bibliographic databases. Generative AI is used solely for natural-language synthesis over verified data.'"),

        ("Q2: 'Most rural smallholder farmers lack smartphones, digital literacy, and internet. How does this reach them?'",
         "<b>The Power Answer:</b> 'AgroBiometrix is designed as B2B and B2G infrastructure, not a direct consumer smartphone app. Our primary users are agricultural extension supervisors, cooperative agronomists, seed outgrower coordinators, and NARS researchers. These professionals use AgroBiometrix to generate localized vernacular audio bulletins broadcast over rural community FM radio stations (which reach over 80% of African rural households) or distributed via 2G voice SMS and cooperative WhatsApp voice notes.'"),

        ("Q3: 'What happens when internet connection drops at remote research stations or field sub-stations?'",
         "<b>The Power Answer:</b> 'AgroBiometrix operates 100% free and functional offline out-of-the-box. The entire biometrical computation engine, experimental design generator, USDA soil texture simulator, and local agricultural knowledge graphs execute locally without cloud dependencies. Live cloud reasoning via Google Gemini is an optional enhancement that activates seamlessly when connectivity is present.'"),

        ("Q4: 'Isn't this just another wrapper around ChatGPT or Gemini?'",
         "<b>The Power Answer:</b> 'Far from it. A generic ChatGPT prompt cannot run a Two-Way ANOVA with interaction terms, cannot perform Duncan's stepwise post-hoc ranking with letter separation, cannot solve Henderson's Mixed Model Equations for livestock BLUP, and has no grounding in tropical Ultisol lime buffering or pastoral THI heat stress indices. AgroBiometrix contains thousands of lines of specialized biometrical algorithms, custom taxonomic datasets covering 48+ African crops and livestock breeds, and a 6-agent orchestration pipeline that has no equivalent in commercial LLMs.'"),

        ("Q5: 'How do you protect institutional data privacy, breeding germplasm IP, and national agricultural sovereignty?'",
         "<b>The Power Answer:</b> 'AgroBiometrix enforces complete data isolation. When researchers upload private trial spreadsheets, they are processed in volatile memory for the active session and are never cached or used to train public foundational models. For national ministries and CGIAR centers, AgroBiometrix can be deployed in private on-premise containers (via our Docker and docker-compose configurations) behind institutional firewalls.'"),

        ("Q6: 'What is your commercialization and long-term sustainability model?'",
         "<b>The Power Answer:</b> 'We operate a four-tier sustainable flywheel: (1) Free open-access tier for university undergraduate teaching and community extension; (2) Freemium Researcher & Postgraduate Tier ($5–$15/month) for unlimited advanced BLUP runs and grant reviews; (3) Agribusiness & Lab Seat Tier ($100–$500/month) for commercial seed and feed mills managing multi-location trials; and (4) Enterprise Institutional Licensing ($10k–$50k/year) for ministries and CGIAR research programs requiring customized knowledge graphs and private server instances.'")
    ]

    for q, a in defense_qa:
        q_table = Table([[Paragraph(f"<b>{q}</b>", table_cell_bold)],
                         [Paragraph(a, body_style)]], colWidths=[504])
        q_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor("#E8F5E9")),
            ('BACKGROUND', (0, 1), (-1, 1), colors.white),
            ('BOX', (0, 0), (-1, -1), 0.6, colors.HexColor("#C8E6C9")),
            ('PADDING', (0, 0), (-1, -1), 5.5),
        ]))
        elements.append(q_table)
        elements.append(Spacer(1, 5))

    elements.append(PageBreak())

    # =========================================================
    # SECTION 5: THE CLOSING STRATEGY & PILOT PROPOSAL
    # =========================================================
    elements.append(Paragraph("5. The Closing Strategy & 90-Day Collaborative Pilot Proposal", h1_style))
    elements.append(Paragraph(
        "Never end a demonstration without securing a concrete, low-risk commitment. Institutional stakeholders hate high-stakes commitments, "
        "but they eagerly accept structured pilot studies that advance their research output. Deliver this exact proposal:",
        body_style
    ))

    pilot_box = (
        "<i>\"We are not asking for a multi-million-dollar institutional contract today. We are proposing a structured <b>90-Day Collaborative Pilot</b> "
        "with your institution:<br/><br/>"
        "<b>1. Departmental Deployment:</b> Provide free enterprise institutional access for up to 50 of your senior scientists, postgraduate students, "
        "or extension officers.<br/>"
        "<b>2. Co-Authored Scientific Validation Study:</b> Conduct a side-by-side productivity study comparing AgroBiometrix against standard software "
        "(SPSS/SAS/manual reviews) to measure reduction in trial data analysis hours and grant turnaround times.<br/>"
        "<b>3. Localized Custom Calibration:</b> Our technical team will calibrate the knowledge graph and trial layouts to your institute's priority "
        "crops, soil zones, and livestock germplasm.<br/><br/>"
        "At the end of 90 days, we review empirical productivity gains. If it transforms your research workflow, we discuss a formal partnership. "
        "If not, your institution has lost nothing and gained 50 accelerated research projects.<br/><br/>"
        "Can we schedule a 30-minute technical onboarding session with your research committee next week?\"</i>"
    )
    pilot_table = Table([[Paragraph(pilot_box, quote_style)]], colWidths=[504])
    pilot_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor("#F1F8F2")),
        ('BORDER', (0, 0), (-1, -1), 1, colors.HexColor("#81C784")),
        ('PADDING', (0, 0), (-1, -1), 8),
    ]))
    elements.append(pilot_table)
    elements.append(Spacer(1, 10))

    # =========================================================
    # SECTION 6: DIRECTORY OF INSTITUTIONAL PITCH LETTERS (.DOCX)
    # =========================================================
    elements.append(Paragraph("6. Directory of Institutional Pitch Letters (.docx Formats)", h1_style))
    elements.append(Paragraph(
        "All customized pitch letters referenced in this playbook have been pre-compiled into publication-grade Microsoft Word (.docx) formats in your workspace. "
        "You can open, customize recipient details, add institutional letterhead, and dispatch them immediately:",
        body_style
    ))

    letters_summary = [
        [
            Paragraph("Target Institution", table_header),
            Paragraph("Generated Word (.docx) File", table_header),
            Paragraph("Key Mandate & Strategic Focus", table_header)
        ],
        [
            Paragraph("<b>IITA</b><br/>(Ibadan / Pan-Africa)", table_cell),
            Paragraph("<code>AgroBiometrix_Pitch_Letter_IITA.docx</code>", table_cell),
            Paragraph("Tropical crop breeding (Cassava, Maize, Yam, Cowpea), bilingual EN/FR regional network, two-way ANOVA & DMRT.", table_cell)
        ],
        [
            Paragraph("<b>ILRI</b><br/>(Nairobi / Ibadan)", table_cell),
            Paragraph("<code>AgroBiometrix_Pitch_Letter_ILRI.docx</code>", table_cell),
            Paragraph("Indigenous livestock genetics, THI heat stress, trypanotolerance markers, pastoral PPR disease early warning.", table_cell)
        ],
        [
            Paragraph("<b>CGIAR System / AI Hub</b><br/>(Global / Africa)", table_cell),
            Paragraph("<code>AgroBiometrix_Pitch_Letter_CGIAR.docx</code>", table_cell),
            Paragraph("Digital public goods, zero-hallucination dual engine, PRISMA reviews, AU CAADP macro policy simulator.", table_cell)
        ],
        [
            Paragraph("<b>FUNAAB</b><br/>(Agricultural Universities)", table_cell),
            Paragraph("<code>AgroBiometrix_Pitch_Letter_FUNAAB.docx</code>", table_cell),
            Paragraph("Postgraduate dissertation computing, Socratic thesis defense mentor, TETFUND grant architect, FUNAAB Alpha breed.", table_cell)
        ],
        [
            Paragraph("<b>ARCN & FMAFS</b><br/>(Abuja / National Policy)", table_cell),
            Paragraph("<code>AgroBiometrix_Pitch_Letter_ARCN_FMAFS.docx</code>", table_cell),
            Paragraph("₦5B–₦250B fiscal budget allocator, 12-commodity import substitution, national food inflation stress-testing, FEC briefs.", table_cell)
        ],
        [
            Paragraph("<b>Master Executive Dossier</b><br/>(All 5 Institutions)", table_cell_bold),
            Paragraph("<code>AgroBiometrix_Institutional_Pitch_Letters_Executive_Dossier.docx</code>", table_cell_bold),
            Paragraph("Complete 5-institution executive compilation with formal title page, table of contents, and individual formatted sections.", table_cell_bold)
        ]
    ]

    letters_table = Table(letters_summary, colWidths=[110, 184, 210])
    letters_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor("#1B5E20")),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor("#C8E6C9")),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('PADDING', (0, 0), (-1, -1), 4.5),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor("#F9FBF9")]),
    ]))
    elements.append(letters_table)
    elements.append(Spacer(1, 12))

    # Concluding Institutional Footer Callout
    final_note = (
        "<b>Playbook Verification & Live Deployment:</b> This playbook is fully synchronized with the live web application at "
        "<b>https://agrobiometrix.streamlit.app</b> and the complete 30-page scientific blueprint "
        "<code>AgroBiometrix_Global_Dominance_and_Pitch_Mastery.pdf</code>. All biometrical models, multi-agent swarms, bilingual language toggles, "
        "and document exporters are verified, hardened, and active."
    )
    final_table = Table([[Paragraph(final_note, callout_style)]], colWidths=[504])
    final_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor("#E8F5E9")),
        ('BORDER', (0, 0), (-1, -1), 1, colors.HexColor("#1B5E20")),
        ('PADDING', (0, 0), (-1, -1), 7),
    ]))
    elements.append(final_table)

    # Build PDF
    doc.build(elements, canvasmaker=NumberedCanvas)
    print(f"Successfully generated: {PDF_FILENAME}")


if __name__ == "__main__":
    build_playbook_pdf()
