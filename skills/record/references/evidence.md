# Gathering evidence

## The fidelity ladder

Evidence comes in at different precisions. Don't stop at a low rung when a
higher one is reachable:

| Rung | Precision | Good for |
| --- | --- | --- |
| Recollection and chat | qualitative | the narrative |
| Tickets and dashboards | minute | who was involved and what was affected |
| Source control and CI/CD APIs | second | code, build, and deploy events: what changed |
| Audit logs | second | the moment a resource changed, and who changed it |
| Local history (reflogs, shell history) | second | a trail that runs through someone's working machine |

Prefer an API over a console when exact timestamps matter. A kind's
`sources.md` maps these rungs to that kind of work, and a team's kind maps them
to its tools.

## Practices that make a timeline hold up

1. **Capture perishable evidence first.** Some systems forget within the hour
   (stopped workloads, short log retention), and a deleted machine takes its
   local state with it. Ask for those records before anything else, and record a
   `source` fact with its retention.
2. **Build the identifier map early.** Every source names things differently.
   Record an `entity` per thing with all its names in `ids`.
3. **Treat gaps as evidence.** A window where a source stopped reporting usually
   marks when something was stuck. Record a `gap`.
4. **Know which timestamps are report times.** Identical times across unrelated
   records usually mean an agent reported them together, not that the events
   happened together. Say so in the basis.
5. **Decode codes at their source.** Find an exit or error code in the program
   that produced it and confirm it against the log line, rather than guessing
   from convention.
6. **Find a control.** A sibling that took the same change and stayed healthy
   shows which difference matters. Record its facts alongside.
7. **Normalize to one zone at write time.** Every source's timestamp goes in
   with its offset; views convert to the audience's zone.
8. **Bracket off-record decisions.** A decision made outside any tracked system
   can be dated between the edit timestamps, reflogs, and pipeline runs around
   it. Record it `inferred`, with the bracket as its basis.
9. **Know the system's propagation semantics.** Replication often mirrors
   creates but not deletes, so a cleanup in one place may not reach another.
   Record what was verified where.

## Don't touch production systems yourself

Read artifacts and accept pasted evidence; don't call production or cloud
control planes directly, not even read calls, unless the user opts in. The user
runs the command and pastes the output; record what it shows.

Never suggest mutating shared state to provoke a reproduction (configuration
other services read, a feature flag, a shared database row or queue): it changes
live behavior for every reader. Prefer passive observation, or a trigger
confined to one instance nothing else depends on.
