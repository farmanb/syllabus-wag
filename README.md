# Syllabus Template

This is a [PreTeXt](https://pretextbook.org/documentation.html) syllabus template for courses that use a weighted average grading scheme.

The course policies and student services sections are written for **Louisiana Tech University** — they cite University Policy 2206, the Louisiana Tech Academic Honor Code, and Louisiana Tech's counseling, disability, emergency-notification, help-desk, and tutoring resources. The template is usable elsewhere, but those sections (and the branding described under [Branding and personal defaults](#branding-and-personal-defaults)) have to be rewritten first.

## Layout

```
project.ptx              PreTeXt project manifest (web, print, scorm targets)
publication/             Publication file: chunking, theme, and version flags
assets/                  Logos and favicons
source/
  main.ptx               Document root; XIncludes every section below
  course-vars.ent        Per-course entities (see below)
  docinfo.ptx            Brand logo
  frontmatter.ptx        Author, copyright, license
  contact_information/   Instructor info, office hours, email etiquette
  course_information/    Description, topics, prerequisites, SLOs, methods
  evaluation/            Weights, grading scale, exams, homework, quizzes, engagement
  course_policies/       Textbook, attendance, late work, make-ups, honor code
  student_services/      Disability, counseling, ENS, withdrawal, LMS help, tutoring
  schedule/              make_weeks.py plus the generated weekXX.ptx files
```

## Customizing the syllabus

Most per-course details are defined as entities in [`source/course-vars.ent`](source/course-vars.ent). Edit the values there to set:

- the course number, section, term, and year;
- the instructor's honorific, first and last name, phone, email, website, and office;
- the department and institution (used on the title page);
- the textbook title, author, edition, and ISBN;
- the two exam dates, the final exam date, and the drop-with-a-`W` deadline.

Each value is reused everywhere the corresponding entity appears, so editing it in one place updates every section that references it.

The remaining placeholder prose should be filled in directly in the corresponding files under `source/`:

| File | Contains |
| --- | --- |
| [`course_information/course_description.ptx`](source/course_information/course_description.ptx) | Course description |
| [`course_information/course_topics.ptx`](source/course_information/course_topics.ptx) | Course topics |
| [`course_information/prereqs.ptx`](source/course_information/prereqs.ptx) | Prerequisites |
| [`course_information/student_learning_outcomes.ptx`](source/course_information/student_learning_outcomes.ptx) | Student learning outcomes |
| [`course_information/instructional_methods.ptx`](source/course_information/instructional_methods.ptx) | Delivery mode (defaults to face-to-face lecture) |
| [`contact_information/office_hours.ptx`](source/contact_information/office_hours.ptx) | Office-hour days and times |
| [`evaluation/weights.ptx`](source/evaluation/weights.ptx) | Grade categories and weights (defaults: homework 30%, two exams 20% each, final 30%) |
| [`evaluation/grading_scale.ptx`](source/evaluation/grading_scale.ptx) | Letter-grade cutoffs (defaults to a straight 90/80/70/60 scale) |

The evaluation and policy sections (`exams.ptx`, `homework.ptx`, `quizzes.ptx`, `engagement.ptx`, `late.ptx`, `attendance.ptx`, `make-up.ptx`) ship with working default prose. Read them before publishing — they state specific policies, such as late work not being accepted and academic dishonesty resulting in a grade of F for the course.

### Branding and personal defaults

A few values are hard-coded rather than driven by entities. Change them when adopting the template:

- [`source/frontmatter.ptx`](source/frontmatter.ptx) — copyright holder and years, and the title-page website URL (this one does not use the `website` entity).
- [`source/docinfo.ptx`](source/docinfo.ptx) — the brand logo and the URL it links to.
- [`assets/images/`](assets/images) — the Louisiana Tech logos, including `logo.png` referenced by `docinfo.ptx`.
- [`publication/publication.ptx`](publication/publication.ptx) — the HTML theme and its primary colors (currently the `boulder` theme in Louisiana Tech blue and red).

## Building

This is a standard PreTeXt project; [`requirements.txt`](requirements.txt) pins the PreTeXt-CLI version the project was generated with. With the CLI installed:

```sh
pip install -r requirements.txt
pretext build          # build the default target (web)
pretext view           # preview in a browser
```

[`project.ptx`](project.ptx) defines three targets: `web` (HTML), `print` (PDF), and `scorm` (HTML packaged for an LMS). Build one at a time with `pretext build web`, and so on. See the [PreTeXt documentation](https://pretextbook.org/documentation.html) for installation and deployment details.

Two conveniences come with the repo:

- [`.devcontainer.json`](.devcontainer.json) lets the project be edited and built in GitHub Codespaces without a local install.
- [`.github/workflows/pretext-cli.yml`](.github/workflows/pretext-cli.yml) builds the project on every pull request (and on demand via *Run workflow*), uploading the staged site as an artifact. It also deploys to Cloudflare Pages when the `CLOUDFLARE_PROJECT_NAME` repository variable is set, and to GitHub Pages when `PTX_ENABLE_DEPLOY_GHPAGES` is `yes` and the run is on the default branch. Building on pushes to `main` is commented out in that file.

## Schedule

Use the utility `make_weeks.py` to generate a skeleton schedule. It will write the files `main.ptx` and `weekXX.ptx` with the boilerplate "Material" listed for each day the course meets.

The script writes its output to the current working directory and overwrites any existing `main.ptx`/`weekXX.ptx`, so run it from inside `source/schedule/`:

```sh
cd source/schedule
python3 make_weeks.py START END DAYS [--no-class DATES]
```

- `START`, `END` — quarter start/end dates as `M/D/YYYY` (inclusive).
- `DAYS` — meeting days, given either as space/comma-separated names (`"Mon Wed"`, `"Tue, Thu"`) or as a compact code string (`"MWF"`, `"TR"`, `"TTh"`, `"MTWRF"`). Day letters are `M T W R F` (with `R` = Thursday) plus `Sa`/`Su` for the weekend.
- `--no-class` — optional space/comma-separated `M/D/YYYY` dates to skip (e.g. holidays). Because the first three arguments are positional, this flag has to come last.

Examples:

```sh
python3 make_weeks.py 3/12/2026 6/2/2026 "Mon Wed"
python3 make_weeks.py 3/12/2026 6/2/2026 "MWF" --no-class 3/27/2026,4/10/2026
python3 make_weeks.py 3/12/2026 6/2/2026 "TTh"
```

Weeks run Monday through Sunday and are numbered from the Monday of the week containing `START`, so a term that begins mid-week still starts at `week01`. Any leftover `weekXX.ptx` files from a longer previous term are not deleted — remove them by hand.

After generating the skeleton, replace each day's "Material" placeholder with the actual topics.

## Optional sections (version flags)

Several sections are conditional. They are tagged in the source with a `component` attribute and are only rendered when that component is listed in the `<version include="…"/>` element in [`publication/publication.ptx`](publication/publication.ptx). To turn a section on or off, add or remove its flag from that list.

| Flag | Controls |
| --- | --- |
| `graduate` | Extra expectations for cross-listed 5XXX/6XXX courses, in the homework and engagement sections. |
| `exams` | Exams section and make-up policy. |
| `engagement` | Graded participation/engagement. |
| `homework` | Homework section. |
| `quizzes` | Quizzes section. |
| `BARC` | BARC university tutoring resources. |
| `mathclub` | Math Club tutoring resources. |

`BARC` and `mathclub` are off by default; enable them only for service-level courses where tutoring is available through those resources.

Turning a section off hides its prose but not its weight — remove the matching row from [`evaluation/weights.ptx`](source/evaluation/weights.ptx) as well, and adjust the remaining weights so they still total 100%.

## License

This work is licensed under the [Creative Commons Attribution-ShareAlike 4.0 International License](https://creativecommons.org/licenses/by-sa/4.0/). See [`LICENSE`](LICENSE) for the full text.
