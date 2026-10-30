"""
Generate AgroBiometrix Institutional Pitch Letters in Microsoft Word (.docx) Format
Includes individual letter files and a unified Executive Dossier.
"""

import os
import re
from docx import Document
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml import OxmlElement, parse_xml
from docx.oxml.ns import nsdecls, qn

def sanitize_xml_text(text: str) -> str:
    """Strip XML invalid control characters."""
    if not text:
        return ""
    return re.sub(r'[\x00-\x08\x0B\x0C\x0E-\x1F\x7F]', '', str(text))

def set_cell_background(cell, fill_hex: str):
    """Sets background color of a table cell."""
    shading_elm = parse_xml(f'<w:shd {nsdecls("w")} w:fill="{fill_hex}"/>')
    cell._tc.get_or_add_tcPr().append(shading_elm)

def set_cell_margins(cell, top=100, bottom=100, left=150, right=150):
    """Sets internal padding for a cell."""
    tcPr = cell._tc.get_or_add_tcPr()
    tcMar = OxmlElement('w:tcMar')
    for m, val in [('top', top), ('bottom', bottom), ('left', left), ('right', right)]:
        node = OxmlElement(f'w:{m}')
        node.set(qn('w:w'), str(val))
        node.set(qn('w:type'), 'dxa')
        tcMar.append(node)
    tcPr.append(tcMar)

