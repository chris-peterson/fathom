---
audience: managers, product owners, and teams whose work was blocked, who need the mechanism and not the evidence
visibility: internal
needs: to see what broke and why the fix holds, without knowing the system
bottom-line: the limit and what crossed it, in plain words ("a node has room for two copies; a reload briefly starts a third")
tone: plain words; things named by their role ("the old proxy", "another app deploys"), identifiers only in hover text
verbosity: one screen per scene; three scenes
leaves-out: identifiers, the timeline, the certainty table (the analysis view has them)
links-to: [analysis]
framing: [blameless, eli]
---

# Incident explainer

Show the failing operation as a picture the reader can watch.

## The same operation three times

| Scene | What it shows |
| --- | --- |
| Normal | The operation succeeding, on the same system and at the same scale as the failure |
| Failure | The same operation, plus the one event that broke it |
| Fixed | The same operation after the fix, absorbing that event |

Keep the picture, the scale, and the opening steps identical across scenes, so
the only difference is what differed in production. The normal scene teaches
the picture, which leaves the failure scene one new thing to explain.

## Draw the limit as a container

Draw the resource that ran out as a box sized to its capacity, and each
consumer as a block sized to what it uses, in units the reader knows (MB,
seconds, connections). When the blocks don't fit, draw the overflow outside the
box. Every size comes from a `measure` fact and carries its citation.

## Narrate one step at a time

One sentence per step, with a clock and a running event log. Beside the
picture, show the readings an operator watches (CPU, free memory, health
checks), and turn them red together when the failure lands. Run the clock fast
through long waits. Start each scene when it scrolls into view, give it a
replay button, and step through without animation when the reader prefers
reduced motion. In a print format, render each scene as a strip of its key
steps instead.

## Back each scene with data

| Question | Show |
| --- | --- |
| How likely was the collision? | The spread of the timing that allowed it |
| How bad was it? | Durations of normal and failed runs, side by side |
| How often? | Each occurrence, with its date |

State each sample's size and how it was picked. For the fixed scene, replay a
real run after the fix, preferably the case that failed before it, then state
the worst case the fix has to hold, so the reader sees the fix covers every
case and not only the observed ones.

## Close with sources and links

Name the sources by category and link the analysis view and the fix's change.
