#!/usr/bin/env python3
"""
Extract and analyze content from Apple's Agentic RAG paper PDF
"""

import sys
try:
    import PyPDF2
    print("Using PyPDF2")
except ImportError:
    PyPDF2 = None

try:
    import pdfplumber
    print("Using pdfplumber")
except ImportError:
    pdfplumber = None

def extract_with_pypdf2(pdf_path):
    """Extract text using PyPDF2"""
    with open(pdf_path, 'rb') as file:
        pdf_reader = PyPDF2.PdfReader(file)
        text = []
        for page_num, page in enumerate(pdf_reader.pages):
            text.append(f"\n{'='*80}\nPage {page_num + 1}\n{'='*80}\n")
            text.append(page.extract_text())
        return '\n'.join(text)

def extract_with_pdfplumber(pdf_path):
    """Extract text using pdfplumber (usually better quality)"""
    text = []
    with pdfplumber.open(pdf_path) as pdf:
        for page_num, page in enumerate(pdf.pages):
            text.append(f"\n{'='*80}\nPage {page_num + 1}\n{'='*80}\n")
            text.append(page.extract_text())
    return '\n'.join(text)

def main():
    pdf_path = '/home/mtk02470/repos/misc/paper_research/agentic_rag_for_testing/2510.10824v1.pdf'
    
    # Try pdfplumber first (better quality), then PyPDF2
    if pdfplumber:
        print(f"Extracting text from {pdf_path} using pdfplumber...")
        text = extract_with_pdfplumber(pdf_path)
    elif PyPDF2:
        print(f"Extracting text from {pdf_path} using PyPDF2...")
        text = extract_with_pypdf2(pdf_path)
    else:
        print("Error: Neither pdfplumber nor PyPDF2 is installed.")
        print("Please install one: pip install pdfplumber  OR  pip install PyPDF2")
        sys.exit(1)
    
    # Save to output file
    output_file = '/home/mtk02470/repos/misc/paper_research/agentic_rag_for_testing/paper_text.txt'
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(text)
    
    print(f"\n✓ Text extracted successfully!")
    print(f"✓ Saved to: {output_file}")
    print(f"✓ Total characters: {len(text):,}")
    
    # Print first 2000 characters as preview
    print(f"\n{'='*80}")
    print("PREVIEW (first 2000 characters):")
    print(f"{'='*80}")
    print(text[:2000])
    print(f"\n... (see {output_file} for full content)")

if __name__ == "__main__":
    main()
