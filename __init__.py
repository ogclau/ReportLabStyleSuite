"""
PDF Generator Package

A modular PDF generation engine with Professional and Cyber visual styles.

Quick Start:
    from pdf_generator import generate_pdf

    # Generate professional PDF
    generate_pdf("professional", data, "report.pdf")

    # Generate cyber PDF
    generate_pdf("cyber", data, "audit.pdf")

Available Styles:
    - ProfessionalStyle: Clean, minimalistic business documents
    - CyberStyle: Neon, code-aesthetic security reports

Classes:
    PDFData: Structured data container
    PDFStyleStrategy: Abstract base for custom styles
    PDFGenerator: Main generation engine

Functions:
    generate_pdf(style, data, output_path): Main entry point
