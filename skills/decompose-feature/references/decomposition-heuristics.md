# Decomposition heuristics

How to cut a plan into issues.

## Where to cut
- **Cut at real seams.** A seam is a place where one piece can be built, reviewed, and merged without the others. API contract vs consumer; a new endpoint vs the UI that calls it; a pure function vs its wiring.
- **Vertical over horizontal.** Prefer "the Disconnect button works end to end" (UI + call + backend op) over "all the UI, then all the hooks, then all the endpoints." Horizontal slices leave everything half-done until the last one lands.
- **Front-load shared dependencies.** If three issues all need a new backend op or a shared type, that op/type is its own issue, first, and the three are `Blocked by` it.
- **Separate backend-contract changes from frontend consumption** when they live in different repos or ship on different cadences — but link them tightly with blocked-by.

## Dependency graph
- Build the graph of `blocked_by`. Compute a topological order. That order becomes the epic checklist and the "Sequence" line on each issue.
- Identify the **critical path** (the longest dependency chain) and mark the rest as parallelisable so multiple agents can run at once.
- Never leave a cycle. If two issues block each other, the seam is wrong — re-cut.

## Sizing (see enrichment-bar.md too)
- Target: one focused PR each. If a competent contributor couldn't land it in under a day, split it.
- A good issue has one coherent acceptance set. Two unrelated "done" definitions = two issues.

## Cross-repo features
- Each issue names its own `repo`. The **epic** lives in the primary/most-user-facing repo.
- Backend issues that unblock frontend issues are referenced across repos as `owner/repo#N` in the blocked-by line.
- Call out explicitly in the epic when the feature is only "done" once issues in *all* repos land — so nobody ships the frontend against a backend that isn't there.

## What each issue must inherit from the code-read
- The exact current behaviour it changes (with `file:line`).
- The pattern to copy, if one exists.
- The traps: fragile parsing, auth/permission gates, backend contracts, env/reload steps.
