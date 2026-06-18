# Syllabus Template
This is a [PreTeXt](https://pretextbook.org/documentation.html) syllabus template for courses that use a weighted average grading scheme.

## Customizing the syllabus

Most per-course details are defined as entities in [`source/course-vars.ent`](source/course-vars.ent). Edit the values there to set:

- the course number, section, term, and year;
- the instructor's honorific, name, phone, email, website, and office;
- the textbook title, author, edition, and ISBN;
- the two exam dates, the final exam date, and the drop-with-a-`W` deadline.

Each value is reused throughout the document, so editing it in one place updates every section that references it.

The remaining placeholder prose — the course description, topics, prerequisites, student learning outcomes, office-hour times, and the grading weights and scale — should be filled in directly in the corresponding files under `source/`.

## Building

This is a standard PreTeXt project. See the [PreTeXt documentation](https://pretextbook.org/documentation.html) for how to install the PreTeXt-CLI, build and preview the document, and deploy it.

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

## Optional sections (version flags)

Several sections are conditional. They are tagged in the source with a `component` attribute and are only rendered when that component is listed in the `<version include="…"/>` element in `publication/publication.ptx`. To turn a section on or off, add or remove its flag from that list.

| Flag | Controls |
| --- | --- |
| `graduate` | Extra expectations for cross-listed 5XXX/6XXX courses. |
| `exams` | Exams section and make-up policy. |
| `engagement` | Graded participation/engagement. |
| `homework` | Homework section. |
| `quizzes` | Quizzes section. |
| `BARC` | BARC university tutoring resources. |
| `mathclub` | Math Club tutoring resources. |

`BARC` and `mathclub` are off by default; enable them only for service-level courses where tutoring is available through those resources.

## License

This work is licensed under the [Creative Commons Attribution-ShareAlike 4.0 International License](https://creativecommons.org/licenses/by-sa/4.0/). See [`LICENSE`](LICENSE) for the full text.
