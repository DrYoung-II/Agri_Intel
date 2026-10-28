"""
AgroBiometrix Document Export Engine
Converts Markdown, Tables, and Scientific Synthesis into Publication-Grade:
1. Portable Document Format (.pdf) via ReportLab with two-pass NumberedCanvas
2. Microsoft Word (.docx) via python-docx with styled headers, XML tables, and runs
3. Markdown (.md)
"""

import io
import re
import streamlit as st
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, HRFlowable
)
from reportlab.pdfgen import canvas

import docx
from docx.shared import Inches, Pt, RGBColor
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml import parse_xml
from docx.oxml.ns import nsdecls


class NumberedCanvas(canvas.Canvas):
    """Two-pass canvas to dynamically compute total page count for PDF exports."""
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
            self.drawString(54, 755, "AGROBIOMETRIX SCIENTIFIC ADVISORY & RESEARCH REPORT")
            self.setFont("Helvetica", 8)
            self.setFillColor(colors.HexColor("#666666"))
            self.drawRightString(558, 755, "Pan-African Agronomic Intelligence")
            self.setStrokeColor(colors.HexColor("#A5D6A7"))
            self.setLineWidth(0.6)
            self.line(54, 748, 558, 748)
            
        # Footer (all pages)
        page_text = f"Page {self._pageNumber} of {page_count}"
        self.setFont("Helvetica", 8)
        self.setFillColor(colors.HexColor("#2E7D32"))
        self.drawString(54, 34, "AgroBiometrix Platform | Verified Institutional Report")
        self.drawRightString(558, 34, page_text)
        self.setStrokeColor(colors.HexColor("#C8E6C9"))
        self.setLineWidth(0.6)
        self.line(54, 44, 558, 44)
        self.restoreState()


def clean_markdown_for_reportlab(text: str) -> str:
    """Sanitizes text for ReportLab paragraph parser."""
    # Convert HTML breaks
    text = text.replace("<br>", "<br/>").replace("<BR>", "<br/>")
    # Escape ampersands not part of HTML entities
    text = re.sub(r'&(?!(?:amp|lt|gt|quot|apos);)', '&amp;', text)
    # Convert bold **text** to <b>text</b>
    text = re.sub(r'\*\*(.*?)\*\*', r'<b>\1</b>', text)
    # Convert italics *text* to <i>text</i>
    text = re.sub(r'\*(.*?)\*', r'<i>\1</i>', text)
    # Convert inline code `code` to Courier
    text = re.sub(r'`(.*?)`', r'<font face="Courier" color="#1B5E20"><b>\1</b></font>', text)
    # Strip any unsupported HTML tags
    text = re.sub(r'<(?!/?(?:b|i|br|font)\b)[^>]*>', '', text)
    return text


