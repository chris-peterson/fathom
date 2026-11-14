# fathom

**fathom** the facts once; render them for every reader.

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

Using fathom (the skills, the CLI, and kinds) is covered in
[docs/README.md](docs/README.md), the home page of the docs site.

To work on it:

```bash
scripts/fathom --help   # the CLI runs with uv; no install step
just docs               # render the docs site into docs/
just preview-docs       # serve it locally
```

## Status

Early. The record, kinds, briefs, and the view check are in place; drift
detection (`DRIFT-*`), views as chat posts and emails (`FORMAT-07` to
`FORMAT-11`), and a plugin manifest are not yet.
