# Tracker adapter (optional)

The GitHub-issue decomposition is the core of this skill and needs no tracker. This file is for teams who *also* run an issue tracker (Jira, Linear, Asana, Azure Boards, …) and want the decomposition mirrored there in product-facing language.

There is deliberately no built-in adapter shipped here — trackers differ in auth, field names, and workflow, and hardcoding one would leak an org's internal setup. Write a small adapter for your own tracker following the contract below.

## The invariant

Every PR carries **both**:
- `Fixes #<N>` — the GitHub issue, the engineering view.
- `Tracker: <KEY>` — the tracker subtask, the product view.

So the code and the product view stay aligned, and a reviewer can jump either direction.

## Manifest block

The decomposition manifest (consumed by `scripts/create_issues.py` for the GitHub side) can carry an optional `tracker` block for your adapter to read:

```json
{
  "epic": { "...": "..." },
  "issues": [ { "key": "be-0", "...": "..." } ],
  "tracker": {
    "system": "jira",
    "parent_key": "TICKET-123",
    "parent_rewrite": {
      "summary": "<product-facing summary>",
      "description": "<what the change delivers, why it matters, what the user sees — no code, no file paths>"
    },
    "subtasks": [
      {
        "title": "<product-facing subtask title>",
        "description": "<plain-language outcome>",
        "covers_issues": ["be-0", "be-1"],
        "start_status": "Selected for Development"
      }
    ]
  }
}
```

## What the adapter must do (run after the GitHub issues exist)

1. **Rewrite the parent ticket** description with `parent_rewrite`. Product-facing only.
2. **Create each subtask** under the parent. Not one per GH issue — grouped (typically 3–6 subtasks total).
3. **Link back:** for each subtask, add a remote link to every GitHub issue in its `covers_issues`.
4. **Stamp the GH issues:** append a `Tracker: <KEY>` line to each covered GitHub issue body.
5. **Optional:** transition each subtask to its `start_status`.
6. **Report:** parent ticket URL, subtask URLs with the GH issues each carries, and the current status each landed in.

## Auth guidance

- Read credentials from the environment or the OS keychain — never hardcode a token, a tracker URL, a project key, or a workflow status ID in a committed file.
- Fail loudly with a clear "here's how to set your credentials" message if auth is missing, rather than prompting mid-run.
- Dry-run by default; require an explicit `--apply` flag to write.
