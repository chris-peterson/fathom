---
name: compact
description: This skill should be used when a fathom record has grown past what its readers need and should be pruned, such as "/fathom:compact", "compact the record", "clean up the record", "prune facts that no longer matter", "these facts are stale, remove them", or when a fathom hook reports that the conversation was compacted and names records to compact. Finds facts that are wrong, duplicated, or no longer relevant, groups them by theme, and retracts only what the user confirms, theme by theme, never on its own judgment.
argument-hint: "[<record name or dir>...]"
---

# Compact

Shrink what a record's current read holds, so every later `show` and render
reads less and states nothing stale. Compaction only appends rows: each dropped
fact gets a retraction with a reason and a basis, so a read as of an earlier
version, and every view stamped with one, still sees what it saw.

**The user decides what goes.** Find candidates, explain each well enough to
judge without scrolling back, and retract only what the user confirms. Even a
fact that looks plainly wrong is put to the user with its evidence.

Run the CLI as `${CLAUDE_PLUGIN_ROOT}/scripts/fathom`, written `fathom` below.

## 1. Pick the records

| Invoked | Records |
| --- | --- |
| By the after-compaction hook | exactly the ones it lists: the records this session wrote |
| By the user, naming records | those |
| By the user, naming none | `fathom touched` (this session's records); ask when it lists several and the user named none |

Never compact a record this session didn't write unless the user names it.

When a conversation compaction triggered this, the summary above carries the
reasoning the session had: facts found wrong, keys describing the same thing,
contradictions left open, and why the lede says what it says. Use it; it is
the evidence the record alone doesn't hold.

## 2. Gather the candidates

```bash
fathom compact <record>              # mechanical findings: identical duplicates, superseded groups, open contradictions, the lede
fathom show <record> --cited         # every current fact, and which saved views cite it
fathom views <record>                # each view's latest render
```

Each `superseded by <key>` group is a ready-made theme: the newer fact names
the ones it replaced. Then read the facts for what `fathom compact` can't find:

| Reason | A fact is a candidate when | Retraction `reason` |
| --- | --- | --- |
| Wrong | Later evidence in the record or the summary contradicts it | `wrong` |
| Duplicate | Another key states the same thing, in other words or other fields | `duplicate` |
| No longer relevant | It describes a design, plan, option, or question the work has moved past, and no reader of the current work needs it to follow the outcome | `irrelevant` |

"No longer relevant" is about the record's current readers, not about truth: a
superseded design is still true history. Leave a fact that explains why the
current outcome was chosen (the alternative a decision rejected, with its
rationale) unless the user drops it; a brief can leave it out of a view without
removing it from the record. Never offer a fact that carries a live condition
("revisit if it proves too costly", "until the last row expires"): it is still
being watched, not history.

## 3. Group by theme

Group candidates by what they are about, not by reason alone: "the first
design (v76) and its Private CA costs", "the threat counts before the scrutiny
correction", "two keys for the token lifetime". One theme is one decision the
user can make at once. Split a theme whose facts don't all go together.

For each theme, work out before asking:

- **What it holds:** each key with a one-line paraphrase of the fact.
- **Why it's a candidate:** the evidence or the later fact that supersedes it,
  by key.
- **What it costs:** each saved view citing a fact in the theme (from
  `--cited`), which goes stale and loses that content on its next render;
  each brief whose sections need this kind of fact (`fathom brief --record
  <record> <name>`), which can no longer be rendered in full, even with no
  saved view yet; and whether the lede rests on any of them.
- **For duplicates:** which key survives and why (the more precise one, the
  one more views cite).

## 4. Ask, theme by theme

Ask with `AskUserQuestion`, up to four themes per call. The user may see only
the question, so each one stands alone: the theme, the count, the facts in
plain words, why they're candidates, and what views and lede rest on them.
For example:

> **The v76 design (4 facts, no longer relevant).** The record still holds the
> first design, which issued certificates from AWS Private CA: its
> header-spoofing risk, its issue-permission gap, and the CA's monthly fee.
> `decision-supersede-v76` replaced it. The `cto` view cites all four in its
> "why we moved off v76" section, which would drop out on its next render.
> The lede doesn't rest on them. Retract them?

Offer **Retract all**, **Keep all**, and **Let me pick**. On **Let me pick**,
list the theme's facts and ask which to keep. Never fold an answer for one
theme into another.

Contradictions the evidence can't settle are not a theme to retract: report
each with the fact, both values, and both bases, and leave both in the record.

## 5. Write the confirmed rows

One `fathom add` for the whole pass, so it lands as one version:

```yaml
- key: <key>
  type: <its type>
  retracted: true
  reason: <wrong | duplicate | irrelevant>
  basis: "<why, and that the user confirmed it: 'user confirmed: superseded by decision-supersede-v76'>"
```

For a duplicate, retract the extra keys with a basis naming the surviving key,
and add a row to the survivor when merging adds anything it lacked.

## 6. Re-check the lede

If the lede rests on a retracted key, or the pass changed what it summarizes,
revise it in the same `add` (`/fathom:record`, "Keep the lede current"),
repointing `rests-on` at surviving keys. Otherwise confirm it still holds and
say so.

## 7. Report

One block per record: current facts before and after (`fathom compact` prints
both counts), each theme with what the user chose, the lede (kept, or old →
new), each contradiction left open, and the views now stale (`fathom views`)
with an offer to render them again.
