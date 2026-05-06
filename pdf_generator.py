"""
PDF Document Generator with Dual Visual Styles
===============================================
A modular PDF generation engine supporting Professional and Cyber/Neon styles.
Compatible with Python 3.10+

Usage:
    from pdf_generator import generate_pdf, ProfessionalStyle, CyberStyle

    # Professional style
    generate_pdf("professional", data, "output.pdf")

    # Cyber style  
    generate_pdf("cyber", data, "output.pdf")
"""

import os
import sys
import json
import hashlib
import datetime
from abc import ABC, abstractmethod
from typing import Dict, List, Optional, Any, Tuple
from dataclasses import dataclass, field

from reportlab.lib import colors
from reportlab.lib.pagesizes import letter, A4
from reportlab.lib.units import inch, mm
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_RIGHT
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle,
    PageBreak, Image, HRFlowable, KeepTogether
)
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.graphics.shapes import Drawing, Rect, Line, String
from reportlab.graphics import renderPDF


# =============================================================================
# DATA MODELS
# =============================================================================

@dataclass
class PDFData:
    """Structured data container for PDF generation."""
    title: Optional[str] = None
    subtitle: Optional[str] = None
    metadata: Dict[str, str] = field(default_factory=dict)
    sections: List[Dict[str, Any]] = field(default_factory=list)
    table: Optional[Dict[str, Any]] = None
    logo_path: Optional[str] = None
    logo_alignment: str = "left"  # "left", "center", "right"
    footer_text: Optional[str] = None
    ascii_art: Optional[str] = None
    code_blocks: List[Dict[str, str]] = field(default_factory=list)

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'PDFData':
        """Create PDFData from dictionary, filtering None values."""
        valid_fields = {k: v for k, v in data.items() if k in cls.__dataclass_fields__}
        return cls(**valid_fields)


# =============================================================================
# STYLE STRATEGY INTERFACE
# =============================================================================

class PDFStyleStrategy(ABC):
    """Abstract base class for PDF styling strategies."""

    def __init__(self, pagesize=A4):
        self.pagesize = pagesize
        self.width, self.height = pagesize
        self.styles = getSampleStyleSheet()
        self._setup_styles()

    @abstractmethod
    def _setup_styles(self):
        """Initialize custom paragraph styles."""
        pass

    @abstractmethod
    def build_header(self, data: PDFData) -> List:
        """Build header elements."""
        pass

    @abstractmethod
    def build_sections(self, data: PDFData) -> List:
        """Build section content elements."""
        pass

    @abstractmethod
    def build_table(self, data: PDFData) -> List:
        """Build table elements if data exists."""
        pass

    @abstractmethod
    def build_footer_canvas(self, canvas_obj, doc, data: PDFData):
        """Draw footer on canvas."""
        pass

    @abstractmethod
    def build_background(self, canvas_obj, doc):
        """Draw page background elements."""
        pass

    def filter_empty(self, items: List) -> List:
        """Remove None/empty items from list."""
        return [item for item in items if item is not None]

    def safe_paragraph(self, text: Optional[str], style_name: str, 
                       default: str = "") -> Optional[Paragraph]:
        """Create paragraph only if text exists."""
        if not text:
            return None
        return Paragraph(text, self.styles[style_name])


# =============================================================================
# PROFESSIONAL / MINIMALISTIC STYLE
# =============================================================================