def markdown_to_pdf(markdown_text: str, title: str = "AgroBiometrix Report") -> bytes:
    """Converts markdown text to a styled, publication-grade PDF buffer."""
    buf = io.BytesIO()
    doc = SimpleDocTemplate(
        buf,
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
        fontSize=18,
        leading=22,
        textColor=primary_green,
        spaceAfter=8
    )
    h1_style = ParagraphStyle(
        'H1_Custom',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=12,
        leading=16,
        textColor=primary_green,
        spaceBefore=12,
        spaceAfter=5,
        keepWithNext=True
    )
    h2_style = ParagraphStyle(
        'H2_Custom',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=10,
        leading=13,
        textColor=leaf_green,
        spaceBefore=8,
        spaceAfter=3,
        keepWithNext=True
    )
    h3_style = ParagraphStyle(
        'H3_Custom',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=9,
        leading=12,
        textColor=colors.HexColor("#333333"),
        spaceBefore=6,
        spaceAfter=2,
        keepWithNext=True
    )
    body_style = ParagraphStyle(
        'Body_Custom',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=8.5,
        leading=12,
        textColor=text_dark,
        spaceAfter=5
    )
    bullet_style = ParagraphStyle(
        'Bullet_Custom',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=8.5,
        leading=12,
        textColor=text_dark,
        leftIndent=14,
        firstLineIndent=-10,
        spaceAfter=3
    )
    table_cell = ParagraphStyle(
        'TCell',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=7.5,
        leading=9.5,
        textColor=text_dark
    )
    table_cell_bold = ParagraphStyle(
        'TCellBold',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=7.5,
        leading=9.5,
        textColor=colors.white
    )

    clean_title = clean_markdown_for_reportlab(title)
    story = [
        Paragraph(clean_title, title_style),
        HRFlowable(width="100%", thickness=1.5, color=primary_green, spaceBefore=2, spaceAfter=10)
    ]

    lines = markdown_text.split("\n")
    i = 0
    while i < len(lines):
        raw_line = lines[i].strip()
        if not raw_line:
            i += 1
            continue

        # Check for markdown table
        if raw_line.startswith("|") and raw_line.endswith("|"):
            table_raw = []
            while i < len(lines) and lines[i].strip().startswith("|") and lines[i].strip().endswith("|"):
                row_line = lines[i].strip()
                # Skip divider rows like |---|---|
                if not re.match(r"^\|(\s*[-:]+\s*\|)+$", row_line):
                    cells = [c.strip() for c in row_line.split("|")[1:-1]]
                    table_raw.append(cells)
                i += 1
            
            if table_raw:
                num_cols = max(len(r) for r in table_raw)
                col_width = 504 / num_cols
                formatted_table_data = []
                for r_idx, row in enumerate(table_raw):
                    padded_row = row + [""] * (num_cols - len(row))
                    row_cells = []
                    for c in padded_row:
                        clean_c = clean_markdown_for_reportlab(c)
                        style = table_cell_bold if r_idx == 0 else table_cell
                        row_cells.append(Paragraph(clean_c, style))
                    formatted_table_data.append(row_cells)

                t = Table(formatted_table_data, colWidths=[col_width] * num_cols)
                t.setStyle(TableStyle([
                    ('BACKGROUND', (0, 0), (-1, 0), primary_green),
                    ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor("#CCCCCC")),
                    ('TOPPADDING', (0, 0), (-1, -1), 4),
                    ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
                    ('LEFTPADDING', (0, 0), (-1, -1), 4),
                    ('RIGHTPADDING', (0, 0), (-1, -1), 4),
                    ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, pale_bg]),
                    ('VALIGN', (0, 0), (-1, -1), 'TOP'),
                ]))
                story.append(t)
                story.append(Spacer(1, 8))
            continue

        # Headings
        if raw_line.startswith("# "):
            h_text = clean_markdown_for_reportlab(raw_line[2:].strip())
            story.append(Paragraph(h_text, h1_style))
        elif raw_line.startswith("## "):
            h_text = clean_markdown_for_reportlab(raw_line[3:].strip())
            story.append(Paragraph(h_text, h1_style))
        elif raw_line.startswith("### "):
            h_text = clean_markdown_for_reportlab(raw_line[4:].strip())
            story.append(Paragraph(h_text, h2_style))
        elif raw_line.startswith("#### "):
            h_text = clean_markdown_for_reportlab(raw_line[5:].strip())
            story.append(Paragraph(h_text, h3_style))
        elif raw_line.startswith("---") or raw_line.startswith("***"):
            story.append(HRFlowable(width="100%", thickness=0.8, color=border_green, spaceBefore=4, spaceAfter=6))
        elif raw_line.startswith("- ") or raw_line.startswith("* ") or (len(raw_line) > 2 and raw_line[0].isdigit() and raw_line[1] == "."):
            bullet_char = "• "
            if raw_line.startswith("- "):
                p_text = raw_line[2:].strip()
            elif raw_line.startswith("* "):
                p_text = raw_line[2:].strip()
            else:
                spl = raw_line.split(".", 1)
                p_text = spl[1].strip() if len(spl) > 1 else raw_line
                bullet_char = spl[0] + ". "

            p_text = clean_markdown_for_reportlab(p_text)
            story.append(Paragraph(f"{bullet_char}{p_text}", bullet_style))
        else:
            p_text = clean_markdown_for_reportlab(raw_line)
            story.append(Paragraph(p_text, body_style))
        
        i += 1

    doc.build(story, canvasmaker=NumberedCanvas)
    return buf.getvalue()


