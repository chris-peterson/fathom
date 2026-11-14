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

Three commands work on a single reply. When you doubt what Claude just said,
`/fathom:proof` rules it true or false with the evidence and how well it is
known, using the same method `/fathom:render` vets a view's facts with. When the
session keeps a record, the ruling goes into it.

When you can't read what Claude just said, `/fathom:wtf` rewrites it as the same facts in a shape you can read:
shorter (`wall`), clearer (`wat`), from the ground up (`eli`), or in Simplified
Technical English (`ste`). `eli` and `ste` are the framing rules briefs use, so
"explain it plainly" means one thing in a reply and in a view.

To share what Claude just said, `/fathom:slack` rewrites it for a channel reader
and copies it in Slack's markup; ask for `transcript` to share the exchange
itself. Like a view, a post is judged against who can read the channel: what
its source's readers couldn't see is withheld, and a secret never goes out.

## Kinds of work

A **kind** says what facts a record can hold and who reads about it. fathom
ships `base`, which fits any work, and `incident`, which adds causes, impact,
and a blameless postmortem. A team adds its own kind for its own tools and
templates; see [Extending](/extending).

## The CLI

The skills drive `scripts/fathom`, which you can also run yourself. It needs
[uv](https://docs.astral.sh/uv/).

```bash
scripts/fathom init <name> --kind incident --title "<title>"
scripts/fathom kind <name>              # fact types, briefs, sources
echo '<row as YAML>' | scripts/fathom add <name>
scripts/fathom show <name>
scripts/fathom brief --record <name> status
scripts/fathom check <view.html> --record <name>
scripts/fathom save <view.html> --record <name>
scripts/fathom views <name>             # each view, and what has moved since it was rendered
```

A record keeps its facts in `record.jsonl` and what was rendered from them in
`views/`. Each saved view is logged with the record version, brief, and style
it came from, so `views` can tell you which documents are stale and why.

A bare name like `checkout-outage` is a record in `.fathom/checkout-outage/` at
the root of the repo you're in. `init` makes git ignore `.fathom/`, so records
stay out of commits until you add one on purpose (`git add -f`). Pass a path
instead to keep a record anywhere else.

`scripts/fathom --help` documents every subcommand and exit code. The behavior
each one promises is in the [Requirements](/spec).
