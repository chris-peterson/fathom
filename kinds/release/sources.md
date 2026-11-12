# Where release evidence comes from

The rungs of the fidelity ladder (see the record skill) for a release, by
category. A team extending this kind adds a `sources.md` naming its own
repositories and the commands for each category; fathom reads every
`sources.md` in the kind's chain.

| Category | What it contributes | Precision |
| --- | --- | --- |
| Roadmaps and planning boards | What comes next, in rough order | qualitative |
| Announcements already drafted | Wording a reader has seen (a one-pager, a what's-new entry) | qualitative |
| Changelogs | Each change a user would notice, and which ones break | the release |
| Tags and release pages | Which version shipped, and when | second |

## Practices specific to releases

- **Check a version against its tag, not a checkout.** A local clone that hasn't
  fetched still reads the old version, and its changelog still calls the new
  one unreleased. The forge's release page is the record of what shipped.
- **Record a breaking change as its own fact**, with what a user does about it,
  so a view can lead with it rather than leave it inside a list.
- **Keep a roadmap's private notes out.** A planning board often names internal
  sources beside each item; record the item, not where it came from, unless the
  view's readers can open that source.
