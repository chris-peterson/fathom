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
```

## Conventions

- This is a public repo: no internal hosts, private paths, or company names in
  committed files. Examples from real work are described without them.
- The suite's conventions apply: `plugin.yml` becomes the source of record for
  metadata once the plugin ships, and every command is namespaced
  `fathom:<skill>`.
