"""
Script to generate the updated AgriIntel Technical Diagnostics, Multi-Agent Advisory & Continental Platform Scope PDF.
Includes:
- Technical Diagnostics (Blank Dropdown, Tomato Maize Mismatch, Poultry Cattle Conflation)
- Specialized Multi-Agent Avian Science Advisory (October/November Transition Bioclimatics)
- Specialized Multi-Agent Tomato Advisory (Western Nigeria Dry-Season Arbitrage)
- Continental Multi-Commodity Matrix (Poultry, Cattle, Sheep/Goats, Aquaculture, Pigs, Crops)
- Upgraded Module 7 (Livestock & Poultry Intelligence Infrastructure with Avian THI & Festive Simulator)
- Dual-Tier Architecture & Operational Health Status
"""

import os
import shutil
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, HRFlowable, KeepTogether
)
from reportlab.pdfgen import canvas

PDF_FILENAME = "6 AgriIntel_Technical_Diagnostics_and_Comprehensive_Platform_Scope.pdf"
ALT_FILENAME = "AgriIntel_Technical_Diagnostics_and_Comprehensive_Platform_Scope.pdf"


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
            self.drawString(54, 755, "AGRIINTEL TECHNICAL DOSSIER — SYSTEM DIAGNOSTICS & CONTINENTAL SCOPE")
            self.setFont("Helvetica", 8)
            self.setFillColor(colors.HexColor("#555555"))
            self.drawRightString(558, 755, "October 2026 | Enterprise Build v2.5")
            self.setStrokeColor(colors.HexColor("#A5D6A7"))
            self.setLineWidth(0.7)
            self.line(54, 748, 558, 748)

        # Footer (all pages)
        page_text = f"Page {self._pageNumber} of {page_count}"
        self.setFont("Helvetica", 8)
        self.setFillColor(colors.HexColor("#2E7D32"))
        self.drawString(54, 34, "AgriIntel: Africa-First, Globally Scalable Generative Intelligence Platform for Agriculture")
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

    title_style = ParagraphStyle(
        'DocTitle',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=17,
        leading=21,
        textColor=colors.HexColor("#1B5E20"),
        spaceAfter=3
    )

    subtitle_style = ParagraphStyle(
        'DocSubTitle',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=10,
        leading=14,
        textColor=colors.HexColor("#2E7D32"),
        spaceAfter=8
    )

    h1_style = ParagraphStyle(
        'Heading1_Custom',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=11.5,
        leading=15,
        textColor=colors.HexColor("#1B5E20"),
        spaceBefore=9,
        spaceAfter=4,
        keepWithNext=True
    )

    h2_style = ParagraphStyle(
        'Heading2_Custom',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=10,
        leading=13.5,
        textColor=colors.HexColor("#2E7D32"),
        spaceBefore=7,
        spaceAfter=3,
        keepWithNext=True
    )

    body_style = ParagraphStyle(
        'Body_Custom',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=8.5,
        leading=12,
        textColor=colors.HexColor("#212121"),
        spaceAfter=4
    )

    bullet_style = ParagraphStyle(
        'Bullet_Custom',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=8.2,
        leading=11.6,
        textColor=colors.HexColor("#212121"),
        leftIndent=10,
        spaceAfter=2.5
    )

    callout_style = ParagraphStyle(
        'Callout_Text',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=8,
        leading=11.4,
        textColor=colors.HexColor("#1B5E20")
    )

    table_header = ParagraphStyle(
        'TH_Style',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=8,
        leading=11,
        textColor=colors.white
    )

    table_cell = ParagraphStyle(
        'TC_Style',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=7.8,
        leading=10.6,
        textColor=colors.HexColor("#212121")
    )

    table_cell_bold = ParagraphStyle(
        'TCB_Style',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=7.8,
        leading=10.6,
        textColor=colors.HexColor("#1B5E20")
    )

    story = []

    # =========================================================================
    # HEADER / COVER BLOCK
    # =========================================================================
    story.append(Paragraph("AgriIntel Technical Diagnostics, Multi-Agent Advisory & Continental Platform Scope", title_style))
    story.append(Paragraph("<b>Enterprise Session Dossier</b> | System Audit, Multi-Enterprise Decoupling (Poultry, Cattle, Aquaculture & Crops), Specialized Agronomic Science & Module 7 Bioclimatic Architecture", subtitle_style))
    story.append(HRFlowable(width="100%", thickness=1.5, color=colors.HexColor("#1B5E20"), spaceBefore=1, spaceAfter=6))

    # Metadata Banner
    meta_data = [
        [
            Paragraph("<b>Platform:</b> AgriIntel Enterprise v2.5", table_cell),
            Paragraph("<b>Target Region:</b> Pan-Africa & Global Ag", table_cell),
            Paragraph("<b>Execution Mode:</b> Dual Offline / Cloud AI", table_cell),
            Paragraph("<b>Updated:</b> October 13, 2026", table_cell)
        ]
    ]
    t_meta = Table(meta_data, colWidths=[126, 126, 126, 126])
    t_meta.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor("#E8F5E9")),
        ('BOX', (0, 0), (-1, -1), 0.8, colors.HexColor("#A5D6A7")),
        ('INNERGRID', (0, 0), (-1, -1), 0.5, colors.HexColor("#C8E6C9")),
        ('TOPPADDING', (0, 0), (-1, -1), 3),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 3),
        ('LEFTPADDING', (0, 0), (-1, -1), 5),
        ('RIGHTPADDING', (0, 0), (-1, -1), 5),
    ]))
    story.append(t_meta)
    story.append(Spacer(1, 8))

    # =========================================================================
    # SECTION 1: FORENSIC ROOT CAUSE ANALYSIS & SYSTEM DIAGNOSTICS
    # =========================================================================
    story.append(Paragraph("1. Forensic Root Cause Analysis: System Debugging & Enterprise Decoupling", h1_style))
    story.append(Paragraph(
        "During progressive user testing of AgriIntel's Multi-Agent Orchestration Layer, three distinct behavioral anomalies "
        "were identified and resolved. A comprehensive forensic audit pinpointed their structural origins in code, leading "
        "to permanent architectural rectifications across the engine.",
        body_style
    ))

    diag_data = [
        [
            Paragraph("Symptom Reported", table_header),
            Paragraph("Root Cause Identified in Code", table_header),
            Paragraph("Permanent Engineering Fix Implemented", table_header)
        ],
        [
            Paragraph("<b>1. 'The quick dropdown does not show any option, it's blank'</b>", table_cell),
            Paragraph("<b>Container Mismatch & Missing Import:</b> The control was authored as an <font face='Courier'>st.expander</font> rather than a selectbox, containing only a blank password box. Concurrently, <font face='Courier'>app.py</font> lacked <font face='Courier'>import os</font>, causing <font face='Courier'>os.getenv('GEMINI_API_KEY')</font> to throw a silent <font face='Courier'>NameError</font> that halted child widget rendering.", table_cell),
            Paragraph("<b>Explicit Selectbox:</b> Replaced the expander with a visible <font face='Courier'>st.selectbox</font> presenting 4 clear engine modes. Added <font face='Courier'>import os</font> and defensive fallbacks. Built-in Offline Engine active by default with zero key prompts.", table_cell)
        ],
        [
            Paragraph("<b>2. 'I asked a question on tomatoes and got maize output, why?'</b>", table_cell),
            Paragraph("<b>Hardcoded Input & Monolithic Fallback:</b> Selecting Custom Query defaulted the text area to a Northern savanna maize prompt. Furthermore, the offline engine initially only contained a single fallback template modeled on IITA maize trials (<font face='Courier'>SAMMAZ 15, SAMMAZ 27</font>).", table_cell),
            Paragraph("<b>Clean Input & Semantic Routing:</b> Custom Query now initializes with a clean placeholder. Upgraded <font face='Courier'>core/orchestrator.py</font> with regex semantic parsing across crops, regions, and seasons. Added Tomato inquiry as a 1-click preset chip.", table_cell)
        ],
        [
            Paragraph("<b>3. 'I asked a question about poultry and got cattle/pastoral grazing response'</b>", table_cell),
            Paragraph("<b>Enterprise Conflation Bug:</b> In <font face='Courier'>core/orchestrator.py</font>, poultry and chickens were grouped into a monolithic <font face='Courier'>is_livestock</font> condition. That branch was written strictly for savanna pastoral cattle (<font face='Courier'>Stylosanthes</font> forage, Zebu bulls, White Fulani cattle).", table_cell),
            Paragraph("<b>Multi-Enterprise Decoupling:</b> Decoupled poultry into a dedicated avian engine with 6 specialized agents (<font face='Courier'>is_poultry</font>). Separate dedicated engines now exist for Cattle, Small Ruminants, Aquaculture, Pigs, and Crops.", table_cell)
        ]
    ]
    t_diag = Table(diag_data, colWidths=[115, 195, 194])
    t_diag.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor("#1B5E20")),
        ('BOX', (0, 0), (-1, -1), 0.8, colors.HexColor("#A5D6A7")),
        ('INNERGRID', (0, 0), (-1, -1), 0.5, colors.HexColor("#E0E0E0")),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.HexColor("#FFFFFF"), colors.HexColor("#F9FBE7"), colors.HexColor("#FFFFFF")]),
        ('TOPPADDING', (0, 0), (-1, -1), 4),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
        ('LEFTPADDING', (0, 0), (-1, -1), 5),
        ('RIGHTPADDING', (0, 0), (-1, -1), 5),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
    ]))
    story.append(t_diag)
    story.append(Spacer(1, 8))

    # =========================================================================
    # SECTION 2: SPECIALIZED MULTI-AGENT AVIAN SCIENCE: POULTRY IN OCT/NOV
    # =========================================================================
    story.append(Paragraph("2. Specialized Agricultural Science: Poultry Bioclimatics (October/November Transition)", h1_style))
    story.append(Paragraph(
        "<b>Inquiry Addressed:</b> <i>'How favourable is the climatic condition is to poultry production at this period?'</i><br/>"
        "<b>Core Verdict:</b> The October/November transition into the Harmattan dry season represents a <b>double-edged operational window</b>. "
        "It provides the single most profitable marketing window of the calendar year (broilers stocked now hit peak December festive demand), "
        "but presents acute bioclimatic and respiratory hazards (afternoon heat panting, midnight chilling, and airborne dust infections).",
        body_style
    ))

    poultry_agents = [
        ("Poultry Science & Housing Agent", "Avian Management, Stocking Trajectory & Housing Architecture", [
            "<b>Prime Commercial Stocking Window:</b> Stocking Day-Old Chicks (DOC) in late October to early November targets target slaughter weight (2.2–2.6 kg) at Day 42–52, perfectly aligning with December 20–25 festive holiday demand.",
            "<b>Diurnal Thermal Swings:</b> Days are hot (31°C–34°C) while late nights drop sharply to 18°C–22°C as dry northern air arrives. Chicks require double-walled brooder curtains from 11:00 PM to 6:00 AM to prevent chilling, but curtains must be <b>lowered by 9:00 AM</b> for cross-ventilation.",
            "<b>Pen Orientation & Stocking Density:</b> Open-sided pens must be oriented East-to-West to avoid direct solar rays hitting birds. Reduce stocking density by 15%–20% during hot transitions (8–10 broilers/m² instead of 12/m²) to prevent bird-to-bird radiant heat trapping."
        ]),
        ("Climate & Bioclimatic Housing Agent", "Avian Thermoregulation, THI & Harmattan Atmospheric Stress", [
            "<b>Thermoregulatory Deficit:</b> Domestic fowl lack sweat glands and have a normal core body temperature of 41.5°C–42.0°C. Above 27°C–28°C, birds can only dissipate heat via evaporative panting, which expels blood CO2 and triggers <b>respiratory alkalosis</b>.",
            "<b>Harmattan Dust & Respiratory Hazard:</b> Declining humidity (<45%) and abrasive airborne dust particles irritate avian mucous membranes, sharply elevating susceptibility to Chronic Respiratory Disease (CRD - <i>Mycoplasma gallisepticum</i>) and viral tracheitis.",
            "<b>Litter Dynamics:</b> Dry air prevents wet-litter coccidiosis (a major rainy season headache), but creates dusty litter. Turn litter gently and mist pen perimeter (without wetting birds) to suppress dust."
        ]),
        ("Poultry Health & Biosecurity Agent", "Airborne Viral Defense, Vaccination Schedule & Genetics", [
            "<b>Newcastle Disease (ND) Shield:</b> The dry Harmattan wind carries wild bird pathogens, dramatically increasing Newcastle risk. Strictly administer <b>ND Lasota / Clone 30</b> at Day 14 and Day 28.",
            "<b>Gumboro (IBD) Protocol:</b> Intermediate Plus vaccine at Day 9–11 and booster at Day 18–20.",
            "<b>Respiratory Prophylaxis:</b> Administer prophylactic tylosin or doxycycline water medication at the first sign of dust haze or rattling tracheas to head off CRD.",
            "<b>Strain Adaptability:</b> Elite commercial broiler strains (Ross 308, Cobb 500, Marshall) achieve fast conversion if heat-mitigated; dual-purpose improved breeds (Noiler, Kuroiler, ShikaBrown) possess higher innate resilience to Harmattan dust and diurnal thermal shifts."
        ]),
        ("Nutrition & Feed Management Agent", "Acid-Base Balance, Split-Feeding & Electrolyte Hydration", [
            "<b>Combating Respiratory Alkalosis:</b> Prolonged panting causes excessive loss of carbon dioxide, raising blood pH. Add <b>Vitamin C (ascorbic acid at 1g/liter)</b>, potassium chloride, or <b>Sodium Bicarbonate</b> to drinking water between 10:00 AM and 4:00 PM.",
            "<b>Split-Feeding Schedule:</b> Heavy feeding during peak afternoon heat causes high Diet-Induced Thermogenesis (DIT), triggering Sudden Death Syndrome. Practice <b>split-feeding</b>: feed 60% of daily ration in the cool early morning (6:00 AM–9:30 AM) and 40% in the evening/night (5:30 PM–9:00 PM), withdrawing feed entirely during peak heat (11:30 AM–3:30 PM).",
            "<b>Water Capacity:</b> Chickens drink 2.5x to 3x more water during heat transitions. Insulate overhead water tanks from direct sun or add ice blocks to keep drinking water under 24°C."
        ]),
        ("Farm Economics & Festive Market Agent", "Festive Arbitrage, Feed Margin Buffering & Net Returns", [
            "<b>Festive Demand Surge:</b> Broilers harvested December 20–25 capture holiday farmgate prices of <b>₦11,000 – ₦16,000 per bird (2.3–2.6 kg)</b>, up from ordinary off-season rates of ₦7,500–₦8,500.",
            "<b>Margin Buffer:</b> Even with high feed costs (maize at ₦650k–₦850k/ton, soya meal at ₦950k/ton), profit margins per 1,000 birds exceed ₦2.5M–₦3.8M (>30%–40% ROI) for well-managed flocks with mortality kept below 4%."
        ]),
        ("Evidence & Standards Agent", "Institutional Benchmarks & Biosecurity Protocols", [
            "<b>Grounding:</b> Formulated from National Animal Production Research Institute (<b>NAPRI, Shika-Zaria</b>), Federal University of Agriculture Abeokuta (<b>FUNAAB Poultry Biotechnology Center</b>), FAO Avian Bioclimatic Housing Standards, and World's Poultry Science Association (WPSA) thermal stress protocols."
        ])
    ]

    for agent_title, focus_subtitle, bullets in poultry_agents:
        content_cells = [
            [Paragraph(f"<b>{agent_title}</b> — <i>{focus_subtitle}</i>", table_cell_bold)],
        ]
        for b in bullets:
            content_cells.append([Paragraph(f"• {b}", bullet_style)])
        
        t_agent = Table(content_cells, colWidths=[504])
        t_agent.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor("#FAFAFA")),
            ('BOX', (0, 0), (-1, -1), 0.6, colors.HexColor("#C8E6C9")),
            ('LINEBELOW', (0, 0), (-1, 0), 0.8, colors.HexColor("#81C784")),
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor("#E8F5E9")),
            ('TOPPADDING', (0, 0), (-1, -1), 2.5),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 2.5),
            ('LEFTPADDING', (0, 0), (-1, -1), 5),
            ('RIGHTPADDING', (0, 0), (-1, -1), 5),
        ]))
        story.append(t_agent)
        story.append(Spacer(1, 4))

    story.append(Spacer(1, 6))

    # =========================================================================
    # SECTION 3: SPECIALIZED SCIENTIFIC ADVISORY: TOMATOES IN WESTERN NIGERIA
    # =========================================================================
    story.append(KeepTogether([
        Paragraph("3. Specialized Agricultural Science: Tomato Advisory for Western Nigeria", h1_style),
        Paragraph(
            "<b>Inquiry Addressed:</b> <i>'Best tomatoes variety for western Nigeria at this period (October/November Transition).'</i><br/>"
            "The AgriIntel Multi-Agent Ensemble synthesized a comprehensive agronomic strategy calibrated to the rainforest/derived savanna "
            "agro-ecological zones (Oyo, Ogun, Osun, Ondo, Ekiti, and Lagos).",
            body_style
        )
    ]))

    tomato_data = [
        [
            Paragraph("Dimension", table_header),
            Paragraph("Specialized Scientific Recommendation (Western Nigeria Oct/Nov Window)", table_header)
        ],
        [
            Paragraph("<b>Elite Cultivars</b>", table_cell_bold),
            Paragraph("<b>Cobra 26 F1</b> (Technisem): Benchmark determinate hybrid; high heat tolerance, thick pericarp (prevents rain-cracking), high firmness, bacterial wilt tolerance.<br/><b>Platinum F1</b> (Syngenta): Dense canopy protects against fruit sunscald; resistant to <i>Ralstonia solanacearum</i> & Fusarium races 1 & 2.<br/><b>Tropimech / NHLe 158</b> (NIHORT Ibadan): High paste solids OPV adapted to rainforest soils.", table_cell)
        ],
        [
            Paragraph("<b>Nursery & Beds</b>", table_cell_bold),
            Paragraph("Nurse in 104-cell seedling trays under 30% shade net for 21–25 days. Transplant on <b>25 cm raised beds</b> (50 cm × 60 cm spacing) to drain late rains and eliminate stem collar rot.", table_cell)
        ],
        [
            Paragraph("<b>Blossom End Rot</b>", table_cell_bold),
            Paragraph("Tropical heat impairs calcium mobility. Incorporate 5–10 t/ha cured poultry manure + NPK 15:15:15 at 2 WAT. Apply <b>Calcium Nitrate (50 kg/ha side-dress)</b> or foliar Calcium-Boron chelate spray at first fruit set to eradicate black sunken fruit bottoms (**Blossom End Rot**).", table_cell)
        ],
        [
            Paragraph("<b>Genomics & Vector</b>", table_cell_bold),
            Paragraph("Target hybrids with <b>Ty-1 or Ty-3</b> gene complexes for Tomato Yellow Leaf Curl Virus (TYLCV) resistance, vectored by whiteflies (<i>Bemisia tabaci</i>). Deploy <b>Mi-1.2</b> root-knot nematode immunity.", table_cell)
        ],
        [
            Paragraph("<b>Market Arbitrage</b>", table_cell_bold),
            Paragraph("Harvest hits peak holiday prices at <b>Mile 12 (Lagos)</b>, <b>Bodija (Ibadan)</b>, and <b>Shasha (Akure)</b> where 50kg baskets rise from ₦15,000 to <b>₦55,000 – ₦90,000</b> (>200% net margins on irrigated acreage). Grounded in NIHORT and WorldVeg/AVRDC bulletins.", table_cell)
        ]
    ]
    t_tom = Table(tomato_data, colWidths=[110, 394])
    t_tom.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor("#1B5E20")),
        ('BOX', (0, 0), (-1, -1), 0.8, colors.HexColor("#A5D6A7")),
        ('INNERGRID', (0, 0), (-1, -1), 0.5, colors.HexColor("#E0E0E0")),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.HexColor("#FFFFFF"), colors.HexColor("#F9FBE7")]),
        ('TOPPADDING', (0, 0), (-1, -1), 3.5),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 3.5),
        ('LEFTPADDING', (0, 0), (-1, -1), 5),
        ('RIGHTPADDING', (0, 0), (-1, -1), 5),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
    ]))
    story.append(t_tom)
    story.append(Spacer(1, 8))

    # =========================================================================
    # SECTION 4: CONTINENTAL MULTI-COMMODITY MATRIX
    # =========================================================================
    story.append(KeepTogether([
        Paragraph("4. Continental Platform Scope: Multi-Commodity Agricultural Matrix", h1_style),
        Paragraph(
            "AgriIntel's offline intelligence engine covers all major African agricultural sub-sectors, ensuring that "
            "queries across diverse livestock species, tree crops, roots, and cereals receive specialized, evidence-grounded responses:",
            body_style
        )
    ]))

    scope_data = [
        [
            Paragraph("Sub-Sector / Commodity", table_header),
            Paragraph("Core Genotypes / Cultivars / Breeds", table_header),
            Paragraph("Agronomic, Edaphic & Genomic Science Engine", table_header),
            Paragraph("Economic & Value Chain Focus", table_header)
        ],
        [
            Paragraph("<b>🐔 Poultry & Avian</b>", table_cell_bold),
            Paragraph("Ross 308, Cobb 500, Isa Brown, Noiler, ShikaBrown", table_cell),
            Paragraph("Avian THI modeling, evaporative panting, Vitamin C/bicarbonate for alkalosis, Newcastle ND Lasota & CRD dust defense.", table_cell),
            Paragraph("December festive harvest window commanding ₦11,000–₦16,000/bird farmgate.", table_cell)
        ],
        [
            Paragraph("<b>🐄 Cattle & Pastoral</b>", table_cell_bold),
            Paragraph("White Fulani (Bunaji), Muturu, N'Dama, Sokoto Gudali", table_cell),
            Paragraph("THI stress threshold (>78 units), HSP70/90 cytoprotection, SLICK PRLR locus, BTA2/7/14 trypanotolerance sweeps.", table_cell),
            Paragraph("Rangeland rotational carrying capacity; 60-day pre-festive bull fattening (>45% gross margin).", table_cell)
        ],
        [
            Paragraph("<b>🐐 Small Ruminants</b>", table_cell_bold),
            Paragraph("West African Dwarf (WAD), Red Sokoto, Sahelian Sheep", table_cell),
            Paragraph("PPR live attenuated vaccination, slatted floor hygiene, deep-rooted browse legumes (<i>Leucaena, Gliricidia</i>).", table_cell),
            Paragraph("90-day intensive ram fattening for festive markets yielding >50% profit margin.", table_cell)
        ],
        [
            Paragraph("<b>🐟 Aquaculture</b>", table_cell_bold),
            Paragraph("Catfish (<i>Clarias gariepinus</i>), Tilapia (<i>O. niloticus</i>)", table_cell),
            Paragraph("Cold Harmattan water temp (<24°C) feeding management, dissolved oxygen >4.5 mg/L, uniodized salt buffering.", table_cell),
            Paragraph("Smoked catfish cluster sales targeting holiday festive markets at ₦5,500–₦7,500/kg.", table_cell)
        ],
        [
            Paragraph("<b>🐖 Swine Production</b>", table_cell_bold),
            Paragraph("Large White × Landrace commercial crossbreeds", table_cell),
            Paragraph("Conductive wallowing/sprinklers for heat dissipation (zero sweat glands), African Swine Fever (ASF) strict biosecurity.", table_cell),
            Paragraph("Commercial slaughter weight of 85–95 kg in 5.5–6 months; pork retail value chain.", table_cell)
        ],
        [
            Paragraph("<b>🍅 Vegetables / Hort</b>", table_cell_bold),
            Paragraph("Cobra 26 F1, Platinum F1, Tropimech, NHLe 158, UC82B", table_cell),
            Paragraph("25 cm raised beds, Calcium Nitrate for Blossom End Rot, <i>Ty-1/Ty-3</i> TYLCV whitefly resistance.", table_cell),
            Paragraph("Dry season harvest window (Dec-Feb); Mile 12/Bodija arbitrage (₦55k-₦90k/basket).", table_cell)
        ],
        [
            Paragraph("<b>🥔 Roots & Tubers</b>", table_cell_bold),
            Paragraph("TME 419, TMS 98/0505, Game-Changer (TMS 01/1368), Yams", table_cell),
            Paragraph("Slanted cuttings (45°), high potassium demand (NPK 12:12:17), <i>CMD2/CMD3</i> mosaic immunity, yam minisett.", table_cell),
            Paragraph("Industrial starch factories & garri clusters paying ₦85,000–₦120,000/ton (>25% dry matter).", table_cell)
        ],
        [
            Paragraph("<b>🌾 Lowland & Upland Rice</b>", table_cell_bold),
            Paragraph("FARO 44 (Siipi), FARO 52 (WITA 4), NERICA L-19 / L-20", table_cell),
            Paragraph("Urea Deep Placement (UDP) cuts nitrogen loss 35%; Alternate Wetting & Drying (AWD); <i>Sub1</i> submergence QTL.", table_cell),
            Paragraph("Integrated commercial paddy milling sales commanding ₦650,000–₦850,000/ton.", table_cell)
        ],
        [
            Paragraph("<b>🌽 Savanna Cereals</b>", table_cell_bold),
            Paragraph("SAMMAZ 15, SAMMAZ 27, SC 719, Oba Super 2, Sorghum, Millet", table_cell),
            Paragraph("Anthesis-Silking Interval (ASI) < 2.5d, canopy stay-green, balanced micro-dosing (60N-30P-30K), Chromosome 1/8 QTLs.", table_cell),
            Paragraph("Smallholder benefit-cost ratio enhancement from 1.35:1 to 2.20:1.", table_cell)
        ],
        [
            Paragraph("<b>🥜 Grain Legumes</b>", table_cell_bold),
            Paragraph("SAMPEA 20-T (Bt Cowpea), TGx 1448-2E Soybean, Groundnut", table_cell),
            Paragraph("<i>Cry1Ab</i> endotoxin against <i>Maruca vitrata</i>; <i>Bradyrhizobium</i> BNF; Aflasafe biocontrol for groundnuts.", table_cell),
            Paragraph("High-protein food security and residual soil nitrogen contribution (40–80 kg N/ha).", table_cell)
        ],
        [
            Paragraph("<b>🌴 Tree Crops / Plantation</b>", table_cell_bold),
            Paragraph("Tenera Oil Palm, F3 Amazon Cocoa, Improved Cashew", table_cell),
            Paragraph("Black pod (<i>Phytophthora</i>) post-rain pruning, Tenera pollinating weevils (<i>Elaeidobius</i>), high potassium/boron.", table_cell),
            Paragraph("Export commodity arbitrage; farmgate cocoa prices commanding historic highs (>₦8M–₦11M/ton).", table_cell)
        ]
    ]
    t_scope = Table(scope_data, colWidths=[90, 110, 184, 120])
    t_scope.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor("#1B5E20")),
        ('BOX', (0, 0), (-1, -1), 0.8, colors.HexColor("#A5D6A7")),
        ('INNERGRID', (0, 0), (-1, -1), 0.5, colors.HexColor("#E0E0E0")),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.HexColor("#FFFFFF"), colors.HexColor("#F9FBE7")]),
        ('TOPPADDING', (0, 0), (-1, -1), 2.5),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 2.5),
        ('LEFTPADDING', (0, 0), (-1, -1), 4),
        ('RIGHTPADDING', (0, 0), (-1, -1), 4),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
    ]))
    story.append(t_scope)
    story.append(Spacer(1, 8))

    # =========================================================================
    # SECTION 5: UPGRADED MODULE 7 & FULL MODULE SUITE
    # =========================================================================
    story.append(KeepTogether([
        Paragraph("5. Enterprise Architecture: Upgraded Module 7 & Platform Suite", h1_style),
        Paragraph(
            "AgriIntel's sidebar modules deliver specialized scientific capability beyond conversational queries. "
            "In response to live testing, <b>Module 7</b> was upgraded into a comprehensive multi-species livestock and poultry suite:",
            body_style
        )
    ]))

    mod7_box = [
        [
            Paragraph(
                "<b>🐾 Module 7: Livestock & Poultry Intelligence Infrastructure (Newly Upgraded Structure)</b><br/>"
                "• <b>Tab 1: 🐄 Bovine & Pastoral Genetics:</b> Multi-trait breeding index configuration (weight, milk, rectal temp, respiration, trypanotolerance) across 100+ cattle genotypes, composite rankings, and interactive scatter biplots.<br/>"
                "• <b>Tab 2: 🐔 Poultry Bioclimatic Housing & Festive Production Simulator:</b><br/>"
                "  - <i>Real-Time Avian THI Engine:</i> Interactive sliders for ambient temperature (°C) and humidity (%) computing the Avian THI index and bioclimatic stress category (Comfort, Mild Alert, Severe Panting / Alkalosis, Critical Danger).<br/>"
                "  - <i>Predictive Impact Analytics:</i> Computes expected drop in feed intake (%), surge in water consumption (%), egg production decline (%), and daily mortality risk.<br/>"
                "  - <i>Festive December Broiler Economics Calculator:</i> Inputs flock size, Day-Old Chick price, feed cost, and festive sale price to project total investment, gross revenue, net festive profit, and ROI (%).<br/>"
                "  - <i>Actionable Bioclimatic Protocol:</i> Step-by-step guidance on diurnal curtain timing (raised midnight–6 AM, dropped 9 AM), feed withdrawal (11:30 AM–3:30 PM), Vitamin C / Sodium Bicarbonate in water, and Newcastle/CRD prophylaxis.<br/>"
                "• <b>Tab 3: 🐐 Small Ruminants & Swine Analytics:</b> West African Dwarf trypanotolerance, 90-day ram fattening formulas, PPR vaccination, swine heat wallowing, and African Swine Fever biosecurity.",
                callout_style
            )
        ]
    ]
    t_mod7 = Table(mod7_box, colWidths=[504])
    t_mod7.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor("#E8F5E9")),
        ('BOX', (0, 0), (-1, -1), 1, colors.HexColor("#2E7D32")),
        ('TOPPADDING', (0, 0), (-1, -1), 5),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 5),
        ('LEFTPADDING', (0, 0), (-1, -1), 7),
        ('RIGHTPADDING', (0, 0), (-1, -1), 7),
    ]))
    story.append(t_mod7)
    story.append(Spacer(1, 8))

    # All Modules Table
    modules_data = [
        [
            Paragraph("Module", table_header),
            Paragraph("Scientific Functionality & Advanced Capabilities", table_header),
            Paragraph("Target User & Output Format", table_header)
        ],
        [
            Paragraph("<b>Module 1: Copilot & Voice</b>", table_cell_bold),
            Paragraph("Agricultural literature synthesis across CGIAR/FAO. <b>Last-Mile Farmer Audio Studio:</b> Generates bilingual broadcast advisories with acoustic chimes in <b>Hausa, Yoruba, Swahili, and Pidgin</b>.", table_cell),
            Paragraph("Extension Agents, Rural Radio Stations, Agricultural NGOs (Audio + Text).", table_cell)
        ],
        [
            Paragraph("<b>Module 2: Autonomous Scientist</b>", table_cell_bold),
            Paragraph("Multi-Environment Trial (MET) processing; Genotype × Environment (GxE) modeling; AMMI variance partitioning; interactive <b>GGE biplots</b> and genotype stability rankings.", table_cell),
            Paragraph("Field Trial Agronomists, CGIAR/NARS Research Stations (Biplots + ANOVA).", table_cell)
        ],
        [
            Paragraph("<b>Module 3: Statistical Geneticist</b>", table_cell_bold),
            Paragraph("Genome-Wide Association Studies (<b>GWAS Manhattan & Q-Q plots</b>); linkage disequilibrium; genomic prediction via rrBLUP and GBLUP; Genomic Estimated Breeding Values (GEBVs).", table_cell),
            Paragraph("Molecular Geneticists, Quantitative Animal & Crop Breeders (Genomic Matrices).", table_cell)
        ],
        [
            Paragraph("<b>Module 4: Plant Breeding Platform</b>", table_cell_bold),
            Paragraph("Speed breeding photoperiod simulation (up to 6 generations/year); crossing block optimization; multi-trait selection index ($I = \sum b_i G_i$); genetic gain trajectory ($R = i r \sigma_A / L$).", table_cell),
            Paragraph("National Breeding Programs, Seed Company R&D Teams (Breeding Roadmaps).", table_cell)
        ],
        [
            Paragraph("<b>Module 5: Soil & Edaphic Intel</b>", table_cell_bold),
            Paragraph("NIR/MIR spectral soil prediction; spatial fertility kriging; micronutrient diagnostics; site-specific variable-rate NPK prescriptions.", table_cell),
            Paragraph("Soil Laboratories, Commercial Farm Agronomists (Fertility Maps + Recipes).", table_cell)
        ],
        [
            Paragraph("<b>Module 6: Climate Resilience</b>", table_cell_bold),
            Paragraph("CHIRPS precipitation tracking; ERA5 thermal anomalies; Standardized Precipitation Evapotranspiration Index (<b>SPEI/SPI</b>); agro-ecological zone shifts.", table_cell),
            Paragraph("Climate Adaptation Planners, Agri-Insurers (Drought Risk Matrices).", table_cell)
        ],
        [
            Paragraph("<b>Module 7: Livestock & Poultry</b>", table_cell_bold),
            Paragraph("Multi-species: Bovine thermotolerance & EBVs (Tab 1); Avian THI bioclimatic stress & Festive Broiler Economics (Tab 2); Small Ruminants & Swine (Tab 3).", table_cell),
            Paragraph("Commercial Dairies, Poultry Integrators, Feedlot Operators (Budgets + Bioclimatics).", table_cell)
        ],
        [
            Paragraph("<b>Module 8: Policy & Economics</b>", table_cell_bold),
            Paragraph("Macroeconomic partial equilibrium modeling; fertilizer subsidy price elasticity simulation; national food security ROI per ₦1B capital allocation.", table_cell),
            Paragraph("Ministries of Agriculture, Central Banks, Development Banks (Policy Briefs).", table_cell)
        ]
    ]
    t_mod = Table(modules_data, colWidths=[110, 274, 120])
    t_mod.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor("#1B5E20")),
        ('BOX', (0, 0), (-1, -1), 0.8, colors.HexColor("#A5D6A7")),
        ('INNERGRID', (0, 0), (-1, -1), 0.5, colors.HexColor("#E0E0E0")),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.HexColor("#FFFFFF"), colors.HexColor("#F9FBE7")]),
        ('TOPPADDING', (0, 0), (-1, -1), 3),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 3),
        ('LEFTPADDING', (0, 0), (-1, -1), 4),
        ('RIGHTPADDING', (0, 0), (-1, -1), 4),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
    ]))
    story.append(t_mod)
    story.append(Spacer(1, 8))

    # =========================================================================
    # SECTION 6: DUAL-TIER ENGINE ARCHITECTURE & SYSTEM HEALTH
    # =========================================================================
    story.append(KeepTogether([
        Paragraph("6. Dual-Tier Intelligence Architecture & Live Verification Status", h1_style),
        Paragraph(
            "AgriIntel maintains a unified dual-tier intelligence model providing maximum resilience in rural "
            "connectivity-constrained African environments while retaining top-tier cloud reasoning:",
            body_style
        )
    ]))

    tier_data = [
        [
            Paragraph("<b>Tier 1: Built-in Offline African Science Engine (Default • 100% Free)</b><br/>"
                      "• Zero internet required, zero API keys needed.<br/>"
                      "• Grounded in verified African research institutions: <b>IITA</b>, <b>NAPRI</b>, <b>FUNAAB</b>, "
                      "<b>NIHORT</b>, <b>AfricaRice</b>, <b>CIMMYT</b>, <b>ILRI</b>, <b>NIFOR</b>, <b>CRIN</b>, and <b>NRCRI</b>.<br/>"
                      "• Features deterministic multi-enterprise semantic parsing for instant, reproducible agronomic and bioclimatic prescriptions.",
                      callout_style),
            Paragraph("<b>Tier 2: Live Multi-Cloud AI Ensemble (Plug-and-Play Cloud Reasoning)</b><br/>"
                      "• Supports <b>Google Gemini API</b> (Free Tier available at AI Studio).<br/>"
                      "• Supports <b>OpenAI API</b> (GPT-4o / GPT-4o-mini).<br/>"
                      "• Supports <b>Groq API</b> (Ultra-fast Llama-3.3 70B inference).<br/>"
                      "• Enables open-ended, real-time natural language reasoning across any crop, animal, or agro-region worldwide.",
                      callout_style)
        ]
    ]
    t_tier = Table(tier_data, colWidths=[248, 248])
    t_tier.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (0, 0), colors.HexColor("#E8F5E9")),
        ('BACKGROUND', (1, 0), (1, 0), colors.HexColor("#F1F8E9")),
        ('BOX', (0, 0), (0, 0), 0.8, colors.HexColor("#81C784")),
        ('BOX', (1, 0), (1, 0), 0.8, colors.HexColor("#AED581")),
        ('TOPPADDING', (0, 0), (-1, -1), 5),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 5),
        ('LEFTPADDING', (0, 0), (-1, -1), 7),
        ('RIGHTPADDING', (0, 0), (-1, -1), 7),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
    ]))
    story.append(t_tier)
    story.append(Spacer(1, 8))

    # Live Verification Box
    status_box = [
        [
            Paragraph(
                "<b>Operational Verification Status:</b><br/>"
                "• <b>Web Application Server:</b> Live & Healthy at <font face='Courier'>http://localhost:8501</font> (HTTP 200 OK).<br/>"
                "• <b>Orchestrator Presets:</b> Poultry and Tomato inquiries pinned as primary 1-click strategic chips.<br/>"
                "• <b>Multi-Enterprise Decoupling:</b> Verified across poultry, cattle, small ruminants, aquaculture, swine, and crops.<br/>"
                "• <b>Module 7 Architecture:</b> Fully active with 3 dedicated tabs including Poultry THI & Festive Broiler Economics Calculator.",
                callout_style
            )
        ]
    ]
    t_status = Table(status_box, colWidths=[504])
    t_status.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor("#E8F5E9")),
        ('BOX', (0, 0), (-1, -1), 1, colors.HexColor("#2E7D32")),
        ('TOPPADDING', (0, 0), (-1, -1), 5),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 5),
        ('LEFTPADDING', (0, 0), (-1, -1), 7),
        ('RIGHTPADDING', (0, 0), (-1, -1), 7),
    ]))
    story.append(t_status)

    doc.build(story, canvasmaker=NumberedCanvas)
    shutil.copyfile(PDF_FILENAME, ALT_FILENAME)
    print(f"Generated {PDF_FILENAME} and copied to {ALT_FILENAME}")


if __name__ == "__main__":
    build_pdf()
