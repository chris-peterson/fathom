---
name: render
description: This skill should be used when the user wants a document made from a fathom record, for one reader, such as "/fathom:render", "write this up for managers", "render the analysis", "make the RCA page", "an explainer for the product team", "a postmortem draft", "render all the views", or "re-render as of the latest version". Renders a view from the record as of a version, an audience brief, a format, and a style; cites every fact, stamps the version and audience, and runs fathom check before the view is published.
argument-hint: "<brief> [as of v<N>] [<format>] [<style>] [<record name or dir>]"
---

# Render

A view is `render(record as of a version, audience brief, format, style)`. It
chooses, orders, phrases, and leaves out; it never adds a fact. Rendering is
cheap and repeatable, so a view that's wrong or stale is rendered again, never
patched.

Run the CLI as `${CLAUDE_PLUGIN_ROOT}/scripts/fathom`, written `fathom` below;
`fathom --help` documents every subcommand and exit code.

## 1. Pin the inputs

| Input | Default | Read with |
| --- | --- | --- |
| Record | the one this session uses | `fathom show <dir>` |
| Version | the latest | `fathom version <dir>` |
| Brief | the one the user names; ask with the kind's list when unclear | `fathom kind <dir>`, then `fathom brief --record <dir> <name>` |
| Format | an HTML page | the user's words: page, artifact, PDF, one-pager |
| Style | the house look of where it's going | the user's words; a named style below, or `fancy` for PDF |
| Visibility | the brief's `visibility` | where the user says the view goes: a public page, a channel the whole organization reads, the team's own space |

Named styles live in `${CLAUDE_PLUGIN_ROOT}/skills/render/styles/`: a
stylesheet each, whose header comment gives the markup it styles, and a script
when the style has one. Inline them in the view and write the body in that
markup. A style is only the look; how plainly a view reads is its brief's
framing (`eli`, `ste`), so a plain-words page in another look is the same brief
in another style.

| Style | Asked for as | Fits |
| --- | --- | --- |
| `how-to` | "how-to", "step by step", "like a wikiHow article", "a runbook" | A procedure the reader follows, which the `how-to` brief writes. Its level pill says who it's for: "Beginner" under `eli` framing. Step, part, and method numbers are CSS counters, so they need no `data-literal` |

When several views are wanted, render every one from the same version unless
the user asks otherwise, so they agree by construction.

`fathom brief` prints the brief, any brief it extends, and every framing rule
they name. Follow all of it: the brief decides the bottom line, what goes in,
the tone, the depth, and what is left out.

## 2. Read the facts

```bash
fathom show <dir> --as-of <N> --full
```

Use only these rows. **When the brief needs a fact the record doesn't hold,
stop**: name the missing fact and record it first (`/fathom:record`), then
render from the new version. A number typed into a view is a fact the record is
missing.

## 3. Vet each fact the view will state

`fathom check` proves a view says what the record says, not that the record is
right. Recording stays fast on purpose, so the render is the last stop before a
reader acts on a fact. Run the five checks in "Vetting a fact" in
`${CLAUDE_PLUGIN_ROOT}/guides/verification.md` (firsthand, read, earned,
consistent, confirmed) on every fact the view will state, and record what they
change before rendering. The guide is the same method `/fathom:proof` rules
with.

## 4. Judge who may read each fact

One record feeds every audience, so each render is a chance to send a fact to
readers its source never had. Recording stays fast by leaving most facts
unclassified; the scrutiny happens here, against this view's visibility
(`public`, `internal`, `private`, widest first, as a GitLab project names them).

For each fact the view will state:

| The fact | Do |
| --- | --- |
| Carries a visibility at or wider than the view's | State it |
| Carries a narrower visibility | Leave it out |
| Unclassified, and its basis and fields are plainly fine for these readers | State it |
| Unclassified, and you're unsure: a customer, a person, an internal host or account, a cost, a security detail, evidence from a source the readers can't open | Ask |

**Ask once, for every unsure fact together**, with `AskUserQuestion`: name each
fact by key with the value the view would show and where it came from, and
offer the visibility levels. Record each answer before writing the view, so no
later render asks again:

