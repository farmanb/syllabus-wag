#!/usr/bin/env python3
"""
Generate a PreTeXt schedule section (main.ptx) laid out as a single table
with one row per class meeting and columns for Date, Topic, and Homework.
Thin rules separate days; heavy rules separate weeks.  The generated file
is a skeleton: fill in the Topic and Homework cells by hand.

Usage:
    python3 make_schedule.py START END DAYS [--no-class DATES] [--force]

    START, END   Quarter start/end dates as M/D/YYYY (inclusive).
    DAYS         Meeting days, given either as space/comma-separated names
                 ("Mon Wed", "Tue, Thu") or as a compact code string
                 ("MWF", "TR", "TTh", "MTWRF"). Day letters: M T W R(=Thu)
                 F, with Sa/Su for the weekend.
    --no-class   Optional space/comma-separated M/D/YYYY dates to skip.
    --force      Overwrite an existing main.ptx (it is never overwritten
                 otherwise, since it holds hand-entered content).

Usage examples:
    python3 make_schedule.py 9/10/2026 11/18/2026 MWF
    python3 make_schedule.py 3/12/2026 6/2/2026 "Mon Wed" --no-class 3/27/2026,4/10/2026

Cell conventions (so both the HTML and PDF builds look right):
    * A Topic or Homework cell that may need to wrap should hold a <p>.
      PreTeXt only wraps table cells in LaTeX when they contain a paragraph.
    * A day with two topics should use two <line> elements instead, which
      keeps the lines tight:
          <cell>
            <line>1.2 Division with Remainder</line>
            <line>1.3 Greatest Common Divisors</line>
          </cell>
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

CAPTION = "Weekly Schedule (the instructor reserves the right to modify the schedule as needed)"


def parse_date(dstr: str) -> date:
    """Parse M/D/YYYY into a date object."""
    m, d, y = (int(x) for x in dstr.strip().split("/"))
    return date(y, m, d)


def parse_date_list(s: str):
    """Parse '3/27/2026,4/10/2026 5/1/2026' -> {date, ...}."""
    if not s:
        return set()
    return {parse_date(p) for p in s.replace(",", " ").split()}


def decompose_compact(tok: str):
    """Decompose 'MWF', 'TR', or 'TTh' into weekday numbers, preferring
    two-character codes ('Th', 'Sa', 'Su') over one-character codes."""
    key = tok.lower()
    weekdays = []
    i = 0
    while i < len(key):
        if key[i:i + 2] in DAY_NAME_MAP:
            weekdays.append(DAY_NAME_MAP[key[i:i + 2]])
            i += 2
        elif key[i:i + 1] in DAY_NAME_MAP:
            weekdays.append(DAY_NAME_MAP[key[i:i + 1]])
            i += 1
        else:
            raise ValueError(f"Unknown day token: {tok!r}")
    return weekdays


def parse_meeting_days(meeting_days_str: str):
    """Convert 'Mon Wed', 'Tue Thu', 'MWF', 'TR', or 'TTh' into a sorted
    list of weekday numbers (Monday = 0)."""
    weekdays = []
    for tok in meeting_days_str.replace(",", " ").split():
        key = tok.lower()
        matches = [DAY_NAME_MAP[key]] if key in DAY_NAME_MAP else decompose_compact(tok)
        for wd in matches:
            if wd not in weekdays:
                weekdays.append(wd)
    return sorted(weekdays)


def build_weeks(start_date: date, end_date: date, meeting_days, no_class_dates):
    """Yield a list of meeting dates for each calendar week (Mon-Sun) that
    has at least one meeting in [start_date, end_date]."""
    first_monday = start_date - timedelta(days=start_date.weekday())
    week_start = first_monday
    while week_start <= end_date:
        meetings = [
            week_start + timedelta(days=wd)
            for wd in meeting_days
            if start_date <= week_start + timedelta(days=wd) <= end_date
            and week_start + timedelta(days=wd) not in no_class_dates
        ]
        if meetings:
            yield meetings
        week_start += timedelta(weeks=1)


def format_date(d: date) -> str:
    """Format a meeting date for the Date column, e.g. 'Wed, Oct 21'."""
    return d.strftime("%a, %b %-d")


def generate_schedule_xml(weeks) -> str:
    """Generate the PreTeXt XML for main.ptx."""
    lines = [
        '<?xml version="1.0" encoding="utf-8"?>',
        '<section xml:id="schedule" label="schedule">',
        '  <title>Schedule</title>',
        '  <table xml:id="schedule-table">',
        f'    <title>{CAPTION}</title>',
        '    <tabular width="100%" halign="left" valign="top" top="minor">',
        '      <col width="17%"/>',
        '      <col width="38%"/>',
        '      <col width="45%"/>',
        '      <row header="yes" bottom="medium">',
        '        <cell>Date</cell>',
        '        <cell>Topic</cell>',
        '        <cell>Homework</cell>',
        '      </row>',
    ]
    for week in weeks:
        for i, d in enumerate(week):
            rule = "major" if i == len(week) - 1 else "minor"
            lines += [
                f'      <row bottom="{rule}">',
                f'        <cell>{format_date(d)}</cell>',
                '        <cell><p>Material</p></cell>',
                '        <cell><p>Homework</p></cell>',
                '      </row>',
            ]
    lines += [
        '    </tabular>',
        '  </table>',
        '</section>',
    ]
    return "\n".join(lines) + "\n"


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

    out = Path(__file__).resolve().parent / "main.ptx"
    if out.exists() and "--force" not in argv:
        raise SystemExit(f"{out} already exists; pass --force to overwrite it")

    weeks = list(build_weeks(start_date, end_date, meeting_days, no_class_dates))
    out.write_text(generate_schedule_xml(weeks), encoding="utf-8")
    print(f"Wrote {out} ({sum(len(w) for w in weeks)} meetings in {len(weeks)} weeks)")


if __name__ == "__main__":
    main(sys.argv)
