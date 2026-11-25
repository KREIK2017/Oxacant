from __future__ import annotations

import re
from datetime import date
from pathlib import Path

from docx import Document
from docx.enum.section import WD_SECTION
from docx.enum.table import WD_CELL_VERTICAL_ALIGNMENT, WD_TABLE_ALIGNMENT
from docx.enum.text import WD_ALIGN_PARAGRAPH, WD_BREAK, WD_LINE_SPACING
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from docx.shared import Cm, Inches, Pt, RGBColor


ROOT = Path(r"D:\Рабочий стол\projeckts\!AlpenPharma\Oxacant")
SOURCE = ROOT / "TZ_OXACANT_DESIGN_REFINEMENT_UA.md"
OUTPUT = ROOT / "output" / "docx" / "TZ_Oxacant_Design_UA.docx"

INK = "111111"
DEEP = "0B4650"
GREEN = "B8D84B"
PALE = "F2F6F0"
PALE_ALT = "F8FAF7"
GRID = "D9D9D9"
MUTED = "5E7272"


def set_cell_shading(cell, fill: str) -> None:
    tc_pr = cell._tc.get_or_add_tcPr()
    shd = tc_pr.find(qn("w:shd"))
    if shd is None:
        shd = OxmlElement("w:shd")
        tc_pr.append(shd)
    shd.set(qn("w:fill"), fill)


def set_cell_borders(cell, color: str = GRID, size: str = "6") -> None:
    tc_pr = cell._tc.get_or_add_tcPr()
    borders = tc_pr.find(qn("w:tcBorders"))
    if borders is None:
        borders = OxmlElement("w:tcBorders")
        tc_pr.append(borders)
    for edge in ("top", "left", "bottom", "right", "insideH", "insideV"):
        tag = qn(f"w:{edge}")
        element = borders.find(tag)
        if element is None:
            element = OxmlElement(f"w:{edge}")
            borders.append(element)
        element.set(qn("w:val"), "single")
        element.set(qn("w:sz"), size)
        element.set(qn("w:color"), color)


def set_cell_margins(cell, top=110, start=130, bottom=110, end=130) -> None:
    tc = cell._tc
    tc_pr = tc.get_or_add_tcPr()
    tc_mar = tc_pr.first_child_found_in("w:tcMar")
    if tc_mar is None:
        tc_mar = OxmlElement("w:tcMar")
        tc_pr.append(tc_mar)
    for margin, value in (("top", top), ("start", start), ("bottom", bottom), ("end", end)):
        node = tc_mar.find(qn(f"w:{margin}"))
        if node is None:
            node = OxmlElement(f"w:{margin}")
            tc_mar.append(node)
        node.set(qn("w:w"), str(value))
        node.set(qn("w:type"), "dxa")


def set_repeat_table_header(row) -> None:
    tr_pr = row._tr.get_or_add_trPr()
    tbl_header = OxmlElement("w:tblHeader")
    tbl_header.set(qn("w:val"), "true")
    tr_pr.append(tbl_header)


def set_font(run, name="Arial", size=None, bold=None, color=None, italic=None) -> None:
    run.font.name = name
    run._element.get_or_add_rPr().rFonts.set(qn("w:ascii"), name)
    run._element.get_or_add_rPr().rFonts.set(qn("w:hAnsi"), name)
    run._element.get_or_add_rPr().rFonts.set(qn("w:eastAsia"), name)
    if size is not None:
        run.font.size = Pt(size)
    if bold is not None:
        run.bold = bold
    if color is not None:
        run.font.color.rgb = RGBColor.from_string(color)
    if italic is not None:
        run.italic = italic


def add_hyperlink(paragraph, text: str, url: str, color=DEEP, underline=True):
    part = paragraph.part
    r_id = part.relate_to(url, "http://schemas.openxmlformats.org/officeDocument/2006/relationships/hyperlink", is_external=True)
    hyperlink = OxmlElement("w:hyperlink")
    hyperlink.set(qn("r:id"), r_id)
    new_run = OxmlElement("w:r")
    r_pr = OxmlElement("w:rPr")
    r_fonts = OxmlElement("w:rFonts")
    r_fonts.set(qn("w:ascii"), "Arial")
    r_fonts.set(qn("w:hAnsi"), "Arial")
    r_pr.append(r_fonts)
    color_el = OxmlElement("w:color")
    color_el.set(qn("w:val"), color)
    r_pr.append(color_el)
    if underline:
        u = OxmlElement("w:u")
        u.set(qn("w:val"), "single")
        r_pr.append(u)
    new_run.append(r_pr)
    text_el = OxmlElement("w:t")
    text_el.text = text
    new_run.append(text_el)
    hyperlink.append(new_run)
    paragraph._p.append(hyperlink)
    return hyperlink