```bash
fathom classify <dir> <visibility> <key>...
```

`classify` adds a row per key carrying the visibility, so the view renders from
the new version. A later correction of the fact keeps its visibility.

When a fact the bottom line rests on is narrower than the view, say so and let
the user choose: leave it out, or narrow the view's visibility (and so where it
can go). A secret value never appears in any view; name the secret instead.

## 5. Write the view as HTML

HTML is the form `fathom check` reads; PDF and published pages print from it.

- **Stamp it.** In `<head>`:
  `<meta name="fathom-version" content="<N>">`,
  `<meta name="fathom-audience" content="<brief name>">`, and
  `<meta name="fathom-visibility" content="<visibility>">`. Show the stamp to
  readers too, in a footer or meta line marked `data-literal` (its version
  number is not a fact): "Rendered from `<record title>` v`<N>` for `<audience>`".
- **Cite every fact.** Wrap each rendered fact in an element carrying
  `data-fact="<key>"` (several keys space-separated when a sentence rests on
  more than one). A table row cites on the `<tr>`; a chart cites on its
  container. Cite facts stated in words too ("the fix shipped"), not only
  numbers.
- **Mark non-facts sparingly.** A number that isn't a fact (a step number typed
  as text, a section count in a heading) goes in an element with
  `data-literal`. The check counts these; a view full of them is hiding facts.
- **Open with the bottom line** the brief defines, then the detail for the
  reader who reads on.
- **State certainty in the audience's terms**: the basis beside the claim for
  engineers, a label ("likely") for a manager, whatever the brief says.
- **Say what's left out and link the view that has it.** The brief's
  `leaves-out` and `links-to` name both. Link the other view's file or URL when
  it exists; otherwise name it and offer to render it.
- **Present, don't compute.** Converting a timestamp to the audience's zone and
  formatting a number are presentation. A difference, a sum, or a rate is a new
  fact: record it as a `measure` first.

## 6. Check

```bash
fathom check <view.html> --record <dir>
```

| Exit | Meaning | Do |
| --- | --- | --- |
| 0 | Every number sits in a citation, every citation resolves as of the stamped version, every cited number is held by a cited row, and no cited fact is narrower than the stamped visibility | Publish (step 7) |
| 3 | Each failure is printed with its text | Fix the view, or record the missing fact and render again. Never publish a failing view |
| 1 | No record, or no such version | Report it |

The check works on facts, not wording: two renders of the same inputs can phrase
things differently and both pass.

## 7. Publish in the format

**Check the destination first.** Who can read where the view is going has to be
within its stamped visibility. A shared artifact, a PDF sent to a list, and a
chat post each reach whoever holds the link or the channel. When the
destination is wider, stop and ask: render again at the wider visibility (step
4 leaves out what can't go), or publish somewhere narrower.

| Format | How |
| --- | --- |
| A page on disk | Save the checked HTML in the record's directory, named `<brief>-v<N>.html`; under `.fathom/` it stays out of commits with the record |
| A shared web page | Publish the checked HTML with the `Artifact` tool |
| PDF | `/fathom:pdf` with the view and `--record`; it re-checks before printing |
| A Markdown page on a site that renders its inline HTML (docsify, for one) | Write the page itself as the view, and check the `.md`: the stamps go in as `<meta>` tags, each fact in an HTML element carrying its `data-fact` (a block, or a `<span>` inside a heading), so the published file is the checked one. A plain `#` line holding a number fails the check; cite it with a `<span>`, and strip the tags wherever the site reads the heading as text |
| Other Markdown, slides, a chat post, a word-processor document | Convert from the checked HTML, keeping every fact as the view states it, and say in the report that the converted copy is outside the check |

A view published once and later edited by hand has drifted from the record.
When the user brings back an edited view, compare it with what was rendered, and
offer to record any new fact it carries and render again.

## 8. Report

Name each view with its brief, version, visibility, and format, linked to where
it lives, the `fathom check` result line, what each view leaves out with the
view that carries it, and each fact left out for its visibility. Then the vet:
how many cited facts were confirmed against a primary source, how many stay
secondhand or inferred, and each contradiction found with how it was resolved.
