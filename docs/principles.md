# Documents are views

A document is a rendering of facts for a reader. fathom keeps the facts in a
record and treats every document as a view of it: generated for one audience,
in one format and style, and thrown away when it's no longer needed. Any
document can be regenerated from the record at any time, and every document
rendered from the same version of the record agrees with every other.

## One piece of work, many readers

An outage ends, and five people want to know about it. An executive needs one
page: is it over, what did it cost, and what has to be decided. The engineers
choosing a fix need ten: the causal chain, the evidence for each link, how sure
anyone is, and the timeline down to the second. The teams it blocked need to
see what broke without learning the system. The postmortem meeting needs the
organization's template, filled. The next on-call needs to recognize it when
it happens again.

These aren't one document at different lengths. Each reader needs different
facts at a different depth, in different words, with different things left out,
and none of them should have to read the others' documents to get theirs. What
they share is the facts and the conclusion: the executive's one line and the
engineer's ten pages have to say the same thing happened, for the same reason.

## A document holds two things

A traditional document holds both the facts and the choices about how to
present them: which facts to include, in what order, at what depth, in what
words, with what layout. The two are woven together until a reader can't tell
a fact from the way it was framed.

Writing for one reader is also lossy. A fact that reader doesn't need is left
out, and when the document is the only place the facts were written down, the
fact is gone. Presenting the same facts to a second reader means writing a
second document from whatever survived, which makes a second copy of every
fact, and copies drift.

Picture that outage. In one working session, the engineers who ran it write two
of those pages: an analysis for engineers, and an explainer for everyone else. They go
out an hour apart, and by then they can disagree in places like these:

| Fact | Analysis | Explainer |
|---|---|---|
| Times the failure had happened in nine days | 5 | 6 |
| One environment's outage | still ongoing | a recovery time for one node |
| The fix | in review | applied |
| How long a node stayed stuck | 85+ minutes | "25 to 90 minutes" in the prose, 38 to 66 in the chart below it |
| Clean deploys on one day | 2 | 3, in its data |

Neither page has to be careless for this to happen. The analysis goes out first
and nobody goes back to it, and the explainer's prose and its chart are each
written from the data, at different moments. Every fix for this that keeps two
documents as sources means someone remembering to update them both.

## One record, rendered for each reader

fathom keeps the facts in a record instead: one named place per piece of work
(`checkout-outage`), where the facts collect as the work happens, along with the
record's current **lede**, the one statement of where the work stands. Each
reader gets a view rendered from it. Here is what three of the incident views
do with the same record:

| | Status | Explainer | Analysis |
|---|---|---|---|
| Reader | managers and planners | teams whose work was blocked | engineers choosing a fix |
| Length | one page | three scenes | as long as the evidence needs |
| Opens with the lede as | the state of the work and the one decision it needs | the limit, and what crossed it | the defect and the trigger, named |
| How it failed | a sentence | the same operation shown normal, failing, and fixed | a numbered causal chain, decisive links highlighted |
| The timeline | left out | left out | in full, with sources |
| How each claim is known | a label, where it changes what to do | left out | the basis beside each claim |
| Identifiers | left out | in hover text only | wherever a reader would look one up |

The views differ in nearly every row and still can't disagree, because none of
them holds a fact of its own. The principles below are what make that work.

## Software solved this already

Programs that show data to people ran into the same problem, and the fix has
the same shape every time: keep one source of record, derive every view from
it, and make the derivation repeatable.

| Pattern | Source of record | Views | What connects them |
|---|---|---|---|
| MVC, MVVM | Model | Views | Controller, or a view model with data binding |
| The web | Content and data | HTML structure, CSS style | The browser renders it; one page restyled by swapping only the stylesheet |
| React | State | Components | `UI = f(state)`: re-render instead of editing the screen |
| Data binding (XAML, Angular, Knockout) | View model | Templates | Bindings declare which field appears where |
| Event sourcing, CQRS | Event log | Read models | Projections, rebuilt from the log whenever needed |
| Relational databases | Tables | SQL views | Queries |
| Compilers | Intermediate representation | Machine code for each target | Back ends |
| OpenAPI | The API spec | Reference docs, client SDKs, contract tests | Generators |
| Cartography | The survey | Charts | A projection chosen for the chart's use |
| This suite | Each plugin's `plugin.yml` | `plugin.json`, the marketplace entry, the catalog page | shipyard's projections |