class ProfessionalStyle(PDFStyleStrategy):
    """
    Clean, modern layout with wide spacing and strong visual hierarchy.
    Neutral color palette with optional company branding.
    """

    # Color Palette
    COLORS = {
        'primary': colors.HexColor('#1A1A1A'),
        'secondary': colors.HexColor('#4A4A4A'),
        'accent': colors.HexColor('#007ACC'),
        'light': colors.HexColor('#EAEAEA'),
        'white': colors.white,
        'border': colors.HexColor('#CCCCCC')
    }

    def _setup_styles(self):
        """Configure typography and spacing."""
        self.styles.add(ParagraphStyle(
            name='ProfTitle',
            fontName='Helvetica-Bold',
            fontSize=20,
            leading=26,
            textColor=self.COLORS['primary'],
            spaceAfter=6,
            alignment=TA_LEFT
        ))

        self.styles.add(ParagraphStyle(
            name='ProfSubtitle',
            fontName='Helvetica',
            fontSize=13,
            leading=18,
            textColor=self.COLORS['secondary'],
            spaceAfter=20,
            alignment=TA_LEFT
        ))

        self.styles.add(ParagraphStyle(
            name='ProfBody',
            fontName='Helvetica',
            fontSize=10.5,
            leading=15,
            textColor=self.COLORS['primary'],
            spaceAfter=12,
            alignment=TA_LEFT
        ))

        self.styles.add(ParagraphStyle(
            name='ProfSectionTitle',
            fontName='Helvetica-Bold',
            fontSize=12,
            leading=16,
            textColor=self.COLORS['accent'],
            spaceAfter=8,
            spaceBefore=16,
            alignment=TA_LEFT
        ))

        self.styles.add(ParagraphStyle(
            name='ProfMeta',
            fontName='Helvetica',
            fontSize=9,
            leading=12,
            textColor=self.COLORS['secondary'],
            alignment=TA_RIGHT
        ))

        self.styles.add(ParagraphStyle(
            name='ProfFooter',
            fontName='Helvetica',
            fontSize=8,
            leading=10,
            textColor=self.COLORS['secondary'],
            alignment=TA_CENTER
        ))

    def build_header(self, data: PDFData) -> List:
        """Build professional header with logo, title, and metadata."""
        elements = []

        # Logo handling
        if data.logo_path and os.path.exists(data.logo_path):
            img = Image(data.logo_path, width=1.2*inch, height=0.6*inch)
            if data.logo_alignment == "center":
                img.hAlign = 'CENTER'
            elif data.logo_alignment == "right":
                img.hAlign = 'RIGHT'
            elements.append(img)
            elements.append(Spacer(1, 12))

        # Title and subtitle
        title = self.safe_paragraph(data.title, 'ProfTitle')
        if title:
            elements.append(title)

        subtitle = self.safe_paragraph(data.subtitle, 'ProfSubtitle')
        if subtitle:
            elements.append(subtitle)

        # Metadata line
        if data.metadata:
            meta_items = []
            for key, value in data.metadata.items():
                if value:
                    meta_items.append(f"<b>{key}:</b> {value}")
            if meta_items:
                meta_text = " | ".join(meta_items)
                meta = Paragraph(meta_text, self.styles['ProfMeta'])
                elements.append(meta)

        # Separator
        elements.append(Spacer(1, 8))
        elements.append(HRFlowable(
            width="100%", 
            thickness=1, 
            color=self.COLORS['light'],
            spaceBefore=6, 
            spaceAfter=6
        ))

        return self.filter_empty(elements)

    def build_sections(self, data: PDFData) -> List:
        """Build section blocks with subtle separators."""
        elements = []

        for section in data.sections:
            if not section:
                continue

            section_elements = []

            # Section title
            title_text = section.get('title')
            if title_text:
                section_elements.append(
                    Paragraph(title_text, self.styles['ProfSectionTitle'])
                )

            # Section content
            content = section.get('content')
            if content:
                if isinstance(content, list):
                    for item in content:
                        if item:
                            section_elements.append(
                                Paragraph(f"• {item}", self.styles['ProfBody'])
                            )
                else:
                    section_elements.append(
                        Paragraph(str(content), self.styles['ProfBody'])
                    )

            # Subtle separator between sections
            if section_elements:
                section_elements.append(Spacer(1, 4))
                section_elements.append(HRFlowable(
                    width="100%",
                    thickness=0.5,
                    color=self.COLORS['light'],
                    spaceBefore=4,
                    spaceAfter=4
                ))
                elements.append(KeepTogether(section_elements))

        return elements

    def build_table(self, data: PDFData) -> List:
        """Build clean table with alternating row backgrounds."""
        if not data.table:
            return []

        table_data = data.table.get('data', [])
        headers = data.table.get('headers', [])

        if not table_data and not headers:
            return []

        # Prepare table data
        if headers:
            display_data = [headers] + table_data
        else:
            display_data = table_data

        if not display_data:
            return []

        # Calculate column widths
        num_cols = len(display_data[0]) if display_data else 1
        col_width = (self.width - 2*inch) / num_cols

        table = Table(display_data, colWidths=[col_width]*num_cols)

        # Table styling
        style_commands = [
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, -1), 9),
            ('TEXTCOLOR', (0, 0), (-1, 0), self.COLORS['white']),
            ('BACKGROUND', (0, 0), (-1, 0), self.COLORS['accent']),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('GRID', (0, 0), (-1, -1), 0.5, self.COLORS['border']),
            ('ROWBACKGROUNDS', (0, 1), (-1, -1), 
             [self.COLORS['white'], self.COLORS['light']]),
            ('TOPPADDING', (0, 0), (-1, -1), 8),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
            ('LEFTPADDING', (0, 0), (-1, -1), 10),
            ('RIGHTPADDING', (0, 0), (-1, -1), 10),
        ]

        table.setStyle(TableStyle(style_commands))

        return [Spacer(1, 20), table, Spacer(1, 20)]

    def build_background(self, canvas_obj, doc):
        """Clean white background - no decoration for professional style."""
        canvas_obj.setFillColor(self.COLORS['white'])
        canvas_obj.rect(0, 0, self.width, self.height, fill=1, stroke=0)

    def build_footer_canvas(self, canvas_obj, doc, data: PDFData):
        """Draw professional footer with page number."""
        canvas_obj.saveState()
        canvas_obj.setFont('Helvetica', 8)
        canvas_obj.setFillColor(self.COLORS['secondary'])

        # Page number
        page_text = f"Page {doc.page}"
        canvas_obj.drawRightString(self.width - 0.75*inch, 0.5*inch, page_text)

        # Footer text
        if data.footer_text:
            canvas_obj.drawString(0.75*inch, 0.5*inch, data.footer_text)
        else:
            # Default contact info placeholder
            canvas_obj.drawString(0.75*inch, 0.5*inch, 
                                "Confidential Document")

        # Bottom line
        canvas_obj.setStrokeColor(self.COLORS['light'])
        canvas_obj.setLineWidth(0.5)
        canvas_obj.line(0.75*inch, 0.65*inch, 
                       self.width - 0.75*inch, 0.65*inch)

        canvas_obj.restoreState()


