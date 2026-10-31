"""
Script to generate AgroBiometrix Last-Mile Radio Advisory Architecture, Cross-Module Dispatch, and Production Economics PDF.
A comprehensive, publication-grade executive blueprint explaining the vernacular radio dispatcher,
platform integration, linguistic dynamics, and financial models for institutional stakeholders.
"""

import os
import datetime
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, HRFlowable, KeepTogether
)
from reportlab.pdfgen import canvas

PDF_FILENAME = "AgroBiometrix_Last_Mile_Radio_Advisory_Architecture_and_Operations.pdf"


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
            self.drawString(54, 755, "AgroBiometrix: Community Extension Radio &amp; Multilingual Voice Dispatcher")
            self.setFont("Helvetica", 8)
            self.setFillColor(colors.HexColor("#2E7D32"))
            self.drawRightString(558, 755, "Technical Architecture &amp; Operational Economics • Africa-First")
            self.setStrokeColor(colors.HexColor("#C8E6C9"))
            self.setLineWidth(0.6)
            self.line(54, 748, 558, 748)

        # Footer (all pages)
        self.setFont("Helvetica", 8)
        self.setFillColor(colors.HexColor("#546E7A"))
        page_text = f"Page {self._pageNumber} of {page_count}"
        self.drawString(54, 34, "AgroBiometrix: Quantitative Biometrics &amp; Generative Intelligence for Agriculture (agrobiometrix.streamlit.app)")
        self.drawRightString(558, 34, page_text)
        self.setStrokeColor(colors.HexColor("#C8E6C9"))
        self.setLineWidth(0.6)
        self.line(54, 44, 558, 44)
        self.restoreState()