LETTERS = [
    {
        "id": "IITA",
        "title": "International Institute of Tropical Agriculture (IITA)",
        "filename": "AgroBiometrix_Pitch_Letter_IITA.docx",
        "recipient": "The Director General & Director of Research for Development (R4D)\nInternational Institute of Tropical Agriculture (IITA)\nHeadquarters: PMB 5320, Oyo Road, Ibadan, Oyo State, Nigeria",
        "subject": "Institutional Partnership: AgroBiometrix Intelligence Platform for IITA Breeding & Extension Networks",
        "salutation": "Dear Director General & Research Leadership,",
        "intro": "I am writing to formally introduce AgroBiometrix (https://agrobiometrix.streamlit.app), an Africa-first generative intelligence and quantitative biometrics platform engineered to accelerate crop breeding trial analytics, research grant ideation, and vernacular extension delivery across tropical cropping systems.",
        "context": "While generic agricultural AI applications focus primarily on leaf-photo diagnostics, AgroBiometrix moves upstream into the biometrical and evidence infrastructure of African agriculture. Built to reflect CGIAR and NARS scientific standards across root, tuber, and cereal value chains, the platform delivers:",
        "pillars": [
            ("Rapid Biometrical & Breeding Engine", "Automated RCBD, CRD, and Split-Plot trial design, multi-location Two-Way ANOVA, and Duncan's Multiple Range Test (DMRT) with distinct letter separations—generating reproducible Python and R scripts for IITA crop biometricians in under 3 seconds."),
            ("Pan-African Bilingual Parity (EN / FR)", "Full operational bilingual capability between English and French with a single click—essential for IITA's cross-border trial networks connecting Ibadan and Kano to Bouaké, Yaoundé, and Kinshasa."),
            ("Multi-Agent Agronomic Intelligence", "Live scientific reasoning combining satellite climate anomalies, soil chemistry, and evidence-grounded IITA/CGIAR literature citations with zero hallucinations."),
            ("Last-Mile Rural Radio Advisory", "Converts complex agronomic findings (such as fertilizer micro-dosing and drought-tolerant seed selection) into vernacular audio broadcast scripts in Hausa, Yoruba, Swahili, and French for community FM radio and extension agents.")
        ],
        "ask": "We would welcome the opportunity to explore a 90-Day Collaborative Validation Pilot with IITA scientists and postgraduate fellows to evaluate how AgroBiometrix can reduce trial data analysis cycles and streamline research-to-extension pipelines.\n\nMay we schedule a 20-minute virtual demonstration with your research and digital innovations team next week?",
        "closing": "Yours sincerely,\n\nLead Geneticist & Founder, AgroBiometrix\nhttps://agrobiometrix.streamlit.app"
    },
    {
        "id": "ILRI",
        "title": "International Livestock Research Institute (ILRI)",
        "filename": "AgroBiometrix_Pitch_Letter_ILRI.docx",
        "recipient": "The Director General & Regional Representative (West & Central Africa)\nInternational Livestock Research Institute (ILRI)\nRegional Station: c/o IITA Campus, Ibadan, Nigeria / Global HQ: Nairobi, Kenya",
        "subject": "Accelerating Livestock Biometrics & Climate Adaptation in Africa: AgroBiometrix / ILRI Collaboration",
        "salutation": "Dear Director General & Livestock Biosciences Leadership,",
        "intro": "I am an animal geneticist and the founder of AgroBiometrix (https://agrobiometrix.streamlit.app), a quantitative biometrics and multi-agent intelligence platform engineered specifically for African livestock, veterinary epidemiology, and pastoral rangeland systems.",
        "context": "Sub-Saharan livestock research faces distinct structural challenges: prolonged generation intervals, severe heat stress anomalies, pastoral disease surges (PPR, CCPP, Trypanosomiasis), and limited specialized biometrical tools calibrated for tropical multi-trait genetic evaluation. AgroBiometrix directly addresses these challenges:",
        "pillars": [
            ("Bovine & Small Ruminant Biometrics", "Real-time Temperature-Humidity Index (THI) calculation, trypanotolerance marker cross-referencing for Zebu and Taurine breeds, and multi-trait selection indexes for pastoral sheep and goat breeding."),
            ("Commercial Herd & Flock Simulation", "Interactive livestock models covering festive bull fattening (>50% margin models), poultry respiratory alkalosis therapy, and heat-stress feed-withdrawal calendars."),
            ("Epidemic Early Warning & Last-Mile Broadcasts", "Synthesizes biosecurity protocols (PPR, African Swine Fever, Newcastle Disease) into indigenous pastoral audio advisories in Hausa, Swahili, and French for pastoralists and field veterinary scouts."),
            ("Scientific Literature & Evidence Matrices", "Synthesizes ILRI peer-reviewed research, QTL associations, and breeding value (EBV) literature with complete bibliographic verification.")
        ],
        "ask": "Given ILRI's continental leadership in livestock genetics and climate-smart pastoral systems, we propose a joint technical review to explore how AgroBiometrix can support ILRI's field research and capacity-building programs.\n\nCould we coordinate a brief 20-minute virtual demonstration with your livestock biosciences team?",
        "closing": "Sincerely yours,\n\nAnimal Geneticist & Founder, AgroBiometrix\nhttps://agrobiometrix.streamlit.app"
    },
    {
        "id": "CGIAR",
        "title": "CGIAR System Organization / CGIAR AI Hub",
        "filename": "AgroBiometrix_Pitch_Letter_CGIAR.docx",
        "recipient": "The Global Director of Digital Agriculture & CGIAR AI Hub Leadership\nCGIAR System Organization\nMontpellier, France / Regional Hubs Africa",
        "subject": "AgroBiometrix: Institutional AI & Biometrical Infrastructure for CGIAR Digital Initiatives",
        "salutation": "Dear CGIAR Digital Agriculture Leadership,",
        "intro": "As the CGIAR System Organization advances its AI Hub and digital innovation agenda for 2025–2030, the continent urgently requires agricultural AI architectures that move beyond generic consumer chatbots to deliver mathematically rigorous, peer-reviewed, and localized scientific intelligence.",
        "context": "AgroBiometrix (https://agrobiometrix.streamlit.app) was developed as an open, Africa-first intelligence infrastructure connecting genomics, field biometrics, edaphic soil science, and macroeconomic policy. Built in alignment with CGIAR digital public goods standards:",
        "pillars": [
            ("Dual-Engine Architecture", "100% deterministic local computation for statistical trial analytics (ANOVA, DMRT, Henderson's BLUP, USDA soil physics) paired with optional live Google Gemini 1.5/2.0 multi-agent reasoning—eliminating scientific hallucinations."),
            ("PRISMA Review & Grant Proposal Studio", "End-to-end systematic literature review mapping (PRISMA 2020) and automated 7-part grant proposal synthesis with Cochran sample sizing and real Crossref/PubMed DOI verification."),
            ("Macro-Policy & AU-CAADP Alignment", "National food balance sheet modeling across 12 strategic commodities, food inflation stress-testing, and ministerial cabinet brief generation for national partners."),
            ("Bilingual Continental Usability (EN / FR)", "Native operational switch between English and French, ensuring immediate usability across all 15 CGIAR centers, Francophone West Africa, Central Africa, and East Africa.")
        ],
        "ask": "We would be honored to demonstrate AgroBiometrix to the CGIAR Digital Agriculture team and explore opportunities for integration into ongoing digital extension, climate resilience, and crop breeding initiatives.\n\nCould we schedule a 20-minute briefing session at your earliest convenience?",
        "closing": "Respectfully yours,\n\nFounder & Lead Scientist, AgroBiometrix\nhttps://agrobiometrix.streamlit.app"
    },
    {
        "id": "FUNAAB",
        "title": "Federal University of Agriculture, Abeokuta (FUNAAB)",
        "filename": "AgroBiometrix_Pitch_Letter_FUNAAB.docx",
        "recipient": "The Vice-Chancellor, Deans of Colleges (COLANIM, COLPLANT, COLAMRUD) & Director of Research\nFederal University of Agriculture, Abeokuta (FUNAAB)\nPMB 2240, Alabata Road, Abeokuta, Ogun State, Nigeria",
        "subject": "Institutional Partnership Proposal: Enhancing Postgraduate Research & Statistical Analytics at FUNAAB via AgroBiometrix",
        "salutation": "Dear Vice-Chancellor & University Academic Leadership,",
        "intro": "I am pleased to present AgroBiometrix (https://agrobiometrix.streamlit.app), a specialized generative biometrics and research platform designed to enhance faculty grant competitiveness, streamline thesis supervision, and empower agricultural postgraduate students.",
        "context": "Postgraduate researchers and academic supervisors frequently lose hundreds of hours navigating complex proprietary statistical packages (SPSS, SAS, GenStat) and structuring funding proposals. AgroBiometrix delivers an institutional-grade suite built specifically for university agriculture faculties:",
        "pillars": [
            ("Automated Biometrics & Post-Hoc Engine", "Instant One-Way and Two-Way ANOVA with Duncan's Multiple Range Test (DMRT), Tukey's HSD, and Dunnett's control comparisons—complete with downloadable field books and clean R/Python scripts for dissertation chapters."),
            ("AI Thesis Defense & Viva Tutor", "Socratic thesis mentor trained across 14 agricultural departments (Agronomy, Animal Breeding, Soil Science, Agricultural Economics, Extension, etc.), interrogating methodology and preparing students for viva examinations."),
            ("TETFUND & International Grant Proposal Architect", "Generates 7-part funding proposals structured for TETFUND, AGRA, and international grants, complete with Cochran sample size equations, peer-reviewed APA citations, and uncorrupted Word (.docx) downloads."),
            ("Indigenous Breed Ground Truth", "Built-in phenotypic models for indigenous breeds, including dual-purpose poultry (e.g. FUNAAB Alpha), West African Dwarf sheep/goats, and tropical cultivars.")
        ],
        "ask": "Proposal for FUNAAB:\nWe propose a 90-Day University Faculty Pilot, granting institutional access to 100 postgraduate researchers and academic supervisors across COLANIM, COLPLANT, and COLAMRUD to measure productivity gains and dissertation acceleration.\n\nMay we request a 20-minute presentation before the Committee of Deans or the Directorate of Research Innovation and Partnerships (DRIP)?",
        "closing": "Warm regards,\n\nLead Geneticist & Founder, AgroBiometrix\nhttps://agrobiometrix.streamlit.app"
    },
    {
        "id": "ARCN_FMAFS",
        "title": "Agricultural Research Council of Nigeria (ARCN) & Federal Ministry of Agriculture",
        "filename": "AgroBiometrix_Pitch_Letter_ARCN_FMAFS.docx",
        "recipient": "The Executive Secretary, Agricultural Research Council of Nigeria (ARCN)\n& The Honorable Minister / Permanent Secretary, Federal Ministry of Agriculture & Food Security (FMAFS)\nAgricultural Research House, Mabushi, Abuja, Nigeria",
        "subject": "National Food Security Decision Infrastructure: AgroBiometrix Policy Simulator & Research Engine",
        "salutation": "Honorable Minister, Executive Secretary & Esteemed Directors,",
        "intro": "I am honored to present AgroBiometrix (https://agrobiometrix.streamlit.app), an indigenous agricultural intelligence infrastructure built to connect field research across our National Agricultural Research Institutes (NIHORT, NCRI, IAR, NAPRI, NVRI) directly to policy decision-making at the Federal Ministry of Agriculture.",
        "context": "While macroeconomic shocks, currency fluctuations, and climate volatility place intense pressure on national grain reserves and food inflation, policymakers often lack real-time simulation tools to model interventions prior to fiscal expenditure. AgroBiometrix provides an Institutional Macro-Policy Platform:",
        "pillars": [
            ("₦5B–₦250B Fiscal Allocation Simulator", "Models multi-ministerial ROI across Treasury Ag-GDP, Labour employment generation, Humanitarian stunting reduction, and Central Bank FX savings."),
            ("12 Strategic Commodity Balance Sheets", "Tracks national self-sufficiency deficits and import substitution timelines across Rice, Maize, Wheat, Cassava, Tomato, Sorghum, and Poultry."),
            ("Food Inflation & Macro-Shock Resilience", "Stress-tests fuel subsidy removals, fertilizer price spikes, and drought return periods to project monthly Food CPI trajectories and strategic grain reserve release schedules."),
            ("Cabinet Policy Memorandum Generator", "Synthesizes structured Federal Executive Council (FEC) and AU CAADP memoranda exportable directly to Microsoft Word and publication PDF."),
            ("Last-Mile Vernacular Extension Dispatcher", "Generates vernacular audio advisory bulletins in Hausa, Yoruba, Igbo, and Pidgin for community radio broadcast across all 36 states and the FCT.")
        ],
        "ask": "We formally request an opportunity to deliver a 30-minute executive presentation at your headquarters to demonstrate how AgroBiometrix can serve as a unified intelligence dashboard across Nigeria's agricultural research institutes and policy directorates.\n\nLive Platform Demonstration: https://agrobiometrix.streamlit.app",
        "closing": "Yours in national service,\n\nFounder & Lead Scientist, AgroBiometrix\nhttps://agrobiometrix.streamlit.app"
    }
]

