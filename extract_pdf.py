import pdfplumber

pdf_path = '附件：2026年工作日历表.pdf'

with pdfplumber.open(pdf_path) as pdf:
    for i, page in enumerate(pdf.pages):
        print(f"--- Page {i+1} ---")
        text = page.extract_text()
        if text:
            print(text)
        
        # Also try to extract tables as calendars are often tables
        tables = page.extract_tables()
        for j, table in enumerate(tables):
            print(f"--- Table {j+1} on Page {i+1} ---")
            for row in table:
                print(row)
