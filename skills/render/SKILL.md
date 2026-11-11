---
name: render
description: This skill should be used when the user wants a document made from a fathom record, for one reader, such as "/fathom:render", "write this up for managers", "render the analysis", "make the RCA page", "an explainer for the product team", "a postmortem draft", "render all the views", or "re-render as of the latest version". Renders a view from the record as of a version, an audience brief, a format, and a style; cites every fact, stamps the version and audience, and runs fathom check before the view is published.
argument-hint: "<brief> [as of v<N>] [<format>] [<style>] [<record dir>]"
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
| Style | the house look of where it's going | the user's words, or `fancy` for PDF |

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

## 3. Write the view as HTML

HTML is the form `fathom check` reads; PDF and published pages print from it.

- **Stamp it.** In `<head>`:
  `<meta name="fathom-version" content="<N>">` and
  `<meta name="fathom-audience" content="<brief name>">`. Show the stamp to
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

## 4. Check

```bash
fathom check <view.html> --record <dir>
```

| Exit | Meaning | Do |
| --- | --- | --- |
| 0 | Every number sits in a citation, every citation resolves as of the stamped version, and every cited number is held by a cited row | Publish (step 5) |
| 3 | Each failure is printed with its text | Fix the view, or record the missing fact and render again. Never publish a failing view |
| 1 | No record, or no such version | Report it |

The check works on facts, not wording: two renders of the same inputs can phrase
things differently and both pass.

## 5. Publish in the format

| Format | How |
| --- | --- |
| A page in the repo or on disk | Save the checked HTML beside the record, named `<brief>-v<N>.html` |
| A shared web page | Publish the checked HTML with the `Artifact` tool |
| PDF | `/fathom:pdf` with the view and `--record`; it re-checks before printing |
| Markdown, slides, a chat post, a word-processor document | Convert from the checked HTML, keeping every fact as the view states it, and say in the report that the converted copy is outside the check |

A view published once and later edited by hand has drifted from the record.
When the user brings back an edited view, compare it with what was rendered, and
offer to record any new fact it carries and render again.

## 6. Report

Name each view with its brief, version, and format, linked to where it lives,
the `fathom check` result line, and what each view leaves out with the view that
carries it.
