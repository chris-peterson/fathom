---
name: slack
description: This skill should be used when the user wants something from the session shared in Slack, such as "/fathom:slack", "copy to Slack", "post this in Slack", "write this up for the channel", "copy the transcript for Slack", "summarize this for the team", or "explain this in Slack for a non-technical audience". Rewrites the last reply (or the transcript, a paste, or what the arguments name) for Slack's composer, withholds what the channel's readers may not see, converts it to Slack markup, and copies it to the clipboard.
argument-hint: "[what to share]"
---

# Slack

A Slack post is a view in the chat-post format: something said in this session,
reshaped for a channel reader who has none of its context and can't click into
the user's terminal. Like `/copy`, the result lands on the clipboard. Unlike it,
the text is rewritten for that reader, and it passes the same visibility
judgment `/fathom:render` makes before a view reaches new readers.

## 1. Pick the source

| The user asked for | Source |
| --- | --- |
| nothing in particular ("copy to Slack", a bare `/fathom:slack`) | The previous reply |
| something named ("the plan", "the test results", "MR !42") | That. When it isn't in the conversation, say so and stop |
| the transcript ("copy the transcript for Slack", "the whole session") | This session's turns, in transcript form (step 4) |
| pasted text that is a transcript (prompts, tool activity, replies) | The paste, in transcript form |
| other pasted text | The paste |

**Pin the range of a transcript before writing it.** When it's evident (the
session is short, or the user named where it starts), use it. When it isn't, or
it would span a long scrollback, ask with `AskUserQuestion`: offer the likely
starting points by the prompt that opened each, and the whole session.

Take the facts from what was already said or done; don't investigate anew. The
message goes out under the user's name and carries their accountability, so the
draft is written as theirs. The exception is content they want to share without
having vetted it, and only when they say so (`unvetted`).

## 2. Apply the arguments

The arguments are free-form instructions. Read them as a request, not a fixed set
of flags:

| Argument | Do |
| --- | --- |
| *(none)* | Keep the content; reshape it for Slack (step 4) and cut what only made sense in the terminal |
| `transcript`, "the whole thing" | Transcript form (step 4): every turn kept, only the markup changed |
| `summarize`, `tl;dr`, `short` | Lead with the one sentence a channel reader needs, then at most a few bullets |
| `audience: <who>` | Pitch it at that reader. For a non-technical one, apply the `eli` framing rule (`${CLAUDE_PLUGIN_ROOT}/kinds/base/framing/eli.md`): outcome first, no unexplained terms, no code |
| a tone or channel (`for #incidents`, `casual`) | Match it: status first for an incident channel, looser register for a casual one. The channel also sets the visibility (step 3) |
| `unvetted` | Open with a one-line disclaimer that the content is AI-generated and the user hasn't reviewed it (`_AI-generated, not yet reviewed by me._`), then the content as the session produced it |

Instructions combine. When two pull against each other (a full audience
walkthrough and `summarize`), cut scope, not accuracy.

## 3. Judge who may read each item

A post is a write to the channel's readers, and something may only go where its
source's readers could already see it: the "no write-down" rule
(`docs/principles.md`, principle 11). A session holds things from sources with
narrower readers than any channel: a private repo, a DM, a cost report, a path
on this machine.

**Set the post's visibility from where it goes**, in the levels a view uses:

| Destination | Visibility |
| --- | --- |
| Not named, or a channel the whole organization can join | `internal` |
| A private channel, a group DM, or a DM | `private` |
| A channel shared with another organization, or a public community | `public` |

Then judge each item the draft would carry: a fact, a name, a host, a path, a
figure, a quoted line.

| The item | Do |
| --- | --- |
| A secret value (a token, a password, a key) | Never. Name the secret instead |
| A path on this machine, a scratchpad file | Withhold it, or link the forge file in its place. No reader can open it, and a home directory names its user |
| From a source narrower than the destination (a private repo, a DM, a ticket only the team sees) | Withhold it |
| Plainly fine for the destination's readers | Keep it |
| Unsure: a customer, a person, an internal host or account, a cost, a security detail | Ask |

**Ask once, for every unsure item together**, with `AskUserQuestion`: name each
item with the text the post would show and where it came from. When the session
keeps a fathom record and an item is one of its facts, use the row's visibility,
and record each answer with `fathom classify <dir> <visibility> <key>...` so no
later render or post asks again.

