"""
pdf_generator.py
================
A modular PDF generation engine with two fully independent visual styles:
  - "professional": Clean, minimalistic corporate layout
  - "cyber":        Neon/cyberpunk code-aesthetic layout

Entry point
-----------
    generate_pdf(style, data, output_path)

Supported styles
----------------
    "professional"  →  ProfessionalStyle
    "cyber"         →  CyberStyle

Data dict keys (all optional unless noted)
------------------------------------------
    title           str   – Main document title
    subtitle        str   – Secondary headline
    date            str   – Date string shown in header
    reference       str   – Reference / document ID
    company         str   – Company or author name
    logo_path       str   – Absolute path to a PNG logo (professional only)
    contact         str   – Footer contact line
    sections        list  – [{"heading": str, "body": str}, ...]
    table           dict  – {"headers": [...], "rows": [[...], ...]}
    ascii_art       str   – Pre-formatted ASCII block (cyber only)
    hash_id         str   – Hash-like ID for cyber footer
"""

from __future__ import annotations

import hashlib
import math
import os
import time
from abc import ABC, abstractmethod
from datetime import datetime
from typing import Any

from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.units import mm
from reportlab.pdfgen import canvas
from reportlab.platypus import (
    BaseDocTemplate,
    Frame,
    PageTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle,
)

# ---------------------------------------------------------------------------
# Shared helpers
# ---------------------------------------------------------------------------

W, H = A4  # 595.27 x 841.89 pts


def _hex(h: str) -> colors.HexColor:
    return colors.HexColor(h)


def _safe(data: dict, key: str, default: Any = None) -> Any:
    """Return data[key] only when it's a non-empty string (or truthy value)."""
    v = data.get(key, default)
    if isinstance(v, str):
        return v.strip() or default
    return v


# ---------------------------------------------------------------------------
# Abstract base style
# ---------------------------------------------------------------------------

class BaseStyle(ABC):
    """Strategy interface.  Each concrete style handles its own canvas drawing."""

    def __init__(self, data: dict):
        self.data = data

    @abstractmethod
    def build(self, output_path: str) -> None:
        ...


# ===========================================================================
# 1.  PROFESSIONAL / MINIMALISTIC STYLE
# ===========================================================================