# =============================================================================
# CYBER / NEON / CODE STYLE
# =============================================================================

class CyberStyle(PDFStyleStrategy):
    """
    Cyberpunk-inspired visual theme with neon colors, grid backgrounds,
    and monospaced typography.
    """

    # Color Palette
    COLORS = {
        'bg': colors.HexColor('#000000'),
        'bg_alt': colors.HexColor('#111111'),
        'cyan': colors.HexColor('#00FFFF'),
        'magenta': colors.HexColor('#FF00FF'),
        'green': colors.HexColor('#00FF00'),
        'white': colors.HexColor('#FFFFFF'),
        'gray': colors.HexColor('#333333'),
        'dark_gray': colors.HexColor('#1A1A1A')
    }

    def _setup_styles(self):
        """Configure monospaced typography."""
        # Try to use monospaced fonts, fallback to Courier
        self.mono_font = 'Courier'
        self.mono_bold = 'Courier-Bold'

        self.styles.add(ParagraphStyle(
            name='CyberTitle',
            fontName=self.mono_bold,
            fontSize=22,
            leading=28,
            textColor=self.COLORS['cyan'],
            spaceAfter=8,
            alignment=TA_LEFT,
            fontEncoding='utf-8'
        ))

        self.styles.add(ParagraphStyle(
            name='CyberSubtitle',
            fontName=self.mono_font,
            fontSize=12,
            leading=16,
            textColor=self.COLORS['magenta'],
            spaceAfter=20,
            alignment=TA_LEFT
        ))

        self.styles.add(ParagraphStyle(
            name='CyberBody',
            fontName=self.mono_font,
            fontSize=9,
            leading=14,
            textColor=self.COLORS['white'],
            spaceAfter=10,
            alignment=TA_LEFT
        ))

        self.styles.add(ParagraphStyle(
            name='CyberSectionTitle',
            fontName=self.mono_bold,
            fontSize=11,
            leading=15,
            textColor=self.COLORS['green'],
            spaceAfter=6,
            spaceBefore=14,
            alignment=TA_LEFT
        ))

        self.styles.add(ParagraphStyle(
            name='CyberCode',
            fontName=self.mono_font,
            fontSize=8,
            leading=12,
            textColor=self.COLORS['cyan'],
            leftIndent=20,
            spaceAfter=8,
            alignment=TA_LEFT
        ))

        self.styles.add(ParagraphStyle(
            name='CyberMeta',
            fontName=self.mono_font,
            fontSize=8,
            leading=11,
            textColor=self.COLORS['gray'],
            alignment=TA_RIGHT
        ))

        self.styles.add(ParagraphStyle(
            name='CyberFooter',
            fontName=self.mono_font,
            fontSize=7,
            leading=10,
            textColor=self.COLORS['gray'],
            alignment=TA_CENTER
        ))

    def _generate_hash_id(self) -> str:
        """Generate a hash-like ID for cyber aesthetic."""
        timestamp = datetime.datetime.now().isoformat()
        return hashlib.md5(timestamp.encode()).hexdigest()[:16].upper()

    def build_header(self, data: PDFData) -> List:
        """Build cyber header with glitch-style title."""
        elements = []

        # Neon frame top
        elements.append(Spacer(1, 4))

        # Title with cyber prefix
        if data.title:
            cyber_title = f">>> {data.title}"
            elements.append(Paragraph(cyber_title, self.styles['CyberTitle']))

        # Subtitle
        subtitle = self.safe_paragraph(data.subtitle, 'CyberSubtitle')
        if subtitle:
            elements.append(subtitle)

        # Metadata in code style
        if data.metadata:
            meta_lines = []
            for key, value in data.metadata.items():
                if value:
                    meta_lines.append(f"[{key.upper()}] => {value}")
            if meta_lines:
                meta_text = "<br/>".join(meta_lines)
                elements.append(Paragraph(meta_text, self.styles['CyberMeta']))

        # Separator line
        elements.append(Spacer(1, 8))
        elements.append(HRFlowable(
            width="100%",
            thickness=1,
            color=self.COLORS['cyan'],
            spaceBefore=6,
            spaceAfter=6
        ))

        return self.filter_empty(elements)

    def build_sections(self, data: PDFData) -> List:
        """Build code-styled section blocks."""
        elements = []

        for i, section in enumerate(data.sections):
            if not section:
                continue

            section_elements = []

            # Section title with code prefix
            title_text = section.get('title')
            if title_text:
                prefixed_title = f"[SEC_{i:02d}] {title_text}"
                section_elements.append(
                    Paragraph(prefixed_title, self.styles['CyberSectionTitle'])
                )

            # Content
            content = section.get('content')
            if content:
                if isinstance(content, list):
                    for item in content:
                        if item:
                            section_elements.append(
                                Paragraph(f"> {item}", self.styles['CyberBody'])
                            )
                else:
                    section_elements.append(
                        Paragraph(str(content), self.styles['CyberBody'])
                    )

            # Neon separator
            if section_elements:
                section_elements.append(Spacer(1, 4))
                section_elements.append(HRFlowable(
                    width="100%",
                    thickness=0.5,
                    color=self.COLORS['dark_gray'],
                    spaceBefore=4,
                    spaceAfter=4
                ))
                elements.append(KeepTogether(section_elements))

        # ASCII Art block
        if data.ascii_art:
            elements.append(Spacer(1, 10))
            elements.append(Paragraph(
                data.ascii_art.replace(chr(10), '<br/>'),
                self.styles['CyberCode']
            ))
            elements.append(Spacer(1, 10))

        # Code blocks
        for code_block in data.code_blocks:
            if code_block.get('code'):
                elements.append(Spacer(1, 8))
                # Code block header
                lang = code_block.get('language', 'RAW')
                elements.append(Paragraph(
                    f"// {lang} //",
                    self.styles['CyberSectionTitle']
                ))
                # Code content
                code_text = code_block['code'].replace(chr(10), '<br/>')
                elements.append(Paragraph(
                    code_text,
                    self.styles['CyberCode']
                ))
                elements.append(Spacer(1, 8))

        return elements

    def build_table(self, data: PDFData) -> List:
        """Build neon-styled data table."""
        if not data.table:
            return []

        table_data = data.table.get('data', [])
        headers = data.table.get('headers', [])

        if not table_data and not headers:
            return []

        if headers:
            display_data = [headers] + table_data
        else:
            display_data = table_data

        if not display_data:
            return []

        num_cols = len(display_data[0]) if display_data else 1
        col_width = (self.width - 2*inch) / num_cols

        table = Table(display_data, colWidths=[col_width]*num_cols)

        style_commands = [
            ('FONTNAME', (0, 0), (-1, -1), 'Courier'),
            ('FONTSIZE', (0, 0), (-1, -1), 8),
            ('TEXTCOLOR', (0, 0), (-1, 0), self.COLORS['bg']),
            ('BACKGROUND', (0, 0), (-1, 0), self.COLORS['cyan']),
            ('TEXTCOLOR', (0, 1), (-1, -1), self.COLORS['cyan']),
            ('BACKGROUND', (0, 1), (-1, -1), self.COLORS['bg_alt']),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('GRID', (0, 0), (-1, -1), 0.5, self.COLORS['cyan']),
            ('TOPPADDING', (0, 0), (-1, -1), 6),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
            ('LEFTPADDING', (0, 0), (-1, -1), 8),
            ('RIGHTPADDING', (0, 0), (-1, -1), 8),
        ]

        table.setStyle(TableStyle(style_commands))

        return [Spacer(1, 16), table, Spacer(1, 16)]

    def build_background(self, canvas_obj, doc):
        """Draw cyber grid background."""
        canvas_obj.saveState()

        # Black background
        canvas_obj.setFillColor(self.COLORS['bg'])
        canvas_obj.rect(0, 0, self.width, self.height, fill=1, stroke=0)

        # Subtle grid pattern
        canvas_obj.setStrokeColor(self.COLORS['dark_gray'])
        canvas_obj.setLineWidth(0.2)

        grid_spacing = 20
        # Vertical lines
        for x in range(0, int(self.width), grid_spacing):
            canvas_obj.line(x, 0, x, self.height)

        # Horizontal lines
        for y in range(0, int(self.height), grid_spacing):
            canvas_obj.line(0, y, self.width, y)

        # Neon frame
        canvas_obj.setStrokeColor(self.COLORS['cyan'])
        canvas_obj.setLineWidth(1)
        margin = 0.4*inch
        canvas_obj.rect(margin, margin, 
                       self.width - 2*margin, 
                       self.height - 2*margin,
                       fill=0, stroke=1)

        # Corner accents
        accent_len = 15
        canvas_obj.setStrokeColor(self.COLORS['magenta'])
        canvas_obj.setLineWidth(2)

        # Top-left corner
        canvas_obj.line(margin, self.height - margin, 
                       margin + accent_len, self.height - margin)
        canvas_obj.line(margin, self.height - margin, 
                       margin, self.height - margin - accent_len)

        # Top-right corner
        canvas_obj.line(self.width - margin, self.height - margin,
                       self.width - margin - accent_len, self.height - margin)
        canvas_obj.line(self.width - margin, self.height - margin,
                       self.width - margin, self.height - margin - accent_len)

        # Bottom-left corner
        canvas_obj.line(margin, margin, margin + accent_len, margin)
        canvas_obj.line(margin, margin, margin, margin + accent_len)

        # Bottom-right corner
        canvas_obj.line(self.width - margin, margin,
                       self.width - margin - accent_len, margin)
        canvas_obj.line(self.width - margin, margin,
                       self.width - margin, margin + accent_len)

        canvas_obj.restoreState()

    def build_footer_canvas(self, canvas_obj, doc, data: PDFData):
        """Draw cyber footer with timestamp and hash ID."""
        canvas_obj.saveState()
        canvas_obj.setFont('Courier', 7)
        canvas_obj.setFillColor(self.COLORS['gray'])

        # Timestamp
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S UTC")
        canvas_obj.drawString(0.75*inch, 0.4*inch, f"[TS] {timestamp}")

        # Hash ID
        hash_id = self._generate_hash_id()
        canvas_obj.drawString(0.75*inch, 0.25*inch, f"[ID] {hash_id}")

        # Page number
        page_text = f"PAGE_{doc.page:03d}"
        canvas_obj.drawRightString(self.width - 0.75*inch, 0.4*inch, page_text)

        # Footer text or default
        footer = data.footer_text or "Generated by PDF Engine v2.0"
        canvas_obj.drawRightString(self.width - 0.75*inch, 0.25*inch, footer)

        # Neon bottom line
        canvas_obj.setStrokeColor(self.COLORS['magenta'])
        canvas_obj.setLineWidth(0.5)
        canvas_obj.line(0.75*inch, 0.55*inch,
                       self.width - 0.75*inch, 0.55*inch)

        canvas_obj.restoreState()


