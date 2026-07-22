# -*- coding: utf-8 -*-
"""
Builds Aria-CV-En.docx / Aria-CV-Fa.docx from scripts/resume_data.py, then
converts each to a matching .pdf with LibreOffice headless — so the PDF is
literally an export of the Word file, guaranteeing the two are identical.

Design goals (per spec): plain, non-graphical, black-and-white, compact,
small font, classic and highly readable, correct/principled use of bold
and italic, ATS-safe (no tables, no icons, no colored chips, no text
boxes) — built to be parsed cleanly by applicant-tracking systems as well
as read comfortably by a human.

Usage:
    python3 build_resume_docs.py

Output:
    assets/files/Aria-CV-En.docx / .pdf
    assets/files/Aria-CV-Fa.docx / .pdf
"""

import subprocess
import sys
from datetime import date
from pathlib import Path

from docx import Document
from docx.enum.text import WD_ALIGN_PARAGRAPH, WD_TAB_ALIGNMENT
from docx.enum.section import WD_SECTION
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from docx.shared import Pt, Cm, RGBColor

sys.path.insert(0, str(Path(__file__).parent))
from resume_data import RESUME_EN, RESUME_FA  # noqa: E402

OUT_DIR = Path(__file__).parent.parent / "assets" / "files"

INK = RGBColor(0x1A, 0x1A, 0x1A)
GREY = RGBColor(0x6E, 0x6E, 0x6E)
LIGHT_GREY = RGBColor(0xA8, 0xA8, 0xA8)
RULE_GREY = RGBColor(0x33, 0x33, 0x33)

FONT_EN = "Arial"
FONT_FA = "Tahoma"


def set_rtl_paragraph(paragraph):
    """Mark a paragraph as bidi (right-to-left) at the XML level — this is
    what makes Word lay it out RTL regardless of which font is applied."""
    pPr = paragraph._p.get_or_add_pPr()
    bidi = OxmlElement("w:bidi")
    pPr.append(bidi)


def set_rtl_run(run):
    rPr = run._r.get_or_add_rPr()
    rtl = OxmlElement("w:rtl")
    rPr.append(rtl)


def add_right_tab(paragraph, usable_width_cm):
    tab_stops = paragraph.paragraph_format.tab_stops
    tab_stops.add_tab_stop(Cm(usable_width_cm), WD_TAB_ALIGNMENT.RIGHT)


