# Enriched issue template

Every issue body follows this structure. Fill every section; delete a section only if it is genuinely N/A and say why. The reader is an agent with no prior context and possibly a weak model — write for that reader.

```markdown
## Summary
<One or two sentences: what this issue delivers and why. Plain language.>

## Where this sits
- **Epic:** #<epic-number> — <epic title>
- **Tracker:** <TICKET-KEY> — <parent summary>   (omit line if the tracker track is off)
- **Sequence:** step <n> of <total> on the <critical path | a parallel track>
- **Blocked by:** #<n>, #<n>  (or "nothing — safe to start now")
- **Blocks:** #<n>, #<n>
- **Repo / branch:** <owner/repo> · base branch `<default-branch>`

> **PR contract:** the PR that closes this issue must include `Fixes #<this>` (and, if the tracker track is on, a `Tracker: <TICKET-KEY>` line pointing at the subtask that covers this issue).

## Context an executor needs
<The slice of the plan relevant to THIS issue. What already exists, what the surrounding code does, and the decision(s) already made so the executor doesn't re-litigate them. Link the plan.>

## Files in scope (the fence)
> **These files only.** This is the complete set the executor may open and edit for this issue. If you find you need a file that is not listed, **stop and flag it on the issue** — do not go searching or expand scope on your own. The list below is the gold context; it was found by a real code-read so you don't have to hunt for it.

| File | Edit? | What / why |
|---|---|---|
| `path/to/file.ext:LINE` | edit | <precise change> |
| `path/to/other.ext:LINE` | read-only | <why the executor needs to see it> |
| ... | ... | ... |

## Implementation
<The literal work. Where you can produce it, include the actual code or a diff. Give exact function signatures, prop shapes, endpoint paths, payload shapes. Reference existing patterns to copy by file:line (e.g. "mirror the existing panel at components/SomePanel.tsx:73-111"). Leave nothing to guesswork.>

```<lang>
<literal code / patch when producible>
```

## Acceptance criteria
- [ ] <observable, checkable outcome>
- [ ] <observable, checkable outcome>

## Tests
<The exact test(s) to add or update — file, what to assert, how to run. If the repo has no test harness for this layer, say so and state the manual verification steps.>

## Verification / rollout
<How to confirm it works end-to-end: commands, the local run, what to click, any config bump / deploy step. Note anything that must be true in the environment.>

## Gotchas & permissions
<Traps discovered during the code-read: fragile string matches, auth requirements, permission gates, ordering hazards, backend contracts that must not break. The stuff that bites an executor who didn't do the investigation.>
```

## Rules for filling it
- **File anchors are mandatory** in "Files in scope" — `path:line`, not "the dashboard".
- **The fence is a closed set.** List every file the executor may touch, mark each edit vs read-only, and state the "these only — flag before wandering" boundary. If the fence sprawls across many unrelated areas, the slice is wrong: tighten it or justify the spread.
- **Prefer real code over prose.** If you can write the diff, write it. The executor should be transcribing, not designing.
- **Copyable precedent.** When a similar thing exists, point at it by `file:line` and say "mirror this."
- **Acceptance criteria are binary.** Each one is something you can check pass/fail, not a vibe.
- **State the order explicitly.** "Safe to start now" or "do not start until #N is merged" — say which.