class ProfessionalStyle(BaseStyle):
    """
    Clean, modern layout.
    Palette: #1A1A1A  #4A4A4A  #EAEAEA  #007ACC
    """

    # --- palette ---
    C_DARK   = _hex("#1A1A1A")
    C_MID    = _hex("#4A4A4A")
    C_LIGHT  = _hex("#EAEAEA")
    C_ACCENT = _hex("#007ACC")
    C_WHITE  = colors.white
    C_ALT_ROW = _hex("#F5F8FB")

    # --- layout ---
    MARGIN_X = 18 * mm
    MARGIN_Y = 16 * mm
    HEADER_H = 28 * mm
    FOOTER_H = 14 * mm

    def build(self, output_path: str) -> None:
        c = canvas.Canvas(output_path, pagesize=A4)
        c.setTitle(_safe(self.data, "title", "Document"))

        page_num = [0]

        def draw_page(c: canvas.Canvas) -> None:
            page_num[0] += 1
            self._draw_header(c)
            self._draw_footer(c, page_num[0])

        # ---- build content area ----
        content_y = H - self.HEADER_H - self.MARGIN_Y
        draw_page(c)
        content_y = self._draw_body(c, content_y, draw_page)

        c.save()

    # ------------------------------------------------------------------
    def _draw_header(self, c: canvas.Canvas) -> None:
        mx, hy = self.MARGIN_X, self.HEADER_H

        # Accent bar at very top
        c.setFillColor(self.C_ACCENT)
        c.rect(0, H - 6, W, 6, fill=1, stroke=0)

        # Logo
        logo = _safe(self.data, "logo_path")
        logo_right = self.MARGIN_X  # track where logo ends (for title offset)
        if logo and os.path.isfile(logo):
            try:
                c.drawImage(logo, mx, H - hy + 4 * mm,
                            width=22 * mm, height=14 * mm,
                            preserveAspectRatio=True, mask="auto")
                logo_right = mx + 26 * mm
            except Exception:
                pass

        # Title
        title = _safe(self.data, "title")
        if title:
            c.setFont("Helvetica-Bold", 18)
            c.setFillColor(self.C_DARK)
            c.drawString(logo_right, H - 14 * mm, title)

        # Subtitle
        subtitle = _safe(self.data, "subtitle")
        if subtitle:
            c.setFont("Helvetica", 12)
            c.setFillColor(self.C_MID)
            c.drawString(logo_right, H - 20 * mm, subtitle)

        # Right-side meta: date + reference
        right_x = W - self.MARGIN_X
        meta_y   = H - 13 * mm
        date_str = _safe(self.data, "date")
        ref_str  = _safe(self.data, "reference")
        if date_str:
            c.setFont("Helvetica", 9)
            c.setFillColor(self.C_MID)
            c.drawRightString(right_x, meta_y, date_str)
            meta_y -= 5 * mm
        if ref_str:
            c.setFont("Helvetica", 9)
            c.setFillColor(self.C_MID)
            c.drawRightString(right_x, meta_y, f"Ref: {ref_str}")

        # Separator line
        c.setStrokeColor(self.C_LIGHT)
        c.setLineWidth(1.2)
        c.line(self.MARGIN_X, H - hy, W - self.MARGIN_X, H - hy)

    # ------------------------------------------------------------------
    def _draw_footer(self, c: canvas.Canvas, page_num: int) -> None:
        fy = self.FOOTER_H
        mx = self.MARGIN_X

        # Top rule
        c.setStrokeColor(self.C_LIGHT)
        c.setLineWidth(0.8)
        c.line(mx, fy, W - mx, fy)

        # Page number
        c.setFont("Helvetica", 8)
        c.setFillColor(self.C_MID)
        c.drawCentredString(W / 2, fy - 5 * mm, f"Page {page_num}")

        # Contact info left
        contact = _safe(self.data, "contact")
        if contact:
            c.setFont("Helvetica", 8)
            c.setFillColor(self.C_MID)
            c.drawString(mx, fy - 5 * mm, contact)

        # Company right
        company = _safe(self.data, "company")
        if company:
            c.setFont("Helvetica-Bold", 8)
            c.setFillColor(self.C_ACCENT)
            c.drawRightString(W - mx, fy - 5 * mm, company)

    # ------------------------------------------------------------------
    def _draw_body(self, c: canvas.Canvas, y: float, new_page_cb) -> float:
        mx    = self.MARGIN_X
        right = W - self.MARGIN_X
        body_w = right - mx
        min_y  = self.FOOTER_H + 8 * mm

        def check_space(needed: float) -> float:
            nonlocal y
            if y - needed < min_y:
                c.showPage()
                new_page_cb(c)
                y = H - self.HEADER_H - self.MARGIN_Y
            return y

        # ---- Sections ----
        sections = _safe(self.data, "sections", [])
        for sec in sections:
            heading = (sec.get("heading") or "").strip()
            body    = (sec.get("body")    or "").strip()

            if heading:
                y = check_space(14 * mm)
                c.setFont("Helvetica-Bold", 13)
                c.setFillColor(self.C_ACCENT)
                c.drawString(mx, y, heading)
                y -= 3 * mm
                # Thin rule under heading
                c.setStrokeColor(self.C_LIGHT)
                c.setLineWidth(0.8)
                c.line(mx, y, right, y)
                y -= 5 * mm

            if body:
                # Word-wrap body text manually
                c.setFont("Helvetica", 10)
                c.setFillColor(self.C_DARK)
                for line in self._wrap_text(body, "Helvetica", 10, body_w):
                    y = check_space(5 * mm)
                    c.drawString(mx, y, line)
                    y -= 4.5 * mm
                y -= 4 * mm

        # ---- Table ----
        table_data_raw = _safe(self.data, "table")
        if table_data_raw:
            headers = table_data_raw.get("headers", [])
            rows    = table_data_raw.get("rows", [])
            if headers and rows:
                y = check_space(20 * mm)
                y = self._draw_table(c, headers, rows, mx, y, body_w, min_y,
                                     new_page_cb)

        return y

    # ------------------------------------------------------------------
    def _draw_table(self, c, headers, rows, x, y, width, min_y, new_page_cb):
        col_n   = len(headers)
        col_w   = width / col_n
        row_h   = 7 * mm
        pad_x   = 3 * mm

        all_rows = [headers] + rows

        for i, row in enumerate(all_rows):
            if y - row_h < min_y:
                c.showPage()
                new_page_cb(c)
                y = H - self.HEADER_H - self.MARGIN_Y

            is_header = (i == 0)
            is_alt    = (not is_header) and (i % 2 == 0)

            # Row background
            if is_header:
                c.setFillColor(self.C_DARK)
            elif is_alt:
                c.setFillColor(self.C_ALT_ROW)
            else:
                c.setFillColor(self.C_WHITE)
            c.rect(x, y - row_h, width, row_h, fill=1, stroke=0)

            # Cell borders
            c.setStrokeColor(self.C_LIGHT)
            c.setLineWidth(0.5)
            c.rect(x, y - row_h, width, row_h, fill=0, stroke=1)

            # Text
            for j, cell in enumerate(row[:col_n]):
                cx = x + j * col_w + pad_x
                if is_header:
                    c.setFont("Helvetica-Bold", 9)
                    c.setFillColor(self.C_WHITE)
                else:
                    c.setFont("Helvetica", 9)
                    c.setFillColor(self.C_DARK)
                c.drawString(cx, y - row_h + 2 * mm, str(cell))

            y -= row_h

        return y - 4 * mm

    # ------------------------------------------------------------------
    @staticmethod
    def _wrap_text(text: str, font: str, size: float, max_width: float) -> list[str]:
        """Simple greedy word-wrapper using ReportLab string width."""
        from reportlab.pdfbase.pdfmetrics import stringWidth
        words  = text.split()
        lines  = []
        current = ""
        for word in words:
            test = (current + " " + word).strip()
            if stringWidth(test, font, size) <= max_width:
                current = test
            else:
                if current:
                    lines.append(current)
                current = word
        if current:
            lines.append(current)
        return lines