def sanitize_xml_text(text: str) -> str:
    """Removes invalid XML 1.0 control characters and cleans raw HTML tags that crash python-docx."""
    if not text:
        return ""
    # Strip HTML tags like <b>, </b>, <br>, <span>, <div>, etc.
    clean = re.sub(r'<[^>]+>', ' ', str(text))
    # Strip XML 1.0 disallowed control characters (ASCII 0-8, 11-12, 14-31, 127-159)
    clean = re.sub(r'[\x00-\x08\x0b\x0c\x0e-\x1f\x7f-\x84\x86-\x9f]', '', clean)
    return clean.strip()


def markdown_to_docx(markdown_text: str, title: str = "AgroBiometrix Report") -> bytes:
    """Converts markdown text to a styled, publication-grade Microsoft Word (.docx) buffer."""
    doc = docx.Document()
    
    # Page setup
    for section in doc.sections:
        section.top_margin = Inches(0.75)
        section.bottom_margin = Inches(0.75)
        section.left_margin = Inches(0.75)
        section.right_margin = Inches(0.75)

    # Document Title
    clean_title = sanitize_xml_text(title)
    title_p = doc.add_paragraph()
    title_run = title_p.add_run(clean_title)
    title_run.font.name = "Arial"
    title_run.font.size = Pt(18)
    title_run.font.bold = True
    title_run.font.color.rgb = RGBColor(0x1B, 0x5E, 0x20)
    title_p.paragraph_format.space_after = Pt(10)

    lines = markdown_text.split("\n")
    i = 0
    while i < len(lines):
        line = lines[i].strip()
        if not line:
            i += 1
            continue

        # Check for table
        if line.startswith("|") and line.endswith("|"):
            table_raw = []
            while i < len(lines) and lines[i].strip().startswith("|") and lines[i].strip().endswith("|"):
                row_line = lines[i].strip()
                if not re.match(r"^\|(\s*[-:]+\s*\|)+$", row_line):
                    cells = [c.strip() for c in row_line.split("|")[1:-1]]
                    table_raw.append(cells)
                i += 1
            
            if table_raw:
                num_cols = max(len(r) for r in table_raw)
                table = doc.add_table(rows=len(table_raw), cols=num_cols)
                table.alignment = WD_TABLE_ALIGNMENT.CENTER
                table.style = 'Table Grid'
                
                for r_idx, row in enumerate(table_raw):
                    for c_idx, cell_text in enumerate(row):
                        cell = table.cell(r_idx, c_idx)
                        cell.text = ""
                        p = cell.paragraphs[0]
                        p.paragraph_format.space_before = Pt(2)
                        p.paragraph_format.space_after = Pt(2)
                        clean_cell = sanitize_xml_text(cell_text.replace("**", ""))
                        run = p.add_run(clean_cell)
                        run.font.name = "Arial"
                        run.font.size = Pt(8.5)
                        
                        if r_idx == 0:
                            run.font.bold = True
                            run.font.color.rgb = RGBColor(0xFF, 0xFF, 0xFF)
                            shading_xml = parse_xml(r'<w:shd {} w:fill="1B5E20"/>'.format(nsdecls('w')))
                            cell._tc.get_or_add_tcPr().append(shading_xml)
                        elif r_idx % 2 == 1:
                            shading_xml = parse_xml(r'<w:shd {} w:fill="F1F8F2"/>'.format(nsdecls('w')))
                            cell._tc.get_or_add_tcPr().append(shading_xml)
                
                doc.add_paragraph().paragraph_format.space_after = Pt(6)
            continue

        # Headings
        if line.startswith("# "):
            h = doc.add_heading(level=1)
            r = h.add_run(sanitize_xml_text(line[2:].strip()))
            r.font.name = "Arial"
            r.font.color.rgb = RGBColor(0x1B, 0x5E, 0x20)
        elif line.startswith("## "):
            h = doc.add_heading(level=2)
            r = h.add_run(sanitize_xml_text(line[3:].strip()))
            r.font.name = "Arial"
            r.font.color.rgb = RGBColor(0x1B, 0x5E, 0x20)
        elif line.startswith("### "):
            h = doc.add_heading(level=3)
            r = h.add_run(sanitize_xml_text(line[4:].strip()))
            r.font.name = "Arial"
            r.font.color.rgb = RGBColor(0x2E, 0x7D, 0x32)
        elif line.startswith("#### "):
            h = doc.add_heading(level=4)
            r = h.add_run(sanitize_xml_text(line[5:].strip()))
            r.font.name = "Arial"
            r.font.color.rgb = RGBColor(0x33, 0x33, 0x33)
        elif line.startswith("---") or line.startswith("***"):
            p = doc.add_paragraph()
            p.paragraph_format.space_after = Pt(4)
        elif line.startswith("- ") or line.startswith("* "):
            p = doc.add_paragraph(style='List Bullet')
            _add_markdown_runs(p, line[2:].strip())
        elif len(line) > 2 and line[0].isdigit() and line[1] == ".":
            p = doc.add_paragraph(style='List Number')
            _add_markdown_runs(p, line.split(".", 1)[1].strip())
        else:
            p = doc.add_paragraph()
            _add_markdown_runs(p, line)

        i += 1

    buf = io.BytesIO()
    doc.save(buf)
    return buf.getvalue()


