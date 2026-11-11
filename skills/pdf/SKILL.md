---
name: pdf
description: This skill should be used when the user wants a PDF to share with people who can't open the original, such as "/fathom:pdf", "make a PDF of this view", "export this artifact to PDF", "turn this into a one-pager", "I need to send this to someone without Claude", or "print this page". Prints a fathom view, a claude.ai artifact, a local HTML page, or what was just said in chat to a PDF that fits one US Letter page by default, condensing or paginating when it doesn't fit. For reading, merging, splitting, or filling existing PDFs, use a general PDF tool instead.
argument-hint: "[a4] [landscape] [pages: <n>] [full] [fancy] [<view | artifact url | file | what to print>]"
---

# PDF

PDF is a format: the one that opens for everyone. An artifact opens only for
people with a Claude license, and a view in a repo only for people with the
repo, so this skill turns the page into one a reader can get as an email
attachment, a ticket attachment, or a chat file. The default is a one-pager,
the shape a reader without the original context will actually read.

## 1. Pick the source

Use the most recent view or artifact in the conversation unless the arguments
name something else.

| Source | Get HTML to print |
| --- | --- |
| A fathom view (an HTML file stamped `<meta name="fathom-version">`) | The view file, printed with `--record <its record dir>` |
| An artifact published in this session | The local `.html` file it was published from |
| A claude.ai artifact URL | `Artifact` `action: "read"`; it saves the full HTML locally and names the path. Copy it into the scratchpad as `artifact.html`, the file you print and pass to `--links-from`. For a multi-file artifact, fetch the files the page references with `paths` into the same folder. A read of someone else's artifact returns a summary rather than HTML: say it can't be printed faithfully and offer a one-pager written from the summary |
| A Claude Docs link | Not this skill: export it with the Docs connector's `export` to PDF, which keeps the doc's own layout |
| A reply, plan, or summary from the chat | Write a one-pager (step 4), then render it |
| A local `.html` file or a URL | Use it as is |

## 2. Read the arguments

| Argument | Script flag |
| --- | --- |
| *(none)* | one US Letter page, portrait |
| `a4` | `--paper a4` |
| `landscape` | `--landscape` |
| `pages: <n>` | `--pages <n>` |
| `full`, `as-is`, `all pages` | `--paginate`: 100% scale, as many pages as it takes |
| `one-pager`, `one page`, `summary` | the user already chose condensing: on overflow, go straight to step 4 without asking |
| `fancy`, `polished`, `dress it up` | the report style (step 4, Style), even when the page would print as is |
| an output path | the `<out.pdf>` argument |

Write the PDF to `~/Downloads/<slug>.pdf`, where the slug is the page's
`<title>` in kebab-case, unless the user names a path; Downloads is where
they'll pick it up to attach it. When producing both a one-pager and the full
document, the full one gets a `-full` suffix.

## 3. Prepare the page

The script prints in the light color scheme with print media, opens every
`<details>`, and injects `assets/print.css`: white paper, no screen padding, no
reading-width cap, tables unboxed from their scroll containers and allowed to
wrap code, no rows split across pages. Read the HTML for what that can't fix,
and write those overrides to a stylesheet in the scratchpad passed with
`--css`:

- **Tabs or toggles**: only the active panel prints. Show every panel and hide
  the tab bar.
- **Full-viewport heroes, sticky headers, fixed sidebars**: reset `height`,
  `position`, and `min-height` so they take their natural size.
- **Hover-only detail** (tooltips, hover cards): lost on paper. Print as is
  unless the detail carries the point, then condense (step 4).

The page's own stylesheet often sits later in the document than the injected
one, so an override needs `!important` to win.

A page whose purpose is interaction (a form, a calculator, a game) has nothing
to print. Say so and offer a one-pager that describes what it does.

## 4. Write a one-pager

Used for chat sources, for condensing a page that doesn't fit, for `fancy`, and
for a summary-only source.

**A fathom view condenses from the record, not from the view.** Rewriting a
view into a shorter one makes a document from a document, which is how two
copies of a fact start to drift. Render a new view with `/fathom:render`, from
the same record version, with a brief whose verbosity is one page (the kind's
`status` brief, or one the user names), then print that. Everything below about
writing the page still applies; the facts come from `fathom show`, and every one
carries its citation.

