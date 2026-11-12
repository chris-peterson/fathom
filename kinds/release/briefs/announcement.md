---
audience: people who use the tools, reading the release's announcement (a blog post, a release page, a newsletter); some already run them, most don't
visibility: public
needs: what they can do now that they couldn't before, what breaks if they upgrade, and how to start
bottom-line: what kind of release it is, counted rather than listed (what was added, released, and retired), and what an existing user has to do before upgrading
tone: plain words, second person; name each tool, and show the command a reader would type
verbosity: one screen per section; a reader who stops after the first section still knows what shipped
leaves-out: how each change was built, its change requests and test runs (each tool's changelog has them)
links-to: []
framing: []
---

# Release announcement

1. **Bottom line.** Set apart as the lead. Count what shipped instead of naming
   it, since the sections below name every tool, and end on the one thing an
   existing user must do (read the breaking changes before upgrading).
2. **New tools.** One card each: its icon, its name linked to its docs, the job
   it helps with, and one or two sentences on what it does.
3. **Major releases.** One heading groups them, with a subheading per tool whose
   major version changed. List breaking changes first, each opening with a red
   "Breaking:" ahead of what to do about it.
4. **Other changes.** The rest, one bullet each. A change that shipped in its
   own release links that release.
5. **What's next.** The `plan` facts as a timeline, one row per tool, ordered
   from now to later with no dates on the axis: a plan is a rough order, not a
   schedule. Draw a tentative plan dashed, and give a short stretch of work room
   to show its whole name. Follow it with the themes in words.
6. **Install.** The command, and where to go next.
