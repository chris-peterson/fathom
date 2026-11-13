# Verifying a claim

fathom checks claims in three places, and this guide is the one method all
three use:

- `/fathom:record` writes each fact with how it is known.
- `/fathom:render` vets every fact a view will state before writing it.
- `/fathom:proof` rules a claim true or false when someone asks "are you sure?"

`fathom check` is not one of them. It proves a view says what the record says,
not that the record is right. The record is right only when its facts were
verified the way this guide describes.

## How a claim is known

A claim's certainty says how it is known, not how plausible it is. The record's
`certainty` field and `/fathom:proof`'s confidence rating are the same scale:

| Certainty | Proof confidence | Means | The basis names |
| --- | --- | --- | --- |
| `measured` | High | A reproduction, a run, or a direct measurement: tests that cover the path and pass, a command whose output shows it | the measurement and how it was taken |
| `observed` | Medium | The work's own record, read: the source file at a line, the audit event, the log line, the shipped package | the record, specifically enough to open it again |
| `inferred` | Low | Timing, a pattern, general knowledge, or memory | the reasoning, and what would confirm it (`confirm-by`) |

A plausible explanation is the dangerous one: it reads as known, so nobody
checks it, and the next decision is built on it. When the data can't be
reached, say so: "my guess is X, but I haven't checked it." Then the claim is
`inferred`, and says what would confirm it.

**Never write "verified", "confirmed", or "checked" for something you only
believe.** Saying a check happened stops the reader from doubting it, so run the
check before claiming it.

**A hedge covers its own sentence and nothing after it.** "My read is X,
so change Y" is an unverified claim driving an action. Verify the premise, or
state the action as blocked on the check that would settle it.

## Where the evidence comes from

Find the strongest evidence for each claim, and spend the most effort on the
claims that matter most: the one a conclusion rests on, a breaking change, a
command the reader will run.

1. **Ask the thing about itself first.** Before reasoning about whether
   something is maintained, current, or supported, read what it says about
   itself: its README, its package metadata, the comment at the top of the
   file. It is the cheapest primary source and the one most often skipped.
2. **The shipped artifact outranks the documentation about it.** To settle what
   software does or ships, go one level below the docs: unpack the package and
   list its files, read the unit file, check what the installer writes.
3. **Read state off the thing, not off the process meant to change it.** A
   pipeline's status, a merge, or a config default describes what was intended.
   The running system describes what is.
4. **Cite the primary datum, not a source's conclusion.** Record the quoted doc
   line, the `file:line`, the command's literal output. A web fetch's answer is
   itself a summary; for a claim that matters, read the passage it summarized.
5. **When a source's summary contradicts the data it cites, trust the data**,
   and say the source contradicts itself. Don't pick one quietly.
6. **A fallback is the cheapest claim to test, so test it.** "An empty config
   falls back to the default" is asserted from the API's shape because the
   degraded input is never the one in front of you. Build it and look.

When no evidence exists, say so. Never invent a source.

## Vetting a fact before a reader acts on it

Recording stays fast on purpose, so a fact can arrive secondhand, with a basis
nobody opened, or at a certainty it didn't earn. Before a view states a fact,
or a reply builds on one, run these checks:

| Check | It fails when | Do |
| --- | --- | --- |
| **Firsthand** | The basis is another document about the work (an earlier view, a post, a summary, a slide) rather than the work's own record | Open what that document drew on, and record the fact again with that basis. A plan or an opinion stays secondhand; say whose it is |
| **Read** | The basis names a file, page, or command nobody in the session opened | Open it now. When it doesn't say what the fact says, record the correction the way `/fathom:record` treats a contradiction |
| **Earned** | A count, summary, or comparison of other facts is marked `observed` | Record it again as `inferred`, naming the facts it rests on in `confirm-by` |
| **Consistent** | Two facts can't both hold: an absolute claim beside its own exception, two values for one thing | Name both keys, both values, and both bases, then record the resolution. Don't pick one quietly |
| **Confirmed** | A fact the bottom line rests on, a breaking change, or a command the reader will run is only secondhand or inferred | Confirm it against the primary source (the tag, the release page, the code, a reproduction) and record it again with that basis, as `measured` when you reproduced it |

**A mechanical pass inherits every claim it edits.** Reformatting, renaming, or
condensing changes a line without reading it for meaning, so a false claim
comes back better worded and still false. When a pass crosses a sentence that
says how something behaves, check it before moving on.

## Ruling on a claim

Two judgments, kept apart. The **verdict** answers "is the claim true?" The
**certainty** answers "how strong is the evidence behind that ruling?" A claim
can be false at `measured` certainty: that is a thorough refutation, not a
failed check.

| Verdict | Means |
| --- | --- |
| 🟢 **TRUE** | The claim holds as stated |
| 🔴 **FALSE** | The claim is wrong as stated |
| 🟡 **PARTLY TRUE** | Right in direction, wrong in a detail that matters; say which half is which |
| ⚪ **UNDETERMINED** | No evidence either way. The only verdict that means the claim couldn't be checked |

- **Rule on the claim as it was stated**, not on your correction of it. "There
  is no way to do X" is FALSE when a way exists.
- **One headline verdict**, on the claim the conclusion rested on. Don't average
  a refutation and three confirmations into a hedge.
- **When a conclusion rested on a refuted claim, say so.** A FALSE
  on the premise of an argument changes the argument's conclusion; follow it
  through. Refuting your own reasoning is the valuable outcome, not a failure.
