---
audience: engineers who will check the reasoning or act on it
needs: what happened, the causal chain, how sure we are of each step, and what to do next
bottom-line: what happened and why, in one sentence, with the mechanism named
tone: precise; identifiers and links wherever a reader would look something up
verbosity: as long as the evidence needs; sections a reader can skip by heading
leaves-out: nothing the record holds that bears on the mechanism
links-to: [status]
framing: []
---

# Analysis

Write for two readers: the top of the page is for anyone, and a section headed
**For engineers** carries the record-level detail.

## Sections, in order

| Section | What it holds |
| --- | --- |
| Summary | One paragraph: what happened, the mechanism in a sentence, where it stands |
| Facts | The window, the scope, and any cause ruled out |
| What happened | A numbered causal chain, one link per step, decisive links highlighted |
| Status | One row per `action`: its state and its link |
| Timeline | The `event` and `gap` facts, one table, one zone |
| How sure we are | Each `claim` on the causal chain with its certainty and basis |
| Options | Each way forward, where it lands, its effect and its cost |

Omit a section the record holds nothing for.

## Timeline

- One table, `Time (<zone>) | Event | Source`, with the zone in the heading.
  Convert each `at` to that zone; the record stores offsets so this is a
  formatting step, not a computation.
- Keep each timestamp on one line: join the time and its AM/PM with a
  non-breaking space.
- **Bold the rows that explain the outcome.** Group rows under phase headings
  when the events carry a `phase`, and give each phase a color with a legend.
- A `gap` is its own row: "no data from `<subject>`, `<start>`–`<end>`".
- Tag a row resting on an `inferred` fact, and give its basis in the Source cell.
- The Source cell links the record itself (the audit event, the log search
  scoped to the minute), never the name of its category.
- Put the identifier map (the `entity` facts' `ids`) in a note above the table.

## How sure we are

| Claim | Certainty | Basis |
| --- | --- | --- |

Certainty says how the claim is known, not how plausible it is. An `inferred`
claim on the causal chain is the first one to confirm; give its `confirm-by`.

Follow the timeline with **What the timeline establishes** and **Open
questions**, kept apart so inference doesn't read as fact.

## Links

Name each `source` fact's retention where it has one ("log links stop
returning rows after 30 days"), so a reader knows when to stop trusting a link.