def build_single_docx(letter_data: dict, output_path: str):
    """Builds a single beautifully formatted Word document for an institutional letter."""
    doc = Document()
    
    # Page Margins
    sections = doc.sections
    for s in sections:
        s.top_margin = Inches(1.0)
        s.bottom_margin = Inches(1.0)
        s.left_margin = Inches(1.0)
        s.right_margin = Inches(1.0)
        
    # Styles
    normal_style = doc.styles['Normal']
    normal_style.font.name = 'Calibri'
    normal_style.font.size = Pt(11)
    normal_style.font.color.rgb = RGBColor(0x26, 0x32, 0x38)
    
    # Document Header Banner
    header_table = doc.add_table(rows=1, cols=1)
    header_table.alignment = WD_TABLE_ALIGNMENT.CENTER
    header_table.autofit = False
    header_table.columns[0].width = Inches(6.5)
    
    cell = header_table.cell(0, 0)
    set_cell_background(cell, "1B5E20")  # Dark Green
    set_cell_margins(cell, top=140, bottom=140, left=180, right=180)
    
    p = cell.paragraphs[0]
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    run_title = p.add_run("AGROBIOMETRIX INSTITUTIONAL BRIEFING")
    run_title.bold = True
    run_title.font.size = Pt(13)
    run_title.font.color.rgb = RGBColor(0xFF, 0xFF, 0xFF)
    
    p_sub = cell.add_paragraph()
    p_sub.alignment = WD_ALIGN_PARAGRAPH.CENTER
    run_sub = p_sub.add_run("The Generative Intelligence Platform for Resilient Agriculture • https://agrobiometrix.streamlit.app")
    run_sub.font.size = Pt(9.5)
    run_sub.font.color.rgb = RGBColor(0xC8, 0xE6, 0xC9)
    
    doc.add_paragraph().paragraph_format.space_after = Pt(14)
    
    # Date & Recipient
    p_meta = doc.add_paragraph()
    p_meta.paragraph_format.space_after = Pt(8)
    run_date = p_meta.add_run("Date: October 2026\n\n")
    run_date.bold = True
    run_date.font.size = Pt(10.5)
    
    run_rec = p_meta.add_run(sanitize_xml_text(letter_data["recipient"]))
    run_rec.font.size = Pt(10.5)
    
    doc.add_paragraph().paragraph_format.space_after = Pt(6)
    
    # Subject Box
    subj_table = doc.add_table(rows=1, cols=1)
    subj_table.alignment = WD_TABLE_ALIGNMENT.CENTER
    subj_table.columns[0].width = Inches(6.5)
    
    subj_cell = subj_table.cell(0, 0)
    set_cell_background(subj_cell, "E8F5E9")  # Pale Leaf Green
    set_cell_margins(subj_cell, top=100, bottom=100, left=150, right=150)
    
    p_subj = subj_cell.paragraphs[0]
    p_subj.paragraph_format.space_after = Pt(0)
    run_s_lbl = p_subj.add_run("SUBJECT: ")
    run_s_lbl.bold = True
    run_s_lbl.font.size = Pt(11)
    run_s_lbl.font.color.rgb = RGBColor(0x1B, 0x5E, 0x20)
    
    run_s_val = p_subj.add_run(sanitize_xml_text(letter_data["subject"]))
    run_s_val.bold = True
    run_s_val.font.size = Pt(11)
    run_s_val.font.color.rgb = RGBColor(0x1B, 0x5E, 0x20)
    
    doc.add_paragraph().paragraph_format.space_after = Pt(12)
    
    # Salutation
    p_sal = doc.add_paragraph()
    p_sal.paragraph_format.space_after = Pt(10)
    run_sal = p_sal.add_run(sanitize_xml_text(letter_data["salutation"]))
    run_sal.bold = True
    
    # Intro
    p_intro = doc.add_paragraph()
    p_intro.paragraph_format.space_after = Pt(10)
    p_intro.paragraph_format.line_spacing = 1.15
    p_intro.add_run(sanitize_xml_text(letter_data["intro"]))
    
    # Context
    p_ctx = doc.add_paragraph()
    p_ctx.paragraph_format.space_after = Pt(10)
    p_ctx.paragraph_format.line_spacing = 1.15
    p_ctx.add_run(sanitize_xml_text(letter_data["context"]))
    
    # Pillars
    for title, desc in letter_data["pillars"]:
        p_pil = doc.add_paragraph(style='List Bullet')
        p_pil.paragraph_format.space_after = Pt(6)
        p_pil.paragraph_format.line_spacing = 1.15
        
        run_p_title = p_pil.add_run(sanitize_xml_text(title) + ": ")
        run_p_title.bold = True
        run_p_title.font.color.rgb = RGBColor(0x1B, 0x5E, 0x20)
        
        p_pil.add_run(sanitize_xml_text(desc))
        
    doc.add_paragraph().paragraph_format.space_after = Pt(8)
    
    # The Ask Box
    ask_table = doc.add_table(rows=1, cols=1)
    ask_table.alignment = WD_TABLE_ALIGNMENT.CENTER
    ask_table.columns[0].width = Inches(6.5)
    
    ask_cell = ask_table.cell(0, 0)
    set_cell_background(ask_cell, "F1F8F2")
    set_cell_margins(ask_cell, top=120, bottom=120, left=150, right=150)
    
    p_ask_title = ask_cell.paragraphs[0]
    p_ask_title.paragraph_format.space_after = Pt(4)
    run_at = p_ask_title.add_run("PROPOSED NEXT STEP: 90-DAY COLLABORATIVE PILOT")
    run_at.bold = True
    run_at.font.size = Pt(10.5)
    run_at.font.color.rgb = RGBColor(0x1B, 0x5E, 0x20)
    
    p_ask_body = ask_cell.add_paragraph()
    p_ask_body.paragraph_format.space_after = Pt(0)
    p_ask_body.paragraph_format.line_spacing = 1.15
    p_ask_body.add_run(sanitize_xml_text(letter_data["ask"]))
    
    doc.add_paragraph().paragraph_format.space_after = Pt(14)
    
    # Closing
    p_cls = doc.add_paragraph()
    p_cls.paragraph_format.space_after = Pt(12)
    p_cls.paragraph_format.line_spacing = 1.15
    p_cls.add_run(sanitize_xml_text(letter_data["closing"]))
    
    doc.save(output_path)
    print(f"Saved: {output_path}")

