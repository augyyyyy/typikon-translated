import fitz
import sys

def extract(pdf_path, page_num, out_path):
    print(f"Extracting page {page_num} from {pdf_path} to {out_path}")
    doc = fitz.open(pdf_path)
    page = doc.load_page(page_num - 1)
    pix = page.get_pixmap(matrix=fitz.Matrix(2, 2))
    pix.save(out_path)
    print("Done.")

slavonic_pdf = r"c:\Users\augus\OneDrive\Documents\Google Antigravity\Projects\Translation\4 Liturgical Books\Church Slavoinc Sources\1761 Pochaiv Menaion\12-MINEA Pochaiv-1761 August.pdf"
greek_pdf = r"c:\Users\augus\OneDrive\Documents\Google Antigravity\Projects\Translation\4 Liturgical Books\Greek Sources\Minea\MenaiaVol6_el.pdf"

extract(slavonic_pdf, 47, r"c:\Users\augus\OneDrive\Documents\Google Antigravity\Projects\Translation\scratch\slavonic_page_47.png")
extract(slavonic_pdf, 48, r"c:\Users\augus\OneDrive\Documents\Google Antigravity\Projects\Translation\scratch\slavonic_page_48.png")
extract(slavonic_pdf, 49, r"c:\Users\augus\OneDrive\Documents\Google Antigravity\Projects\Translation\scratch\slavonic_page_49.png")
extract(greek_pdf, 334, r"c:\Users\augus\OneDrive\Documents\Google Antigravity\Projects\Translation\scratch\greek_page_334.png")
extract(greek_pdf, 335, r"c:\Users\augus\OneDrive\Documents\Google Antigravity\Projects\Translation\scratch\greek_page_335.png")
extract(greek_pdf, 336, r"c:\Users\augus\OneDrive\Documents\Google Antigravity\Projects\Translation\scratch\greek_page_336.png")
