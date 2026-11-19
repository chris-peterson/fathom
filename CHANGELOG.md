# Changelog

## Unreleased

### Breaking

- **A record is now `record.jsonl`, one row per line, with the kind and title in its first row.** `fathom.yml` and `record.yml` are no longer read, and there is no converter: start a new record, or rewrite an old one's rows as JSON lines after a row 0 of `{"seq": 0, "record": {"kind": "<kind>", "title": "<title>"}}`.

### Added

- **A `session` kind keeps a record per tack.** When tack binds a session to a tack, fathom starts `<route>/<tack>` and asks Claude to record only where the work stands (the goal, outcomes, decisions, open actions), never the path. `/goal` updates the record's goal. On `/tack:end`, before the retrospective, it revises the lede and renders the `recap` brief as a polished page, published as an artifact, with a PDF and a link from the retro on offer. tack needs no change: fathom watches for it.
- **`fathom metrics` says what fathom costs**: CLI time from a log every run writes, and, from a session's transcript, the output spent writing fathom calls, the context their results added and how often it was re-read, and each hook's runs and duration.
- **`/fathom:compact` prunes a record, with your say-so.** It finds facts that are wrong, duplicated, or no longer relevant, groups them by theme, and asks about each theme with what it would cost: the saved views that cite those facts, the briefs that need them, and whether the lede rests on them. Only what you confirm is retracted, and only by appending rows, so every earlier version and every view stamped with one is unchanged. When Claude Code compacts the conversation, fathom asks the summary to carry the reasoning behind each record this session wrote, then starts the pass on exactly those records.
- **Facts can say how they bear on each other.** A fact names what it `supersedes`, `contradicts`, or `corroborates`. `show` prints both directions, a lede resting on a superseded or contradicted fact goes stale, `fathom check` names any cited fact in either state, and `fathom compact` offers each superseded group as one theme. An open contradiction now stays in the record instead of living only in the conversation.
- **A retraction says why**: `reason: wrong | duplicate | irrelevant`, so superseded history isn't later read as a fact found false.
- **`fathom show --cited`** lists the saved views citing each fact: what retracting it would make stale.
- **A record can be named `<route>/<tack>`**, as tack names a unit of work, and lives at `.fathom/<route>/<tack>/`.
- **`fathom touched`** lists the records a Claude session wrote, from a ledger fathom keeps outside the records.
- **A record keeps its own bottom line, the lede.** One `lede` fact states where the work stands, resting on named facts, and `/fathom:record` revises it out loud whenever new facts move it ("lede: X → Y, because Z"). `fathom show` leads with it and marks it stale when a fact it rests on changes; `fathom add` refuses a lede that isn't inferred, rests on a fact the record doesn't hold, or states a number those facts don't. Every view opens with the lede reframed for its reader, so a one-page status and a long analysis start from the same conclusion.
- **A `code` field type holds verbatim source**: a diff, a config file, a command's output. Unlike `text`, it may contain `<`, so an XML or HTML diff can be recorded exactly; views escape it.
- **Views are kept apart from the facts, with the inputs they came from.** `fathom save` checks a view and keeps it in the record's `views/<name>/v<N>.html`, logging the record version, the brief and style it was rendered with, and the visibility. A re-render at the same version sits beside the earlier one instead of replacing it. `/fathom:render` saves every view it writes.
- **`fathom views` says which documents are stale and why**: the cited facts that changed since each view's version, and whether its brief or style changed since.
- **`fathom publish` logs where a view went**, so a hand-edited copy can later be compared with what readers got.
- **`fathom retitle` changes a record's title as a new version**, so a view rendered earlier keeps the title it had.

### Changed

- **`/fathom:pdf` designs a one-pager instead of only fitting it.** It plans the layout around the shape the content already has (a chain as linked cards, a before and after as two columns, counts as a proportion bar) with the `frontend-design` skill, then reviews the preview for lopsided columns, labels or code lines that wrap, empty regions, and weak hierarchy, rendering again until the page reads well. fathom now depends on the `frontend-design` plugin from `claude-plugins-official`, which installs with it.

### Fixed

- **Concurrent writes to one record no longer share a version.** `add`, `classify`, and `retitle` hold a lock on the record while they read its version and append, so two sessions, a hook, and a background agent can write to one record at once.
- **`fathom save` no longer loses a render.** A brief with invalid front matter made `save` copy the view and then stop with a traceback before logging it, and every later save reported the copy as "already saved", so `views` and `publish` never saw the render. `save` now settles everything it logs before writing anything, and logs a render an earlier save left unlogged. An invalid brief is reported in one line with its file, line, and column, and `fathom kind` lists every broken brief.
- **`/fathom:pdf` prints the view `fathom save` just wrote.** A re-save at the same record version lands beside the original as `v<N>-2.html`, and printing `v<N>.html` printed the earlier layout.

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