class ResumeBuilder:
    """One instance per language. Call .build() then .save(path)."""

    def __init__(self, data, is_fa):
        self.data = data
        self.is_fa = is_fa
        self.font = FONT_FA if is_fa else FONT_EN
        self.doc = Document()
        self._setup_page()

    # ---- low-level helpers -------------------------------------------------

    def _setup_page(self):
        section = self.doc.sections[0]
        section.page_width = Cm(21.0)
        section.page_height = Cm(29.7)
        section.top_margin = Cm(0.4)
        section.bottom_margin = Cm(0.35)
        section.left_margin = Cm(1.6)
        section.right_margin = Cm(1.6)
        self.usable_width_cm = 21.0 - 1.6 - 1.6

        normal = self.doc.styles["Normal"]
        normal.font.name = self.font
        normal.font.size = Pt(9.0)
        normal.font.color.rgb = INK
        # ensure the East-Asian/complex-script font slot also points at our
        # font, otherwise some renderers fall back to a default for Arabic
        # script even when the "ascii" font is set correctly
        rpr = normal.element.get_or_add_rPr()
        rFonts = rpr.find(qn("w:rFonts"))
        if rFonts is None:
            rFonts = OxmlElement("w:rFonts")
            rpr.append(rFonts)
        rFonts.set(qn("w:cs"), self.font)
        rFonts.set(qn("w:ascii"), self.font)
        rFonts.set(qn("w:hAnsi"), self.font)

    def _para(self, align=None, space_before=0, space_after=2, rtl=None):
        p = self.doc.add_paragraph()
        if align is not None:
            p.alignment = align
        p.paragraph_format.space_before = Pt(space_before)
        p.paragraph_format.space_after = Pt(space_after)
        p.paragraph_format.line_spacing = 0.95
        if rtl is None:
            rtl = self.is_fa
        if rtl:
            set_rtl_paragraph(p)
        return p

    def _run(self, paragraph, text, bold=False, italic=False, size=9.2, color=INK, font=None):
        run = paragraph.add_run(text)
        run.font.name = font or self.font
        run.font.size = Pt(size)
        run.font.bold = bold
        run.font.italic = italic
        run.font.color.rgb = color
        if self.is_fa:
            set_rtl_run(run)
            rpr = run._r.get_or_add_rPr()
            rFonts = rpr.find(qn("w:rFonts"))
            if rFonts is None:
                rFonts = OxmlElement("w:rFonts")
                rpr.append(rFonts)
            rFonts.set(qn("w:cs"), font or self.font)
        return run

    def _section_title(self, text):
        p = self._para(space_before=3, space_after=1)
        self._run(p, text.upper() if not self.is_fa else text, bold=True, size=9.3)
        # thin classic rule under the heading
        pPr = p._p.get_or_add_pPr()
        pBdr = OxmlElement("w:pBdr")
        bottom = OxmlElement("w:bottom")
        bottom.set(qn("w:val"), "single")
        bottom.set(qn("w:sz"), "5")
        bottom.set(qn("w:space"), "2")
        bottom.set(qn("w:color"), "333333")
        pBdr.append(bottom)
        pPr.append(pBdr)
        p.paragraph_format.space_after = Pt(2)
        return p

    def _entry_head_line(self, left_text, right_text, left_bold, left_italic=False):
        """Classic resume pattern: left-aligned text, right-aligned date,
        using a right tab stop rather than a table (safer for ATS parsers
        and screen readers alike)."""
        p = self._para(space_before=0, space_after=0)
        add_right_tab(p, self.usable_width_cm)
        self._run(p, left_text, bold=left_bold, italic=left_italic, size=9.7)
        if right_text:
            self._run(p, "\t" + right_text, italic=False, size=8.4, color=GREY, font=self.font)
        return p

    def _bullet(self, text):
        p = self._para(space_before=0, space_after=0)
        p.paragraph_format.left_indent = Cm(0.5)
        marker = "\u2013 " if not self.is_fa else ""
        suffix = " \u2013" if self.is_fa else ""
        self._run(p, (marker + text + suffix) if self.is_fa else (marker + text), size=8.6, color=RGBColor(0x33, 0x33, 0x33))

    # ---- sections ------------------------------------------------------

    def header(self):
        d = self.data
        p = self._para(align=WD_ALIGN_PARAGRAPH.CENTER, space_after=0)
        self._run(p, d["name"], bold=True, size=15.5)

        p = self._para(align=WD_ALIGN_PARAGRAPH.CENTER, space_after=1)
        self._run(p, d["role"], italic=True, size=9.6, color=GREY)

        p = self._para(align=WD_ALIGN_PARAGRAPH.CENTER, space_after=3)
        self._run(p, d["contact"], size=8.1, color=GREY)

    def about(self):
        self._section_title("About" if not self.is_fa else "\u062f\u0631\u0628\u0627\u0631\u0647\u200c\u0645\u0646")
        p = self._para(space_after=3)
        p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY if not self.is_fa else WD_ALIGN_PARAGRAPH.JUSTIFY
        self._run(p, self.data["about"], size=9.1)

    def interests(self):
        self._section_title("Interests" if not self.is_fa else "\u0639\u0644\u0627\u0642\u0647\u200c\u0645\u0646\u062f\u06cc\u200c\u0647\u0627")
        p = self._para(space_after=3)
        p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
        self._run(p, self.data["interests"], size=9.1)

    def education(self):
        self._section_title("Education" if not self.is_fa else "\u062a\u062d\u0635\u06cc\u0644\u0627\u062a")
        for e in self.data["education"]:
            self._entry_head_line(e["degree"], e["period"], left_bold=True)
            p = self._para(space_after=0)
            self._run(p, e["org"], italic=True, size=8.5, color=GREY)
            for note in e["notes"]:
                self._bullet(note)

    def experience(self):
        title = "Professional Experience" if not self.is_fa else "\u062a\u062c\u0631\u0628\u0647 \u062d\u0631\u0641\u0647\u200c\u0627\u06cc"
        self._section_title(title)
        for e in self.data["experience"]:
            # org is the bold heading now; role + period follow beneath it
            p = self._para(space_before=3, space_after=0)
            self._run(p, e["org"], bold=True, size=9.2)
            self._entry_head_line(e["role"], e["period"], left_bold=False, left_italic=True)

    def books(self):
        self._section_title("Books" if not self.is_fa else "\u06a9\u062a\u0627\u0628\u200c\u0647\u0627")
        for b in self.data["books"]:
            p = self._para(space_before=2, space_after=0)
            self._run(p, b["citation"], size=8.9)
            p2 = self._para(space_after=0)
            self._run(p2, b["role"], italic=True, size=8.3, color=GREY)

    def _chip_group(self, groups):
        for label, items in groups.items():
            p = self._para(space_before=1, space_after=0)
            self._run(p, label + ":  ", bold=True, size=8.8)
            self._run(p, "  \u2022  ".join(items), size=8.8)

    def skills(self):
        self._section_title("Skills" if not self.is_fa else "\u0645\u0647\u0627\u0631\u062a\u200c\u0647\u0627")
        self._chip_group(self.data["skills"])

    def software(self):
        self._section_title("Software" if not self.is_fa else "\u0646\u0631\u0645\u200c\u0627\u0641\u0632\u0627\u0631\u0647\u0627")
        self._chip_group(self.data["software"])

    def languages(self):
        self._section_title("Languages" if not self.is_fa else "\u0632\u0628\u0627\u0646\u200c\u0647\u0627")
        parts = [f'{l["name"]} \u2014 {l["level"]}' for l in self.data["languages"]]
        p = self._para(space_after=3)
        self._run(p, "   |   ".join(parts), size=8.8)

    def memberships(self):
        title = "Professional Memberships" if not self.is_fa else "\u0639\u0636\u0648\u06cc\u062a\u200c\u0647\u0627\u06cc \u062d\u0631\u0641\u0647\u200c\u0627\u06cc"
        self._section_title(title)
        for m in self.data["memberships"]:
            self._entry_head_line(m["role"], m["period"], left_bold=True)
            p = self._para(space_after=0)
            self._run(p, m["org"], italic=True, size=8.5, color=GREY)

    def volunteer(self):
        title = "Volunteer Activities" if not self.is_fa else "\u0641\u0639\u0627\u0644\u06cc\u062a\u200c\u0647\u0627\u06cc \u062f\u0627\u0648\u0637\u0644\u0628\u0627\u0646\u0647"
        self._section_title(title)
        for v in self.data["volunteer"]:
            self._entry_head_line(v["role"], v["period"], left_bold=True)
            p = self._para(space_after=0)
            self._run(p, v["org"], italic=True, size=8.5, color=GREY)

    def footer(self):
        section = self.doc.sections[0]
        footer = section.footer
        p = footer.paragraphs[0]
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        if self.is_fa:
            set_rtl_paragraph(p)
        label = "Last updated: " if not self.is_fa else "\u0622\u062e\u0631\u06cc\u0646 \u0628\u0647\u200c\u0631\u0648\u0632\u0631\u0633\u0627\u0646\u06cc: "
        today = date.today().strftime("%Y-%m")
        self._run(p, label + today, size=7, color=LIGHT_GREY, italic=False, font=self.font)

    def build(self):
        self.header()
        self.about()
        self.interests()
        self.education()
        self.experience()
        self.books()
        self.skills()
        self.software()
        self.languages()
        self.memberships()
        self.volunteer()
        self.footer()
        return self.doc

    def save(self, path):
        self.doc.save(str(path))


def convert_to_pdf(docx_path, out_dir):
    subprocess.run(
        ["soffice", "--headless", "--convert-to", "pdf", "--outdir", str(out_dir), str(docx_path)],
        check=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )


def main():
    OUT_DIR.mkdir(parents=True, exist_ok=True)

    jobs = [
        (RESUME_EN, False, "Aria-CV-En"),
        (RESUME_FA, True, "Aria-CV-Fa"),
    ]

    for data, is_fa, stem in jobs:
        builder = ResumeBuilder(data, is_fa)
        builder.build()
        docx_path = OUT_DIR / f"{stem}.docx"
        builder.save(docx_path)
        print(f"wrote {docx_path}")
        convert_to_pdf(docx_path, OUT_DIR)
        print(f"converted {stem}.docx -> {stem}.pdf")


if __name__ == "__main__":
    main()
