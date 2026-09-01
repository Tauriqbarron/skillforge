---
name: decompose-feature
description: Turn a completed project or feature plan into a set of richly-enriched, ready-to-execute GitHub issues on the relevant repo(s). Use when the user has a finished plan (a plan doc, spec, design, or the output of a planning session) and wants it broken down into GitHub issues, decomposed into tasks/tickets, or "sharded"/"sliced" into independently-pickup-able units of work. Runs a real code-read/impact pass first, decomposes into the smallest sensible vertical slices, then enriches every issue so heavily — exact files, line anchors, the literal code to write, acceptance criteria, dependencies, and ordering — that even a weak model with no prior context can execute any single issue. Triggers on "decompose", "break this plan into issues", "turn the plan into tickets", "create GitHub issues from the plan", "shard/slice this feature".
---

# Decompose Feature

Convert a finished plan into GitHub issues that are so complete a basic agent on a basic model can pick up any one of them and execute it correctly, in the right order, with no further investigation. All the reading, thinking, and design happens **up front** in this pipeline — not at execution time.

> Harness-agnostic. This skill is a set of instructions plus two helper scripts. It works in any agent harness that can read a skill file, run a code-read, and shell out to `gh`. Nothing here is tied to a specific model or vendor.

## Why the up-front enrichment matters

Coding agents are measurably bad at *retrieving* the right code. On ContextBench — a benchmark that scores how well agents find the gold context for a task rather than just whether the final patch passes — state-of-the-art models score block-level F1 below 0.45, and every model over-fetches: it floods its context to maximise recall and drags in noise, sacrificing precision. See [`docs/context-retrieval.md`](../../docs/context-retrieval.md).

This skill front-loads the retrieval so the executor never has to do the thing it is worst at. The code-read finds the real surface; the enriched issue hands it over as a closed set. That is the whole point of the **gold-context file fence** (principle 3.1).

## Operating principles (do not violate)

1. **Read before you cut.** Never decompose from the plan text alone. Do a real code-read of everything the change touches first. The decomposition must reflect the actual code surface, not the plan's guesses.
2. **Executable slices.** Each issue is independently pickup-able and sized to one focused PR. Prefer vertical slices (a thing that works end-to-end) over horizontal layers (all-the-types, then all-the-hooks). Split only where the seam is real.
3. **Self-sufficiency bar.** An enriched issue must let a weak agent execute with zero extra investigation. If the agent would have to go find a file, guess a signature, or re-derive a decision — that information is missing. See `references/enrichment-bar.md`.
   1. **Gold-context file fence.** Every issue names a *closed* set of files the executor is allowed to open and edit — the gold context for that slice — and says "these files only; if you think you need another, stop and flag it." The code-read already found the real surface; the fence hands it to the executor so it never has to search-and-over-fetch. An issue that touches files scattered across many far-apart areas is a decomposition smell: either slice it tighter or justify the spread on the issue. (Agents fail retrieval by wandering and flooding context — the fence is how the up-front read kills that at execution time.)
4. **Order lives on the issue.** Dependencies (`Blocked by #N`), sequence, and "safe to start now?" are written onto each issue, not held in your head or a side doc.
5. **Human gate before writing.** Draft the entire issue set and show it. Create nothing on GitHub until the user approves. Issue creation is outward-facing and hard to reverse.
6. **Traceable.** Every issue links to one tracking/epic issue and cites the source plan. The epic carries the full ordered checklist.
7. **Principle-based, inherited (optional).** If the project has a principles library or coding-standards doc, carry its basis into the decomposition: cite the relevant principle on any issue where a design choice is load-bearing, and flag tensions. If the source plan is already principle-sound this is light — you are reflecting its principles, not re-deriving them; a weak plan needs more here. Skip this cleanly if the project has no such library.
8. **Honor standing architectural rules.** Before cutting, load the target repo's standing constraints (its `CLAUDE.md` / `AGENTS.md` / equivalent, and any recalled project memory) — mandated service boundaries, migration directions, deprecated surfaces. Route **new** work to the sanctioned side of every such rule, and do not create issues that invest in a surface the repo is trying to leave. When a rule exists, an issue that violates it is a decomposition bug.
9. **Issue-tracker mirror when one exists (optional).** If the team also tracks work in Jira / Linear / a similar tracker, the decomposition can mirror there: enrich the parent ticket in **product-facing** language, and create a small set of **grouped subtasks** (not one per GH issue — bundle related slices). Every GH issue then carries a tracker link and every subtask carries the GH issue links it covers, so a PR references both. This is an adapter you write for your own tracker — see `references/tracker-adapter.md`.

## Pipeline

Run these stages in order. Use a todo list to track them.

