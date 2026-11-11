---
name: record
description: This skill should be used when the user is gathering the facts of a piece of work (an incident, an investigation, a migration, a test campaign) and wants them kept in one place every document can be rendered from, such as "/fathom:record", "start a record for this incident", "add this to the record", "here's the audit log export", "what does this change in the timeline", "keep track of what we know", or when the user pastes a blob of evidence (a log export, a chat transcript, an API dump) into a session that already has a fathom record. Extracts what's new, records each fact with its certainty and basis, and surfaces contradictions instead of silently revising.
argument-hint: "[<record dir>] [--kind <kind>] | <evidence to add>"
---

# Record

Keep the facts of a piece of work in one versioned record while the work
happens, before anyone knows which documents will be needed. Every document
later renders from this record (`/fathom:render`), so a fact that never reaches
the record never reaches a reader. The idea and its principles are in the
plugin's `docs/principles.md`.

Run the CLI as `${CLAUDE_PLUGIN_ROOT}/scripts/fathom`, written `fathom` below;
`fathom --help` documents every subcommand and exit code.

## 1. Find or start the record

A record is a directory holding `fathom.yml` (its kind and title) and
`record.yml` (its rows). Look for one the session already uses. Otherwise ask
where it should live once, then start it:

```bash
fathom init <dir> --kind <kind> --title "<title>"
```

Put it beside the work: a branch of the repo the change lives in, or a folder
the team already shares. The record is the durable artifact; views are
disposable.

Pick the kind from the work: `fathom kind --name <kind>` shows a kind's fact
types, briefs, and sources. `base` fits any work; `incident` extends it for
outages. A team's own kinds come first through `FATHOM_KINDS` (see
`docs/extending.md`). Read the kind's `sources.md` files, which `fathom kind`
lists, before gathering evidence.

## 2. Incorporate, don't restate

The value of a record kept through a session is that the user can drop in a raw
blob (a transcript, an API dump, an audit-log export, a hallway summary) and ask
a narrow question without re-establishing context. For each blob:

1. **Extract what's new.** Read `fathom show <dir>` first, and compare.
2. **Record it.** One row per fact (step 3), written in one `fathom add` call.
3. **Answer the narrow question** with the new facts in place.

Don't ask the user where a fact fits; work it out from the record. Don't
re-summarize what the record already holds; report what changed, what is now
more precise, and what is newly evidenced.

**When new data contradicts a recorded fact, say so before recording it.** An
identifier that doesn't match a recorded wildcard, an audit timestamp an hour
off a recorded event: name the fact key, both values, and both sources, then
record the correction as a new row of the same key with a basis that explains
it. The record keeps both rows, and the user learns which views it changes. A
silent revision corrupts the record the user relies on.

## 3. Write rows

`fathom add <dir>` reads YAML (or JSON) rows from stdin, validates all of them
against the kind's schema, and appends them all or none. Each row:

```yaml
- key: <kebab-case name for the fact, stable across corrections>
  type: <a fact type from the kind's schema>
  certainty: <measured | observed | inferred>
  basis: <the record or reasoning the fact rests on>
  fields: {<field>: <value>, ...}
```

| Certainty | Means | Basis names |
| --- | --- | --- |
| `measured` | A reproduction or a direct measurement | the measurement and how it was taken |
| `observed` | Records from the work itself | the record: the audit event, the log line, the job |
| `inferred` | Timing or a pattern | the reasoning; put what would confirm it in the claim's `confirm-by` |

Certainty says how the fact is known, not how plausible it is.

Rules the schema enforces, so a refusal explains itself: keys are kebab-case and
keep their type; timestamps carry a UTC offset; text fields hold Markdown inline
at most (code, bold, links), never HTML, since presentation belongs to views.

Rules the schema can't enforce:

- **Record numbers a view will state.** A duration, a percentage, a count, a
  difference between two timestamps: if a reader will see it, it's a `measure`
  row. A view can't compute it, and `fathom check` fails a number no cited row
  holds.
- **Keep precise identifiers precise.** Once a version, tag, or ID is pinned,
  record it exactly; don't generalize it back to a wildcard.
- **Record names under every alias.** An `entity` row's `ids` map holds each
  name sources use for the thing (instance ID, host name, IP, log host). This is
  the identifier map every timeline needs.
- **Retract rather than delete.** A fact found false gets a row with
  `retracted: true` and a basis saying why. Views as of later versions drop it;
  views as of earlier ones still render it, stamped with their version.

## 4. Climb the fidelity ladder

Evidence arrives at different precisions. For each precise-sounding fact ("at
18:13:36 the job pruned 42 records"), ask what the actual source is, and reach
for the next rung when the fact outpaces its evidence. The ladder, the
practices that make a timeline hold up, and the boundary on touching production
systems are in **`references/evidence.md`**. Read it before gathering evidence
for a timeline.

## 5. Report

After each `fathom add`, report the version it reached (`v<N>`), the keys added
or corrected, any contradiction surfaced, and any `inferred` fact on the causal
chain with what would confirm it. Offer `/fathom:render` when a reader is
waiting on a document.

## Additional resources

- **`references/evidence.md`**: the fidelity ladder, timeline practices, and
  the production-systems boundary.
- **`${CLAUDE_PLUGIN_ROOT}/docs/extending.md`**: adding a kind, or extending one
  with a team's own sources and briefs.
