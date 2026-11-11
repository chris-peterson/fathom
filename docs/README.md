# <img src="favicon.svg" alt="fathom" width="64" height="64" style="vertical-align: middle"> fathom

**One record of facts, rendered for each reader.**

Engineers write the analysis, someone else writes the explainer, and an hour
later the two disagree on how many times the failure happened. fathom keeps the
facts of a piece of work (an incident, an investigation, a migration) in one
versioned record, and renders every document from it: an analysis for
engineers, a status for managers, an explainer for everyone else. Each document
is a view. It can be thrown away and rendered again, and every view rendered
from the same version of the record agrees with every other.

Why it works this way, and the patterns it shares with MVC, React, and event
sourcing, is in [Principles](/principles).

## How it works

1. **Record.** `/fathom:record` turns evidence you drop into the session (a log
   export, a chat transcript, an audit trail) into facts. Each fact carries how
   it is known (measured, observed, or inferred) and what it rests on. A fact
   that changes gets a new row; the old one stays.
2. **Render.** `/fathom:render` writes a view for one reader, following that
   reader's brief: what they need, the line it opens with, its tone, and what it
   leaves out. Every fact in the view cites the record, and the view is stamped
   with the version it came from.
3. **Check.** Before a view is published, `fathom check` fails any number in it
   that the facts it cites don't hold.
4. **Share.** `/fathom:pdf` prints a view for readers outside Claude, on one page
   by default.

## Kinds of work

A **kind** says what facts a record can hold and who reads about it. fathom
ships `base`, which fits any work, and `incident`, which adds causes, impact,
and a blameless postmortem. A team adds its own kind for its own tools and
templates; see [Extending](/extending).

## The CLI

The skills drive `scripts/fathom`, which you can also run yourself. It needs
[uv](https://docs.astral.sh/uv/).

```bash
scripts/fathom init <dir> --kind incident --title "<title>"
scripts/fathom kind <dir>              # fact types, briefs, sources
echo '<row as YAML>' | scripts/fathom add <dir>
scripts/fathom show <dir>
scripts/fathom brief --record <dir> status
scripts/fathom check <view.html> --record <dir>
```

`scripts/fathom --help` documents every subcommand and exit code. The behavior
each one promises is in the [Requirements](/spec).