# =============================================================================
# PDF GENERATOR ENGINE
# =============================================================================

class PDFGenerator:
    """Main PDF generation engine using strategy pattern."""

    def __init__(self, style_strategy: PDFStyleStrategy):
        self.strategy = style_strategy

    def generate(self, data: PDFData, output_path: str) -> str:
        """Generate PDF document."""
        doc = SimpleDocTemplate(
            output_path,
            pagesize=self.strategy.pagesize,
            rightMargin=0.75*inch,
            leftMargin=0.75*inch,
            topMargin=0.75*inch,
            bottomMargin=0.75*inch
        )

        # Build content
        story = []
        story.extend(self.strategy.build_header(data))
        story.extend(self.strategy.build_sections(data))
        story.extend(self.strategy.build_table(data))

        # Build function for page templates
        def draw_background(canvas_obj, doc):
            self.strategy.build_background(canvas_obj, doc)
            self.strategy.build_footer_canvas(canvas_obj, doc, data)

        # Build PDF
        doc.build(story, onFirstPage=draw_background, onLaterPages=draw_background)

        return output_path


# =============================================================================
# PUBLIC API
# =============================================================================

def generate_pdf(style: str, data: Dict[str, Any], output_path: str, 
                 pagesize=A4) -> str:
    """
    Generate a PDF document with the specified style.

    Args:
        style: "professional" or "cyber"
        data: Dictionary containing document data
        output_path: Path for the output PDF file
        pagesize: Page size (default A4)

    Returns:
        Path to the generated PDF file
    """
    pdf_data = PDFData.from_dict(data)

    if style.lower() == "professional":
        strategy = ProfessionalStyle(pagesize)
    elif style.lower() == "cyber":
        strategy = CyberStyle(pagesize)
    else:
        raise ValueError(f"Unknown style: {style}. Use 'professional' or 'cyber'.")

    generator = PDFGenerator(strategy)
    return generator.generate(pdf_data, output_path)


