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
- **version**: a point in the record's history. Reading the record *as of* a
  version gives, for each fact, the latest row recorded at or before it.
- **certainty**: how a fact is known: measured, observed, or inferred.
- **view**: one rendered document: the record as of a version, rendered for an
  audience, in a format and a style.
- **audience brief**: the instructions the renderer follows to turn the record
  into a view, written the way a skill is: who the view is for, what they need
  from it, its tone and verbosity, and what it leaves out.
- **format**: the output medium: a web page, Markdown, a slide deck, a Word
  document, a chat post.
- **style**: the visual treatment within a format.
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
Where a view leaves out facts another view of the same record carries, the
system shall link the view to that other view.

#### `VIEW-08`
When the same record is rendered for several audiences, the system shall render
every view from the same version unless a version is requested for one.

### `BRIEF`
Audience briefs

#### `BRIEF-01`
The system shall describe each audience in a brief that states who reads the
view, what they need from it, its tone and verbosity, and what it leaves out.

#### `BRIEF-02`
The system shall keep briefs as files reviewed and versioned with the schema.

#### `BRIEF-03`
Where a brief sets a framing rule (a blameless rewrite, a plain-words
vocabulary), the system shall apply it to every view rendered from that brief.

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

### `DRIFT`
Views edited by hand

#### `DRIFT-01`
If a published view's text differs from the text the system published, then the
system shall report the edit as drift, since a rendered view's wording can vary
between renders and only an edit after publishing is drift.

#### `DRIFT-02`
When drift carries a fact the record lacks, the system shall offer to record the
fact and render again.
