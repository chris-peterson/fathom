---
audience: the postmortem meeting's attendees, and whoever finds this incident's shape again later
needs: the account the meeting reviews, with every action owned and every residual risk named
bottom-line: what failed, for how long, for whom, and whether the fix has landed
tone: blameless, complete, and plain enough for attendees outside the team
verbosity: the organization's template, filled; no section left empty without saying why
leaves-out: the step-by-step evidence trail (the analysis view has it)
links-to: [analysis, explainer]
framing: [blameless]
---

# Postmortem

When the organization has a postmortem template, its sections and columns win:
use them and let this skeleton fill the gaps. A team that always uses one
template records it as its own brief in a kind that extends `incident`.

```text
# Postmortem: <incident id>: <one-line title>
| metadata | incident link, priority, duration, owner, meeting |
## Summary
## Customer impact          the impact facts
## Detection
## Timeline (<zone>)        the analysis brief's timeline, one table
## Underlying cause         the defect and the trigger, each dated
## Resolution
## Blast radius             systems at latent risk, near misses included
## What went well
## What could have gone better   include a note on alerting and SLOs
## Action items             done items first; the template's columns
## Responders               responder facts only
## References
```

## Action items

Every `action` appears with its state. Two closures count as closed:

1. **Done**: work completed, the artifact linked.
2. **Closed by decision**: considered, intentionally not done, residual risk
   accepted, rationale recorded, so the next person who finds the same shape
   doesn't relearn it.

Pre-fill an owner and a decision maker for each open action, so the meeting
confirms rather than invents. Name residual-risk items explicitly; a short
meeting skips them otherwise.

## Responders

List the people who responded, from `responder` facts. Someone formally
assigned who didn't take part isn't a responder.