# =============================================================================
# EXAMPLE DATA
# =============================================================================

def get_professional_example_data() -> Dict[str, Any]:
    """Return example data for professional style."""
    return {
        "title": "Quarterly Business Report",
        "subtitle": "Q3 2026 Financial and Operational Summary",
        "metadata": {
            "Date": "October 15, 2026",
            "Reference": "RPT-2026-Q3-001",
            "Department": "Finance",
            "Confidentiality": "Internal Use Only"
        },
        "sections": [
            {
                "title": "Executive Summary",
                "content": [
                    "Revenue increased by 24% compared to Q2 2026",
                    "Operating costs reduced by 8% through automation initiatives",
                    "Customer satisfaction score reached 94.2%",
                    "Three new enterprise contracts signed worth $2.4M"
                ]
            },
            {
                "title": "Key Performance Indicators",
                "content": [
                    "Monthly Recurring Revenue (MRR): $485K (+18% YoY)",
                    "Customer Acquisition Cost (CAC): $1,240 (-12% QoQ)",
                    "Lifetime Value (LTV): $24,500 (+9% YoY)",
                    "Net Promoter Score (NPS): 72 (+5 points)"
                ]
            },
            {
                "title": "Risk Assessment",
                "content": "Current market volatility presents moderate risk to Q4 projections. "
                          "Mitigation strategies include diversification of revenue streams and "
                          "cost optimization programs."
            }
        ],
        "table": {
            "headers": ["Department", "Budget", "Actual", "Variance"],
            "data": [
                ["Engineering", "$1,200,000", "$1,150,000", "+4.2%"],
                ["Marketing", "$800,000", "$820,000", "-2.5%"],
                ["Sales", "$600,000", "$580,000", "+3.3%"],
                ["Operations", "$400,000", "$390,000", "+2.5%"]
            ]
        },
        "footer_text": "Acme Corporation | 123 Business Ave | contact@acme.com"
    }


