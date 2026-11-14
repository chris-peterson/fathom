# fathom: Specification

fathom keeps the facts of a piece of work in one versioned record and renders
each document from it, for one audience in one format and style at a time. The
rendered documents are views: disposable, regenerated from the record on demand,
and checked so that every figure in them traces to a fact. Why this shape, and
how it relates to MVC, React, data binding, and event sourcing, is in
[docs/principles.md](docs/principles.md).

Requirements use [EARS syntax](https://alistairmavin.com/ears). Each is one of:
Ubiquitous (`The <system> shall …`), State-Driven (`While …`), Event-Driven
(`When …`), Optional (`Where …`), or Unwanted Behaviour (`If … then …`).

Each requirement is its own heading carrying a stable ID (`XX-NN`), one level
below its category's heading, so every requirement has a linkable anchor
(`SPEC.md#record-01`). Lettered decompositions (`XX-NNa`) each count as one.

## Concepts

- **fact**: one thing that is true about the work, named by a stable key
  (`outage-window-2`, `fix-01`). Views cite facts by key.
- **row**: one version of one fact: its fields, when it was recorded, how it is
  known, and why it is believed.
- **record**: every row for one piece of work. Append-only.
- **schema**: the declaration of every kind of fact a record can hold. The
  record's storage and validation are generated from it.
- **kind**: a schema, the briefs for its readers, the framing rules those
  briefs apply, and where its evidence comes from, for one kind of work. A kind
  can extend another.
- **version**: a point in the record's history. Reading the record *as of* a
  version gives, for each fact, the latest row recorded at or before it.
- **certainty**: how a fact is known: measured, observed, or inferred.
- **visibility**: who may see something, in the levels a GitLab project uses:
  public (anyone), internal (anyone in the organization), or private (the
  people on the work). A fact's visibility is who can see its source; a view's
  is who can see where it is published.
- **view**: one rendered document: the record as of a version, rendered for an
  audience, in a format and a style.
- **audience brief**: the instructions the renderer follows to turn the record
  into a view, written the way a skill is: who the view is for, what they need
  from it, its tone and verbosity, and what it leaves out.
- **bottom line**: the one statement a view's reader needs if they read nothing
  else, set by the view's brief and stated first
  ([BLUF](https://en.wikipedia.org/wiki/BLUF_%28communication%29)).
- **format**: the output medium: a web page, Markdown, a slide deck, a Word
  document, a chat post, an email.
- **message**: a format written to be pasted into a composer rather than opened:
  a chat post or an email. A message keeps no stamps, so it is checked as the
  view it was converted from.
- **style**: the visual treatment within a format.
- **chat engine**: the chat product a chat post is written for, which sets the
  post's markup, the link form its composer keeps on a paste, and what it can't
  render. fathom supports one, Slack.
- **citation**: the link from a rendered fact back to the fact key it came from.
- **check**: the verification run over a rendered view before it is published.

## Requirements

### `DESIGN`
Shape of the system

#### `DESIGN-01`
The system shall treat the record as the only source of facts, and every view as
derived from it.

#### `DESIGN-02`
The system shall keep its core independent of any one kind of work, taking the
kinds of fact it handles from a schema, so incidents, investigations, and other
work each bring their own schema and briefs.

#### `DESIGN-03`
The system shall let the record, the audience, the format, and the style each
change without requiring a change to the others.

### `RECORD`
The record

#### `RECORD-01`
The system shall store every fact as rows carrying the fact's key, its fields,
the time the row was recorded, its certainty, and its basis.

#### `RECORD-02`
When a fact changes, the system shall add a row for the new version and keep
every earlier row.

#### `RECORD-03`
The system shall generate the record's storage and its validation from the
schema.

#### `RECORD-04`
If a row does not validate against the schema, then the system shall refuse to
record it and report why.

#### `RECORD-05`
If a text field holds markup outside the allowed set, then the system shall
refuse the row, so presentation can't be stored as data.

#### `RECORD-06`
The system shall read the record as of any version it holds.

#### `RECORD-07`
When a fact is recorded, the system shall accept it whether or not any view
exists yet.

#### `RECORD-08`
When new evidence contradicts a fact the record holds, the system shall name the
fact, both values, and both bases before recording the correction.

#### `RECORD-09`
When a fact is found false, the system shall record a retraction row with its
basis, so reads as of later versions drop the fact and reads as of earlier
versions keep it.

#### `RECORD-10`
If a row's timestamp carries no UTC offset, then the system shall refuse the
row, so evidence from every source merges into one zone.

#### `RECORD-11`
If any row in one addition is invalid, then the system shall record none of
them.

#### `RECORD-12`
Where a record is named by a bare name rather than a path, the system shall keep
it in `.fathom/<name>/` at the root of the git repository holding the working
directory, or in `./.fathom/<name>/` outside a repository.

#### `RECORD-13`
When the system creates the `.fathom/` directory, it shall make git ignore what
it holds, so a record is committed only when someone adds it on purpose.

#### `RECORD-14`
The system shall keep a record's rows in one append-only file, one row per
line, whose first row, version 0, holds the record's kind and title.

#### `RECORD-15`
When a record is retitled, the system shall add a row holding the new title, so
a read as of an earlier version keeps the earlier title.

### `KIND`
Kinds of work

#### `KIND-01`
The system shall take each record's fact types, briefs, framing rules, and
evidence sources from the kind the record names.

#### `KIND-02`
Where a kind extends another, the system shall give it the other kind's fact
types, briefs, framing rules, and sources, replacing any it redefines.

#### `KIND-03`
Where a brief extends the same-named brief of the kind its kind extends, the
system shall apply both briefs and the framing rules either names.

#### `KIND-04`
The system shall look a kind up in the directories a project names before the
kinds it ships with, so a team can add or extend a kind without changing the
plugin.

#### `KIND-05`
If a kind's schema lists an enum value that isn't text, then the system shall
refuse the kind and name the field, since YAML reads a bare `yes` or `no` as a
boolean that no row can match.

### `VIEW`
Rendering views

#### `VIEW-01`
The system shall render a view from four inputs: the record as of a version, an
audience brief, a format, and a style.

#### `VIEW-02`
The system shall stamp every rendered view with the record version and the
audience it was rendered for.

#### `VIEW-03`
The system shall give a view facts only through citation, so every fact a view
states is tied to the row it came from.

#### `VIEW-04`
If a view states a number that none of the rows it cites holds, then the system
shall fail the render.

#### `VIEW-05`
When a view needs a fact the record doesn't hold as of its version, the system
shall fail the render and name the missing fact.

#### `VIEW-06`
When the same version, brief, format, and style are rendered again, the system
shall produce a view stating the same facts.

#### `VIEW-07`
When the same record is rendered for several audiences, the system shall render
every view from the same version unless a version is requested for one.

#### `VIEW-08`
Before a view is written, the system shall vet each fact it will state: that its
basis is firsthand and was read, that its certainty matches how it is known, and
that it agrees with the other facts the view states. It shall confirm against a
primary source each fact the bottom line, a breaking change, or a reader's next
action rests on, and record what the vetting changes before rendering.

#### `VIEW-09`
The system shall keep saved views apart from the record's rows, in the record's
`views/` directory, so deleting every view loses no fact.

#### `VIEW-10`
When a view is saved, the system shall log the render with every input it came
from: the record version, the brief and a digest of the brief as resolved with
its framing rules, the style and a digest of its files, the format, and the
visibility.

#### `VIEW-11`
If a view is saved before its check passes, then the system shall refuse to
save it.

#### `VIEW-12`
When a view is saved at a version that already has a different render of it,
the system shall keep both rather than replace the earlier one.

#### `VIEW-13`
When a view is published, the system shall log where it went, when, and which
saved render it was, so the published text is what drift is measured against
(`DRIFT-01`).

#### `VIEW-14`
When asked for a record's views, the system shall report each view's latest
render and why it is stale: each cited fact that has changed since its version,
and whether its brief or style has changed since it was saved.

### `COMM`
Communication style: how a view reads

#### `COMM-01`
The system shall open every view with the bottom line its brief defines, before
any detail, citing the facts it rests on.

#### `COMM-02`
Where a view leaves out facts another view of the same record carries, the
system shall say what it leaves out and link the view to that other view.

#### `COMM-03`
The system shall state each fact's certainty in the terms its brief sets for
the audience: the basis beside the claim for a reader who checks it, a label
for a reader who acts on it.

#### `COMM-04`
Where a brief sets a framing rule (a blameless rewrite, a plain-words
vocabulary), the system shall apply it to every view rendered from that brief.

### `BRIEF`
Audience briefs

#### `BRIEF-01`
The system shall describe each audience in a brief that states who reads the
view, the visibility it is published at, what they need from it, the bottom
line it opens with, its tone and verbosity, and what it leaves out.

#### `BRIEF-02`
The system shall keep briefs as files reviewed and versioned with the schema.

### `CITE`
Citations in a view

#### `CITE-01`
The system shall mark every rendered fact with the key of the fact it came from,
in a form a script can read.

#### `CITE-02`
Where a reader asks to see a view's sources, the system shall show, for any
cited fact, its row, when it was recorded, its certainty, and its basis.

### `CHECK`
Checking a view

#### `CHECK-01`
The system shall check that every number a reader can see in a view sits inside
a citation.

#### `CHECK-02`
The system shall check that every citation in a view resolves to the row the
view used, as of the view's version.

#### `CHECK-03`
The system shall check that views rendered from the same version resolve every
fact they share to the same row.

#### `CHECK-04`
If any check fails, then the system shall refuse to publish the view and report
each failure with the view and the text that failed.

#### `CHECK-05`
When a view is published, the system shall have checked it at the version it is
stamped with.

#### `CHECK-06`
When a view is checked, the system shall report how the facts it cites are
known (measured, observed, inferred) and name the inferred ones, since a passing
check shows the view matches the record, not that the record is right.

### `ACCESS`
Who may read a fact: a view is no wider than its narrowest fact

#### `ACCESS-01`
The system shall let a row carry the fact's visibility, and shall record a row
whether or not its visibility is known.

#### `ACCESS-02`
When a row is recorded without a visibility, the system shall give it the
visibility of its fact's previous row.

#### `ACCESS-03`
The system shall stamp every view with its visibility, which is the brief's
unless the user names where the view is published.

#### `ACCESS-04`
Before a view is written, the system shall judge each fact it will state
against the view's visibility, from the fact's visibility, its basis, and its
fields.

#### `ACCESS-05`
If the system is unsure whether a fact may be read at the view's visibility,
then it shall ask the user to classify the fact and record the answer as the
fact's visibility.

#### `ACCESS-06`
If a fact is narrower than the view's visibility, then the system shall leave
it out of the view and report it, unless the user narrows the view's
visibility instead.

#### `ACCESS-07`
If a view cites a fact whose visibility is narrower than the view's stamped
visibility, then the system shall fail the check.

#### `ACCESS-08`
Before a view is published, the system shall compare who can read the
destination with the view's visibility, and ask the user when the destination
is wider.

#### `ACCESS-09`
If evidence holds a secret value (a token, a password, a key), then the system
shall record the secret by its name in its store and never the value.

### `FORMAT`
Formats

#### `FORMAT-01`
The system shall render each view first as HTML, the form its checks read, and
derive every other format from the checked HTML.

#### `FORMAT-02`
If a page stamped as a view is printed to PDF before its check passes, then the
system shall refuse to print it.

#### `FORMAT-03`
When a page is printed to PDF, the system shall fit it to one US Letter page by
default, at the largest scale between 75% and 100% that fits.

#### `FORMAT-04`
If a view does not fit its page budget, then the system shall render a shorter
view from the same record version with a shorter brief, rather than condensing
the view's text.

#### `FORMAT-05`
When a page is printed to PDF, the system shall keep every link its readers can
open.

#### `FORMAT-06`
Where a Markdown page is published on a site that renders its inline HTML, the
system shall accept the page itself as the view, stamped and cited in inline
HTML and checked as written, so no copy outside the check reaches readers.

#### `FORMAT-07`
When a view is wanted as a message, the system shall convert it from the
checked HTML view, carrying each fact as the view states it and no fact the view
doesn't.

#### `FORMAT-08`
If a stamped view is converted to a message before its check passes, then the
system shall refuse to convert it.

#### `FORMAT-09`
The system shall convert to each message format with one converter, whether the
source is a view or what the session said (`CHAT-01`), so a message is held to
the same rules whichever it came from.

#### `FORMAT-10`
When a message is converted from a view, the system shall end it with the view's
record version and audience, and with a link to the full view where one is
published somewhere the message's readers can open, so a reader can trace what
it states.

#### `FORMAT-11`
When a view is converted to an email, the system shall take the subject from the
view's bottom line, write the body in the style named (rich text a mail client
renders, or plain text), show the subject, and copy the body to the clipboard in
that style.

#### `FORMAT-12`
If a message holds a value shaped like a secret or a path under a home
directory, then the system shall refuse to copy it and name each line.

### `PROOF`
Ruling on a claim

#### `PROOF-01`
When the user asks whether a claim holds, the system shall rule it true, false,
partly true, or undetermined, and state the certainty of the ruling separately
from the verdict.

#### `PROOF-02`
The system shall cite, for each claim it rules on, the primary datum the ruling
rests on (a line of source, a test's output, a quoted passage), not a source's
summary of it.

#### `PROOF-03`
Where the session keeps a record and the claim is about the work, the system
shall record the ruling, and record a false fact's correction as a new row of
its key.

#### `PROOF-04`
The system shall use one method to record a fact's certainty, vet a fact before
rendering it, and rule on a claim, so the three mean the same thing by
`measured`, `observed`, and `inferred`.

### `REWRITE`
Rewriting a reply the reader couldn't read

#### `REWRITE-01`
When the user asks for a rewrite of the last reply, the system shall replace it
with the same facts in the modes named (`wat` unintelligible, `wall` too long,
`eli` too advanced, `ste` too complex), or in the modes it diagnoses when none
is named.

#### `REWRITE-02`
The system shall keep every fact the reply stated. Where a length the user asked
for can't be met otherwise, it shall name each fact it dropped.

#### `REWRITE-03`
Where the unreadable text was written to files, the system shall edit those
files in place rather than summarizing them in the reply.

#### `REWRITE-04`
The system shall define each writing style once, so a brief's framing rule and a
rewrite mode of the same name apply the same rules.

### `CHAT`
Chat posts: `CHAT-01` to `CHAT-04` cover a post made from what the session said;
the rest cover every chat post, one converted from a view included (`FORMAT-09`)

#### `CHAT-01`
When the user asks to share something in a chat channel, the system shall take
the previous reply as the source, unless the user names another source:
something said earlier, pasted text, or the session's transcript.

#### `CHAT-02`
If the user asks for the session's transcript and the range is not evident or
spans a long scrollback, then the system shall ask which range to share before
writing it.

#### `CHAT-03`
Where the source is a transcript, the system shall keep every turn and its
wording and change only the markup, quoting each prompt without the terminal's
prompt marker.

#### `CHAT-04`
If the source's text was cut off, then the system shall mark each gap rather
than reconstruct the missing text.

#### `CHAT-05`
Before a post is copied, the system shall judge each item it carries against
the destination's visibility as a view's facts are judged (`ACCESS-04` to
`ACCESS-06`), withhold any item narrower than the destination or any path on the
user's machine, never carry a secret value, and name each withheld item to the
user.

#### `CHAT-06`
If a draft holds a line the chat engine can't render (in Slack, a table row
outside a code block), then the system shall refuse to copy it and name each
line, as it refuses a secret or a home-directory path in any message
(`FORMAT-12`).

#### `CHAT-07`
When a post is ready, the system shall copy it to the clipboard in the chat
engine's markup and show it as the exact text copied.

#### `CHAT-08`
The system shall write every link in the form the chat engine's composer keeps
on a paste, and rewrite any link written in a form only the engine's API
accepts before copying (in Slack, `[text](url)` is kept, and `<url|text>` or
`<url>` is rewritten).

### `DRIFT`
Views edited by hand

#### `DRIFT-01`
If a published view's text differs from the text the system published, then the
system shall report the edit as drift, since a rendered view's wording can vary
between renders and only an edit after publishing is drift.

#### `DRIFT-02`
When drift carries a fact the record lacks, the system shall offer to record the
fact and render again.
