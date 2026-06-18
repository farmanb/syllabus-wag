# Syllabus Template
This is a [PreTeXt](https://pretextbook.org/documentation.html) syllabus template for courses that use a weighted average grading scheme.
## Schedule

Use the utility `make_weeks.py` to generate a skeleton schedule. It will write the files `main.ptx` and `weekXX.ptx` with the boilerplate "Material" listed for each day the course meets.

The script writes its output to the current working directory and overwrites any existing `main.ptx`/`weekXX.ptx`, so run it from inside `source/schedule/`:

```sh
cd source/schedule
python3 make_weeks.py START END DAYS [--no-class DATES]
```

- `START`, `END` — quarter start/end dates as `M/D/YYYY` (inclusive).
- `DAYS` — meeting days, given either as space/comma-separated names (`"Mon Wed"`, `"Tue, Thu"`) or as a compact code string (`"MWF"`, `"TR"`, `"TTh"`, `"MTWRF"`). Day letters are `M T W R F` (with `R` = Thursday) plus `Sa`/`Su` for the weekend.
- `--no-class` — optional space/comma-separated `M/D/YYYY` dates to skip (e.g. holidays).

Examples:

```sh
python3 make_weeks.py 3/12/2026 6/2/2026 "Mon Wed"
python3 make_weeks.py 3/12/2026 6/2/2026 "MWF" --no-class 3/27/2026,4/10/2026
python3 make_weeks.py 3/12/2026 6/2/2026 "TTh"
```

After generating the skeleton, replace each day's "Material" placeholder with the actual topics.