# ===========================================================================
# 2.  DARK NEON MINIMAL STYLE  (formerly "Cyber")
# ===========================================================================

class CyberStyle(BaseStyle):
    """
    Dark, modern, minimalistic with deliberate neon accents.
    Palette: deep charcoal background, off-white text, neon green
    primary accent, electric violet secondary, warm amber highlight.
    No grids, no glitch, no clutter — just clean geometry and light.
    """

    # --- palette ---
    C_BG       = _hex("#0D0D0D")   # near-black background
    C_SURFACE  = _hex("#161616")   # card / panel surface
    C_BORDER   = _hex("#242424")   # subtle separator
    C_TEXT     = _hex("#E8E8E8")   # primary text
    C_MUTED    = _hex("#606060")   # secondary / meta text
    C_NEON     = _hex("#AAFF4D")   # neon green — primary accent
    C_VIOLET   = _hex("#8B5CF6")   # electric violet — secondary accent
    C_AMBER    = _hex("#F59E0B")   # warm amber — highlight / warning
    C_WHITE    = colors.white

    # --- layout ---
    MARGIN_X = 20 * mm
    MARGIN_Y = 14 * mm
    HEADER_H = 32 * mm
    FOOTER_H = 13 * mm

    SANS      = "Helvetica-Bold"
    SANS_REG  = "Helvetica"
    MONO      = "Courier-Bold"
    MONO_REG  = "Courier"

    def build(self, output_path: str) -> None:
        c = canvas.Canvas(output_path, pagesize=A4)
        c.setTitle(_safe(self.data, "title", "Document"))

        page_num = [0]

        def draw_page(c: canvas.Canvas) -> None:
            page_num[0] += 1
            self._draw_background(c)
            self._draw_header(c)
            self._draw_footer(c, page_num[0])

        draw_page(c)
        self._draw_body(c, draw_page)
        c.save()

    # ------------------------------------------------------------------
    def _draw_background(self, c: canvas.Canvas) -> None:
        # Full-page dark fill
        c.setFillColor(self.C_BG)
        c.rect(0, 0, W, H, fill=1, stroke=0)

        # Very faint horizontal scan-lines (4 pt gap) — subtle texture
        c.setStrokeColor(self.C_SURFACE)
        c.setLineWidth(0.5)
        y = 0
        while y <= H:
            c.line(0, y, W, y)
            y += 4

        # Left neon accent strip — slim vertical bar
        c.setFillColor(self.C_NEON)
        c.rect(0, 0, 3, H, fill=1, stroke=0)

        # Top-right corner decoration: two concentric quarter-circle arcs
        cx_arc, cy_arc = W, H
        c.setStrokeColor(self.C_VIOLET)
        c.setLineWidth(0.6)
        c.setStrokeAlpha(0.35)
        c.arc(cx_arc - 60, cy_arc - 60, cx_arc + 60, cy_arc + 60, startAng=180, extent=90)
        c.arc(cx_arc - 90, cy_arc - 90, cx_arc + 90, cy_arc + 90, startAng=180, extent=90)
        c.setStrokeAlpha(1.0)

        # Bottom-left mirrored decoration
        c.setStrokeColor(self.C_NEON)
        c.setLineWidth(0.4)
        c.setStrokeAlpha(0.20)
        c.arc(-50, -50, 50, 50, startAng=0, extent=90)
        c.arc(-80, -80, 80, 80, startAng=0, extent=90)
        c.setStrokeAlpha(1.0)

    # ------------------------------------------------------------------
    def _draw_header(self, c: canvas.Canvas) -> None:
        mx = self.MARGIN_X
        hy = self.HEADER_H

        # Header surface panel
        c.setFillColor(self.C_SURFACE)
        c.rect(0, H - hy, W, hy, fill=1, stroke=0)

        # Left accent re-draw on top of panel (keep it visible)
        c.setFillColor(self.C_NEON)
        c.rect(0, H - hy, 3, hy, fill=1, stroke=0)

        # Neon dot marker before title
        dot_x = mx + 2
        dot_y = H - 16 * mm
        c.setFillColor(self.C_NEON)
        c.circle(dot_x, dot_y + 1.5, 2.8, fill=1, stroke=0)

        # Title — clean sans-serif, white, generous size
        title = _safe(self.data, "title", "UNTITLED")
        c.setFont(self.SANS, 20)
        c.setFillColor(self.C_TEXT)
        c.drawString(dot_x + 7, dot_y, title)

        # Subtitle — muted, smaller, below title
        subtitle = _safe(self.data, "subtitle")
        if subtitle:
            c.setFont(self.SANS_REG, 10)
            c.setFillColor(self.C_MUTED)
            c.drawString(dot_x + 7, dot_y - 6 * mm, subtitle)

        # Right-side meta block — date + reference stacked
        right_x  = W - mx
        meta_y   = H - 10 * mm
        date_str = _safe(self.data, "date", datetime.now().strftime("%Y-%m-%d"))
        ref_str  = _safe(self.data, "reference")

        c.setFont(self.MONO_REG, 8)
        c.setFillColor(self.C_NEON)
        c.drawRightString(right_x, meta_y, date_str)
        if ref_str:
            c.setFillColor(self.C_MUTED)
            c.drawRightString(right_x, meta_y - 4.5 * mm, ref_str)

        # Separator — single pixel-thin line in neon
        sep_y = H - hy + 0.5
        c.setStrokeColor(self.C_NEON)
        c.setLineWidth(0.8)
        c.line(0, sep_y, W, sep_y)

    # ------------------------------------------------------------------
    def _draw_footer(self, c: canvas.Canvas, page_num: int) -> None:
        mx = self.MARGIN_X
        fy = self.FOOTER_H

        # Footer surface
        c.setFillColor(self.C_SURFACE)
        c.rect(0, 0, W, fy, fill=1, stroke=0)

        # Left accent strip in footer
        c.setFillColor(self.C_NEON)
        c.rect(0, 0, 3, fy, fill=1, stroke=0)

        # Separator top
        c.setStrokeColor(self.C_BORDER)
        c.setLineWidth(0.6)
        c.line(mx, fy, W - mx, fy)

        # Left: generated-by label
        c.setFont(self.MONO_REG, 7)
        c.setFillColor(self.C_MUTED)
        c.drawString(mx, fy / 2 - 1.5, "PDF ENGINE  ·  DARK NEON STYLE")

        # Centre: page indicator with neon dot decoration
        centre_text = f"{page_num:02d}"
        c.setFont(self.SANS, 8)
        c.setFillColor(self.C_TEXT)
        c.drawCentredString(W / 2, fy / 2 - 1.5, centre_text)

        # Right: hash / id
        hash_id = _safe(self.data, "hash_id")
        if not hash_id:
            raw = _safe(self.data, "title", "PDF") + str(page_num)
            hash_id = hashlib.sha256(raw.encode()).hexdigest()[:12].upper()
        c.setFont(self.MONO_REG, 7)
        c.setFillColor(self.C_VIOLET)
        c.drawRightString(W - mx, fy / 2 - 1.5, hash_id)

    # ------------------------------------------------------------------
    def _draw_body(self, c: canvas.Canvas, new_page_cb) -> None:
        mx     = self.MARGIN_X
        right  = W - self.MARGIN_X
        body_w = right - mx
        y      = H - self.HEADER_H - self.MARGIN_Y
        min_y  = self.FOOTER_H + 10 * mm

        def check_space(needed: float) -> float:
            nonlocal y
            if y - needed < min_y:
                c.showPage()
                new_page_cb(c)
                y = H - self.HEADER_H - self.MARGIN_Y
            return y

        # ---- ASCII Art block ----
        ascii_art = _safe(self.data, "ascii_art")
        if ascii_art:
            lines   = ascii_art.splitlines()
            line_h  = 3.8 * mm
            pad     = 5 * mm
            panel_h = len(lines) * line_h + pad * 2
            y = check_space(panel_h + 4 * mm)

            # Panel: surface background with neon left border
            c.setFillColor(self.C_SURFACE)
            c.rect(mx, y - panel_h, body_w, panel_h, fill=1, stroke=0)
            c.setFillColor(self.C_NEON)
            c.rect(mx, y - panel_h, 2.5, panel_h, fill=1, stroke=0)

            ty = y - pad
            for line in lines:
                c.setFont(self.MONO_REG, 7.5)
                c.setFillColor(self.C_NEON)
                c.drawString(mx + 6 * mm, ty, line)
                ty -= line_h
            y -= panel_h + 6 * mm

        # ---- Sections ----
        sections = _safe(self.data, "sections", [])
        for sec_idx, sec in enumerate(sections):
            heading = (sec.get("heading") or "").strip()
            body    = (sec.get("body")    or "").strip()

            if heading:
                y = check_space(14 * mm)

                # Section index badge (01, 02 …)
                badge = f"{sec_idx + 1:02d}"
                c.setFont(self.MONO, 7)
                c.setFillColor(self.C_NEON)
                c.drawString(mx, y, badge)

                # Heading text — white, bold, slightly indented
                c.setFont(self.SANS, 12)
                c.setFillColor(self.C_TEXT)
                c.drawString(mx + 8 * mm, y, heading.upper())

                y -= 4 * mm

                # Full-width thin rule, neon left segment + muted rest
                neon_w = 12 * mm
                c.setStrokeColor(self.C_NEON)
                c.setLineWidth(1.0)
                c.line(mx, y, mx + neon_w, y)
                c.setStrokeColor(self.C_BORDER)
                c.setLineWidth(0.5)
                c.line(mx + neon_w, y, right, y)

                y -= 5 * mm

            if body:
                wrapped = self._wrap_text(body, self.SANS_REG, 9.5, body_w - 4 * mm)
                needed  = len(wrapped) * 5 * mm + 4 * mm
                y = check_space(needed)

                c.setFont(self.SANS_REG, 9.5)
                c.setFillColor(self.C_TEXT)
                for line in wrapped:
                    y = check_space(5 * mm)
                    c.drawString(mx + 2 * mm, y, line)
                    y -= 5 * mm

                y -= 4 * mm  # breathing room between sections

        # ---- Table ----
        table_raw = _safe(self.data, "table")
        if table_raw:
            headers = table_raw.get("headers", [])
            rows    = table_raw.get("rows", [])
            if headers and rows:
                y = check_space(20 * mm)
                y = self._draw_dark_table(c, headers, rows, mx, y, body_w,
                                          min_y, new_page_cb)

    # ------------------------------------------------------------------
    def _draw_dark_table(self, c, headers, rows, x, y, width, min_y, new_page_cb):
        col_n   = len(headers)
        col_w   = width / col_n
        row_h   = 7.5 * mm
        pad_x   = 3.5 * mm

        all_rows = [headers] + rows

        for i, row in enumerate(all_rows):
            if y - row_h < min_y:
                c.showPage()
                new_page_cb(c)
                y = H - self.HEADER_H - self.MARGIN_Y

            is_header = (i == 0)
            is_alt    = (not is_header) and (i % 2 == 0)

            # Row fill
            if is_header:
                c.setFillColor(self.C_SURFACE)
            elif is_alt:
                c.setFillColor(_hex("#121212"))
            else:
                c.setFillColor(self.C_BG)
            c.rect(x, y - row_h, width, row_h, fill=1, stroke=0)

            # Bottom border only — cleaner than full box
            c.setStrokeColor(self.C_BORDER)
            c.setLineWidth(0.4)
            c.line(x, y - row_h, x + width, y - row_h)

            # Header: neon accent bar on top
            if is_header:
                c.setStrokeColor(self.C_NEON)
                c.setLineWidth(1.2)
                c.line(x, y, x + width, y)

            for j, cell in enumerate(row[:col_n]):
                cx = x + j * col_w + pad_x
                ty = y - row_h + 2.5 * mm

                if is_header:
                    c.setFont(self.SANS, 7.5)
                    c.setFillColor(self.C_NEON)
                elif j == 0:
                    # First column — slightly highlighted
                    c.setFont(self.SANS_REG, 8)
                    c.setFillColor(self.C_TEXT)
                else:
                    c.setFont(self.SANS_REG, 8)
                    c.setFillColor(self.C_MUTED)

                # Amber highlight for cells containing "CRITICAL" or "PWNED"
                cell_str = str(cell)
                if not is_header and any(
                    kw in cell_str.upper()
                    for kw in ("CRITICAL", "PWNED", "EXPLOITED", "HIGH")
                ):
                    c.setFillColor(self.C_AMBER)

                c.drawString(cx, ty, cell_str)

                # Vertical column divider (very subtle)
                if j < col_n - 1:
                    c.setStrokeColor(self.C_BORDER)
                    c.setLineWidth(0.3)
                    c.line(x + (j + 1) * col_w, y - row_h, x + (j + 1) * col_w, y)

            y -= row_h

        return y - 5 * mm

    # ------------------------------------------------------------------
    @staticmethod
    def _wrap_text(text: str, font: str, size: float, max_width: float) -> list[str]:
        from reportlab.pdfbase.pdfmetrics import stringWidth
        words   = text.split()
        lines   = []
        current = ""
        for word in words:
            test = (current + " " + word).strip()
            if stringWidth(test, font, size) <= max_width:
                current = test
            else:
                if current:
                    lines.append(current)
                current = word
        if current:
            lines.append(current)
        return lines


# ===========================================================================
# Registry + public entry point
# ===========================================================================

_STYLE_REGISTRY: dict[str, type[BaseStyle]] = {
    "professional": ProfessionalStyle,
    "cyber":        CyberStyle,
}


def register_style(name: str, cls: type[BaseStyle]) -> None:
    """Register a custom style class under a given name."""
    _STYLE_REGISTRY[name] = cls


def generate_pdf(style: str, data: dict, output_path: str) -> str:
    """
    Generate a PDF document.

    Parameters
    ----------
    style       : "professional" | "cyber"  (or any registered custom style)
    data        : dict of content fields (see module docstring)
    output_path : destination file path (.pdf)

    Returns
    -------
    Absolute path of the written PDF.
    """
    style_key = style.lower().strip()
    if style_key not in _STYLE_REGISTRY:
        raise ValueError(
            f"Unknown style '{style}'. Available: {list(_STYLE_REGISTRY)}"
        )

    os.makedirs(os.path.dirname(os.path.abspath(output_path)), exist_ok=True)
    renderer = _STYLE_REGISTRY[style_key](data)
    renderer.build(output_path)
    return os.path.abspath(output_path)