def build_executive_dossier(letters: list, output_path: str):
    """Builds a single unified Word document containing all pitch letters."""
    doc = Document()
    
    sections = doc.sections
    for s in sections:
        s.top_margin = Inches(1.0)
        s.bottom_margin = Inches(1.0)
        s.left_margin = Inches(1.0)
        s.right_margin = Inches(1.0)
        
    normal_style = doc.styles['Normal']
    normal_style.font.name = 'Calibri'
    normal_style.font.size = Pt(11)
    normal_style.font.color.rgb = RGBColor(0x26, 0x32, 0x38)
    
    # Dossier Title Page
    p_title = doc.add_paragraph()
    p_title.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_title.paragraph_format.space_before = Pt(80)
    p_title.paragraph_format.space_after = Pt(10)
    
    run_t = p_title.add_run("AGROBIOMETRIX\nINSTITUTIONAL PITCH DOSSIER")
    run_t.bold = True
    run_t.font.size = Pt(24)
    run_t.font.color.rgb = RGBColor(0x1B, 0x5E, 0x20)
    
    p_sub = doc.add_paragraph()
    p_sub.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_sub.paragraph_format.space_after = Pt(25)
    run_s = p_sub.add_run("Executive Partnership Letters Tailored for CGIAR, IITA, ILRI, FUNAAB, & National Agricultural Research Systems (NARS)")
    run_s.font.size = Pt(12)
    run_s.font.color.rgb = RGBColor(0x2E, 0x7D, 0x32)
    
    p_meta = doc.add_paragraph()
    p_meta.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_meta.paragraph_format.space_after = Pt(40)
    run_m = p_meta.add_run("Platform Live Web Application: https://agrobiometrix.streamlit.app\nOctober 2026 • Confidential Institutional Proposal")
    run_m.font.size = Pt(10.5)
    run_m.font.color.rgb = RGBColor(0x54, 0x6E, 0x7A)
    
    doc.add_page_break()
    
    # Table of Contents
    p_toc_head = doc.add_paragraph()
    p_toc_head.paragraph_format.space_after = Pt(14)
    run_th = p_toc_head.add_run("TABLE OF CONTENTS")
    run_th.bold = True
    run_th.font.size = Pt(14)
    run_th.font.color.rgb = RGBColor(0x1B, 0x5E, 0x20)
    
    toc_items = [
        ("1. International Institute of Tropical Agriculture (IITA)", "Breeding trial biometrics, bilingual EN/FR crop network"),
        ("2. International Livestock Research Institute (ILRI)", "Tropical livestock genetics, THI heat stress, pastoral early warning"),
        ("3. CGIAR System Organization / AI Hub", "Pan-African digital public goods, PRISMA literature, AU-CAADP macro policy"),
        ("4. Federal University of Agriculture, Abeokuta (FUNAAB)", "Postgraduate dissertation computing (ANOVA/DMRT), thesis mentor, grant proposals"),
        ("5. Agricultural Research Council of Nigeria (ARCN / FMAFS)", "National strategic food balance sheets, commodity import substitution, cabinet briefs")
    ]
    
    for title, desc in toc_items:
        p_t = doc.add_paragraph(style='List Bullet')
        p_t.paragraph_format.space_after = Pt(6)
        r_t = p_t.add_run(title)
        r_t.bold = True
        r_t.font.color.rgb = RGBColor(0x1B, 0x5E, 0x20)
        p_t.add_run(f" — {desc}")
        
    doc.add_page_break()
    
    # Append each letter
    for idx, letter_data in enumerate(letters):
        # Section Header Banner
        header_table = doc.add_table(rows=1, cols=1)
        header_table.alignment = WD_TABLE_ALIGNMENT.CENTER
        header_table.columns[0].width = Inches(6.5)
        
        cell = header_table.cell(0, 0)
        set_cell_background(cell, "1B5E20")
        set_cell_margins(cell, top=120, bottom=120, left=150, right=150)
        
        p = cell.paragraphs[0]
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        run_title = p.add_run(f"SECTION {idx + 1}: {letter_data['title'].upper()}")
        run_title.bold = True
        run_title.font.size = Pt(11)
        run_title.font.color.rgb = RGBColor(0xFF, 0xFF, 0xFF)
        
        doc.add_paragraph().paragraph_format.space_after = Pt(12)
        
        # Date & Recipient
        p_meta = doc.add_paragraph()
        p_meta.paragraph_format.space_after = Pt(8)
        run_date = p_meta.add_run("Date: October 2026\n\n")
        run_date.bold = True
        run_date.font.size = Pt(10.5)
        
        run_rec = p_meta.add_run(sanitize_xml_text(letter_data["recipient"]))
        run_rec.font.size = Pt(10.5)
        
        doc.add_paragraph().paragraph_format.space_after = Pt(6)
        
        # Subject Box
        subj_table = doc.add_table(rows=1, cols=1)
        subj_table.alignment = WD_TABLE_ALIGNMENT.CENTER
        subj_table.columns[0].width = Inches(6.5)
        
        subj_cell = subj_table.cell(0, 0)
        set_cell_background(subj_cell, "E8F5E9")
        set_cell_margins(subj_cell, top=90, bottom=90, left=140, right=140)
        
        p_subj = subj_cell.paragraphs[0]
        run_s_lbl = p_subj.add_run("SUBJECT: ")
        run_s_lbl.bold = True
        run_s_lbl.font.size = Pt(10.5)
        run_s_lbl.font.color.rgb = RGBColor(0x1B, 0x5E, 0x20)
        
        run_s_val = p_subj.add_run(sanitize_xml_text(letter_data["subject"]))
        run_s_val.bold = True
        run_s_val.font.size = Pt(10.5)
        run_s_val.font.color.rgb = RGBColor(0x1B, 0x5E, 0x20)
        
        doc.add_paragraph().paragraph_format.space_after = Pt(10)
        
        # Salutation
        p_sal = doc.add_paragraph()
        p_sal.paragraph_format.space_after = Pt(8)
        run_sal = p_sal.add_run(sanitize_xml_text(letter_data["salutation"]))
        run_sal.bold = True
        
        # Intro
        p_intro = doc.add_paragraph()
        p_intro.paragraph_format.space_after = Pt(8)
        p_intro.paragraph_format.line_spacing = 1.15
        p_intro.add_run(sanitize_xml_text(letter_data["intro"]))
        
        # Context
        p_ctx = doc.add_paragraph()
        p_ctx.paragraph_format.space_after = Pt(8)
        p_ctx.paragraph_format.line_spacing = 1.15
        p_ctx.add_run(sanitize_xml_text(letter_data["context"]))
        
        # Pillars
        for p_title, p_desc in letter_data["pillars"]:
            p_pil = doc.add_paragraph(style='List Bullet')
            p_pil.paragraph_format.space_after = Pt(5)
            p_pil.paragraph_format.line_spacing = 1.15
            
            run_p_title = p_pil.add_run(sanitize_xml_text(p_title) + ": ")
            run_p_title.bold = True
            run_p_title.font.color.rgb = RGBColor(0x1B, 0x5E, 0x20)
            
            p_pil.add_run(sanitize_xml_text(p_desc))
            
        doc.add_paragraph().paragraph_format.space_after = Pt(6)
        
        # The Ask Box
        ask_table = doc.add_table(rows=1, cols=1)
        ask_table.alignment = WD_TABLE_ALIGNMENT.CENTER
        ask_table.columns[0].width = Inches(6.5)
        
        ask_cell = ask_table.cell(0, 0)
        set_cell_background(ask_cell, "F1F8F2")
        set_cell_margins(ask_cell, top=100, bottom=100, left=140, right=140)
        
        p_ask_title = ask_cell.paragraphs[0]
        p_ask_title.paragraph_format.space_after = Pt(4)
        run_at = p_ask_title.add_run("PROPOSED NEXT STEP: 90-DAY COLLABORATIVE PILOT")
        run_at.bold = True
        run_at.font.size = Pt(10)
        run_at.font.color.rgb = RGBColor(0x1B, 0x5E, 0x20)
        
        p_ask_body = ask_cell.add_paragraph()
        p_ask_body.paragraph_format.space_after = Pt(0)
        p_ask_body.paragraph_format.line_spacing = 1.15
        p_ask_body.add_run(sanitize_xml_text(letter_data["ask"]))
        
        doc.add_paragraph().paragraph_format.space_after = Pt(12)
        
        # Closing
        p_cls = doc.add_paragraph()
        p_cls.paragraph_format.space_after = Pt(12)
        p_cls.paragraph_format.line_spacing = 1.15
        p_cls.add_run(sanitize_xml_text(letter_data["closing"]))
        
        if idx < len(letters) - 1:
            doc.add_page_break()
            
    doc.save(output_path)
    print(f"Saved Executive Dossier: {output_path}")

if __name__ == "__main__":
    print("Generating individual Word (.docx) pitch letters...")
    for l in LETTERS:
        build_single_docx(l, l["filename"])
        
    print("\nGenerating combined Executive Dossier Word document...")
    build_executive_dossier(LETTERS, "AgroBiometrix_Institutional_Pitch_Letters_Executive_Dossier.docx")
    print("All DOCX pitch letters created successfully!")