INLINE_PATTERN = re.compile(r"(\*\*.+?\*\*|`.+?`|https?://[^\s)]+)")


def add_inline(paragraph, text: str, *, base_size=10.5, base_color=INK, italic=False) -> None:
    cursor = 0
    for match in INLINE_PATTERN.finditer(text):
        if match.start() > cursor:
            run = paragraph.add_run(text[cursor:match.start()])
            set_font(run, size=base_size, color=base_color, italic=italic)
        token = match.group(0)
        if token.startswith("**"):
            run = paragraph.add_run(token[2:-2])
            set_font(run, size=base_size, bold=True, color=base_color, italic=italic)
        elif token.startswith("`"):
            run = paragraph.add_run(token[1:-1])
            set_font(run, name="Consolas", size=base_size - 0.5, color=DEEP, italic=italic)
        else:
            add_hyperlink(paragraph, token, token)
        cursor = match.end()
    if cursor < len(text):
        run = paragraph.add_run(text[cursor:])
        set_font(run, size=base_size, color=base_color, italic=italic)


def add_page_number(paragraph) -> None:
    paragraph.alignment = WD_ALIGN_PARAGRAPH.RIGHT
    run = paragraph.add_run()
    set_font(run, size=8.5, color=MUTED)
    fld_char1 = OxmlElement("w:fldChar")
    fld_char1.set(qn("w:fldCharType"), "begin")
    instr_text = OxmlElement("w:instrText")
    instr_text.set(qn("xml:space"), "preserve")
    instr_text.text = "PAGE"
    fld_char2 = OxmlElement("w:fldChar")
    fld_char2.set(qn("w:fldCharType"), "end")
    run._r.append(fld_char1)
    run._r.append(instr_text)
    run._r.append(fld_char2)


def configure_styles(doc: Document) -> None:
    styles = doc.styles

    normal = styles["Normal"]
    normal.font.name = "Arial"
    normal._element.rPr.rFonts.set(qn("w:ascii"), "Arial")
    normal._element.rPr.rFonts.set(qn("w:hAnsi"), "Arial")
    normal.font.size = Pt(10.5)
    normal.font.color.rgb = RGBColor.from_string(INK)
    normal.paragraph_format.space_after = Pt(6)
    normal.paragraph_format.line_spacing = 1.18

    title = styles["Title"]
    title.font.name = "Arial"
    title._element.rPr.rFonts.set(qn("w:ascii"), "Arial")
    title._element.rPr.rFonts.set(qn("w:hAnsi"), "Arial")
    title.font.size = Pt(29)
    title.font.bold = True
    title.font.color.rgb = RGBColor.from_string("000000")
    title.paragraph_format.space_after = Pt(12)
    title.paragraph_format.line_spacing = 1.03

    subtitle = styles["Subtitle"]
    subtitle.font.name = "Arial"
    subtitle._element.rPr.rFonts.set(qn("w:ascii"), "Arial")
    subtitle._element.rPr.rFonts.set(qn("w:hAnsi"), "Arial")
    subtitle.font.size = Pt(15)
    subtitle.font.color.rgb = RGBColor.from_string(MUTED)
    subtitle.paragraph_format.space_after = Pt(16)

    h1 = styles["Heading 1"]
    h1.font.name = "Arial"
    h1._element.rPr.rFonts.set(qn("w:ascii"), "Arial")
    h1._element.rPr.rFonts.set(qn("w:hAnsi"), "Arial")
    h1.font.size = Pt(18)
    h1.font.bold = True
    h1.font.color.rgb = RGBColor.from_string("000000")
    h1.paragraph_format.space_before = Pt(18)
    h1.paragraph_format.space_after = Pt(8)
    h1.paragraph_format.keep_with_next = True

    h2 = styles["Heading 2"]
    h2.font.name = "Arial"
    h2._element.rPr.rFonts.set(qn("w:ascii"), "Arial")
    h2._element.rPr.rFonts.set(qn("w:hAnsi"), "Arial")
    h2.font.size = Pt(13.5)
    h2.font.bold = True
    h2.font.color.rgb = RGBColor.from_string("000000")
    h2.paragraph_format.space_before = Pt(12)
    h2.paragraph_format.space_after = Pt(6)
    h2.paragraph_format.keep_with_next = True

    for name in ("List Bullet", "List Number"):
        style = styles[name]
        style.font.name = "Arial"
        style._element.rPr.rFonts.set(qn("w:ascii"), "Arial")
        style._element.rPr.rFonts.set(qn("w:hAnsi"), "Arial")
        style.font.size = Pt(10.5)
        style.font.color.rgb = RGBColor.from_string(INK)
        style.paragraph_format.space_after = Pt(3)
        style.paragraph_format.line_spacing = 1.12


