---
audience: engineers choosing a fix, the next on-call, and anyone checking the reasoning
visibility: private
needs: what failed, the mechanism, how sure we are, and which fix to make, before the postmortem exists
bottom-line: what failed and why, in one sentence, naming the defect and the trigger
tone: precise; identifiers and links wherever a reader would look something up
verbosity: as long as the evidence needs; the top half reads without the bottom half
leaves-out: nothing the record holds that bears on the mechanism
links-to: [status, explainer, postmortem]
framing: [blameless]
extends: true
---

# Incident analysis (RCA)

This brief adds what an incident needs to the base analysis brief, which
follows it.

## Facts

The `impact` window and scope, and any cause ruled out ("not the
`<known issue>`").

## Separate the defect from the trigger

Give the `cause` facts their own section: the defect and the trigger, each
dated with `introduced` and linked to its `change`, then the fix. Together they
answer "why now" and "can it happen again", and keep the fix aimed at the
defect.

## Timeline phases

Group the rows under before (normal activity), trigger, degraded, recovery,
and resolution.

## Supporting evidence

Render these when the record holds them:

- **The control.** The same operation on a day it succeeded and on the incident
  day, at the same scale, with the limit that was crossed drawn as a line
  (memory against capacity, latency against a timeout). When two actors
  collided, a two-column timeline with time down the middle shows where they
  overlapped.
- **The pattern the trigger broke.** When the trigger is normally harmless,
  tabulate its earlier occurrences and what followed each, then the one that
  broke the pattern. Their regularity supports an inferred row in the timeline.
- **Earlier occurrences.** A table of past occurrences (date, scope, duration)
  shows whether the problem is new, and whether it is getting worse.

## Fix options

Each option, where it lands, and its effect, including the cost. When cleanup
covers many items, rank them (first, next, low) and state the rule for each
rank.
