import fitz # PyMuPDF
import sys

pdf_path = r"E:\Google Drive\Liturgical Library\Typikon and Service Books\Typikon\Ruthenian\The Ruthenian Annual Typikon 2026.pdf"

doc = fitz.open(pdf_path)
print(f"Loaded {pdf_path}")
print(f"Metadata: {doc.metadata}")
print(f"Number of pages: {len(doc)}")

# Let's search first 10 pages for key terms
print("\nSearching first 10 pages for key terms...")
search_terms = ["petras", "david", "case", "paradigm", "lviv", "dolnytsky"]
matches = {term: [] for term in search_terms}

for page_idx in range(min(10, len(doc))):
    text = doc[page_idx].get_text()
    for term in search_terms:
        if term in text.lower():
            matches[term].append(page_idx + 1)

for term, pages in matches.items():
    print(f"Term '{term}' found on {len(pages)} pages: {pages}...")