def add_table(doc: Document, rows: list[list[str]]) -> None:
    if not rows:
        return
    table = doc.add_table(rows=1, cols=len(rows[0]))
    table.alignment = WD_TABLE_ALIGNMENT.CENTER
    table.autofit = False
    table.style = "Table Grid"

    widths = None
    if len(rows[0]) == 3 and rows[0][0].strip() == "№":
        widths = [Cm(1.0), Cm(4.2), Cm(11.2)]
    elif len(rows[0]) == 3:
        widths = [Cm(7.0), Cm(4.2), Cm(4.2)]

    header = table.rows[0]
    set_repeat_table_header(header)
    for idx, text in enumerate(rows[0]):
        cell = header.cells[idx]
        if widths:
            cell.width = widths[idx]
        set_cell_shading(cell, DEEP)
        set_cell_borders(cell)
        set_cell_margins(cell, top=120, start=140, bottom=120, end=140)
        cell.vertical_alignment = WD_CELL_VERTICAL_ALIGNMENT.CENTER
        p = cell.paragraphs[0]
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER if idx == 0 else WD_ALIGN_PARAGRAPH.LEFT
        p.paragraph_format.space_after = Pt(0)
        run = p.add_run(text)
        set_font(run, size=9.5, bold=True, color="FFFFFF")

    for row_index, row_data in enumerate(rows[1:], start=1):
        cells = table.add_row().cells
        for idx, text in enumerate(row_data):
            cell = cells[idx]
            if widths:
                cell.width = widths[idx]
            set_cell_shading(cell, "FFFFFF" if row_index % 2 else PALE)
            set_cell_borders(cell)
            set_cell_margins(cell)
            cell.vertical_alignment = WD_CELL_VERTICAL_ALIGNMENT.CENTER
            p = cell.paragraphs[0]
            p.alignment = WD_ALIGN_PARAGRAPH.CENTER if idx == 0 and len(row_data) == 3 else WD_ALIGN_PARAGRAPH.LEFT
            p.paragraph_format.space_after = Pt(0)
            add_inline(p, text, base_size=9.2)

    paragraph = doc.add_paragraph()
    paragraph.paragraph_format.space_after = Pt(2)


def parse_markdown(doc: Document, markdown: str) -> None:
    lines = markdown.splitlines()
    i = 0
    skipped_title = False
    paragraph_buffer: list[str] = []

    def flush_paragraph() -> None:
        nonlocal paragraph_buffer
        if paragraph_buffer:
            text = " ".join(line.strip() for line in paragraph_buffer).strip()
            if text:
                p = doc.add_paragraph()
                add_inline(p, text)
            paragraph_buffer = []

    while i < len(lines):
        raw = lines[i]
        line = raw.strip()

        if not line:
            flush_paragraph()
            i += 1
            continue

        if line.startswith("# ") and not skipped_title:
            skipped_title = True
            i += 1
            continue

        if line.startswith("## "):
            flush_paragraph()
            p = doc.add_paragraph(style="Heading 1")
            add_inline(p, line[3:].strip(), base_size=18)
            i += 1
            continue

        if line.startswith("### "):
            flush_paragraph()
            p = doc.add_paragraph(style="Heading 2")
            add_inline(p, line[4:].strip(), base_size=13.5)
            i += 1
            continue

        if line.startswith("|"):
            flush_paragraph()
            table_lines = []
            while i < len(lines) and lines[i].strip().startswith("|"):
                table_lines.append(lines[i].strip())
                i += 1
            parsed = []
            for table_line in table_lines:
                cells = [c.strip() for c in table_line.strip("|").split("|")]
                if all(re.fullmatch(r":?-{3,}:?", c) for c in cells):
                    continue
                parsed.append(cells)
            add_table(doc, parsed)
            continue

        if line.startswith("- "):
            flush_paragraph()
            p = doc.add_paragraph(style="List Bullet")
            add_inline(p, line[2:].strip())
            i += 1
            continue

        if re.match(r"^\d+\.\s", line):
            flush_paragraph()
            p = doc.add_paragraph(style="List Number")
            add_inline(p, re.sub(r"^\d+\.\s+", "", line))
            i += 1
            continue

        if line.startswith("> "):
            flush_paragraph()
            p = doc.add_paragraph()
            p.paragraph_format.left_indent = Cm(0.7)
            p.paragraph_format.right_indent = Cm(0.4)
            p.paragraph_format.space_before = Pt(4)
            p.paragraph_format.space_after = Pt(8)
            add_inline(p, line[2:].strip(), base_size=10.5, base_color=MUTED, italic=True)
            i += 1
            continue

        paragraph_buffer.append(line)
        i += 1

    flush_paragraph()