def get_cyber_example_data() -> Dict[str, Any]:
    """Return example data for cyber style."""
    return {
        "title": "SECURITY AUDIT REPORT",
        "subtitle": "/// SYSTEM INTEGRITY ANALYSIS ///",
        "metadata": {
            "Target": "192.168.1.0/24",
            "Scanner": "NEXUS-v9.2",
            "Duration": "4h 23m 15s",
            "Threat Level": "MEDIUM"
        },
        "sections": [
            {
                "title": "Network Topology",
                "content": [
                    "48 active hosts detected on subnet",
                    "3 unauthorized devices flagged",
                    "Firewall rules: 124/128 active",
                    "VPN tunnel status: ENCRYPTED"
                ]
            },
            {
                "title": "Vulnerability Scan",
                "content": [
                    "CRITICAL: 0",
                    "HIGH: 3 (CVE-2026-8841, CVE-2026-9902, CVE-2026-1123)",
                    "MEDIUM: 12",
                    "LOW: 28"
                ]
            },
            {
                "title": "Intrusion Detection",
                "content": "Anomaly detected in packet flow at 03:42:15 UTC. "
                          "Signature match: APT29 variant. Recommended action: "
                          "Isolate segment 192.168.1.64/26 and initiate forensic capture."
            }
        ],
        "table": {
            "headers": ["PORT", "SERVICE", "VERSION", "STATUS"],
            "data": [
                ["22", "SSH", "OpenSSH 9.4", "FILTERED"],
                ["80", "HTTP", "nginx 1.24", "OPEN"],
                ["443", "HTTPS", "nginx 1.24", "OPEN"],
                ["3306", "MySQL", "8.0.34", "CLOSED"],
                ["8080", "Tomcat", "10.1.12", "OPEN"]
            ]
        },
        "ascii_art": """
    ███████╗███████╗ ██████╗██╗   ██╗██████╗ ██╗████████╗██╗   ██╗
    ██╔════╝██╔════╝██╔════╝██║   ██║██╔══██╗██║╚══██╔══╝╚██╗ ██╔╝
    ███████╗█████╗  ██║     ██║   ██║██████╔╝██║   ██║    ╚████╔╝ 
    ╚════██║██╔══╝  ██║     ██║   ██║██╔══██╗██║   ██║     ╚██╔╝  
    ███████║███████╗╚██████╗╚██████╔╝██║  ██║██║   ██║      ██║   
    ╚══════╝╚══════╝ ╚═════╝ ╚═════╝ ╚═╝  ╚═╝╚═╝   ╚═╝      ╚═╝   
        """,
        "code_blocks": [
            {
                "language": "PYTHON",
                "code": """def scan_target(host, ports):
    results = []
    for port in ports:
        if is_open(host, port):
            service = identify_service(port)
            results.append({
                'port': port,
                'service': service,
                'status': 'VULNERABLE'
            })
    return results"""
            },
            {
                "language": "BASH",
                "code": """$ nmap -sV -sC -O 192.168.1.0/24
Starting Nmap 7.94 ( https://nmap.org )
Nmap scan report for 192.168.1.1
Host is up (0.0003s latency).
Not shown: 995 closed ports
PORT    STATE SERVICE VERSION
22/tcp  open  ssh     OpenSSH 9.4"""
            }
        ],
        "footer_text": "/// CLASSIFIED - EYES ONLY ///"
    }


