import pdfplumber

pdf_path = '附件：2026年工作日历表.pdf'

with pdfplumber.open(pdf_path) as pdf:
    page = pdf.pages[0]
    tables = page.find_tables()
    
    if tables:
        t1 = tables[0]
        print(f"Table 1 cells count: {len(t1.cells)}")
        
        # Check rows
        if hasattr(t1, 'rows'):
            print(f"Table 1 has {len(t1.rows)} rows")
            first_row = t1.rows[0]
            print(f"First row has {len(first_row.cells)} cells")
        else:
            print("Table object does not have 'rows' attribute")
