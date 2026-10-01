import os
import sys

pdf_path = r"E:\Google Drive\Liturgical Library\Typikon and Service Books\Typikon\Ruthenian\The Ruthenian Common Typikon.pdf"

# Check if file exists
if not os.path.exists(pdf_path):
    print(f"File not found: {pdf_path}")
    sys.exit(1)

print(f"File found: {pdf_path}, size: {os.path.getsize(pdf_path)} bytes")

# Let's try importing different PDF libraries to see what's available
try:
    import pypdf
    print("pypdf is available")
except ImportError:
    pypdf = None

try:
    import fitz # PyMuPDF
    print("pymupdf is available")
except ImportError:
    fitz = None

try:
    import pdfplumber
    print("pdfplumber is available")
except ImportError:
    pdfplumber = None

# Let's write a search function using whatever is available
if pypdf:
    reader = pypdf.PdfReader(pdf_path)
    print(f"Number of pages (pypdf): {len(reader.pages)}")
    
    # Search first 20 pages for "Petras" or case/paradigm mentions
    for idx in range(min(50, len(reader.pages))):
        text = reader.pages[idx].extract_text()
        if "petras" in text.lower() or "case" in text.lower() or "paradigm" in text.lower():
            print(f"Page {idx+1} matches:")
            for line in text.splitlines():
                if any(w in line.lower() for w in ["petras", "case", "paradigm"]):
                    print(f"  {line}")
elif fitz:
    doc = fitz.open(pdf_path)
    print(f"Number of pages (pymupdf): {len(doc)}")
    for idx in range(min(50, len(doc))):
        text = doc[idx].get_text()
        if "petras" in text.lower() or "case" in text.lower() or "paradigm" in text.lower():
            print(f"Page {idx+1} matches:")
            for line in text.splitlines():
                if any(w in line.lower() for w in ["petras", "case", "paradigm"]):
                    print(f"  {line}")
else:
    print("No pdf parsing library available in .venv. Let's install pypdf.")
