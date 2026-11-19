# Where session evidence comes from

A session's facts come from the work itself, so its sources are the artifacts
that work left behind. Prefer the artifact to the conversation's account of it:
a merged change request over "I pushed the fix".

| Category | What it contributes | Precision |
| --- | --- | --- |
| The forge (commits, change requests, pipelines) | What landed, with links | the commit |
| The issue or tracker item | The goal as it was asked for, and what done means | the issue |
| `/goal` | The goal as the user set it for the session | the session |
| tack (`tack status <route>`) | The route and tack this work belongs to, and its deliverables | the route |
| The conversation | Decisions and their reasons, which no artifact records | the session; record as `observed` with the turn it came from |
