# Extending fathom with a kind

fathom's core knows nothing about incidents, migrations, or test campaigns. A
**kind** brings that knowledge: the fact types a record of that work can hold,
the briefs for the people who read about it, and where its evidence comes from.
fathom ships `base`, which fits any work, and `incident`, which extends it as an
example. A team adds its own kind to carry what only it knows: its tools, its
templates, its readers.

## What a kind holds

```text
<kind>/
  schema.yml        fact types; `extends: <kind>` to build on another
  briefs/<name>.md  one per audience
  framing/<name>.md rules a brief applies to every sentence it renders
  sources.md        where this kind's evidence comes from, rung by rung
```

`fathom kind --name <kind>` prints what a kind resolves to, including
everything it inherits.

### schema.yml

```yaml
kind: <name>
extends: <base kind>          # optional
facts:
  <fact type>:
    about: <one line: what a row of this type records>
    fields:
      <field>: {type: <text | number | datetime | date | url | enum | list | map>, required: <bool>}
      <enum field>: {type: enum, values: [<value>, ...]}
```

A kind inherits every fact type of the kind it extends and replaces any it
redefines. Keep fact types about the work, not about a document: a `cause` is a
fact type, a "root cause section" is a brief's choice.

### briefs/\<name\>.md

Front matter says who the view is for; the body says how to build it.

```yaml
---
audience: <who reads it>
visibility: <public | internal | private>   # where its views are published, as GitLab names the levels
needs: <what they need from it>
bottom-line: <the one line it opens with>
tone: <register, and how things are named>
verbosity: <length or depth>
leaves-out: <what it drops, and which view has it>
links-to: [<brief>, ...]
framing: [<framing rule>, ...]
extends: true                 # optional: also follow the same-named brief of the base kind
---
```

A brief with the same name as one in a base kind replaces it. With
`extends: true` it adds to it instead: `fathom brief` prints this brief, then
the base kind's, then every framing rule either names.

## Where fathom finds kinds

`fathom` looks up a kind by name in each directory of `FATHOM_KINDS`
(separated by `:`), then in the plugin's own `kinds/`. The first match wins, and
a kind's `extends` resolves the same way, so a team's kind can build on a
bundled one.

Set it for a project in `.claude/settings.json`, so every session in the repo
sees the team's kinds:

```json
{ "env": { "FATHOM_KINDS": "<path to the team's kinds directory>" } }
```

## A worked extension

A platform team runs incidents on its own cloud tooling and has a postmortem
template with fixed columns. It adds one kind:

```text
kinds/acme-incident/
  schema.yml          extends: incident; adds a `deploy` fact type with pipeline and image fields
  sources.md          the team's commands for each source category in incident's sources.md
  briefs/postmortem.md  the template's sections and action-item columns
  briefs/analysis.md    extends: true; adds the team's dashboards to the evidence section
```

Its records start with `fathom init <dir> --kind acme-incident`. They get
`incident`'s fact types, the `blameless` framing rule, and the `status` and
`explainer` briefs unchanged; the team's postmortem replaces the bundled one,
and its analysis adds to the bundled one.

Keep a kind to what differs. A brief that restates a base brief with one change
is a brief that drifts from the base the next time the base improves; extend it
instead.