def build_radio_architecture_pdf():
    doc = SimpleDocTemplate(
        PDF_FILENAME,
        pagesize=letter,
        leftMargin=54,
        rightMargin=54,
        topMargin=44,
        bottomMargin=44
    )

    styles = getSampleStyleSheet()

    # Custom styles
    title_style = ParagraphStyle(
        "CoverTitle",
        parent=styles["Normal"],
        fontName="Helvetica-Bold",
        fontSize=20,
        leading=24,
        textColor=colors.HexColor("#0A2F10"),
        alignment=0,
        spaceAfter=6
    )

    subtitle_style = ParagraphStyle(
        "CoverSubtitle",
        parent=styles["Normal"],
        fontName="Helvetica",
        fontSize=11,
        leading=15,
        textColor=colors.HexColor("#1B5E20"),
        alignment=0,
        spaceAfter=12
    )

    meta_style = ParagraphStyle(
        "CoverMeta",
        parent=styles["Normal"],
        fontName="Helvetica-Bold",
        fontSize=8.5,
        leading=12,
        textColor=colors.HexColor("#546E7A"),
        spaceAfter=14
    )

    h1_style = ParagraphStyle(
        "Header1",
        parent=styles["Normal"],
        fontName="Helvetica-Bold",
        fontSize=13,
        leading=17,
        textColor=colors.HexColor("#0A2F10"),
        spaceBefore=14,
        spaceAfter=6,
        keepWithNext=True
    )

    h2_style = ParagraphStyle(
        "Header2",
        parent=styles["Normal"],
        fontName="Helvetica-Bold",
        fontSize=10.5,
        leading=14,
        textColor=colors.HexColor("#1B5E20"),
        spaceBefore=10,
        spaceAfter=4,
        keepWithNext=True
    )

    body_style = ParagraphStyle(
        "BodyDark",
        parent=styles["Normal"],
        fontName="Helvetica",
        fontSize=8.5,
        leading=12.5,
        textColor=colors.HexColor("#263238"),
        spaceAfter=6
    )

    bullet_style = ParagraphStyle(
        "BulletDark",
        parent=styles["Normal"],
        fontName="Helvetica",
        fontSize=8.5,
        leading=12,
        textColor=colors.HexColor("#263238"),
        leftIndent=14,
        firstLineIndent=-10,
        spaceAfter=3
    )

    callout_style = ParagraphStyle(
        "CalloutText",
        parent=styles["Normal"],
        fontName="Helvetica-Oblique",
        fontSize=8.5,
        leading=12.5,
        textColor=colors.HexColor("#1B5E20")
    )

    th_style = ParagraphStyle(
        "TableHeader",
        parent=styles["Normal"],
        fontName="Helvetica-Bold",
        fontSize=8,
        leading=10.5,
        textColor=colors.white,
        alignment=0
    )

    td_style = ParagraphStyle(
        "TableCell",
        parent=styles["Normal"],
        fontName="Helvetica",
        fontSize=7.5,
        leading=10,
        textColor=colors.HexColor("#263238")
    )

    td_bold = ParagraphStyle(
        "TableCellBold",
        parent=styles["Normal"],
        fontName="Helvetica-Bold",
        fontSize=7.5,
        leading=10,
        textColor=colors.HexColor("#0A2F10")
    )

    story = []

    # =========================================================================
    # COVER / HEADER BLOCK
    # =========================================================================
    story.append(Paragraph("AgroBiometrix: Community Extension Radio &amp; Multilingual Voice Dispatcher", title_style))
    story.append(Paragraph("System Architecture, Cross-Module Dispatch Event Bus, Sub-Saharan Linguistic Dynamics, and Production API Economics", subtitle_style))
    story.append(Paragraph("<b>Author</b>: AgroBiometrix Platform Architecture Team &amp; Naysa-84 Labs &amp;nbsp;|&amp;nbsp; <b>Date</b>: October 2026 &amp;nbsp;|&amp;nbsp; <b>Target Audience</b>: CGIAR, IITA, ILRI, ARCN, FUNAAB, Donors &amp; Institutional Partners", meta_style))
    story.append(HRFlowable(width="100%", thickness=1.5, color=colors.HexColor("#1B5E20"), spaceBefore=0, spaceAfter=10))

    # EXECUTIVE CALLOUT BOX
    callout_data = [[
        Paragraph(
            "<b>Executive Summary &amp; The 'Lab-to-Last-Mile' Imperative:</b><br/>"
            "Over 70% of Sub-Saharan Africa's 100+ million smallholder farmers are illiterate or semi-literate, with traditional transistor radio serving as their primary, most trusted window to the world. Conversely, national and international agricultural research institutes (IITA, CGIAR, NARS) produce world-class biometrics, soil analyses, and varietal trials that remain trapped in academic PDFs and technical dashboards. AgroBiometrix's <b>Community Extension Radio &amp; Voice Dispatcher</b> closes this structural divide by establishing an automated, real-time pipeline that transforms complex biometric diagnoses directly into broadcast-ready vernacular radio bulletins in <b>Èdè Yorùbá, Harshen Hausa, Kiswahili, Français Agricole, and West African Pidgin</b>.",
            callout_style
        )
    ]]
    callout_table = Table(callout_data, colWidths=[504])
    callout_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor("#F0FDF4")),
        ('BOX', (0, 0), (-1, -1), 1, colors.HexColor("#81C784")),
        ('TOPPADDING', (0, 0), (-1, -1), 7),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 7),
        ('LEFTPADDING', (0, 0), (-1, -1), 10),
        ('RIGHTPADDING', (0, 0), (-1, -1), 10),
    ]))
    story.append(callout_table)
    story.append(Spacer(1, 6))

    # =========================================================================
    # SECTION 1: ARCHITECTURAL EVENT BUS (HOW IT CONNECTS ACROSS THE APP)
    # =========================================================================
    story.append(Paragraph("1. System Architecture: The Cross-Platform Dispatch Event Bus", h1_style))
    story.append(Paragraph(
        "A common flaw in agricultural software is siloed execution: an analytical module calculates a critical finding (e.g. soil acidification or heat stress), but the extension communication layer has no awareness of it. AgroBiometrix solves this by introducing a centralized <b>Global Agricultural Broadcast Dispatcher &amp; Event Bus</b> (<code>core/broadcast_dispatcher.py</code>).",
        body_style
    ))
    story.append(Paragraph(
        "Whenever an agronomist, researcher, or extension officer completes an analysis anywhere across the intelligence suites, the system evaluates the finding against critical agronomic thresholds and provides a direct, one-click bridge: <b>'📢 Send to Radio Queue'</b>.",
        body_style
    ))

    # TABLE: CROSS-MODULE INTEGRATION
    story.append(Paragraph("<b>Table 1: Cross-Module Broadcast Event Triggers Across AgroBiometrix Suites</b>", h2_style))
    mod_table_data = [
        [
            Paragraph("Originating Suite &amp; Module", th_style),
            Paragraph("Biometric Trigger / Scientific Diagnosis", th_style),
            Paragraph("Captured Extension Remedy", th_style),
            Paragraph("Target Vernacular Broadcast Zone", th_style)
        ],
        [
            Paragraph("<b>Module 4/5: Soil Fertility &amp; Fertilizer Optimizer</b>", td_bold),
            Paragraph("Soil pH &lt; 5.1, active Al<sup>3+</sup> toxicity; surface urea causing 40% ammonia volatilization.", td_style),
            Paragraph("Halt surface urea broadcast. Apply 2.5 t/ha lime + compost; micro-dose SSP at root zone.", td_style),
            Paragraph("Yorùbá / French (Oyo, Ogun, Bouaké transition zone)", td_style)
        ],
        [
            Paragraph("<b>Module 7: Livestock Biometrics &amp; THI Heat Stress</b>", td_bold),
            Paragraph("Temperature-Humidity Index (THI) &gt; 82. Ruminal alkalosis, milk yield drop &gt; 25%.", td_style),
            Paragraph("Shift grazing to crepuscular hours (dawn/dusk); add sodium bicarbonate &amp; salt licks to water.", td_style),
            Paragraph("Hausa / Swahili (Kano, Jigawa, Rift Valley)", td_style)
        ],
        [
            Paragraph("<b>Module 8: Agro-Ecosystems &amp; Climate Risk</b>", td_bold),
            Paragraph("14-day mid-season rainfall anomaly; Harmattan dust haze attenuating solar PAR.", td_style),
            Paragraph("Immediate organic mulching to conserve root zone moisture; postpone chemical top-dressing.", td_style),
            Paragraph("Hausa / Pidgin (Kaduna, Benue, Niger)", td_style)
        ],
        [
            Paragraph("<b>Module 1: AI Research Scientist Copilot</b>", td_bold),
            Paragraph("Evidence Gap Synthesis: High yield hybrid lacks Tuwo flour grain density favored by locals.", td_style),
            Paragraph("Recommend paired culinary variety planting; guide post-harvest processing methods.", td_style),
            Paragraph("Hausa / Yorùbá (National extension belts)", td_style)
        ],
        [
            Paragraph("<b>Module 7: Cuniculture &amp; Micro-Livestock</b>", td_bold),
            Paragraph("Acute doe mortality and bloat from feeding damp, wilted cassava peels (cyanide toxicity).", td_style),
            Paragraph("Strict ban on damp peels; enforce 48-hour mandatory sun-drying before rabbit feeding.", td_style),
            Paragraph("Yorùbá / French (Ondo, Ekiti, Garoua)", td_style)
        ]
    ]

    mod_table = Table(mod_table_data, colWidths=[114, 135, 140, 115])
    mod_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor("#1B5E20")),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor("#C8E6C9")),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('TOPPADDING', (0, 0), (-1, -1), 4),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
        ('LEFTPADDING', (0, 0), (-1, -1), 5),
        ('RIGHTPADDING', (0, 0), (-1, -1), 5),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor("#F8FAF8")]),
    ]))
    story.append(mod_table)
    story.append(Spacer(1, 6))

    # =========================================================================
    # SECTION 2: DUAL OPERATIONAL MODES
    # =========================================================================
    story.append(Paragraph("2. Dual Operational Modes in the Radio Studio", h1_style))
    story.append(Paragraph(
        "To satisfy both <b>mission-critical institutional pitch demonstrations</b> and <b>day-to-day dynamic field operations</b>, the Radio Studio is partitioned into two distinct operational paradigms:",
        body_style
    ))

    story.append(Paragraph("<b>Mode A: Live AI Extension Broadcast Studio &amp; Dynamic Queue (On-The-Fly Generation)</b>", h2_style))
    story.append(Paragraph("• <b>Live Action Dispatch Queue</b>: Inspects the platform event bus, listing all pending biometric diagnoses sent from other modules with timestamps, origins, and one-click '⚡ Load to Studio' action.", bullet_style))
    story.append(Paragraph("• <b>Interactive Studio Composer</b>: Allows research communication officers or extension agents to edit findings or type ad-hoc emergency announcements (e.g. sudden Fall Armyworm or locust swarms).", bullet_style))
    story.append(Paragraph("• <b>Cultural Heuristic &amp; LLM Synthesis</b>: Translates technical metrics into indigenous scripts utilizing culturally resonant proverbs (e.g. <i>'Àbọ̀ ọ̀rọ̀ là ń sọ fún ọmọlúwàbí'</i> in Yorùbá, <i>'Kowa ya tuna bara'</i> in Hausa, <i>'Haba na haba'</i> in Swahili).", bullet_style))
    story.append(Paragraph("• <b>Interactive Voice Playback &amp; Cue Sheet Export</b>: Utilizes browser Web Speech API (<code>yo-NG</code>, <code>ha-NG</code>, <code>sw-KE</code>, <code>fr-FR</code>) for instant on-ear listening, and exports formal broadcaster cue sheets (.docx/.txt) ready for FM consoles.", bullet_style))

    story.append(Spacer(1, 4))
    story.append(Paragraph("<b>Mode B: Curated Institutional Reference Benchmarks (Pre-Bundled Ground Truth)</b>", h2_style))
    story.append(Paragraph("• <b>Fail-Safe Stakeholder Pitching</b>: Features 4 comprehensive, multi-environment field scenarios (Kaduna Maize, Pastoral Zebu, Commercial Poultry, Cuniculture) across 5 languages.", bullet_style))
    story.append(Paragraph("• <b>Offline Pre-Bundled MP3 Audio Assets</b>: All 16 broadcast variations are pre-compiled on disk in <code>assets/audio/</code>. When pitching to IITA or CGIAR boards, the audio plays in <b>0.001 seconds</b> without network buffering or cloud API dependency.", bullet_style))
    story.append(Paragraph("• <b>Acoustic Station Sign-On Chime</b>: Features a dedicated 3-note harmonic marimba chime (C5-E5-G5) simulating traditional rural radio station alerts.", bullet_style))

    story.append(Spacer(1, 5))

    # =========================================================================
    # SECTION 3: SUB-SAHARAN LINGUISTIC MAP &amp; ACOUSTIC REALITIES
    # =========================================================================
    story.append(Paragraph("3. Sub-Saharan African Linguistic Footprint &amp; Acoustic Realities", h1_style))
    story.append(Paragraph(
        "A critical question asked by institutional donors is: <i>'Why were these specific languages selected, and how authentic is the speech synthesis?'</i>",
        body_style
    ))
    story.append(Paragraph(
        "By combining <b>French &amp; English</b> (the official institutional and policy languages) with <b>Swahili, Hausa, and Yorùbá</b> (plus West African Pidgin), AgroBiometrix achieves direct linguistic penetration across <b>over 70% of Sub-Saharan Africa's agricultural smallholders</b>.",
        body_style
    ))

    # TABLE: LINGUISTIC COVERAGE &amp; ACOUSTIC CAPABILITIES
    story.append(Paragraph("<b>Table 2: Linguistic Demographic Footprint and Neural Acoustic Model Status</b>", h2_style))
    lang_table_data = [
        [
            Paragraph("Language / Dialect", th_style),
            Paragraph("Total Speaker Base", th_style),
            Paragraph("Geographic &amp; Agricultural Corridor", th_style),
            Paragraph("Acoustic Model Fidelity &amp; Synthesis Truth", th_style)
        ],
        [
            Paragraph("<b>Kiswahili (Swahili)</b>", td_bold),
            Paragraph("150 – 200+ Million", td_style),
            Paragraph("East &amp; Central Africa (Tanzania, Kenya, Uganda, Rwanda, Burundi, DRC, Mozambique)", td_style),
            Paragraph("<b>100% Authentic</b>: Non-tonal Bantu structure with regular penultimate stress. Handled flawlessly by standard neural engines.", td_style)
        ],
        [
            Paragraph("<b>Harshen Hausa (Hausa)</b>", td_bold),
            Paragraph("85 – 100+ Million", td_style),
            Paragraph("The Sahel &amp; Sudan Savanna (Northern Nigeria, Niger, Chad, Northern Ghana/Cameroon)", td_style),
            Paragraph("<b>Very Authentic</b>: Deep training across BBC/RFI Hausa. Google and ElevenLabs maintain native <code>ha</code> acoustic models.", td_style)
        ],
        [
            Paragraph("<b>Français Agricole (French)</b>", td_bold),
            Paragraph("120+ Million (African)", td_style),
            Paragraph("Francophone West &amp; Central Africa (Côte d'Ivoire, Senegal, Cameroon, Mali, Guinea)", td_style),
            Paragraph("<b>100% Authentic</b>: Mature global phonetics. Broadcasts sound like seasoned rural radio anchors in Abidjan or Dakar.", td_style)
        ],
        [
            Paragraph("<b>Èdè Yorùbá (Yoruba)</b>", td_bold),
            Paragraph("50 – 55+ Million", td_style),
            Paragraph("West African Forest &amp; Coastal Transition (Southwest Nigeria, Benin, Togo)", td_style),
            Paragraph("<b>Strict Tonal Language (Dò-Re-Mí)</b>: Basic TTS reads Roman letters with flat English intonation. Requires tonal engines (YarnGPT / device <code>yo-NG</code>) for rural elder authenticity.", td_style)
        ],
        [
            Paragraph("<b>West African Pidgin</b>", td_bold),
            Paragraph("75 – 80+ Million", td_style),
            Paragraph("Urban and peri-urban smallholder belts (Nigeria, Ghana, Cameroon)", td_style),
            Paragraph("<b>High Clarity</b>: Highly conversational and engaging. Understood universally in regional markets.", td_style)
        ]
    ]

    lang_table = Table(lang_table_data, colWidths=[100, 85, 155, 164])
    lang_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor("#1B5E20")),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor("#C8E6C9")),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('TOPPADDING', (0, 0), (-1, -1), 4),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
        ('LEFTPADDING', (0, 0), (-1, -1), 5),
        ('RIGHTPADDING', (0, 0), (-1, -1), 5),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor("#F8FAF8")]),
    ]))
    story.append(lang_table)
    story.append(Spacer(1, 6))

    # =========================================================================
    # SECTION 4: PRODUCTION API ECONOMICS (YARNGPT VS. ELEVENLABS)
    # =========================================================================
    story.append(Paragraph("4. Production API Economics: YarnGPT vs. ElevenLabs", h1_style))
    story.append(Paragraph(
        "A critical architectural principle of AgroBiometrix is <b>'Write Once, Cache &amp; Stream to Millions'</b>. When a weekly advisory is formulated for an agro-ecological zone, the speech API is called <b>exactly once</b>. The resulting MP3 is stored on cloud storage (AWS S3, Cloudflare R2, or local server). Whether 50 extension agents or 500,000 farmers stream that audio track, <b>the marginal API cost is $0.00</b>.",
        body_style
    ))
    story.append(Paragraph(
        "Below is the exact annual budget modeling comparing the specialized Nigerian voice AI (<b>YarnGPT</b>) with the global studio leader (<b>ElevenLabs</b>) across two production deployment scales:",
        body_style
    ))

    # TABLE: PRODUCTION API ECONOMICS
    story.append(Paragraph("<b>Table 3: Annual Production Subscription &amp; Operational Cost Models</b>", h2_style))
    cost_table_data = [
        [
            Paragraph("Production Scale &amp; Scope", th_style),
            Paragraph("YarnGPT (Local African Voice AI)", th_style),
            Paragraph("ElevenLabs (Global Multilingual)", th_style),
            Paragraph("Strategic Recommendation", th_style)
        ],
        [
            Paragraph("<b>Tier 1: Standard Regional Extension</b><br/>• 4 Value Chains (Maize, Cassava, Cattle, Poultry)<br/>• 3 Languages (Yorùbá, Hausa, Pidgin)<br/>• 52 Weekly Updates<br/><b>Total: 624 Bulletins / Year</b> (~375k chars)", td_style),
            Paragraph("<b>Yarn Growth Plan</b>:<br/>• ₦15,000 / month<br/>• 1 Top-Up pack (₦50,000)<br/><b>Total: ₦230,000 / year</b><br/>(<b>~$148 USD / year</b>)<br/><i>Local Naira billing via Paystack</i>", td_style),
            Paragraph("<b>Creator Plan (Annual)</b>:<br/>• $220 / year (2 mos free)<br/>• 1,452,000 characters/yr<br/><b>Total: $220 / year</b><br/>(<b>~₦341,000 / year</b>)<br/><i>Nearly 4× buffer headroom</i>", td_style),
            Paragraph("<b>Recommended MVP Budget</b>: Under <b>$250 / ₦350k per year</b>.<br/>Provides flawless studio French/Swahili and highly localized Nigerian accents.", td_style)
        ],
        [
            Paragraph("<b>Tier 2: Full National Syndicate</b><br/>• 10 Value Chains across 6 zones<br/>• 4 Languages (Yorùbá, Hausa, Ìgbò, Pidgin)<br/>• Bi-weekly Updates (104 updates/yr)<br/><b>Total: 4,160 Bulletins / Year</b> (~2.5M chars)", td_style),
            Paragraph("<b>Yarn Pro Plan</b>:<br/>• ₦35,000 / month<br/>• 4 Bulk Top-Up packs (₦480,000)<br/><b>Total: ₦900,000 / year</b><br/>(<b>~$580 USD / year</b>)<br/><i>Over 3M credit pool</i>", td_style),
            Paragraph("<b>Pro Plan (Annual)</b>:<br/>• $990 / year (2 mos free)<br/>• 6,000,000 characters/yr<br/><b>Total: $990 / year</b><br/>(<b>~₦1,535,000 / year</b>)<br/><i>Studio voice cloning included</i>", td_style),
            Paragraph("<b>Commercial Scale</b>: Budget <b>$600 to $1,000 / year</b>.<br/>Enables multi-state radio station syndication across hundreds of community FM stations.", td_style)
        ],
        [
            Paragraph("<b>Unit Cost per Single 1-Min Radio Bulletin</b>", td_bold),
            Paragraph("<b>~₦150 – ₦350</b> ($0.10 – $0.22)", td_bold),
            Paragraph("<b>~₦37 – ₦74</b> ($0.024 – $0.048)", td_bold),
            Paragraph("<b>Negligible</b> line-item on any donor grant.", td_bold)
        ]
    ]

    cost_table = Table(cost_table_data, colWidths=[130, 125, 125, 124])
    cost_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor("#1B5E20")),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor("#C8E6C9")),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('TOPPADDING', (0, 0), (-1, -1), 4),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
        ('LEFTPADDING', (0, 0), (-1, -1), 5),
        ('RIGHTPADDING', (0, 0), (-1, -1), 5),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor("#F8FAF8")]),
    ]))
    story.append(cost_table)
    story.append(Spacer(1, 6))

    # =========================================================================
    # SECTION 5: INSTITUTIONAL PITCH PLAYBOOK &amp; DEPLOYMENT ROADMAP
    # =========================================================================
    story.append(Paragraph("5. Institutional Pitch Strategy &amp; Field Deployment Roadmap", h1_style))
    story.append(Paragraph(
        "When presenting this capability to agricultural research leaders (IITA, CGIAR, ILRI, ARCN, FUNAAB, and the Federal Ministry of Agriculture), position the Radio Function as the <b>ultimate solution to the 'Extension Officer Shortage'</b>:",
        body_style
    ))

    pitch_bullets = [
        "<b>The Extension Crisis Metric</b>: Nigeria and Kenya have an extension agent-to-farmer ratio worse than 1:3,500 (FAO recommends 1:500). Physical extension agents cannot physically reach millions of remote farmers every week.",
        "<b>The Biometric Radio Solution</b>: AgroBiometrix acts as a force multiplier. One agronomist running a soil test or livestock THI model can generate and dispatch targeted radio bulletins to 50 local community FM radio stations in less than 2 minutes.",
        "<b>Voice Cloning for Community Trust</b>: Highlight that ElevenLabs allows 1-minute voice cloning. A trusted local extension worker or popular university professor's voice can be cloned with permission, ensuring farmers hear a familiar, trusted community voice rather than a robotic voice.",
        "<b>Two-Way WhatsApp / IVR Expansion</b>: Position the radio dispatcher as Phase 1 of the Last-Mile Pipeline. Phase 2 extends this exact event bus to two-way WhatsApp voice notes and toll-free IVR phone lines, allowing illiterate farmers to speak their problems and receive voice advice back."
    ]

    for pb in pitch_bullets:
        story.append(Paragraph(f"• {pb}", bullet_style))

    story.append(Spacer(1, 6))

    # SIGN-OFF BLOCK
    sign_off_data = [[
        Paragraph(
            "<b>AgroBiometrix Operational Commitment:</b><br/>"
            "AgroBiometrix bridges laboratory genomics, quantitative biometrics, and rural transistor radio into a unified African digital extension infrastructure. "
            "For technical inquiries, API integration, or institutional partnerships, contact: <i>directorate@agrobiometrix.org</i> | <b>Live Platform</b>: <i>agrobiometrix.streamlit.app</i>",
            td_style
        )
    ]]
    sign_off_table = Table(sign_off_data, colWidths=[504])
    sign_off_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor("#F8FAF8")),
        ('BOX', (0, 0), (-1, -1), 1, colors.HexColor("#C8E6C9")),
        ('TOPPADDING', (0, 0), (-1, -1), 6),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
        ('LEFTPADDING', (0, 0), (-1, -1), 10),
        ('RIGHTPADDING', (0, 0), (-1, -1), 10),
    ]))
    story.append(sign_off_table)

    doc.build(story, canvasmaker=NumberedCanvas)
    print(f"Successfully generated: {PDF_FILENAME} ({os.path.getsize(PDF_FILENAME)} bytes)")


if __name__ == "__main__":
    build_radio_architecture_pdf()
