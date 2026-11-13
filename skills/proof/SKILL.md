---
name: proof
disable-model-invocation: true
description: Rule a claim true or false, with sources and how each is known. Triggers on 'are you sure?', 'prove it', 'source?'. When the session keeps a fathom record, the ruling goes into the record.
argument-hint: "[the claim, when it isn't your last reply]"
---

# Proof

Rule on a claim, true or false, and show the evidence behind the ruling and how
well it is known. The method (where evidence comes from, the certainty scale,
and how to rule) is in `${CLAUDE_PLUGIN_ROOT}/guides/verification.md`. Read it
before gathering evidence: it is the same method `/fathom:render` vets a view's
facts with, so a ruling here and a vetted fact there mean the same thing.

## 1. Pin the claim

- **Backward (the default):** audit your most recent substantive reply, before
  this invocation. List every factual claim, recommendation, and code change in
  it, and find the one its conclusion rested on.
- **Forward:** when the invocation sits next to a premise in the user's own
  message ("there's no way to override that, as far as I know /fathom:proof"),
  the claim under proof is that premise, not anything you said. Pin it exactly.

## 2. Gather evidence

Run each evidence stream that applies, as parallel agents when there are
several, and merge what they find before ruling:

| Stream | Settles |
| --- | --- |
| The test suite | Behavior on the paths the tests cover, when they pass |
| Source inspection | What the code does, cited by `file:line`, in the working tree, the index, or `HEAD` as the claim needs |
| The artifact's own description, then official docs | Status and intended behavior: the README, package metadata, the docs page's own passage |
| Git history | What changed and when: the commit, the blame, the diff |
| A run | What actually happens: the command, the request, the degraded input built on purpose |

Spend the most on the claim the conclusion rested on. A naming or formatting
claim needs a glance, not an evidence chain. Brief each agent with the guide's
evidence order, so its report cites the primary datum and not a summary.

## 3. Rule

Give the verdict and its certainty separately, as the guide's "Ruling on a
claim" section sets out: TRUE, FALSE, PARTLY TRUE, or UNDETERMINED, at
`measured`, `observed`, or `inferred` certainty (High, Medium, or Low
confidence). Rule on the claim as it was stated.

## 4. Report

The verdict comes first, above the evidence and above any account of how you
checked:

```
> <the claim, quoted as it was stated>

## <🟢 TRUE | 🔴 FALSE | 🟡 PARTLY TRUE | ⚪ UNDETERMINED>

<What is actually true, in one or two sentences.>

**Certainty:** <measured | observed | inferred> (<High | Medium | Low>): <what settled it, in a clause>

### Evidence

#### <verdict> <the headline claim>
- **Source:** <file:line, test output, quoted doc line, command output>
- <what that datum shows>

#### <verdict> <each other claim>
- ...

### Gaps
- <what you couldn't check, and why>
```

Leave out Gaps when nothing is outstanding. When the conclusion of your earlier
reply rested on a claim that is now FALSE, say what that changes, in the
paragraph under the verdict, not in the evidence.

## 5. Record it, when there is a record

When the session keeps a fathom record and the claim is about the work, the
ruling is a fact:

- **TRUE or PARTLY TRUE:** record the claim (or its corrected half) as a row
  whose certainty and basis are the ruling's.
- **FALSE, on a fact the record holds:** name the key, both values, and both
  bases, then record the correction as a new row of that key, or a retraction,
  the way `/fathom:record` treats a contradiction. Views rendered from earlier
  versions keep the old row; say which views the correction changes.
- **UNDETERMINED:** record nothing new. When the record holds the claim, record
  it again as `inferred`, with `confirm-by` naming the check that would settle
  it.
