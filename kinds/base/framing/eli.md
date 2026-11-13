# ELI (explain it from the ground up)

For a reader who doesn't share the work's vocabulary. The text states the same
facts at a lower altitude: it rebuilds from what the reader already knows
instead of building on what the team knows.

This is the one definition of `eli`. A brief that names it applies it to every
sentence its view renders, and `/fathom:wtf eli` applies it to a reply the
reader couldn't follow.

**The defect:** wrong altitude. The text assumed knowledge the reader doesn't
have and built on top of it, so every sentence after the assumption was wasted.

**The remedy:** rebuild from the ground up.

- **Find the one concept the rest hangs off**, and anchor it in something the
  reader already knows before using it.
- **Name things by their role, not their identifier.** "The old proxy", not the
  host name; "the nightly job", not the pipeline ID. Put identifiers in hover
  text, or leave them to the view that carries them.
- **Gloss a term the first time it appears**, in five words or fewer, and only
  the terms the reader needs to act. A term the reader doesn't need is left out.
- **End on what the reader can do.** The reader finishes knowing the actual
  thing and their next step, not only a story they could follow.

Expect the text to run longer than one written for the team: descending an
altitude costs words. Spend them on the concept the rest depends on, not on
covering more facts.

> Before: The migration is blocked on an advisory lock held by the previous
> transaction, so you'll need to terminate the holder before the DDL can
> acquire it.
>
> After: Two things are trying to change the database's shape at once, so the
> database made the second one wait. An older change never finished and is
> still holding its turn. Cancel that older one and yours goes through.

"Advisory lock", "DDL", and "the holder" all assume the concept the reader is
missing. The rewrite builds the waiting-in-line idea first, then ends on the
action.

**How it loses content:** the analogy replaces the answer instead of carrying
it. A comfortable story the reader can follow and can't act on is worse than
the version they couldn't parse. Every fact the original stated still appears
inside the plain-words version. In a view, each stays cited, and an analogy
states no fact of its own: a number it seems to imply ("about the size of a
football field") is a fact the record must hold.

`eli` is not `ste`: `ste` gives a reader who has the concepts unambiguous
sentences, and `eli` gives a reader without them a way in. A reader who lacks
both needs both.
