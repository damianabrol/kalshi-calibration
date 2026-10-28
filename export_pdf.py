"""Step 5: export the memos from Markdown to PDF with headless Chrome.

Usage:  .venv/bin/python export_pdf.py
Writes  memo_1page.pdf and memo_3page.pdf, and fails if either isn't its target length.

Markdown -> HTML (python-markdown) -> styled with CSS below -> printed to PDF by Chrome.
"""

import subprocess
import sys
import tempfile
from pathlib import Path

import markdown
from pypdf import PdfReader

CHROME = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
MEMOS = {  # file: (base font size, target page count)
    "memo_1page.md": ("9.2pt", 1),
    "memo_3page.md": ("9.6pt", 3),
}

# Colors are the same ink/hairline tokens as the charts
CSS = """
@page { size: Letter; margin: 0.5in 0.6in; }
body { font-family: "Helvetica Neue", Helvetica, Arial, sans-serif; font-size: FONT_SIZE;
       line-height: 1.36; color: #0b0b0b; background: #ffffff; }
h1 { font-size: 15pt; font-weight: 600; margin: 0 0 2pt; }
h2 { font-size: 11pt; font-weight: 600; margin: 9pt 0 3pt; break-after: avoid; }
h3 { font-size: 10pt; font-weight: 600; margin: 7pt 0 2pt; break-after: avoid; }
p { margin: 0 0 5pt; }
ul, ol { margin: 0 0 5pt; padding-left: 15pt; }
li { margin-bottom: 2.5pt; }
.byline { color: #52514e; margin-bottom: 8pt; }
.caption { color: #52514e; font-size: 0.88em; margin-top: 2pt; }
img { width: 100%; display: block; break-inside: avoid; }
table { border-collapse: collapse; width: 100%; margin: 3pt 0 7pt; font-size: 0.92em;
        font-variant-numeric: tabular-nums; break-inside: avoid; }
th { text-align: left; font-weight: 600; border-bottom: 1px solid #c3c2b7; padding: 2pt 5pt 2pt 0; }
td { border-bottom: 1px solid #e1e0d9; padding: 2pt 5pt 2pt 0; vertical-align: top; }
td:last-child { white-space: nowrap; }
.page-break { break-before: page; }
"""


def export(md_name, font_size, target_pages):
    md_path = Path(md_name).resolve()
    body = markdown.markdown(md_path.read_text(), extensions=["tables", "attr_list", "md_in_html"])
    html = (f"<!doctype html><html><head><meta charset='utf-8'>"
            f"<style>{CSS.replace('FONT_SIZE', font_size)}</style></head><body>{body}</body></html>")
    pdf_path = md_path.with_suffix(".pdf")

    # The HTML sits next to the memo so image paths like results/comparison.png resolve.
    html_path = md_path.with_suffix(".html")
    html_path.write_text(html)
    try:
        with tempfile.TemporaryDirectory() as profile:  # throwaway profile: never touches your Chrome
            subprocess.run([CHROME, "--headless=new", "--disable-gpu", f"--user-data-dir={profile}",
                            "--no-pdf-header-footer", f"--print-to-pdf={pdf_path}", html_path.as_uri()],
                           check=True, capture_output=True, timeout=120)
    finally:
        html_path.unlink()

    pages = len(PdfReader(pdf_path).pages)
    status = "OK" if pages == target_pages else f"WRONG LENGTH (target {target_pages})"
    print(f"{pdf_path.name}: {pages} page(s) {status}")
    return pages == target_pages


def main():
    results = [export(name, size, pages) for name, (size, pages) in MEMOS.items()]
    sys.exit(0 if all(results) else 1)


if __name__ == "__main__":
    main()
