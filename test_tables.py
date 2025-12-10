import pdfplumber

pdf_path = '附件：2026年工作日历表.pdf'

with pdfplumber.open(pdf_path) as pdf:
    page = pdf.pages[0]
    tables = page.find_tables()
    
    print(f"Found {len(tables)} tables")
    
    if tables:
        t1 = tables[0]
        print(f"Table 1 cells count: {len(t1.cells)}")
        print(f"Table 1 first cell: {t1.cells[0]}")
        
        # Check if we can extract text by cell
        c0 = t1.cells[0]
        # crop page to cell
        cell_crop = page.crop(c0)
        print(f"Cell 0 text: '{cell_crop.extract_text()}'")
        
        # Check for yellow intersection
        # Yellow is (1, 1, 0)
        yellow_rects = [r for r in page.rects if r['non_stroking_color'] == (1.0, 1.0, 0.0)]
        print(f"Found {len(yellow_rects)} yellow rects")
        
        def is_yellow(cell_bbox):
            cx0, ctop, cx1, cbottom = cell_bbox
            # Check intersection with any yellow rect
            # Simple intersection check
            for r in yellow_rects:
                rx0, rtop, rx1, rbottom = r['x0'], r['top'], r['x1'], r['bottom']
                
                # Check overlap
                overlap_x0 = max(cx0, rx0)
                overlap_y0 = max(ctop, rtop)
                overlap_x1 = min(cx1, rx1)
                overlap_y1 = min(cbottom, rbottom)
                
                if overlap_x1 > overlap_x0 and overlap_y1 > overlap_y0:
                    return True
            return False

        print(f"Is Cell 0 yellow? {is_yellow(c0)}")
