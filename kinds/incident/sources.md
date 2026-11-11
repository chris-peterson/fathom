# Where incident evidence comes from

The rungs of the fidelity ladder (see the record skill) for an incident, by
category. A team extending this kind adds a `sources.md` naming its own tools
and the commands for each category; fathom reads every `sources.md` in the
kind's chain.

| Category | What it contributes | Precision |
| --- | --- | --- |
| Chat and recollection | The response narrative | qualitative |
| Tickets, paging, dashboards | Incident-window actors and impact | minute |
| Source control and CI/CD APIs | What changed in code, build, and deploy: the cause timeline | second |
| Audit trail | Who changed which resource, and when | second |
| Orchestrator records | Placement, start and stop, exit codes, stop reasons | second |
| Scaling activity | Launches and terminations, with the stated cause | second |
| Metrics | Resource pressure over the window, at the source's resolution | the source's period |
| Application logs | The process's last lines before it exited | second |
| Local history | Who did what on a working machine (reflogs, shell history) | second |

## Practices specific to incidents

- **Filter as narrowly as the source allows.** Many audit APIs accept one
  server-side filter: apply the most selective one there (usually the event
  name) and post-filter to the resource IDs.
- **Compare a stop's request time with its completion.** A long gap means the
  stop was requested and didn't take effect.
- **Check whether log timestamps can be trusted** during a degraded window.
  When ingestion lags the event time, events were buffered: order rows by event
  time, and record that the timestamps came from a backlog.
- **Look for the natural experiment.** A node that recovered when one factor
  went away and relapsed when it came back is stronger evidence than any single
  correlation.
