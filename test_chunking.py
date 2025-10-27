"""Test script for header-based chunking functionality"""
from services.document_processor import document_processor
from pypdf import PdfWriter, PdfReader
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
import io

# Create a test PDF with headers
def create_test_pdf():
    """Create a PDF with various header styles for testing"""
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=letter)
    story = []
    styles = getSampleStyleSheet()
    
    # Add content with various header styles
    content = [
        ("EXECUTIVE SUMMARY", "Heading1"),
        ("This document contains important information about our project.", "BodyText"),
        ("", "BodyText"),
        ("1. Introduction", "Heading1"),
        ("The introduction provides an overview of the document structure.", "BodyText"),
        ("", "BodyText"),
        ("1.1 Purpose", "Heading2"),
        ("The purpose is to demonstrate the new chunking capabilities.", "BodyText"),
        ("", "BodyText"),
        ("1.2 Scope", "Heading2"),
        ("This covers all aspects of the implementation.", "BodyText"),
        ("", "BodyText"),
        ("2. Technical Details", "Heading1"),
        ("Here are the technical aspects of the solution.", "BodyText"),
        ("", "BodyText"),
        ("2.1 Architecture", "Heading2"),
        ("The system uses a modular architecture with multiple components.", "BodyText"),
        ("", "BodyText"),
        ("CONCLUSION", "Heading1"),
        ("Final thoughts and summary of the document.", "BodyText"),
    ]
    
    for text, style_name in content:
        if text:
            story.append(Paragraph(text, styles[style_name]))
        story.append(Spacer(1, 12))
    
    doc.build(story)
    return buffer.getvalue()

print("Testing header-based chunking...\n")
print("="*70)

# Create test PDF
print("Creating test PDF with headers...")
pdf_content = create_test_pdf()
print(f"Generated PDF of size: {len(pdf_content)} bytes\n")

# Process the PDF
chunks = document_processor.process_pdf(pdf_content, "test_document.pdf")

print(f"Generated {len(chunks)} chunks:\n")

for i, chunk_data in enumerate(chunks):
    print(f"\n{'='*70}")
    print(f"CHUNK {i + 1}")
    print(f"{'='*70}")
    print(f"Header: {chunk_data.get('header', 'N/A')}")
    print(f"Level: {chunk_data.get('header_level', 'N/A')}")
    print(f"Type: {chunk_data.get('chunk_type', 'N/A')}")
    print(f"Is Partial: {chunk_data.get('is_partial', False)}")
    print(f"Chunk Index: {chunk_data.get('chunk_index', 'N/A')}")
    print(f"\nContent Preview (first 150 chars):")
    text = chunk_data.get('text', '')
    print(f"{text[:150]}..." if len(text) > 150 else text)
    print(f"\nFull length: {len(text)} characters")

print(f"\n{'='*70}")
print("Test completed!")
