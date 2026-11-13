# Changelog

## 0.2.0

### Added

- **A `release` kind for announcing what a release shipped.** Its records hold each tool (new, released, or archived, with the job it helps with), each change a user would notice with whether it breaks, and the plans after the release on a rough timeline. Its `announcement` brief opens with what kind of release it is and what an existing user must do before upgrading, then cards for new tools, the major releases with breaking changes first, and the plans as a timeline. `sources.md` covers where release evidence comes from, including why a version is checked against its tag rather than a checkout.
- **A Markdown page can be the checked view.** On a site that renders inline HTML, such as docsify, `/fathom:render` writes the page itself with its stamps as `<meta>` tags and each fact in an element carrying `data-fact`, and `fathom check` reads the `.md` as written, so the file readers get is the one that passed.
- **`/fathom:proof` rules a claim true or false, with the evidence.** Ask "are you sure?" of the last reply, or name a claim, and it shows what the ruling rests on and how well each source is known. It weighs evidence by the same method `/fathom:render` vets a view's facts with, and when the session keeps a record, the ruling goes into it. It moves here from a private skill library.
- **`/fathom:wtf` rewrites the last reply so you can read it.** Name what was wrong (`wat` unintelligible, `wall` too long, `eli` too advanced, `ste` for Simplified Technical English) or let it diagnose, and add a percentage to cut the length. `eli` and `ste` are also framings a brief can name, so a rewrite and a view mean the same thing by "explain it plainly". It moves here from a private skill library.
- **A `how-to` brief and style for a procedure the reader follows**, such as an upgrade, a recovery, or a setup, one action per step, laid out the way popular how-to sites do.
- **`/fathom:slack` shares what the session said in Slack.** By default it rewrites the last reply for a channel reader. Ask for `transcript` to share the exchange itself: each prompt becomes a quote, tables become code blocks, and text the source cut off is marked rather than guessed. Before copying, it judges the post against who can read the channel, the way a view is judged: it withholds anything whose source had narrower readers, and any path on your machine, and never carries a secret. It moves here from a private skill library.

### Changed

- **A record named by a bare name lives in `.fathom/` at the repo root and stays out of commits.** `fathom init checkout-outage` makes `.fathom/checkout-outage/`, and `.fathom/` is git-ignored, so a record reaches a commit only when someone adds it on purpose. A record started elsewhere under a bare name is now reached by its path, such as `./checkout-outage`.

- **`/fathom:pdf` suggests one argument as you type, `[what to print]`.** The paper, page, and style options still work in your own words.
- **`/fathom:render` vets the facts before it writes the view.** A passing `fathom check` only shows the view says what the record says, so the render now checks the record too: that each fact's source is firsthand and was actually read, that a count or summary is marked `inferred` rather than `observed`, and that no two facts in the view contradict each other. Anything the bottom line, a breaking change, or a reader's next step rests on is confirmed against its primary source first. What the vetting corrects lands in the record, and the report says how many facts were confirmed and how many stay secondhand.
- **`fathom check` says how the cited facts are known**: a second line counts them as measured, observed, and inferred, and names the inferred ones.

### Fixed

- **A kind whose enum lists a bare `yes` or `no` is refused with the field named.** YAML reads those as booleans, so no row could match, and the error for the first row crashed instead of saying why. Quote the values.

## 0.1.0

### Added

- **`/fathom:record` keeps the facts of a piece of work in one versioned record.** Drop in evidence (a log export, a chat transcript, an audit trail) and it records each new fact with how it is known and what it rests on. A changed fact gets a new row and the old one stays, and evidence that contradicts a recorded fact is named before it is recorded.
- **`/fathom:render` writes a document for one reader from the record.** Each reader's brief sets the bottom line, the tone, the depth, and what to leave out. Every fact in the view cites the record, the view is stamped with the record version it came from, and `fathom check` fails any number the cited facts don't hold.
- **`/fathom:pdf` prints a view for readers outside Claude**, on one US Letter page by default. It refuses a view that fails `fathom check`.
- **Two kinds of work ship with fathom:** `base`, which fits any work, and `incident`, which adds causes, impact, and a blameless postmortem. A team adds or extends a kind from its own directory through `FATHOM_KINDS`.
- **The `fathom` CLI** starts a record, adds rows, reads the record as of any version, and checks a rendered view. It runs with uv and needs no install.
- **Docs at [chris-peterson.github.io/fathom](https://chris-peterson.github.io/fathom/).**
