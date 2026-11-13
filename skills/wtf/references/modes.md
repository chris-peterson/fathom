# The four modes

One section per mode for `wat` and `wall`; `eli` and `ste` are fathom's framing rules, defined once so a rewrite and a view mean the same thing by them. Read the one you picked — each carries the remedy, a worked before/after, and the specific way that remedy loses content while it rewrites.

That last part is the reason these sections exist rather than a one-line instruction each. Every remedy has a characteristic failure, and it's the failure the user cannot catch: they asked for readable, so they have no way to see what stopped arriving. Knowing your mode's failure ahead of the edit is what keeps the rewrite honest.

## wat

Also `?`. **The defect:** unintelligible. A referent with no antecedent, an unglossed term, the subject buried behind three clauses. The reader can't tell what you're even talking about.

**The remedy:** name the thing, then say what happened to it. Concrete nouns, one clause each. Prefer a repeated noun over a pronoun — "the handler" twice beats "it" twice pointing at different things.

**Loses content by over-explaining.** The instinct on "I don't follow" is to add, and adding is how you hand back a wall of text in answer to a complaint about clarity. Replace the unclear sentence; don't append a gloss to it.

> Before: The handler wasn't idempotent so it was retrying against the stale cursor, which is why it showed up twice.
>
> After: Duplicate rows came from the webhook handler. A retry re-read the same cursor position, so it processed the same event twice. Fixed by keying on the event id.

Three "it"s in the original point at three different things, and the subject of the complaint — duplicate rows — never appears until the end.

## wall

**The defect:** wrong volume and shape. Prose carrying what was a list, no conclusion up front, process narrated instead of result stated.

**The remedy:** lead with the answer ([BLUF](https://en.wikipedia.org/wiki/BLUF_%28communication%29)). Then give the content its own shape — a table when items have per-item attributes, bullets when they don't. Cut whatever isn't the answer or needed to act on it.

**Loses content by dropping the caveat** that made the answer conditional. It's the first thing to look cuttable and the most expensive to lose, because its absence reads as certainty you don't have. Demote it to a line under the answer; don't drop it.

> Before: I went through the config and checked each of the environment files, and after comparing them I found that there are differences in a few places — staging has DEBUG set to true whereas production has it false, staging points at the replica database but production points at the primary, and the timeout is 30 seconds in staging versus 5 in production.
>
> After: Three settings differ:
>
> | Setting | staging | production |
> |---|---|---|
> | `DEBUG` | true | false |
> | database | replica | primary |
> | timeout | 30s | 5s |

The first clause is pure process ("I went through", "after comparing"), and a three-row table was dissolved into one sentence.

## eli

**The defect:** wrong altitude. Defined in `${CLAUDE_PLUGIN_ROOT}/kinds/base/framing/eli.md`: the remedy, a worked before/after, and how it loses content. Read it before you write.

## ste

**The defect:** language complexity. Defined in `${CLAUDE_PLUGIN_ROOT}/kinds/base/framing/ste.md`: the ASD-STE100 rules, a worked before/after, and why technical names stay. `ste` is neither `eli` nor `wall`; its closing section says why, worth reading before you pair it with either.
