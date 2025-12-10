import pdfplumber

pdf_path = '附件：2026年工作日历表.pdf'

with pdfplumber.open(pdf_path) as pdf:
    page = pdf.pages[0]
    
    print(f"Page size: {page.width}x{page.height}")
    
    print("\n--- Rects (first 20) ---")
    # Rects often represent background colors
    for i, rect in enumerate(page.rects[:20]):
        print(f"Rect {i}: {rect}")
        
    print("\n--- Text with layout ---")
    # Extract words to see positions
    words = page.extract_words()
    for i, word in enumerate(words[:10]):
        print(f"Word {i}: {word}")
