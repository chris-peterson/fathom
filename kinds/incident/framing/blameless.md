# Blameless

Blameless means precise at the systems level, not soft. Removing blame makes
the account more accurate, for two reasons:

- People who don't fear punishment give the detailed "second story": the
  misleading signals, the decisions that were reasonable at the time, the
  conditions. A blame-seeking review never surfaces it.
- A description that assigns fault to a person stops one level short of the
  cause. Describing the system and its conditions is the more precise account,
  and the one where the fixes live.

Apply it to every sentence the view renders:

- **Make the system the subject.** "Someone forgot the attribute" becomes "the
  error mapping is per-endpoint with no test that fails when one is missing, so
  an uncovered endpoint ships silently."
- **Treat "human error" as the start of the investigation, not its
  conclusion.** Say what made the action reasonable in the moment, and what let
  it matter.
- **Names attach to responses, never to causes.** A `responder` appears in the
  responders list; a `cause` names no one.

The record holds raw observations captured during the response. This rule is
the calm rewrite, applied at render time, so the record itself never needs
sanitizing.

## References

- John Allspaw, [Blameless PostMortems and a Just Culture](https://www.etsy.com/codeascraft/blameless-postmortems/) (2012).
- Google SRE Book, [Postmortem Culture: Learning from Failure](https://sre.google/sre-book/postmortem-culture/).
- Richard I. Cook, [How Complex Systems Fail](https://how.complexsystems.fail/).
- Sidney Dekker, *The Field Guide to Understanding 'Human Error'* and *Just Culture*.