A withheld item leaves a rewrite without a trace. In a transcript, it becomes
`[withheld: <kind>]` (`[withheld: local path]`, `[withheld: cost]`), so the
reader can tell something was removed. When the point of the post rests on a
withheld item, say so and let the user choose: leave it out, or post somewhere
narrower.

## 4. Write for a channel reader

**A rewrite** (the default):

- **Lead with the point** ([BLUF](https://en.wikipedia.org/wiki/BLUF_%28communication%29)).
  The first line is what someone skimming the channel reads; it carries the
  outcome or the ask.
- **Replace terminal references.** `file.py:42` and scratchpad files mean
  nothing in Slack. Link the forge URL (a change request, an issue, a file link
  with a line anchor) or drop the reference.
- **Drop session narration.** What was run and in what order stays in the
  terminal; the message carries the result.

**A transcript** keeps every turn and its wording, and changes only the markup:

- **Each prompt is a block quote of the prompt text alone**, in bold. Drop the
  terminal's prompt marker (`❯`, `$`): the quote already says who spoke, and a
  quote with a marker reads as quoted twice. The script drops one that slips
  through.
- **Tool activity and timings** ("Ran 3 shell commands", "done 10:21 AM") are
  italic lines of their own. Terminal chrome around them, such as a permission
  box, condenses into that line.
- **Tables and commands go in code blocks.** A table keeps its columns there,
  aligned with spaces rather than pipes or box drawing.
- **Text the source cut off is marked `[…]`, never reconstructed.** A guess at
  the missing words would go out under the user's name as something the session
  said.

In both:

- **Mention people only on request.** An `@name` notifies someone when it's
  sent, so add one only when the user names who to ping.

Shape the draft for what Slack renders. Its markup
([Slack: format with markup](https://slack.com/help/articles/360039953113-Use-markup-to-format-text))
covers bold, italic, strikethrough, inline code, code blocks, block quotes, and
links; it has no headings, tables, horizontal rules, images, or syntax
highlighting ([Markdown Guide: Slack](https://www.markdownguide.org/tools/slack/)).

| Markdown habit | In Slack |
| --- | --- |
| a heading | a bold line, converted by the script |
| a table | a bulleted list, one item per row with its attributes inline; in a transcript, a code block. The script refuses a table row outside one |
| deep nesting | one level of bullets; flatten the rest into the parent line |
| a long message | a short top message, with detail offered as a thread reply |

**Write every link as `[text](url)`**, the form Slack's markup lists and the
only one the composer keeps on a paste. The mrkdwn forms `<url|text>` and
`<url>` are for the API: pasted into the composer, the `|` is percent-encoded to
`%7C` and the link breaks. The script rewrites either one to a form that pastes,
so one that slips through is corrected rather than refused.

## 5. Convert and copy

Write the draft in ordinary markdown to a file in the scratchpad, and pass it to
the bundled script. It converts the syntax Slack spells differently (`**bold**`
to `*bold*`, `*italic*` to `_italic_`, `~~strike~~` to `~strike~`, headings,
bullets, legacy links), strips fence language hints and quoted prompt markers,
and copies the result with `pbcopy`:

```bash
uv run --script ${CLAUDE_PLUGIN_ROOT}/skills/slack/scripts/to-slack.py < <draft.md>
```

| Exit | Meaning | Do |
| --- | --- | --- |
| 0 | Converted and copied; stdout is the message | Step 6 |
| 2 | stderr names lines that can't go: a table row Slack can't render, a value shaped like a secret, a path under a home directory. Nothing was copied | Rewrite those lines (step 3 for the last two) and rerun |
| 1 | `pbcopy` is missing or failed | Report it; rerun with `--no-copy` only when the session runs where the user's clipboard isn't (a remote host), and say the clipboard wasn't set |

The script's checks are a floor. A host, a customer, or a cost passes them, so
step 3 is still the judgment.

## 6. Report

Show the script's output in a raw fenced block (a fence longer than any inside
it), so it reads as the exact text on the clipboard and can be copied from the
terminal too. Follow it with one line: that it's on the clipboard, or that it
isn't and why, and each item withheld. Nothing else; the message is the
deliverable.

The markup assumes the bold, italic, and strike syntax Slack documents for typed
markup. When the user reports that a pasted message rendered wrong, ask which
client and whether the formatting toolbar is hidden (Preferences > Advanced),
since that setting changes how the composer treats typed syntax.
