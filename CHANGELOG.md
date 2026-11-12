# Changelog

## 0.1.0

### Added

- **`/fathom:record` keeps the facts of a piece of work in one versioned record.** Drop in evidence (a log export, a chat transcript, an audit trail) and it records each new fact with how it is known and what it rests on. A changed fact gets a new row and the old one stays, and evidence that contradicts a recorded fact is named before it is recorded.
- **`/fathom:render` writes a document for one reader from the record.** Each reader's brief sets the bottom line, the tone, the depth, and what to leave out. Every fact in the view cites the record, the view is stamped with the record version it came from, and `fathom check` fails any number the cited facts don't hold.
- **`/fathom:pdf` prints a view for readers outside Claude**, on one US Letter page by default. It refuses a view that fails `fathom check`.
- **Two kinds of work ship with fathom:** `base`, which fits any work, and `incident`, which adds causes, impact, and a blameless postmortem. A team adds or extends a kind from its own directory through `FATHOM_KINDS`.
- **The `fathom` CLI** starts a record, adds rows, reads the record as of any version, and checks a rendered view. It runs with uv and needs no install.
- **Docs at [chris-peterson.github.io/fathom](https://chris-peterson.github.io/fathom/).**
