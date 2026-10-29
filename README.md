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

## Status

Design. The principles and the requirements are written; the implementation
starts from a proof of concept that rebuilt an outage's analysis and explainer
from one record and checked every figure in them.
