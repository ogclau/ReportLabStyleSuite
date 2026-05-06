<div  align="center">

[![Typing SVG](https://readme-typing-svg.demolab.com?font=Fira+Code&size=17&duration=900&pause=120&color=00FFFF&center=true&vCenter=true&width=950&lines=%5B+0.001s+%5D+init+pdf.engine...;%5B+0.032s+%5D+loading+styles...;%5B+0.087s+%5D+professional.theme+ready;%5B+0.142s+%5D+cyber.theme+ready;%5B+0.201s+%5D+layout.system+initialized;%5B+0.248s+%5D+font.registry+loaded;%5B+0.301s+%5D+render.pipeline+online;%5B+0.355s+%5D+table.module+active;%5B+0.402s+%5D+grid.background+enabled;%5B+0.447s+%5D+ascii.renderer+ready;%5B+0.501s+%5D+integrity+check+%5BOK%5D;%5B+0.533s+%5D+style.system+%5BENABLED%5D;%5B+0.600s+%5D+pdf.generator+%3A+READY;%3E+SYSTEM+READY+%C2%B7+RENDER+ENGINE+ONLINE_)](https://git.io/typing-svg)

#  PDF STYLE ENGINE · v1.0

![Status](https://img.shields.io/badge/STATUS-ACTIVO-00ffff?style=for-the-badge&labelColor=0d1117)
![Python](https://img.shields.io/badge/Python-3.10+-ffd700?style=for-the-badge&labelColor=0d1117)
![PDF](https://img.shields.io/badge/PDF-ReportLab-ff6b6b?style=for-the-badge&labelColor=0d1117)
![Styles](https://img.shields.io/badge/Styles-2%20Themes-ff00ff?style=for-the-badge&labelColor=0d1117)

**Generador de PDFs modular — Estilo Profesional · Estilo Cyber · Layout dinámico · CLI · ReportLab**

</div>

---

# PDF Document Generator
```python
A Python module for generating visually distinct PDF documents using ReportLab with two fully independent visual styles.
```

## 📚 INDEX

- [⚡ Tech Stack](#-tech-stack)
- [🎨 Style System](#-style-system)
- [🎯 Features](#-features)
- [📦 Installation](#-installation)
- [💻 Usage](#-usage)
- [⌨ CLI](#-cli)
- [🧱 Data Structure](#-data-structure)
- [🖌 Extending with Custom Styles](#-extending-with-custom-styles)
- [📑 Requirements](#requirements)


---

## ⚡ Tech Stack

| Layer     | Tech             | Role                      |
|-----------|------------------|---------------------------|
| Core      | Python 3.10+     | Main engine               |
| PDF       | ReportLab        | Document rendering        |
| CLI       | argparse         | Terminal-based generation |
| Layout    | Custom           | Modular style system      |
| Fonts     | Helvetica / Mono | Adaptable typography      |

---

## 🎨 Style System

✔️ Decoupled architecture
✔️ Strategy pattern (each style is independent)
✔️ Extensible (easy to add new styles)

| Professional Style | Dark / Neon / Modern Style |
|:---:|:---:|
| ![Professional Preview](sample_professional_preview.png) | ![Cyber Preview](sample_cyber_preview.png) |
| Clean, minimalistic business documents | Dark-mode aesthetic with refined neon accents |

## 🎯 Features

- **Professional Style**: Clean, minimalistic layout with Helvetica typography, neutral colors, and structured sections
- **Cyber Style**: Neon-inspired aesthetic with monospaced fonts, grid backgrounds, and code-block elements
- **Modular Architecture**: Strategy pattern for easy extension with new styles
- **Dynamic Field Handling**: Only renders fields that exist in the data
- **CLI Tool**: Command-line interface for quick PDF generation

## 📦 Installation

```bash
pip install reportlab
```

## 💻 Usage

### Python API

```python
from pdf_generator import generate_pdf

data = {
    "title": "My Document",
    "subtitle": "A Subtitle",
    "sections": [
        {"title": "Section 1", "content": "Some content here"}
    ]
}

# Professional style
generate_pdf("professional", data, "output.pdf")

# Cyber style
generate_pdf("cyber", data, "output.pdf")
```

### ⌨ CLI

```bash
# Generate professional sample
python pdf_generator.py professional -o report.pdf

# Generate cyber sample
python pdf_generator.py cyber -o audit.pdf

# Generate both styles
python pdf_generator.py both -o samples.pdf

# Use custom data
python pdf_generator.py professional --data mydata.json -o report.pdf
```

## 🧱 Data Structure

```python
{
    "title": str,              # Document title
    "subtitle": str,           # Subtitle text
    "metadata": dict,          # Key-value pairs for header metadata
    "sections": [              # List of sections
        {
            "title": str,      # Section heading
            "content": str/list # Text or bullet points
        }
    ],
    "table": {                 # Optional data table
        "headers": list,
        "data": list of lists
    },
    "logo_path": str,          # Path to logo image (PNG/SVG)
    "logo_alignment": str,     # "left", "center", or "right"
    "footer_text": str,        # Custom footer text
    "ascii_art": str,          # ASCII art block (cyber style)
    "code_blocks": [           # Code blocks (cyber style)
        {"language": str, "code": str}
    ]
}
```

## 🖌 Extending with Custom Styles

Create a new style by subclassing `PDFStyleStrategy`:

```python
from pdf_generator import PDFStyleStrategy

class CustomStyle(PDFStyleStrategy):
    def _setup_styles(self):
        # Define your styles
        pass

    def build_header(self, data):
        # Build header elements
        pass

    # ... implement other abstract methods
```

## 📑 Requirements

- Python 3.10+
- ReportLab 4.0+

<div align="center">

Python · ReportLab · Modular Architecture

</div> 
