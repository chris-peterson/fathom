# STE (Simplified Technical English)

For a reader who follows the text step by step, or reads it in a second
language: an operator mid-incident, a team in another region, anyone running a
procedure.

This is the one definition of `ste`. A brief that names it applies it to every
sentence its view renders, and `/fathom:wtf ste` applies it to a reply whose
sentences were too complex to follow.

[ASD-STE100](https://www.asd-ste100.org/) is a controlled-language standard
from aerospace maintenance documentation, maintained by the Simplified Technical
English Maintenance Group at ASD. It exists so that a procedure written by one
engineer is unambiguous to a technician reading it in a second language under
time pressure, which is why it constrains grammar and vocabulary rather than
tone. It has two parts: writing rules, and a dictionary of approved words, each
with one meaning and one part of speech. Apply the rules, which carry most of
the benefit, and use one-word-one-meaning as a test on the words you choose.

## The rules that do the work

| Rule | What it means when you write |
| --- | --- |
| **One topic per sentence** | Split on every "and", "which", and semicolon that joins two ideas. The single highest-yield edit |
| **20 words at most in a procedure, 25 in description** | Over the limit means two sentences were joined |
| **Six sentences at most per paragraph** | Over that, it's two paragraphs or a list |
| **Active voice** | Name the actor. Passive is allowed in description only when the actor is unknown, never to avoid naming it |
| **Simple tenses only** | Infinitive, imperative, simple present, past, and future. "Will have been persisted" becomes "the system stores" |
| **No omitted sentence parts** | Keep the article, the subject, the verb. Don't telegraph to save words; split the sentence instead |
| **`-ing` only as a technical noun or its modifier** | "Reprocessing can be initiated" becomes "an operator can process it again" |
| **Noun clusters of three words at most** | "Dead-letter queue table" is four: "the table for the dead-letter queue" |
| **One word, one meaning** | A word that means two things gets replaced in one of the two places. Watch *check*, *set*, *handle*, *run*, *process*, *update* |
| **One instruction per sentence** | Two actions are two sentences, even when they always happen together |
| **A condition before its instruction, a warning before its step** | "If the job fails, run it again"; the warning comes before the step it applies to, never after |

> Before: If the request is rejected by the upstream validation service, the
> payload will have been persisted to the dead-letter queue table already, and
> reprocessing can subsequently be initiated by an operator.
>
> After: The validation service can reject the request. Then the system puts
> the payload in the dead-letter queue. An operator can process the payload
> again.

Three sentences from one, each naming its actor. "Will have been persisted"
collapses to "puts", "reprocessing can be initiated" to "can process again", and
the four-word cluster breaks into a phrase.

## Keep the technical names

The standard permits technical nouns and verbs a general dictionary wouldn't
hold. `mutex`, `idempotent`, `rebase`, and `advisory lock` are legitimate
technical names. Keep the exact term and gloss it once on first use, so it is a
name the reader carries rather than a word they decode each time.

**How it loses content:** dodging an exact term because it isn't a common word,
which trades precision for simplicity: the opposite of the point.

## What STE is not

It isn't `eli`. STE gives a reader with domain knowledge unambiguous sentences;
`eli` gives a reader without it a way in. An STE procedure for a database
migration still assumes the reader knows what a migration is.

It isn't necessarily shorter. Splitting one long sentence into three and
restoring the dropped articles often adds words. It reads faster anyway,
because nothing has to be read twice.