def build() -> None:
    markdown = SOURCE.read_text(encoding="utf-8")
    doc = Document()
    configure_styles(doc)

    section = doc.sections[0]
    section.page_width = Cm(21)
    section.page_height = Cm(29.7)
    section.top_margin = Cm(1.8)
    section.bottom_margin = Cm(1.7)
    section.left_margin = Cm(1.9)
    section.right_margin = Cm(1.9)

    doc.core_properties.title = "Технічне завдання для дизайнерів Oxacant"
    doc.core_properties.subject = "Візуальне доопрацювання advertorial Oxacant sedativ Liquid"
    doc.core_properties.author = "Oxacant project"
    doc.core_properties.keywords = "Oxacant, design handoff, Figma, advertorial"

    # Cover
    kicker = doc.add_paragraph()
    kicker.paragraph_format.space_before = Pt(46)
    kicker.paragraph_format.space_after = Pt(16)
    run = kicker.add_run("DESIGN HANDOFF  2026")
    set_font(run, size=10, bold=True, color=DEEP)

    title = doc.add_paragraph(style="Title")
    title.add_run("Технічне завдання для дизайнерів")

    subtitle = doc.add_paragraph(style="Subtitle")
    subtitle.add_run("Візуальне доопрацювання advertorial Oxacant® sedativ Liquid")

    intro = doc.add_paragraph()
    intro.paragraph_format.space_before = Pt(18)
    intro.paragraph_format.space_after = Pt(18)
    intro.paragraph_format.line_spacing = 1.25
    add_inline(
        intro,
        "Документ визначає завдання для фінального UI/UX-полірування сторінки у Figma: адаптивність, відступи, типографіку, кольорову систему, фотонапрям і сценарій медичного попередження.",
        base_size=12,
        base_color=INK,
    )

    ref_label = doc.add_paragraph()
    ref_label.paragraph_format.space_before = Pt(8)
    run = ref_label.add_run("Основний референс")
    set_font(run, size=9.5, bold=True, color=MUTED)
    ref = doc.add_paragraph()
    add_hyperlink(ref, "oxacant.maksimkamychko.workers.dev", "https://oxacant.maksimkamychko.workers.dev/")

    date_p = doc.add_paragraph()
    date_p.paragraph_format.space_before = Pt(44)
    run = date_p.add_run("29 жовтня 2026")
    set_font(run, size=10, color=MUTED)

    doc.add_page_break()
    parse_markdown(doc, markdown)

    # Footer
    for sec in doc.sections:
        footer = sec.footer
        table = footer.add_table(rows=1, cols=2, width=Cm(17.2))
        table.autofit = False
        table.columns[0].width = Cm(13.8)
        table.columns[1].width = Cm(3.4)
        left = table.cell(0, 0).paragraphs[0]
        left.paragraph_format.space_after = Pt(0)
        r = left.add_run("Oxacant®  ·  ТЗ для дизайнерів")
        set_font(r, size=8.5, color=MUTED)
        right = table.cell(0, 1).paragraphs[0]
        right.paragraph_format.space_after = Pt(0)
        add_page_number(right)
        for cell in table.rows[0].cells:
            tc_pr = cell._tc.get_or_add_tcPr()
            borders = OxmlElement("w:tcBorders")
            for edge in ("top", "left", "bottom", "right", "insideH", "insideV"):
                e = OxmlElement(f"w:{edge}")
                e.set(qn("w:val"), "nil")
                borders.append(e)
            tc_pr.append(borders)

    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    doc.save(OUTPUT)
    print(OUTPUT)


if __name__ == "__main__":
    build()
