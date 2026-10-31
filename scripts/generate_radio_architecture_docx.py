"""
Script to generate AgroBiometrix Last-Mile Radio Advisory Architecture and Operations DOCX.
Companion editable document for institutional stakeholders.
"""

import os
from docx import Document
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml import OxmlElement, parse_xml
from docx.oxml.ns import nsdecls, qn

DOCX_FILENAME = "AgroBiometrix_Last_Mile_Radio_Advisory_Architecture_and_Operations.docx"

def set_cell_background(cell, fill_hex):
    shading_elm = parse_xml(f'<w:shd {nsdecls("w")} w:fill="{fill_hex}"/>')
    cell._tc.get_or_add_tcPr().append(shading_elm)

def set_cell_margins(cell, top=100, bottom=100, left=150, right=150):
    tcPr = cell._tc.get_or_add_tcPr()
    tcMar = OxmlElement('w:tcMar')
    for margin_name, val in [('top', top), ('bottom', bottom), ('left', left), ('right', right)]:
        node = OxmlElement(f'w:{margin_name}')
        node.set(qn('w:w'), str(val))
        node.set(qn('w:type'), 'dxa')
        tcMar.append(node)
    tcPr.append(tcMar)

def create_document():
    doc = Document()

    for sec in doc.sections:
        sec.top_margin = Inches(0.75)
        sec.bottom_margin = Inches(0.75)
        sec.left_margin = Inches(0.75)
        sec.right_margin = Inches(0.75)

    # Document Header / Title
    p_title = doc.add_paragraph()
    r_title = p_title.add_run("AgroBiometrix: Community Extension Radio & Multilingual Voice Dispatcher")
    r_title.bold = True
    r_title.font.name = "Arial"
    r_title.font.size = Pt(18)
    r_title.font.color.rgb = RGBColor(10, 47, 16)
    p_title.paragraph_format.space_after = Pt(4)

    p_sub = doc.add_paragraph()
    r_sub = p_sub.add_run("Technical Architecture, Cross-Module Dispatch Event Bus, Sub-Saharan Linguistic Dynamics, and Production API Economics")
    r_sub.font.name = "Arial"
    r_sub.font.size = Pt(11)
    r_sub.font.color.rgb = RGBColor(27, 94, 32)
    p_sub.paragraph_format.space_after = Pt(6)

    p_meta = doc.add_paragraph()
    r_meta = p_meta.add_run("Author: AgroBiometrix Platform Architecture Team & Naysa-84 Labs  |  Date: October 2026  |  Audience: CGIAR, IITA, ILRI, ARCN, FUNAAB, Donors")
    r_meta.font.name = "Arial"
    r_meta.font.size = Pt(8.5)
    r_meta.font.color.rgb = RGBColor(84, 110, 122)
    r_meta.italic = True
    p_meta.paragraph_format.space_after = Pt(12)

    # Executive Summary Callout Box
    table_callout = doc.add_table(rows=1, cols=1)
    table_callout.alignment = WD_TABLE_ALIGNMENT.CENTER
    cell_callout = table_callout.rows[0].cells[0]
    cell_callout.width = Inches(7.0)
    set_cell_background(cell_callout, "F0FDF4")
    set_cell_margins(cell_callout, top=140, bottom=140, left=180, right=180)

    p_c = cell_callout.paragraphs[0]
    r_c_bold = p_c.add_run("Executive Summary & The 'Lab-to-Last-Mile' Imperative:\n")
    r_c_bold.bold = True
    r_c_bold.font.name = "Arial"
    r_c_bold.font.size = Pt(9)
    r_c_bold.font.color.rgb = RGBColor(27, 94, 32)

    r_c_text = p_c.add_run(
        "Over 70% of Sub-Saharan Africa's 100+ million smallholder farmers rely on traditional transistor radio as their primary, "
        "most trusted agricultural advisory medium. However, cutting-edge biometric findings, soil test interpretations, and breeding trials "
        "remain trapped in academic research papers that rural smallholders never see. AgroBiometrix's Community Extension Radio & Voice Dispatcher "
        "closes this gap by establishing an automated, real-time pipeline that transforms complex biometric calculations directly into "
        "broadcast-ready spoken vernacular radio bulletins in Èdè Yorùbá, Harshen Hausa, Kiswahili, Français Agricole, and West African Pidgin."
    )
    r_c_text.font.name = "Arial"
    r_c_text.font.size = Pt(8.5)
    r_c_text.font.color.rgb = RGBColor(27, 94, 32)

    doc.add_paragraph().paragraph_format.space_after = Pt(6)

    # Section 1
    h1 = doc.add_heading(level=1)
    r_h1 = h1.add_run("1. System Architecture: The Cross-Platform Dispatch Event Bus")
    r_h1.font.name = "Arial"
    r_h1.font.color.rgb = RGBColor(10, 47, 16)

    p1 = doc.add_paragraph(
        "A common flaw in agricultural platforms is siloed execution: an analytical module calculates an urgent finding (e.g., severe soil acidification or heat stress), "
        "but the extension communication layer has no awareness of it. AgroBiometrix solves this by introducing a centralized Global Agricultural Broadcast Dispatcher & Event Bus "
        "(core/broadcast_dispatcher.py). Whenever an agronomist or researcher completes an analysis across any module, the platform evaluates the finding against critical agronomic "
        "thresholds and provides an immediate bridge: '📢 Send to Radio Queue'."
    )
    p1.paragraph_format.space_after = Pt(8)

    # Table 1: Cross-Module Integration
    t1 = doc.add_table(rows=6, cols=4)
    t1.alignment = WD_TABLE_ALIGNMENT.CENTER
    headers = ["Originating Suite & Module", "Biometric Trigger / Scientific Diagnosis", "Captured Extension Remedy", "Target Broadcast Zone"]
    col_widths = [Inches(1.8), Inches(1.9), Inches(1.8), Inches(1.5)]

    for j, h in enumerate(headers):
        cell = t1.cell(0, j)
        cell.width = col_widths[j]
        set_cell_background(cell, "1B5E20")
        set_cell_margins(cell, top=80, bottom=80, left=100, right=100)
        p = cell.paragraphs[0]
        r = p.add_run(h)
        r.bold = True
        r.font.name = "Arial"
        r.font.size = Pt(8)
        r.font.color.rgb = RGBColor(255, 255, 255)

    rows_data = [
        ("Module 4/5: Soil Fertility & Fertilizer Optimizer", "Soil pH < 5.1, active Al3+ toxicity; surface urea causing 40% ammonia volatilization.", "Halt surface urea broadcast. Apply 2.5 t/ha lime + compost; micro-dose SSP at root zone.", "Yorùbá / French (Oyo, Ogun, Bouaké)"),
        ("Module 7: Livestock Biometrics & THI Heat Stress", "Temperature-Humidity Index (THI) > 82. Ruminal alkalosis, milk yield drop > 25%.", "Shift grazing to crepuscular hours (dawn/dusk); add sodium bicarbonate & salt licks to water.", "Hausa / Swahili (Kano, Jigawa, Rift Valley)"),
        ("Module 8: Agro-Ecosystems & Climate Risk", "14-day mid-season rainfall anomaly; Harmattan dust haze attenuating solar PAR.", "Immediate organic mulching to conserve root zone moisture; postpone chemical top-dressing.", "Hausa / Pidgin (Kaduna, Benue, Niger)"),
        ("Module 1: AI Research Scientist Copilot", "Evidence Gap Synthesis: High yield hybrid lacks Tuwo flour grain density favored by locals.", "Recommend paired culinary variety planting; guide post-harvest processing methods.", "Hausa / Yorùbá (National extension belts)"),
        ("Module 7: Cuniculture & Micro-Livestock", "Acute doe mortality and bloat from feeding damp, wilted cassava peels (cyanide toxicity).", "Strict ban on damp peels; enforce 48-hour mandatory sun-drying before rabbit feeding.", "Yorùbá / French (Ondo, Ekiti, Garoua)")
    ]

    for i, row in enumerate(rows_data):
        bg = "FFFFFF" if i % 2 == 0 else "F8FAF8"
        for j, val in enumerate(row):
            cell = t1.cell(i + 1, j)
            cell.width = col_widths[j]
            set_cell_background(cell, bg)
            set_cell_margins(cell, top=60, bottom=60, left=80, right=80)
            p = cell.paragraphs[0]
            r = p.add_run(val)
            r.font.name = "Arial"
            r.font.size = Pt(7.5)
            if j == 0:
                r.bold = True

    doc.add_paragraph().paragraph_format.space_after = Pt(8)

    # Section 2
    h2 = doc.add_heading(level=1)
    r_h2 = h2.add_run("2. Dual Operational Modes in the Radio Studio")
    r_h2.font.name = "Arial"
    r_h2.font.color.rgb = RGBColor(10, 47, 16)

    p_modes = doc.add_paragraph(
        "To satisfy both high-stakes institutional pitch demonstrations and live day-to-day agricultural operations, the Radio Studio is partitioned into two distinct paradigms:"
    )
    p_modes.paragraph_format.space_after = Pt(4)

    doc.add_paragraph("• Mode A: Live AI Extension Broadcast Studio & Dynamic Queue (On-The-Fly Generation)", style='List Bullet')
    doc.add_paragraph("  Inspects the platform event bus, listing all pending biometric diagnoses sent from other modules with timestamps, origins, and one-click '⚡ Load to Studio' action. Allows free-form editing and synthesizes authentic indigenous scripts with cultural proverbs (e.g. 'Àbọ̀ ọ̀rọ̀ là ń sọ fún ọmọlúwàbí' in Yorùbá, 'Kowa ya tuna bara' in Hausa, 'Haba na haba' in Swahili). Plays via browser Web Speech API and exports formal broadcaster cue sheets (.docx/.txt).", style='Normal')
    doc.add_paragraph("• Mode B: Curated Institutional Reference Benchmarks (Pre-Bundled Ground Truth)", style='List Bullet')
    doc.add_paragraph("  Features 4 comprehensive, multi-environment field scenarios (Kaduna Maize, Pastoral Zebu, Commercial Poultry, Cuniculture) across 5 languages. All 16 broadcast variations are pre-compiled on disk in assets/audio/ so that during institutional demos, the audio plays in 0.001 seconds without network buffering or API failure.", style='Normal')

    doc.add_paragraph().paragraph_format.space_after = Pt(8)

    # Section 3
    h3 = doc.add_heading(level=1)
    r_h3 = h3.add_run("3. Sub-Saharan African Linguistic Footprint & Acoustic Realities")
    r_h3.font.name = "Arial"
    r_h3.font.color.rgb = RGBColor(10, 47, 16)

    p_ling = doc.add_paragraph(
        "By combining French & English (the official institutional and policy languages) with Swahili, Hausa, and Yorùbá (plus West African Pidgin), AgroBiometrix achieves direct linguistic penetration across over 70% of Sub-Saharan Africa's agricultural smallholders."
    )
    p_ling.paragraph_format.space_after = Pt(8)

    # Table 2: Linguistic Breakdown
    t2 = doc.add_table(rows=6, cols=4)
    t2.alignment = WD_TABLE_ALIGNMENT.CENTER
    headers_l = ["Language / Dialect", "Total Speaker Base", "Geographic & Agricultural Corridor", "Acoustic Model Fidelity & Synthesis Truth"]
    col_widths_l = [Inches(1.6), Inches(1.3), Inches(2.1), Inches(2.0)]

    for j, h in enumerate(headers_l):
        cell = t2.cell(0, j)
        cell.width = col_widths_l[j]
        set_cell_background(cell, "1B5E20")
        set_cell_margins(cell, top=80, bottom=80, left=100, right=100)
        p = cell.paragraphs[0]
        r = p.add_run(h)
        r.bold = True
        r.font.name = "Arial"
        r.font.size = Pt(8)
        r.font.color.rgb = RGBColor(255, 255, 255)

    rows_l = [
        ("Kiswahili (Swahili)", "150 – 200+ Million", "East & Central Africa (Tanzania, Kenya, Uganda, Rwanda, Burundi, DRC, Mozambique)", "100% Authentic: Non-tonal Bantu structure with regular penultimate stress. Flawless native output."),
        ("Harshen Hausa (Hausa)", "85 – 100+ Million", "The Sahel & Sudan Savanna (Northern Nigeria, Niger, Chad, Northern Ghana/Cameroon)", "Very Authentic: Mature training across BBC/RFI Hausa. Dedicated native ha acoustic neural models."),
        ("Français Agricole (French)", "120+ Million (African)", "Francophone West & Central Africa (Côte d'Ivoire, Senegal, Cameroon, Mali, Guinea)", "100% Authentic: Mature global phonetics. Broadcasts sound like professional rural radio anchors."),
        ("Èdè Yorùbá (Yoruba)", "50 – 55+ Million", "West African Forest & Coastal Transition (Southwest Nigeria, Benin, Togo)", "Strict Tonal Language (Dò-Re-Mí): Standard TTS uses English phonetics. Requires tonal models (YarnGPT/device yo-NG) for rural elder cadence."),
        ("West African Pidgin", "75 – 80+ Million", "Urban and peri-urban smallholder belts (Nigeria, Ghana, Cameroon)", "High Clarity: Highly conversational and engaging. Understood universally in regional markets.")
    ]

    for i, row in enumerate(rows_l):
        bg = "FFFFFF" if i % 2 == 0 else "F8FAF8"
        for j, val in enumerate(row):
            cell = t2.cell(i + 1, j)
            cell.width = col_widths_l[j]
            set_cell_background(cell, bg)
            set_cell_margins(cell, top=60, bottom=60, left=80, right=80)
            p = cell.paragraphs[0]
            r = p.add_run(val)
            r.font.name = "Arial"
            r.font.size = Pt(7.5)
            if j == 0:
                r.bold = True

    doc.add_paragraph().paragraph_format.space_after = Pt(8)

    # Section 4
    h4 = doc.add_heading(level=1)
    r_h4 = h4.add_run("4. Production API Economics: YarnGPT vs. ElevenLabs")
    r_h4.font.name = "Arial"
    r_h4.font.color.rgb = RGBColor(10, 47, 16)

    p_eco = doc.add_paragraph(
        "A foundational design principle of AgroBiometrix is 'Write Once, Cache & Stream to Millions'. When a weekly advisory is formulated for an agro-ecological zone, the speech API is invoked exactly once. The resulting audio is stored in cloud storage (AWS S3, Cloudflare R2, or local server). Whether 50 extension workers or 500,000 farmers stream that audio track, the marginal API cost is $0.00."
    )
    p_eco.paragraph_format.space_after = Pt(8)

    # Table 3: Economic Models
    t3 = doc.add_table(rows=4, cols=4)
    t3.alignment = WD_TABLE_ALIGNMENT.CENTER
    headers_e = ["Production Scale & Scope", "YarnGPT (Local African Voice AI)", "ElevenLabs (Global Multilingual)", "Strategic Recommendation"]
    col_widths_e = [Inches(1.8), Inches(1.8), Inches(1.8), Inches(1.6)]

    for j, h in enumerate(headers_e):
        cell = t3.cell(0, j)
        cell.width = col_widths_e[j]
        set_cell_background(cell, "1B5E20")
        set_cell_margins(cell, top=80, bottom=80, left=100, right=100)
        p = cell.paragraphs[0]
        r = p.add_run(h)
        r.bold = True
        r.font.name = "Arial"
        r.font.size = Pt(8)
        r.font.color.rgb = RGBColor(255, 255, 255)

    rows_e = [
        ("Tier 1: Standard Regional Extension\n• 4 Value Chains (Maize, Cassava, Cattle, Poultry)\n• 3 Languages (Yorùbá, Hausa, Pidgin)\n• 52 Weekly Updates\nTotal: 624 Bulletins / Year", "Yarn Growth Plan:\n• ₦15,000 / month\n• 1 Top-Up pack (₦50,000)\nTotal: ₦230,000 / year\n(~$148 USD / year)\nLocal Naira billing via Paystack", "Creator Plan (Annual):\n• $220 / year (2 mos free)\n• 1,452,000 characters/yr\nTotal: $220 / year\n(~₦341,000 / year)\nNearly 4× buffer headroom", "Recommended MVP Budget: Under $250 / ₦350k per year. Provides studio French/Swahili and authentic Nigerian accents."),
        ("Tier 2: Full National Syndicate\n• 10 Value Chains across 6 zones\n• 4 Languages (Yorùbá, Hausa, Ìgbò, Pidgin)\n• Bi-weekly Updates (104 updates/yr)\nTotal: 4,160 Bulletins / Year", "Yarn Pro Plan:\n• ₦35,000 / month\n• 4 Bulk Top-Up packs (₦480k)\nTotal: ₦900,000 / year\n(~$580 USD / year)\nOver 3M credit pool", "Pro Plan (Annual):\n• $990 / year (2 mos free)\n• 6,000,000 characters/yr\nTotal: $990 / year\n(~₦1,535,000 / year)\nStudio voice cloning included", "Commercial Scale: Budget $600 to $1,000 / year. Enables multi-state radio syndication across 100+ community stations."),
        ("Unit Cost per 1-Min Radio Bulletin", "~₦150 – ₦350 ($0.10 – $0.22)", "~₦37 – ₦74 ($0.024 – $0.048)", "Negligible line-item on any donor grant.")
    ]

    for i, row in enumerate(rows_e):
        bg = "FFFFFF" if i % 2 == 0 else "F8FAF8"
        for j, val in enumerate(row):
            cell = t3.cell(i + 1, j)
            cell.width = col_widths_e[j]
            set_cell_background(cell, bg)
            set_cell_margins(cell, top=60, bottom=60, left=80, right=80)
            p = cell.paragraphs[0]
            r = p.add_run(val)
            r.font.name = "Arial"
            r.font.size = Pt(7.5)
            if i == 2:
                r.bold = True

    doc.add_paragraph().paragraph_format.space_after = Pt(8)

    # Section 5
    h5 = doc.add_heading(level=1)
    r_h5 = h5.add_run("5. Institutional Pitch Strategy & Field Deployment Roadmap")
    r_h5.font.name = "Arial"
    r_h5.font.color.rgb = RGBColor(10, 47, 16)

    bullets_final = [
        "The Extension Officer Crisis Metric: Nigeria and Kenya suffer from an extension agent-to-farmer ratio worse than 1:3,500 (FAO recommended standard is 1:500). Physical agents cannot reach millions of smallholders weekly.",
        "The Biometric Radio Solution: AgroBiometrix serves as an operational force multiplier. A single agronomist running a soil or heat stress model can dispatch vernacular radio bulletins to 50 community FM stations in under 2 minutes.",
        "Voice Cloning for Community Trust: ElevenLabs allows 1-minute voice cloning. A beloved local extension worker or university professor's voice can be cloned with consent, ensuring farmers hear a familiar, trusted community voice rather than a generic machine.",
        "Two-Way WhatsApp / IVR Expansion: Phase 2 extends this exact event bus to two-way WhatsApp voice notes and toll-free IVR phone lines, allowing illiterate smallholders to voice their challenges and receive spoken advice back."
    ]

    for b in bullets_final:
        doc.add_paragraph(f"• {b}", style='List Bullet')

    doc.add_paragraph().paragraph_format.space_after = Pt(10)

    # Sign-off box
    table_sign = doc.add_table(rows=1, cols=1)
    table_sign.alignment = WD_TABLE_ALIGNMENT.CENTER
    cell_sign = table_sign.rows[0].cells[0]
    cell_sign.width = Inches(7.0)
    set_cell_background(cell_sign, "F8FAF8")
    set_cell_margins(cell_sign, top=100, bottom=100, left=150, right=150)
    p_s = cell_sign.paragraphs[0]
    r_s = p_s.add_run(
        "AgroBiometrix Operational Commitment: AgroBiometrix bridges laboratory genomics, quantitative biometrics, and rural transistor radio "
        "into a unified African digital extension infrastructure. For technical inquiries, API integration, or institutional partnerships, "
        "contact: directorate@agrobiometrix.org | Live Platform: agrobiometrix.streamlit.app"
    )
    r_s.font.name = "Arial"
    r_s.font.size = Pt(8)
    r_s.font.color.rgb = RGBColor(84, 110, 122)
    r_s.italic = True

    doc.save(DOCX_FILENAME)
    print(f"Successfully generated: {DOCX_FILENAME} ({os.path.getsize(DOCX_FILENAME)} bytes)")

if __name__ == "__main__":
    create_document()