# =============================================================================
# CLI INTERFACE
# =============================================================================

def main():
    """CLI entry point for generating sample PDFs."""
    import argparse

    parser = argparse.ArgumentParser(
        description="PDF Document Generator with Professional and Cyber styles"
    )
    parser.add_argument(
        "style",
        choices=["professional", "cyber", "both"],
        help="PDF style to generate"
    )
    parser.add_argument(
        "-o", "--output",
        default="output.pdf",
        help="Output file path (default: output.pdf)"
    )
    parser.add_argument(
        "--data",
        help="Path to JSON data file (optional, uses example data if not provided)"
    )
    parser.add_argument(
        "--pagesize",
        choices=["A4", "letter"],
        default="A4",
        help="Page size (default: A4)"
    )

    args = parser.parse_args()

    pagesize = A4 if args.pagesize == "A4" else letter

    # Load data from file or use examples
    if args.data:
        with open(args.data, 'r') as f:
            data = json.load(f)
    else:
        data = None

    styles_to_generate = []
    if args.style == "both":
        styles_to_generate = ["professional", "cyber"]
    else:
        styles_to_generate = [args.style]

    for style in styles_to_generate:
        if data is None:
            if style == "professional":
                doc_data = get_professional_example_data()
            else:
                doc_data = get_cyber_example_data()
        else:
            doc_data = data

        if args.style == "both":
            output_path = args.output.replace('.pdf', f'_{style}.pdf')
        else:
            output_path = args.output

        try:
            result = generate_pdf(style, doc_data, output_path, pagesize)
            print(f"✓ Generated {style.upper()} PDF: {result}")
        except Exception as e:
            print(f"✗ Error generating {style} PDF: {e}")
            sys.exit(1)

    print("\nDone!")


if __name__ == "__main__":
    main()