Technical writers have a version too:
[single-source publishing](https://en.wikipedia.org/wiki/Single-source_publishing),
with [DITA](https://www.oasis-open.org/committees/tc_home.php?wg_abbrev=dita)
as its formal standard and the [DITA Open Toolkit](https://www.dita-ot.org/) as
its reference renderer. It reuses passages of prose across outputs and filters
them by audience. fathom goes one level lower: the source is the facts, and the prose
is generated per reader.

These are all the same idea. fathom applies it to documents.

## Principles

### 1. The record is the source of truth

A record has a name, a growing set of facts, and a lede. Facts live in the
record. A document is a view of the record and never a source
for it. To change a fact, change the record and render again. A fact that shows
up first in a document, such as a number someone typed into a draft, is a fact
the record is missing.

### 2. The record keeps its own bottom line

The lede is the record's conclusion, kept as a fact: one statement of where the
work stands, naming the facts it rests on. It is revised as facts arrive, while
the person recording them still knows how much each one matters, and every
revision says what moved it. Worked out again at every render, the conclusion
would lean toward whatever was discussed last, and two views could reach two
different ones. Kept in the record, it is the same for every reader: each view
opens with the lede and only reframes it. When a fact the lede rests on changes,
the lede is stale until someone revises it, and so is every view that opened
with it.

### 3. The reader sets the depth

How much a view says, and how, belongs to its reader. An executive's one page
and an engineer's ten pages differ in what they include, not only in how they
look: the one page leaves out the evidence, the timeline, and the identifiers,
and the ten pages leave out nothing that bears on the cause. Both come from the
same record and open with the same lede. Adding a reader means writing down
what that reader needs, not writing another document.

### 4. Views are disposable

Deleting every rendered document loses nothing. Rendering is cheap and
repeatable, so a view is regenerated, not patched. This is React's model: you
don't edit the screen, you change the state and render again.

### 5. Every view is a function of four inputs

```text
view = render(record as of a version, audience, format, style)
```

Each input varies on its own:

| Input | Examples |
|---|---|
| Record version | as of now; as of when the first analysis went out |
| Audience | engineers, managers and planners, customers, the next on-call |
| Format | a web page, Markdown, a slide deck, a Word document, a chat post, an email |
| Style | the house design, a brand, plain text for an email |

The audience carries the depth (principle 3). Changing any input means
rendering again; none of them touches the record.

### 6. Views can't add facts

A view chooses, orders, phrases, and leaves out. Every fact it states comes from
the record, and it carries a citation to the row it came from. A view that
needs a fact the record doesn't hold sends that fact to the record first. This is
the data-binding rule: a template shows the properties it is bound to and makes
up nothing.

### 7. Facts carry their provenance

Each fact records where it came from and how it is known: measured, observed,
or inferred from a pattern. A view shows that certainty in its audience's
terms. An engineer sees the basis next to the claim; a manager sees a label.

### 8. The record is append-only and versioned

A correction adds a row; the old row stays. Every version of the record can be
read again, so any view can be rendered as of any point in time, and each
rendered view is stamped with the version it came from. Two views from the same
version agree by construction. A view from an earlier version is visibly
earlier, not silently wrong.

### 9. Agreement is checked

Every rendered view is checked before it's published. Every number a reader sees
has to sit inside a citation, and every citation has to resolve to the row the
view used. A type checker makes a promise about code; this check makes the same
kind of promise about documents.

### 10. Collect first, render when a reader needs it

Facts go into the record while the work happens, before anyone knows which
documents will be needed. Rendering waits until a reader asks. Rendering early
is fine too, since a stale view can be rendered again at the newer version.

### 11. Every projection distorts, so pick the distortion for the reader

The Mercator projection keeps angles true so a navigator can steer a straight
course, and pays for it by stretching areas toward the poles. Every view makes a
trade like that. A brief keeps "is it over, and what's left to decide" and drops
the evidence. An analysis keeps the evidence and takes an hour to read. Each
view says what it leaves out and links to the view that has it.

Inside a view the same order holds: it opens with the lede, put in that
reader's terms ([BLUF](https://en.wikipedia.org/wiki/BLUF_%28communication%29)),
and the detail below is there for the reader who chooses to read on. The link to the
deeper view is the next step of that expansion.

### 12. A view is defined the way a skill is

The instructions that turn the record into a view are written down, the way a
skill tells an agent how to do a job. This audience brief names the reader and
sets the tone, the verbosity, the format, and what to leave out, plus any
framing rule such as a blameless rewrite. The renderer follows the brief; the
brief is versioned and reviewed like code. A new kind of reader is a new brief,
not a new document.

### 13. A view is no wider than its narrowest fact

One record feeds every audience, so it joins facts whose sources had different
readers: a public status update beside a customer's name, an outage window
beside an internal host. Each view is a write to a new set of readers, and a
fact may only go where its source's readers could already see it. This is the
"no write-down" rule of the
[Bell–LaPadula model](https://en.wikipedia.org/wiki/Bell%E2%80%93LaPadula_model).
A view's visibility is capped by its most private fact, its
[high-water mark](https://en.wikipedia.org/wiki/High-water_mark_%28computer_security%29).

The scrutiny happens at render time, not while recording. Facts go in fast and
unclassified, since who may read one is often unclear until a reader asks for
it. The renderer judges each fact against the view's visibility, asks the user
about the ones it can't place, and records the answer, so the next render
doesn't ask again. The check then fails any view that cites a fact narrower
than the visibility it is stamped with.

## How rendered prose differs from rendered code

The software patterns above are deterministic: the same state renders the same
screen. A view written by a language model is deterministic about facts and not
about wording. Two renders of the same version can phrase things differently,
but they have to state the same facts. That's why the check works on facts and
citations, not on text.

Some facts are stated in words ("three environments", "the fix shipped"). The
renderer cites those the same way it cites numbers, and the check grows to cover
them.

Framing choices, such as a blameless rewrite or which point to lead with, are
presentation, but they carry meaning, so they live in the audience brief
(principle 12). Review effort moves from each document to the record and the
briefs, which serve every document.