def _add_markdown_runs(paragraph, text: str):
    """Helper to parse bold (**...**) and italics (*...*) into docx runs safely."""
    # First sanitize XML invalid characters
    sanitized = re.sub(r'[\x00-\x08\x0b\x0c\x0e-\x1f\x7f-\x84\x86-\x9f]', '', str(text))
    # Strip raw HTML tags like <b>, </b>, <span>
    sanitized = re.sub(r'<[^>]+>', ' ', sanitized)
    
    parts = re.split(r'(\*\*.*?\*\*|\*.*?\*)', sanitized)
    for part in parts:
        if not part:
            continue
        if part.startswith("**") and part.endswith("**") and len(part) >= 4:
            clean_part = part[2:-2].strip()
            if clean_part:
                run = paragraph.add_run(clean_part)
                run.font.name = "Arial"
                run.font.size = Pt(9.5)
                run.font.bold = True
        elif part.startswith("*") and part.endswith("*") and len(part) >= 2:
            clean_part = part[1:-1].strip()
            if clean_part:
                run = paragraph.add_run(clean_part)
                run.font.name = "Arial"
                run.font.size = Pt(9.5)
                run.font.italic = True
        else:
            run = paragraph.add_run(part)
            run.font.name = "Arial"
            run.font.size = Pt(9.5)


def render_download_buttons(
    content_text: str,
    filename_prefix: str = "AgroBiometrix_Document",
    title: str = "AgroBiometrix Scientific Report",
    key_prefix: str = "dl"
):
    """
    Renders 3 publication-ready download buttons in Streamlit:
    1. PDF (.pdf)
    2. Microsoft Word (.docx)
    3. Markdown (.md)
    """
    st.markdown("##### 📥 Export Document in Publication Formats:")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        try:
            pdf_bytes = markdown_to_pdf(content_text, title=title)
            st.download_button(
                label="📄 Download PDF (.pdf)",
                data=pdf_bytes,
                file_name=f"{filename_prefix}.pdf",
                mime="application/pdf",
                key=f"{key_prefix}_pdf"
            )
        except Exception as e:
            st.caption(f"PDF export error: {e}")
            
    with col2:
        try:
            docx_bytes = markdown_to_docx(content_text, title=title)
            st.download_button(
                label="📝 Download Word (.docx)",
                data=docx_bytes,
                file_name=f"{filename_prefix}.docx",
                mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
                key=f"{key_prefix}_docx"
            )
        except Exception as e:
            st.caption(f"Word export error: {e}")
            
    with col3:
        st.download_button(
            label="📋 Download Markdown (.md)",
            data=content_text.encode("utf-8"),
            file_name=f"{filename_prefix}.md",
            mime="text/markdown",
            key=f"{key_prefix}_md"
        )