For any other source, copy `assets/one-pager.html` into the scratchpad as
`<slug>.html` and fill it. Many artifacts build their page with a script from an
embedded data object (`const DATA = {…}`). Read the numbers from that object with
a short script rather than from the rendered text: it holds the item-level data
the per-row comparisons need. Run it with `python3 -I` and keep it out of the
folder holding the artifact.

**What the user asked for earlier in the conversation outranks every default
below.** A request made while the page was being built ("link the pipelines",
"show which tests changed", "keep it to the decision") still holds when the user
asks for the PDF, even though it isn't in the arguments. Reread the conversation
for them before condensing.

- **Header**: when the page exists to deliver a verdict and the source states
  one, the H1 is that finding ("Upgrading the database broke no integration
  tests"), and the source's name moves to the meta line. Otherwise the H1 is the
  title. **The H1 fits on one line**: shorten the wording before shrinking the
  type. The meta line carries today's date and the user's name (`git config
  user.name`) when the content is their work.
- **The takeaway, highlighted**: right under the header, the template's verdict
  box holds the page's
  [bottom line up front](https://en.wikipedia.org/wiki/BLUF_%28communication%29):
  the one line a reader needs if they read nothing else, written for the reader
  the user names. Its color answers the question the page exists to settle, not
  the raw results: when the source rules the failures it shows out of that
  question, the box stays green. Use `warn` or `bad` only when the answer itself
  is bad news.
- **Body**: the key facts, the decisions or asks, and only the evidence that
  carries them. Use the template's facts strip, tables, comparison bars, and two
  columns as fits the content, and add CSS for patterns the template lacks. A
  table of a few narrow columns goes in a column, not stretched across the page.
- **Sort rows by the number the reader compares**, largest first, ties
  alphabetical.
- **Explain each count where it's counted.** Each category row carries the
  category in bold and a one-line explanation under it (the template's `.why`),
  next to its numbers, instead of a counts table plus a separate section
  restating the categories.
- **Show the evidence for the claim on each row.** When the point is sameness,
  overlap, or change in specific items, put the item-level comparison on the row:
  a label ("10 same, 3 now pass") and the template's comparison bar. Leave a zero
  segment out of the bar rather than giving it a width.
- **Facts stay as the source states them.** Reshape, select, and count what the
  source itemizes. Don't compute values the source can't support item by item (a
  gap between two timestamps, an estimate), and don't summarize into new claims.
  When the source's own derived number disagrees with its item-level data, print
  the number the items support, and tell the user about the discrepancy. In a
  fathom view, a value the record lacks goes to the record first
  (`/fathom:record`), never onto the page.
- **Links: keep as many as the page can carry.** Carry over every link to
  pipelines, jobs, change requests, tickets, and dashboards, even when its row is
  condensed. Set each on a cell the row already has (a failed count links to its
  job) so links cost no space. Drop only links the readers can't open:
  claude.ai artifacts, consoles behind access the audience lacks.
- **When condensing**, drop what serves a screen reader of the original:
  minute-by-minute timelines, source columns, instance IDs. Collapse rows that
  all say the same thing into one line and keep every link those rows carried
  (`orders-api (before | after)`). When a full PDF goes alongside, end with a
  footer naming it as where the dropped detail lives.
- **End with the conclusion box** when the source has a recommendation, a next
  step, or a closing line. It says what follows from the page, not a restatement
  of the verdict.
- **Short content stays short.** A half-empty page is fine.

**Style.** Who reads the page decides it:

| Keep the source's style (default) | `fancy` |
| --- | --- |
| The user's team, the thread the page came from | Leadership, another team, an auditor, a ticket attachment |
| A working update or progress snapshot | A verdict or decision: a sign-off, an assessment, an incident summary |
| A source with a look worth keeping (its charts, its colors) | A source whose look is plain or built for a screen |

Use `fancy` only when the arguments ask for it. When the page delivers a
verdict, or the user names a reader from the right-hand column, render the
default and offer the fancy version in the report.

A page written from a source without `fancy` keeps the source's look: copy its
font `<link>` tags, set the template's tokens (`--body`, `--mono`, `--display`,
`--fg`, `--muted`, `--rule`, `--accent`, `--good`/`--bad`) from its light theme,
match its headings, and keep its signature elements (a pill, an eyebrow line, its
chart colors). A page written from chat uses the template's tokens as they are.

With `fancy`, render with `--css ${CLAUDE_PLUGIN_ROOT}/skills/pdf/assets/fancy.css
--margin 0`: a dark header band with a metadata grid, serif headings, dark table
heads, and status pills. Fill the template's eyebrow, metadata grid (source,
date, author, a tracking link when there is one; for a fathom view, the record
version and audience), verdict box, cards, and conclusion box. Put a sensitivity
label in the footer only when the user or the source names one.

## 5. Render

```bash
uv run --script ${CLAUDE_PLUGIN_ROOT}/skills/pdf/scripts/to-pdf.py <page.html | url> <out.pdf> --preview <scratchpad>/preview [flags]
```

For a fathom view, add `--record <dir>`: the script runs `fathom check` on the
view first and prints nothing when it fails. A PDF reaches whoever it's sent
to, so before printing a view, ask who that is when the user hasn't said, and
when they are wider than the view's `fathom-visibility` stamp, render the view
again at that visibility (`/fathom:render`) instead of printing this one. When
the page is a one-pager written from an artifact, add `--links-from <artifact.html>`: the script reports
how many of its links the PDF kept, naming the ones it lost. Put each missing
link back unless the readers can't open it.

A layout fits when it lands on the page budget with nothing past the right
margin. The script renders real PDFs and counts their pages, picking the largest
scale between `--min-scale` (75% by default, the smallest that still reads
comfortably) and 100% that fits. Its first run downloads its Python packages
into uv's cache; it prints with the installed Google Chrome.

| Exit | Meaning | Do |
| --- | --- | --- |
| 0 | Written; stdout names pages, scale, link count, path, and the preview PNGs | Step 6, after restoring any missing link the readers can open |
| 3 | Too many pages at the floor; stdout gives the page count at 100% and at 75% | Handle the overflow (below) |
| 4 | Content runs past the right margin; stdout names the widest elements | Write `--css` that wraps or narrows them, or rerun with `--landscape` when it's one wide table |
| 5 | A fathom view failed its check, or has no `--record` | Fix the view (or the record) with `/fathom:render`; never print around it |
| 1 | Chrome, uv, or the page failed to load | Report the error as printed |

**Overflow.** Take the first row that matches:

1. **The user asked for a one-pager**: write it (step 4) and render it; offer the
   full document in the report.
2. **2 pages at 75%**: try `--margin 0.3in`, or `--landscape` when a wide table
   is what grows the page. If neither fits, go to 3.
3. **3 pages or fewer at 100%**: condense (step 4) and render the one-pager.
4. **More than 3 pages at 100%**: ask with `AskUserQuestion`. Offer a condensed
   one-pager (name what it leaves out), the full document (`--paginate`, giving
   its page count), or both.

**Fit a one-pager by layout before scale.** A page you wrote should print at 95%
or more. At 90% or more, tighten (shorter lede, table padding, one-line rows);
below 90%, restructure (move or merge sections, fold a list into a table's rows,
collapse rows that say the same thing). Cut content only after the layout has no
slack left, and never lower `--min-scale`.

**When the script warns that the H1 wraps**, shorten the H1 and rerender.

## 6. Look at it, then report

Read the preview PNGs before reporting. A render can succeed and still be wrong:
a chart that drew blank because its script failed, text clipped inside a
fixed-height box, a dark panel that ignored the light theme. Fix it with `--css`
or in the one-pager and rerender.

Report in a few lines: each file as a link (`[name.pdf](file:///full/path)`)
with its page count and scale, for a condensed page what it left out, for a
fathom view the record version, audience, and visibility it was stamped with, any number in
the source that its own data contradicts, and the offer of a fancy version when
the Style table points there.

## Resources

- **`scripts/to-pdf.py`**: render, fit, check width, gate fathom views on their
  check, and write previews. `--help` lists every flag.
- **`assets/print.css`**: the print overrides injected into every page.
- **`assets/one-pager.html`**: the print-first template for step 4, sized in
  points for Letter and A4.
- **`assets/fancy.css`**: the `fancy` style.
