"""
Generates the executive PDF on AgroBiometrix's Pan-African and Global Scope.
"""

from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, HRFlowable
)
from reportlab.pdfgen import canvas

PDF_FILENAME = "AgroBiometrix_Pan_African_and_Global_Strategy.pdf"


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
            self.drawString(54, 755, "AgroBiometrix Strategic Brief — Geographic Scope & Global Architecture")
            self.drawRightString(558, 755, "Africa-First, Globally Relevant")
            self.setStrokeColor(colors.HexColor("#C8E6C9"))
            self.setLineWidth(0.6)
            self.line(54, 750, 558, 750)
            
        # Footer
        page_text = f"Page {self._pageNumber} of {page_count}"
        self.drawString(54, 35, "AgroBiometrix Platform Strategy — Executive Assessment")
        self.drawRightString(558, 35, page_text)
        self.setStrokeColor(colors.HexColor("#C8E6C9"))
        self.setLineWidth(0.6)
        self.line(54, 45, 558, 45)
        self.restoreState()


def create_strategy_pdf():
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
        fontSize=13,
        leading=17,
        textColor=primary_green,
        spaceBefore=12,
        spaceAfter=5,
        keepWithNext=True
    )

    body_style = ParagraphStyle(
        'Body_Custom',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=9,
        leading=13,
        textColor=text_dark,
        spaceAfter=6
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
        fontSize=9.5,
        leading=14,
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
        leading=11,
        textColor=text_dark
    )

    story = []

    # Title & Banner
    story.append(Paragraph("AgroBiometrix: Geographic Scope & Global Scale", title_style))
    story.append(Paragraph("<b>Is AgroBiometrix Focused Only on Nigeria? An Architectural & Strategic Evaluation</b>", subtitle_style))
    story.append(HRFlowable(width="100%", thickness=1.5, color=leaf_green, spaceBefore=0, spaceAfter=8))

    # Core Thesis Callout Box
    thesis_box = [
        [Paragraph("<b>CORE STRATEGIC THESIS: AFRICA-FIRST, GLOBALLY RELEVANT</b>", body_bold)],
        [Paragraph(
            "<i>\"No, AgroBiometrix is not focused only on Nigeria. AgroBiometrix is founded on a bold global thesis: "
            "<b>'The world's agricultural intelligence layer, built from African realities outward.'</b> "
            "While Nigeria serves as an ideal initial proving ground due to its enormous population and rich agro-ecological diversity, "
            "the platform is architected for Pan-African deployment and Global South relevance from Day 1.\"</i>",
            quote_style
        )]
    ]
    t_thesis = Table(thesis_box, colWidths=[504])
    t_thesis.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), pale_bg),
        ('BOX', (0, 0), (-1, -1), 1.2, leaf_green),
        ('PADDING', (0, 0), (-1, -1), 8),
    ]))
    story.append(t_thesis)
    story.append(Spacer(1, 8))

    # SECTION 1: WHY NIGERIA IS THE ANCHOR, NOT THE LIMIT
    story.append(Paragraph("1. Why Nigeria is the Anchor Testbed, Not the Boundary", h1_style))
    story.append(Paragraph(
        "Nigeria represents an optimal initial crucible for agricultural AI for three specific reasons:<br/>"
        "• <b>Complete Agro-Ecological Cross-Section</b>: Nigeria encompasses almost every major tropical agro-ecological zone found across Sub-Saharan Africa—from the per-humid mangrove swamp and humid rainforest in the south, through the Derived and Guinea Savannas, to the semi-arid Sudan Savanna and arid Sahel fringe in the extreme north.<br/>"
        "• <b>Concentrated Agricultural Activity</b>: Over 38 million hectares of arable land and 70% of households engaged in crop and livestock production.<br/>"
        "• <b>High Institutional Density</b>: Headquarters of premier international and regional agricultural research institutes, including the <b>International Institute of Tropical Agriculture (IITA)</b> in Ibadan and the <b>National Animal Production Research Institute (NAPRI)</b> in Shika/Zaria.<br/>"
        "However, agricultural systems, climate corridors, and germplasm do not stop at national borders.",
        body_style
    ))

    # SECTION 2: PAN-AFRICAN ARCHITECTURE
    story.append(Paragraph("2. Pan-African Scope & Multi-Regional Coverage", h1_style))
    story.append(Paragraph(
        "AgroBiometrix is built to serve agricultural ecosystems across Eastern, Western, Central, and Southern Africa:",
        body_style
    ))

    pan_african_data = [
        ("Agro-Ecological Corridors", "• <b>Sudan & Sahelian Zone</b>: Senegal, Mali, Burkina Faso, Niger, Chad, Northern Nigeria, Sudan.<br/>• <b>Guinea Savanna Belt</b>: Ghana, Côte d'Ivoire, Guinea, Togo, Benin, Central African Republic.<br/>• <b>Humid Rainforest & Coastal Zones</b>: Liberia, Sierra Leone, Cameroon, Gabon, DR Congo.<br/>• <b>East African Rift & Highlands</b>: Kenya, Uganda, Rwanda, Burundi, Ethiopia.<br/>• <b>Southern African Sub-Humid Savannas</b>: Malawi, Zambia, Mozambique, Zimbabwe, Angola."),
        ("Indigenous Livestock Breeds", "• <b>West Africa</b>: N'Dama (trypanotolerant humpless taurine), Muturu, Baoulé, Somba, Djallonké sheep.<br/>• <b>East Africa</b>: Boran Zebu (arid beef adaptation), Ankole-Watusi (sanga dairy/cultural), Small East African Zebu.<br/>• <b>Southern Africa</b>: Nguni (tick & drought resistant), Afrikaner, Bonsmara.<br/>• <b>Shared Pastoral Ecotypes</b>: White Fulani (Bunaji), Sokoto Gudali, Red Bororo (Rahaji)."),
        ("Priority Commodity Systems", "• <b>Cereals</b>: Maize (IITA/CIMMYT drought synthetics), Sorghum, Pearl Millet, Upland & Lowland Rice (AfricaRice), Teff (Ethiopian staple).<br/>• <b>Roots & Tubers</b>: Cassava (CMD2/CMD3 resistant varieties across Africa), Yam, Sweet Potato, Plantain.<br/>• <b>Legumes & Oilseeds</b>: Cowpea, Groundnut, Soybean, Pigeon pea."),
        ("Regional Agricultural Bodies", "• <b>AFAAS</b>: African Forum for Agricultural Advisory Services (testing GenAI extension in Nigeria, Kenya, Liberia, Uganda).<br/>• <b>CGIAR Network</b>: IITA, ILRI (Nairobi/Addis Ababa), CIMMYT, AfricaRice, ICRAF.<br/>• <b>Regional Economic Hubs</b>: ASARECA (East/Central), CORAF (West/Central), CCARDESA (Southern Africa).")
    ]

    pan_rows = [[Paragraph(f"<b>{d[0]}</b>", table_cell_style), Paragraph(d[1], table_cell_style)] for d in pan_african_data]
    pan_table = Table([[Paragraph("<b>Strategic Dimension</b>", table_header_style), Paragraph("<b>Pan-African Scope & Geographic Coverage</b>", table_header_style)]] + pan_rows, colWidths=[130, 374])
    pan_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), primary_green),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('GRID', (0, 0), (-1, -1), 0.5, border_green),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, pale_bg]),
        ('PADDING', (0, 0), (-1, -1), 5),
    ]))
    story.append(pan_table)
    story.append(Spacer(1, 10))

    # SECTION 3: GLOBAL RELEVANCE
    story.append(PageBreak())
    story.append(Paragraph("3. Why AgroBiometrix is Globally Relevant", h1_style))
    story.append(Paragraph(
        "AgroBiometrix is not merely a regional software package; it addresses global scientific and economic imperatives:",
        body_style
    ))
    story.append(Paragraph(
        "<b>1. Agricultural Biometrics Know No Geographic Boundaries:</b><br/>"
        "The biometrical engine at the heart of AgroBiometrix—implementing <b>Duncan's Multiple Range Test (DMRT)</b>, <b>Tukey's HSD</b>, <b>Fisher's Protected LSD</b>, <b>Dunnett's Test</b>, <b>Two-Way Factorial ANOVA</b>, and <b>Henderson's Mixed Model BLUP</b>—is universally applicable. "
        "A field agronomist or quantitative geneticist at <i>Wageningen University (Netherlands)</i>, <i>Cornell University (USA)</i>, <i>EMBRAPA (Brazil)</i>, <i>ICAR (India)</i>, or the <i>University of Nairobi (Kenya)</i> uses the exact same mathematical formulas, degrees of freedom, and error protection levels. Any researcher on Earth can upload their trial data into AgroBiometrix and receive instant publication-grade analysis.",
        body_style
    ))
    story.append(Paragraph(
        "<b>2. Global South Climate & Agro-Ecological Analogues:</b><br/>"
        "The challenges AgroBiometrix solves—thermal stress in livestock (THI > 78), vegetative water deficit, sudden drought spells during flowering, low-CEC weathered soils, phosphorus fixation in acidic profiles, and fertilizer price volatility—are shared by over <b>500 million smallholders worldwide</b> across:<br/>"
        "• <b>South Asia</b> (India, Pakistan, Bangladesh, Nepal)<br/>"
        "• <b>Southeast Asia</b> (Vietnam, Indonesia, Philippines)<br/>"
        "• <b>Latin America</b> (Cerrado in Brazil, Llanos in Colombia/Venezuela, Dry corridors in Central America).",
        body_style
    ))
    story.append(Paragraph(
        "<b>3. Planetary-Scale Global Open APIs:</b><br/>"
        "The environmental, soil, and bibliographic engines powering AgroBiometrix are not restricted to Nigerian coordinates:<br/>"
        "• <b>NASA POWER API</b>: Delivers global solar radiation, precipitation, and relative humidity for any latitude/longitude on Earth.<br/>"
        "• <b>Open-Meteo API</b>: Global numerical weather models and high-resolution forecasts worldwide.<br/>"
        "• <b>ISRIC SoilGrids</b>: Planetary soil profile database mapped at 250m resolution across all continents.<br/>"
        "• <b>FAOSTAT & Crossref APIs</b>: Universal global trade, agricultural production statistics, and peer-reviewed DOI literature metadata.",
        body_style
    ))

    # SECTION 4: MULTI-COUNTRY EXPANSION ROADMAP
    story.append(Paragraph("4. Country & Currency Scalability Roadmap", h1_style))
    story.append(Paragraph(
        "The application architecture is designed with modular parameter files enabling instant country switching:",
        body_style
    ))

    roadmap_data = [
        ("Phase 1: Anchor Market (Current)", "Nigeria", "₦ (NGN)", "IAR / NAPRI / IITA (Ibadan) / NCRI (Badeggi)"),
        ("Phase 2: East Africa Expansion", "Kenya, Uganda, Ethiopia, Rwanda", "KSh, USh, ETB, RWF", "KALRO / NARO / EIAR / ILRI (Nairobi & Addis)"),
        ("Phase 3: West & Central Africa", "Ghana, Côte d'Ivoire, Senegal, Cameroon", "GH₵, CFA (XOF/XAF)", "CSIR (Ghana) / ISRA (Senegal) / AfricaRice"),
        ("Phase 4: Southern Africa & SADC", "Malawi, Zambia, Zimbabwe, Mozambique", "MWK, ZMW, ZiG, MZN", "DARS (Malawi) / ZARI (Zambia) / CIMMYT-Harare"),
        ("Phase 5: Global South Expansion", "India, Brazil, Colombia, Vietnam", "₹ (INR), R$ (BRL), $ (COP), ₫ (VND)", "ICAR (India) / EMBRAPA (Brazil) / CIAT (Colombia)")
    ]

    road_rows = [[Paragraph(f"<b>{r[0]}</b>", table_cell_style), Paragraph(r[1], table_cell_style), Paragraph(f"<code>{r[2]}</code>", table_cell_style), Paragraph(r[3], table_cell_style)] for r in roadmap_data]
    road_table = Table([[Paragraph("<b>Phase & Horizon</b>", table_header_style), Paragraph("<b>Target Countries</b>", table_header_style), Paragraph("<b>Currencies</b>", table_header_style), Paragraph("<b>Primary Institutional Partners</b>", table_header_style)]] + road_rows, colWidths=[110, 130, 85, 179])
    road_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), primary_green),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('GRID', (0, 0), (-1, -1), 0.5, border_green),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, pale_bg]),
        ('PADDING', (0, 0), (-1, -1), 4.5),
    ]))
    story.append(road_table)
    story.append(Spacer(1, 12))

    story.append(Paragraph(
        "<b>Summary Conclusion:</b> AgroBiometrix is fundamentally built to be <b>the world's agricultural intelligence layer</b>. "
        "Anchored in African realities, powered by universal mathematical and biometrical principles, and accessible across the globe.",
        body_bold
    ))

    doc.build(story, canvasmaker=NumberedCanvas)
    print(f"Generated {PDF_FILENAME} successfully!")


if __name__ == "__main__":
    create_strategy_pdf()
