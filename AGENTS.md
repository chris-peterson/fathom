# fathom

A Claude Code plugin that keeps the facts of a piece of work in one versioned
record and renders each audience's document from it. The idea and its
principles are in `docs/principles.md`.

`SPEC.md` is the requirement source of record. A change to behavior updates the
requirement in the same commit.

## Layout

```text
SPEC.md              requirements (EARS), the source of record for behavior
docs/principles.md   why documents are views, and the patterns this follows
docs/extending.md    how a team adds or extends a kind
scripts/fathom       the CLI: record, kinds, briefs, and the view check
skills/              fathom:record, fathom:render, fathom:pdf, fathom:proof, fathom:wtf
guides/              long-form methods the skills name by path (verification)
skills/render/styles/ named view styles, one stylesheet each (how-to)
kinds/base/framing/  writing styles (eli, ste): a brief's framing and a /fathom:wtf mode
kinds/               the kinds fathom ships: base, and incident and release as examples
```

## Running it

Both scripts are self-contained [uv](https://docs.astral.sh/uv/) scripts: their
dependencies sit in the `# /// script` header, so they run directly with no
install step. `skills/pdf/scripts/to-pdf.py` also needs Google Chrome installed,
since it prints through Playwright's `chrome` channel.

```bash
scripts/fathom --help                    # every subcommand and exit code
scripts/fathom kind --name <kind>        # what a kind resolves to, inheritance included
scripts/fathom brief --kind <kind> <brief>
```

Verify a change by exercising the CLI against a scratch record outside the repo:
`init`, pipe rows to `add`, then `show`, and `check` a hand-written view. The
`check` exit codes (0 pass, 3 failures) are what the skills route on.

## How the pieces fit

- **Record.** A directory with `fathom.yml` (kind, title) and `record.yml`, an
  append-only YAML list of rows. A row's `seq` is the record's version; reading
  as of version N takes each key's latest row with `seq <= N` and drops
  retractions. `add` validates every row against the kind's fact types and
  writes all of them or none. A bare kebab-case name in place of a directory
  resolves to `.fathom/<name>/` at the repo root, which `init` makes git ignore.
- **Kinds.** Resolution through `FATHOM_KINDS`, `extends`, and brief stacking is
  in `docs/extending.md`. `fathom brief` prints the resolved stack plus every
  framing rule it names, and that output is what `fathom:render` follows.
- **Views.** `fathom:render` writes HTML stamped with
  `<meta name="fathom-version">`, `<meta name="fathom-audience">`, and
  `<meta name="fathom-visibility">`, wrapping each fact in `data-fact="<key>"`
  and non-fact numbers in `data-literal`. `fathom check` parses that HTML and
  fails any visible number whose digits none of its cited rows hold as of the
  stamped version, and any cited row whose `visibility` is narrower than the
  view's. `to-pdf.py` refuses a stamped view unless given `--record`, and runs
  the check before printing.
- **Plugin root.** Skills call the CLI as `${CLAUDE_PLUGIN_ROOT}/scripts/fathom`;
  run from a checkout, the script falls back to its own parent directory to find
  `kinds/`.

Requirements in `SPEC.md` carry stable IDs (`RECORD-04`, `CHECK-02`), each a
linkable heading. The `README.md` Status section tracks which requirement groups
are not built yet.

## Conventions

- This is a public repo: no internal hosts, private paths, or company names in
  committed files. Examples from real work are described without them.
- The suite's conventions apply: `plugin.yml` becomes the source of record for
  metadata once the plugin ships, and every command is namespaced
  `fathom:<skill>`.
