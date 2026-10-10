import pdfplumber
from ics import Calendar, Event
import re
import csv

def is_lunar_day(text):
    if not text: return False
    # Common lunar day patterns
    # 初一 to 初十
    if re.match(r'^初[一二三四五六七八九十]$', text): return True
    # 十一 to 十九
    if re.match(r'^十[一二三四五六七八九]$', text): return True
    # 二十
    if text == '二十': return True
    # 廿一 to 廿九
    if re.match(r'^廿[一二三四五六七八九]$', text): return True
    # 三十
    if text == '三十': return True
    # Lunar months (e.g., 正月, 二月, 腊月, 冬月)
    if re.match(r'^[正二三四五六七八九十冬腊]月$', text): return True
    return False

pdf_path = '附件：2026年工作日历表.pdf'
c = Calendar()
events_list = [] # For CSV

def add_event(year, month, day, description, is_holiday, is_weekend):
    # Logic:
    # Yellow (is_holiday=True) -> Rest Day
    # Sat/Sun (is_weekend=True) AND NOT Yellow -> Work Day
    
    event_type = None
    subject = None
    
    if is_holiday:
        event_type = "Rest"
        subject = "休息"
    elif is_weekend and not is_holiday:
        event_type = "Work"
        subject = "班"
    
    # If it's a normal weekday (Mon-Fri) and not holiday, we usually don't mark it, 
    # unless there is a specific description we want to keep?
    # The user request specifically focuses on "Yellow=Rest" and "Sat/Sun No Yellow=Work".
    # So we only generate events for these two cases.
    
    if event_type:
        # ICS Event
        e = Event()
        e.name = subject
        e.begin = f"{year}-{month:02d}-{day:02d}"
        e.make_all_day()
        c.events.add(e)
        
        # CSV Data
        events_list.append({
            'Subject': subject,
            'Start Date': f"{year}-{month:02d}-{day:02d}",
            'All Day Event': 'True',
            'Description': description or '',
            'Type': event_type
        })

def check_intersection(cell_bbox, yellow_rects):
    cx0, ctop, cx1, cbottom = cell_bbox
    # Define a small margin to avoid touching borders triggering intersection
    margin = 1
    cx0 += margin
    ctop += margin
    cx1 -= margin
    cbottom -= margin
    
    if cx0 >= cx1 or ctop >= cbottom: return False

    for r in yellow_rects:
        rx0, rtop, rx1, rbottom = r['x0'], r['top'], r['x1'], r['bottom']
        
        overlap_x0 = max(cx0, rx0)
        overlap_y0 = max(ctop, rtop)
        overlap_x1 = min(cx1, rx1)
        overlap_y1 = min(cbottom, rbottom)
        
        if overlap_x1 > overlap_x0 and overlap_y1 > overlap_y0:
            return True
    return False

try:
    with pdfplumber.open(pdf_path) as pdf:
        page = pdf.pages[0]
        
        # 1. Get Yellow Rects
        # Yellow is (1, 1, 0) in RGB. pdfplumber returns 0-1 floats.
        yellow_rects = [r for r in page.rects if r.get('non_stroking_color') == (1.0, 1.0, 0.0)]
        print(f"Found {len(yellow_rects)} yellow highlights.")

        # 2. Find Tables
        tables = page.find_tables()
        if not tables:
            print("No tables found")
            exit(1)

        # Table 1: Jan, Feb, Mar
        t1 = tables[0]
        rows = t1.rows
        
        print("Processing Jan, Feb, Mar...")
        # Skip header rows (0, 1, 2) -> Start from 3
        for row in rows[3:]:
            # Jan: Cols 0-6
            for i in range(7):
                if i < len(row.cells):
                    cell = row.cells[i]
                    if cell:
                        # Extract text from cell area
                        cell_text = page.crop(cell).extract_text()
                        if cell_text:
                            parts = cell_text.split('\n')
                            day_str = parts[0]
                            desc = parts[1] if len(parts) > 1 else None
                            
                            if day_str.isdigit():
                                day = int(day_str)
                                is_yellow = check_intersection(cell, yellow_rects)
                                # Jan 2026
                                # Check if weekend
                                # 2026-01-01 is Thursday.
                                # We can use datetime to check weekend, or just rely on column index?
                                # Column 0=Mon, 1=Tue... 5=Sat, 6=Sun
                                is_weekend = (i == 5 or i == 6)
                                add_event(2026, 1, day, desc, is_yellow, is_weekend)

            # Feb: Cols 8-14
            for i in range(8, 15):
                if i < len(row.cells):
                    cell = row.cells[i]
                    if cell:
                        cell_text = page.crop(cell).extract_text()
                        if cell_text:
                            parts = cell_text.split('\n')
                            day_str = parts[0]
                            desc = parts[1] if len(parts) > 1 else None
                            
                            if day_str.isdigit():
                                day = int(day_str)
                                is_yellow = check_intersection(cell, yellow_rects)
                                # Col 8=Mon ... 13=Sat, 14=Sun
                                col_idx = i - 8
                                is_weekend = (col_idx == 5 or col_idx == 6)
                                add_event(2026, 2, day, desc, is_yellow, is_weekend)

            # Mar: Cols 16-22
            for i in range(16, 23):
                if i < len(row.cells):
                    cell = row.cells[i]
                    if cell:
                        cell_text = page.crop(cell).extract_text()
                        if cell_text:
                            parts = cell_text.split('\n')
                            day_str = parts[0]
                            desc = parts[1] if len(parts) > 1 else None
                            
                            if day_str.isdigit():
                                day = int(day_str)
                                is_yellow = check_intersection(cell, yellow_rects)
                                # Col 16=Mon ... 21=Sat, 22=Sun
                                col_idx = i - 16
                                is_weekend = (col_idx == 5 or col_idx == 6)
                                add_event(2026, 3, day, desc, is_yellow, is_weekend)

        # Tables 2-10: Apr-Dec
        for m_idx, table in enumerate(tables[1:], start=4):
            print(f"Processing Month {m_idx}...")
            rows = table.rows
            # Skip header rows (0, 1) -> Start from 2
            for row in rows[2:]:
                for i, cell in enumerate(row.cells):
                    if cell:
                        cell_text = page.crop(cell).extract_text()
                        if cell_text:
                            parts = cell_text.split('\n')
                            day_str = parts[0]
                            desc = parts[1] if len(parts) > 1 else None
                            
                            if day_str.isdigit():
                                day = int(day_str)
                                is_yellow = check_intersection(cell, yellow_rects)
                                # Col 0=Mon ... 5=Sat, 6=Sun
                                is_weekend = (i == 5 or i == 6)
                                add_event(2026, m_idx, day, desc, is_yellow, is_weekend)

    output_file = 'calendar_2026.ics'
    with open(output_file, 'w', encoding='utf-8') as f:
        f.writelines(c.serialize_iter())

    # CSV Generation
    csv_file = 'calendar_2026.csv'
    with open(csv_file, 'w', newline='', encoding='utf-8-sig') as f:
        writer = csv.DictWriter(f, fieldnames=['Subject', 'Start Date', 'All Day Event', 'Description', 'Type'])
        writer.writeheader()
        writer.writerows(events_list)
        
    print(f"CSV generated: {csv_file}")
    print(f"Calendar generated: {output_file}")

except Exception as e:
    print(f"Error: {e}")
    import traceback
    traceback.print_exc()
