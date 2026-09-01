# The enrichment bar

The test for whether an issue is enriched enough:

> **Could a weak model, opening only this issue with no other context and no ability to ask questions, execute it correctly and know when it's done?**

If any answer below is "it would have to go figure that out" — the issue is not done. Go back and add it.

## Checklist per issue

- [ ] **Location is exact.** Every file to touch is named with a line anchor. No "somewhere in the dashboard."
- [ ] **The fence is closed.** The issue declares the complete set of files in scope and states "these only — if another file seems needed, stop and flag it, don't wander." The executor knows its boundary before it starts, so it never searches the repo to find the surface. A fence spanning many scattered areas is a smell: tighten the slice or justify the spread.
- [ ] **The change is spelled out, not described.** The literal code/diff is present wherever it can be produced. Signatures, prop shapes, endpoint paths, and payload shapes are given, not implied.
- [ ] **Precedent is linked.** If the codebase already does this pattern, the issue points at it by `file:line` and says "copy this."
- [ ] **Decisions are pre-made.** Naming, placement, which library, which pattern — all decided here. The executor is not asked to choose.
- [ ] **Done is checkable.** Acceptance criteria are binary and observable. There is a concrete test or a concrete manual verification.
- [ ] **Order is stated.** Blocked-by / blocks are listed; "safe to start now" is explicit.
- [ ] **Traps are surfaced.** Anything the code-read revealed that would trip an unaware executor (auth gates, fragile parsing, backend contracts, env steps) is written down.
- [ ] **Context is self-contained.** The relevant slice of the plan is quoted/summarised in the issue. The executor does not need to read the whole plan to understand this piece.

## Anti-patterns (reject these)
- "Update the relevant components" — which files, which lines?
- "Add appropriate error handling" — what error, handled how, asserted where?
- "Follow existing patterns" — name the pattern and its `file:line`.
- "Wire up the backend" — which endpoint, which payload, which handler?
- An issue that only makes sense if you've read three other issues first — inline the dependency's relevant output.

## Sizing
- One issue ≈ one focused PR a competent contributor lands in well under a day.
- Too big: it has two unrelated acceptance sets, or touches two layers that could ship independently → split.
- Too small: it can't be verified on its own, or it's a fragment of one edit → merge upward.
