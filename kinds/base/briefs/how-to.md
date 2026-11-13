---
audience: anyone who has to carry out what the work produced, without having been part of it
visibility: internal
needs: to do the thing (upgrade, recover, set up, verify) correctly the first time, and know when they are done
bottom-line: what the reader will have done when they finish, and the one thing most likely to go wrong
tone: plain words, commands in the active voice
verbosity: one action per step; as many steps as the procedure takes, and no more
leaves-out: why the procedure is this way, the evidence, and the timeline (the analysis view has them)
links-to: [analysis]
framing: [eli, ste]
---

# How-to

A procedure the reader follows, one step at a time. Render it in the `how-to`
style unless the user names another.

1. **Bottom line, as a summary.** Up to three bullets: what the reader ends up
   with, how long it takes when the record holds a `measure` of it, and the
   step most likely to go wrong.
2. **What you need.** The access, tools, and versions the steps assume, each
   from an `entity` or `claim` fact. Leave this out when the steps assume
   nothing.
3. **The steps.** One `action`, `decision`, or `claim` per step, each a single
   command with a bold lead sentence and the detail under it. A command the
   reader runs goes in a code block, copied from the record exactly.
   - Group steps into **parts** when they must all happen in order, and into
     **methods** when the reader picks one (a fresh install or an upgrade).
   - A step that rests on an `inferred` fact carries a warning saying it is
     unconfirmed and what would confirm it.
   - Put a warning before the step it applies to, never after.
4. **How you know it worked.** The check that proves the procedure succeeded,
   as the last step.
5. **Tips, warnings, and questions**, only those the record holds facts for.
