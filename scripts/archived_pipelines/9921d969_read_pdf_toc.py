import fitz # PyMuPDF
import sys

pdf_path = r"E:\Google Drive\Liturgical Library\Typikon and Service Books\Typikon\Ruthenian\The Ruthenian Common Typikon.pdf"

doc = fitz.open(pdf_path)
print(f"Loaded {pdf_path}")
print(f"Metadata: {doc.metadata}")
print(f"Number of pages: {len(doc)}")

# Check Table of Contents (Outline)
toc = doc.get_toc()
print(f"Table of Contents (first 20 entries):")
for item in toc[:20]:
    print(f"  {item}")

# Let's search all pages for key terms
print("\nSearching entire PDF for key terms...")
search_terms = ["petras", "david", "case", "paradigm", "lviv", "dolnytsky"]
matches = {term: [] for term in search_terms}

for page_idx in range(len(doc)):
    text = doc[page_idx].get_text()
    for term in search_terms:
        if term in text.lower():
            matches[term].append(page_idx + 1)

for term, pages in matches.items():
    print(f"Term '{term}' found on {len(pages)} pages: {pages[:20]}...")
