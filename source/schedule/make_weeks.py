#!/usr/bin/env python3
"""
Generate PreTeXt weekly schedule files (weekXX.ptx) for a course,
plus a main.ptx that includes them all.

Usage examples:
    python3 make_weeks.py 3/12/2026 6/2/2026 "Mon Wed"
    python3 make_weeks.py 3/12/2026 6/2/2026 "MWF" --no-class 3/27/2026,4/10/2026
"""

import sys
from datetime import date, timedelta
from pathlib import Path

DAY_NAME_MAP = {
    "m": 0, "mon": 0, "monday": 0,
    "t": 1, "tu": 1, "tue": 1, "tues": 1, "tuesday": 1,
    "w": 2, "wed": 2, "wednesday": 2,
    "r": 3, "th": 3, "thu": 3, "thur": 3, "thurs": 3, "thursday": 3,
    "f": 4, "fri": 4, "friday": 4,
    "sa": 5, "sat": 5, "saturday": 5,
    "su": 6, "sun": 6, "sunday": 6,
}


def parse_date(dstr: str) -> date:
    """Parse M/D/YYYY into a date object."""
    m, d, y = (int(x) for x in dstr.strip().split("/"))
    return date(y, m, d)


def parse_date_list(s: str):
    """Parse '3/27/2026,4/10/2026 5/1/2026' -> {date, ...}."""
    if not s:
        return set()
    parts = s.replace(",", " ").split()
    return {parse_date(p) for p in parts}


def parse_meeting_days(meeting_days_str: str):
    """
    Convert 'Mon Wed' or 'MWF' into a sorted list of weekday numbers.
    Monday = 0, Sunday = 6.
    """
    s = meeting_days_str.replace(",", " ").strip()

    # Compact form like "MWF" or "TR"
    if " " not in s and s.isalpha() and 1 < len(s) <= 3:
        tokens = list(s)
    else:
        tokens = s.split()

    weekdays = []
    for tok in tokens:
        key = tok.lower()
        if key not in DAY_NAME_MAP:
            raise ValueError(f"Unknown day token: {tok!r}")
        wd = DAY_NAME_MAP[key]
        if wd not in weekdays:
            weekdays.append(wd)

    weekdays.sort()
    return weekdays


def build_schedule(start_date: date, end_date: date, meeting_days, no_class_dates):
    """
    Yield (week_number, week_start, week_end, [meeting_dates]) for each calendar
    week (Mon–Sun) intersecting [start_date, end_date].
    """
    first_monday = start_date - timedelta(days=start_date.weekday())
    week_index = 0

    while True:
        week_start = first_monday + timedelta(weeks=week_index)
        week_end = week_start + timedelta(days=6)

        if week_start > end_date:
            break

        meetings = []
        for wd in meeting_days:
            d = week_start + timedelta(days=wd)
            if start_date <= d <= end_date and d not in no_class_dates:
                meetings.append(d)

        yield (week_index + 1, week_start, week_end, meetings)
        week_index += 1


def format_date_for_title(d: date) -> str:
    """Format date for the Week title (e.g., 'March 9')."""
    # On macOS/Linux, %-d is fine; change to "%B %d" if you prefer 0-padded days.
    return d.strftime("%B %-d")


def format_date_for_meeting_title(d: date) -> str:
    """Format date for the <title> of each meeting (e.g., 'March 09')."""
    return d.strftime("%B %d")


def generate_week_xml(week_number: int, week_start: date, week_end: date, meeting_dates):
    """Generate the PreTeXt XML string for a single weekXX.ptx file."""
    week_id = f"{week_number:02d}"

    start_str = format_date_for_title(week_start)
    end_str = format_date_for_title(week_end)

    lines = []
    lines.append('<?xml version="1.0" encoding="utf-8"?>')
    lines.append(f'<subsection xml:id="week-{week_id}">')
    lines.append(f'  <title>{start_str} <ndash/> {end_str}</title>')
    lines.append('  <p>')
    lines.append('    <dl>')

    for d in meeting_dates:
        day_title = format_date_for_meeting_title(d)
        lines.append('      <li>')
        lines.append(f'        <title>{day_title}</title>')
        lines.append('        <p>')
        lines.append('          Material')
        lines.append('        </p>')
        lines.append('      </li>')

    lines.append('    </dl>')
    lines.append('  </p>')
    lines.append('</subsection>')

    return "\n".join(lines)


def generate_main_ptx(week_files):
    """
    Create main.ptx that XIncludes each weekXX.ptx file in order.
    """
    lines = []
    lines.append('<?xml version="1.0" encoding="utf-8"?>')
    lines.append('<section xml:id="schedule" xmlns:xi="http://www.w3.org/2001/XInclude">')
    lines.append('  <title>Schedule</title>')

    for wf in week_files:
        lines.append(f'  <xi:include href="{wf}"/>')

    lines.append('')
    lines.append('  <conclusion>')
    lines.append('    <warning>')
    lines.append('      <p>')
    lines.append('        The instructor reserves the right to modify the schedule as needed.')
    lines.append('      </p>')
    lines.append('    </warning>')
    lines.append('  </conclusion>')
    lines.append('</section>')

    Path("main.ptx").write_text("\n".join(lines), encoding="utf-8")
    print("Wrote main.ptx")


def main(argv):
    if len(argv) < 4:
        print(__doc__)
        sys.exit(1)

    start_date = parse_date(argv[1])
    end_date = parse_date(argv[2])
    if end_date < start_date:
        raise SystemExit("end_date must be on or after start_date")

    meeting_days = parse_meeting_days(argv[3])

    no_class_dates = set()
    if "--no-class" in argv:
        idx = argv.index("--no-class")
        if idx + 1 >= len(argv):
            raise SystemExit("--no-class requires a value")
        no_class_dates = parse_date_list(argv[idx + 1])

    week_files = []

    for week_number, week_start, week_end, meetings in build_schedule(
        start_date, end_date, meeting_days, no_class_dates
    ):
        xml = generate_week_xml(week_number, week_start, week_end, meetings)
        filename = f"week{week_number:02d}.ptx"
        Path(filename).write_text(xml, encoding="utf-8")
        week_files.append(filename)
        print(f"Wrote {filename}")

    # Now generate main.ptx that includes all the weeks we just wrote
    generate_main_ptx(week_files)


if __name__ == "__main__":
    main(sys.argv)
