# <img src="favicon.svg" alt="fathom" width="64" height="64" style="vertical-align: middle"> fathom

**One record of facts, rendered for each reader.**

An outage needs a one-page status for leadership, a root-cause analysis for
the engineers fixing it, a plain-words explainer for the teams it blocked, and
a postmortem for the review meeting. Written by hand, those are four documents
holding four copies of the facts, and within an hour they disagree on how many
times the failure happened.

fathom keeps one **record** per piece of work instead: a named place
(`checkout-outage`) where the facts collect as the work happens, together with
the record's current **lede**, the one statement of where the work stands.
Every document is a **view** rendered from the record for one reader. A view
can be thrown away and rendered again, and every view rendered from the same
version of the record agrees with every other.

## One record, many readers

What changes between views is the reader, so each reader gets a brief that
says how deep to go and what to leave out. The facts and the lede stay the
same. The `incident` kind ships these:

| View | For | Depth | Opens with the lede as |
| --- | --- | --- | --- |
| `status` | managers and planners | one page | the state of the work and the one decision it needs |
| `explainer` | teams whose work was blocked | three scenes, in plain words | the limit, and what crossed it |
| `postmortem` | the review meeting | the organization's template, filled | what failed, for how long, for whom, and whether the fix landed |
| `analysis` | engineers choosing a fix | as long as the evidence needs | the defect and the trigger, named |

Each view says what it leaves out and links to the view that carries it, so
the one-pager's reader is one click from the evidence. A team adds a reader by
writing a brief, not a document; see [Extending](/extending).

Why it works this way, and the patterns it shares with MVC, React, and event
sourcing, is in [Principles](/principles).

## How it works

1. **Record.** `/fathom:record` turns evidence you drop into the session (a log
   export, a chat transcript, an audit trail) into facts. Each fact carries how
   it is known (measured, observed, or inferred) and what it rests on. A fact
   that changes gets a new row; the old one stays.
2. **Keep the lede.** As facts land, `/fathom:record` decides whether they move
   the bottom line, and when they do, revises the lede out loud: the old
   statement, the new one, and why. The lede names the facts it rests on, so
   `fathom show` can tell you when one of them has changed under it.
3. **Render.** `/fathom:render` writes a view for one reader, following that
   reader's brief. It opens with the lede in that reader's terms, cites every
   fact, and is stamped with the record version it came from.
4. **Check.** Before a view is published, `fathom check` fails any number in it
   that the facts it cites don't hold.
5. **Share.** `/fathom:pdf` prints a view for readers outside Claude, on one page
   by default.
6. **Compact.** `/fathom:compact` finds what a record no longer needs (wrong,
   duplicated, or superseded facts), asks you theme by theme, and retracts only
   what you confirm. It runs on its own after Claude Code compacts the
   conversation.

## Kinds of work

A **kind** says what facts a record can hold and who reads about it. fathom
ships `base`, which fits any work, `incident`, which adds causes, impact, and a
blameless postmortem, `release`, for announcing what a release shipped, and
`session`, for a unit of AI-assisted work. A team adds its own kind for its own
tools and templates; see [Extending](/extending).

### With tack

When [tack](https://github.com/chris-peterson/tack) binds a session to a tack,
fathom starts a `session` record named for it (`auth-rewrite/t3`) and keeps
only where the work stands: the goal, what landed, what was decided, what is
left. Never the path; the transcript has that. `/goal` updates the record's
goal, and `/tack:end` renders a one-screen recap before the retrospective, so
the retro can link it. tack needs no change; fathom watches for it.

## The CLI

The skills drive `scripts/fathom`, which you can also run yourself. It needs
[uv](https://docs.astral.sh/uv/).

```bash
scripts/fathom init <name> --kind incident --title "<title>"
echo '<row as YAML>' | scripts/fathom add <name>
scripts/fathom show <name>              # the lede first, then the facts
scripts/fathom history <name> lede      # how the bottom line changed
scripts/fathom brief --record <name> status
scripts/fathom check <view.html> --record <name>
scripts/fathom save <view.html> --record <name>
scripts/fathom views <name>             # each view, and what has moved since it was rendered
scripts/fathom compact <name>           # what a compaction pass can find mechanically
scripts/fathom metrics --transcript <session.jsonl>   # what fathom cost a session
```

A bare name like `checkout-outage` is a record in `.fathom/checkout-outage/` at
the root of the repo you're in. `init` makes git ignore `.fathom/`, so records
stay out of commits until you add one on purpose (`git add -f`). Pass a path
instead to keep a record anywhere else.

A record keeps its facts in `record.jsonl` and what was rendered from them in
`views/`. Each saved view is logged with the record version, brief, and style
it came from, so `views` can tell you which documents are stale and why.

`scripts/fathom --help` documents every subcommand and exit code. The behavior
each one promises is in the [Requirements](/spec).

## Utilities

Three commands work on a single reply rather than a record. They share the
record's methods, so they mean the same things by the same words.

- **[`/fathom:proof`](/skills/proof)** rules a claim true or false, with the
  evidence and how well it is known, using the method `/fathom:render` vets a
  view's facts with. When the session keeps a record, the ruling goes into it.
- **[`/fathom:wtf`](/skills/wtf)** rewrites the last reply as the same facts in
  a shape you can read: shorter (`wall`), clearer (`wat`), from the ground up
  (`eli`), or in Simplified Technical English (`ste`). `eli` and `ste` are the
  framing rules briefs use.
- **[`/fathom:slack`](/skills/slack)** rewrites the last reply for a channel and
  copies it in Slack's markup, or shares the exchange itself (`transcript`).
  Like a view, a post is judged against who can read the channel.