### 1 · Intake
- Locate and fully read the plan (file path, pasted text, or a prior planning session's output). If no plan exists yet, stop and say so — this skill decomposes a *finished* plan; it does not write one.
- Identify the **target repo(s)** and their default branch. Verify with `gh api repos/<org>/<repo> --jq .default_branch` — do not trust local clone HEAD.
- Identify the **starter tracker ticket**, if any. Ask the user, or scan the plan for a tracker reference. If one exists, or if the user explicitly wants tracker representation, turn on the tracker track (stages 5b, 6b, 7b below). Otherwise skip those stages entirely — the tracker mirror is optional, not mandatory.
- Restate the plan's goal in one paragraph and the definition of done. Confirm scope with the user only if genuinely ambiguous.

### 2 · Code read / impact analysis
- Read every file the change plausibly touches — call sites, the data flow end to end, the tests, the config, and the layer boundaries. Fan out with parallel read-only agents when the surface is wide.
- Produce a **change map**: for each area, the files (with line anchors), the functions/endpoints/components involved, what currently exists, and what has to change. Note cross-repo touch-points and anything that turns out to be harder or different than the plan assumed. Surface these deltas to the user.
- If the plan's assumptions are wrong, say so now — a decomposition built on a wrong premise wastes every downstream issue.

### 3 · Decompose
- Cut the work into the smallest set of independently-executable units. Each unit → one issue.
- For each unit decide: does it stand alone, or is it blocked by another? Build the dependency graph and a topological order. Mark which units are **parallelisable** and which are the **critical path**.
- Pull cross-cutting concerns (a shared type, a new endpoint others depend on) to the front as their own early issues.
- See `references/decomposition-heuristics.md` for how to size and where to cut.

### 4 · Draft + enrich (the core value)
- For every issue, write the full body using `references/issue-template.md`.
- Then do a dedicated **enrichment pass** over the whole set against `references/enrichment-bar.md`: fill in exact file paths and line anchors, the literal code / diff to write where you can produce it, exact acceptance criteria and the test to add, the dependency lines, the permission/gotcha notes, and where this sits in the overall plan. **Close the fence on every issue** (principle 3.1): the complete file set, marked edit vs read-only, with the "these only — flag before wandering" boundary. Enrich until the bar is met for every issue.
- If a principles library applies, cite the relevant principle on issues where a design choice is load-bearing, and flag any tension.

### 5 · Assemble the manifest
- Write the decomposition to a JSON manifest at the path the create script expects (see `scripts/create_issues.py` header for the schema). One epic + N issues, each with `key`, `title`, `body`, `labels`, `depends_on` (keys), and optional per-issue `repo`.
- Keep the manifest in the repo's working area or a scratch dir; it is the reproducible source for creation and for re-runs.

### 5b · Assemble the tracker track (only if enabled in stage 1)
- **Enrich the parent ticket.** Rewrite the starter ticket's summary/description in **product-facing** language — what the change delivers, why it matters, what the user will see. No code, no file paths, no signatures. Cite constraints and the definition of done.
- **Group GH issues into subtasks.** Not one subtask per GH issue. Cluster related slices into a small set of coherent, reviewable pieces of work (typical: 3–6 subtasks). Each subtask has a product-facing title, a plain-language description of the outcome, and a `covers_issues` list of the GH issue keys it represents.
- Add the tracker block to the manifest. See `references/tracker-adapter.md` for the shape and how to wire your own tracker's API.

### 6 · Review gate
- Present: the change map, the ordered issue list (title + one-line scope + dependencies), and 1–2 fully-rendered example issue bodies so the user can judge the enrichment depth and the fence.
- If the tracker track is enabled, also present: the rewritten parent ticket (before/after), the subtask list (title + which GH issues each covers + starting status), and one fully-rendered subtask body.
- Get explicit approval. Adjust on feedback. **Do not create issues before this.**

### 7 · Create (GitHub)
- Verify `gh` can reach the target repo and account (`gh repo view <org>/<repo>`). If `gh` can't see the repo (org-scoped account, missing PAT scope), tell the user rather than failing mid-batch.
- Dry-run the script first (`python3 scripts/create_issues.py <manifest>` — dry-run is the default), show the plan, then create with `--create`.
- The script creates the epic, then each issue in dependency order, wires `Blocked by #N` / `Part of #<epic>` cross-references, ensures labels exist, and updates the epic with the ordered checklist.
- Report the created issue URLs and the recommended execution order.

### 7b · Create (tracker, only if enabled)
- Run after stage 7 so the GH issue numbers exist and can be linked back into the tracker.
- Use your tracker adapter (see `references/tracker-adapter.md`). The adapter should: (a) update the parent ticket description with the product-facing rewrite, (b) create each subtask under the parent, (c) for each subtask add a remote link to every GH issue in its `covers_issues`, (d) append a tracker-key line to each covered GH issue body, (e) optionally transition each subtask to a starting status.
- Report: parent ticket URL, subtask URLs with the GH issues each carries, and the current status each landed in.

## Notes
- Batch issue creation is a bulk outward-facing write. Confirm before running with `--create`; never create speculatively.
- If the feature spans repos, issues carry their own `repo`; the epic lives in the primary repo and references the others by full `owner/repo#N`.
- The goal is always the same: move all the hard thinking to now, so execution is mechanical.
