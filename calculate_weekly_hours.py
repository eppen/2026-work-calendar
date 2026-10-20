"""基于 calendar_2026.csv 计算 2026 年每周工作小时数及周平均。"""
import csv
from collections import defaultdict
from datetime import date, timedelta

HOURS_PER_DAY = 8
YEAR = 2026
CSV_INPUT = "calendar_2026.csv"
CSV_OUTPUT = "weekly_hours_2026.csv"


def load_exception_dates(path):
    """从异常日 CSV 构建休息日与补班日集合。"""
    rest_dates = set()
    work_dates = set()
    with open(path, encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            d = date.fromisoformat(row["Start Date"])
            if row["Type"] == "Rest":
                rest_dates.add(d)
            elif row["Type"] == "Work":
                work_dates.add(d)
    return rest_dates, work_dates


def is_workday(d, rest_dates, work_dates):
    """Rest 不上班；Work 上班；其余周一至周五上班，周末不上班。"""
    if d in rest_dates:
        return False
    if d in work_dates:
        return True
    return d.weekday() < 5  # Mon=0 .. Fri=4


def main():
    rest_dates, work_dates = load_exception_dates(CSV_INPUT)

    # key: (iso_year, iso_week) -> {work_days, first, last}
    weeks = defaultdict(lambda: {"work_days": 0, "first": None, "last": None})

    start = date(YEAR, 1, 1)
    end = date(YEAR, 12, 31)
    total_work_days = 0
    d = start
    while d <= end:
        iso_year, iso_week, _ = d.isocalendar()
        bucket = weeks[(iso_year, iso_week)]
        if bucket["first"] is None or d < bucket["first"]:
            bucket["first"] = d
        if bucket["last"] is None or d > bucket["last"]:
            bucket["last"] = d
        if is_workday(d, rest_dates, work_dates):
            total_work_days += 1
            bucket["work_days"] += 1
        d += timedelta(days=1)

    rows = []
    for (iso_year, iso_week) in sorted(weeks.keys()):
        bucket = weeks[(iso_year, iso_week)]
        work_days = bucket["work_days"]
        hours = work_days * HOURS_PER_DAY
        rows.append({
            "ISO Year": iso_year,
            "ISO Week": iso_week,
            "Week Start": bucket["first"].isoformat(),
            "Week End": bucket["last"].isoformat(),
            "Work Days": work_days,
            "Hours": hours,
        })

    with open(CSV_OUTPUT, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(
            f,
            fieldnames=["ISO Year", "ISO Week", "Week Start", "Week End", "Work Days", "Hours"],
        )
        writer.writeheader()
        writer.writerows(rows)

    total_hours = total_work_days * HOURS_PER_DAY
    week_count = len(rows)
    avg_weekly_hours = total_hours / week_count if week_count else 0

    print(f"全年工作日: {total_work_days}")
    print(f"全年总小时: {total_hours}")
    print(f"年内周数:   {week_count}")
    print(f"周平均小时: {avg_weekly_hours:.2f}")
    print(f"已写入:     {CSV_OUTPUT}")


if __name__ == "__main__":
    main()
