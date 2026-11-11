# fathom

**fathom:** one record of facts, rendered for each reader.

A Claude Code plugin in the [bridge.ai](https://chris-peterson.github.io/claude-marketplace/)
suite. It keeps the facts of a piece of work (an incident, an investigation) in
one versioned record, and renders each document from it: an analysis for
engineers, a brief for managers, an explainer for everyone else. A rendered document is a
view. It can be thrown away and regenerated in another format, style, or depth,
and every view rendered from the same version of the record agrees with every
other.

- [docs/principles.md](docs/principles.md): the idea, and the patterns it shares
  with MVC, React, data binding, and event sourcing.
- [SPEC.md](SPEC.md): the requirements, the source of record for behavior.
- [docs/extending.md](docs/extending.md): adding a kind of work, or extending
  one with a team's own sources and briefs.

## Getting started

```bash
scripts/fathom init <dir> --kind incident --title "<title>"
scripts/fathom kind <dir>              # fact types, briefs, sources
echo '<row as YAML>' | scripts/fathom add <dir>
scripts/fathom show <dir>
scripts/fathom brief --record <dir> status
scripts/fathom check <view.html> --record <dir>
```

The CLI runs with [uv](https://docs.astral.sh/uv/). In Claude Code,
`/fathom:record` gathers facts, `/fathom:render` writes a view for one reader,
and `/fathom:pdf` prints a view for readers outside Claude.

## Status

Early. The record, kinds, briefs, and the view check are in place; drift
detection (`DRIFT-*`) and a plugin manifest are not yet.
