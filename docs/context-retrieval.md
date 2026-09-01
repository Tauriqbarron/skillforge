# Context retrieval: the research these skills are built on

Several skills in this repo exist to fix a specific, measured weakness in coding agents: they are bad at **retrieving the right code**, and they compensate by over-fetching. This note records the evidence so the design choices in the skills have a citation, not just a hunch.

## The finding

**ContextBench: A Benchmark for Context Retrieval in Coding Agents** (Li et al., Nanjing University & University College London) evaluates *how* LLM coding agents find code when resolving a software issue, instead of only scoring whether the final patch passes tests.

- Paper: https://arxiv.org/abs/2602.05892 (HTML: https://arxiv.org/html/2602.05892v2)

For each of 1,136 tasks across 66 repositories and 8 languages, human experts traced the dependencies and marked the **gold context** — the exact files, blocks, and lines you actually need to read to solve the issue (~522k lines of verified gold context in total). Agent retrieval is then scored against that gold set as precision / recall / F1 at three granularities: file, AST block, and line.

## What they found

1. **Fancy scaffolding doesn't help retrieval.** Elaborate multi-step agent frameworks often don't beat simple baselines at finding the right code. Complexity is not the win.
2. **Even top models are bad at it.** Block-level F1 stays below 0.45. Agents do not reliably locate the code that matters.
3. **They over-fetch.** Every model floods context to maximise recall, tanking precision and dragging in noise.
4. **Balance beats brute force.** Models measured about how often and how granularly they retrieve get better line-level F1 *and* higher fix rates at lower cost.
5. **Finding ≠ using.** There is a big gap between what an agent explores and what it actually uses in the final patch. Consolidating found context into a fix is a real bottleneck.

## How the skills here respond

The through-line: **do the retrieval up front, once, with a real code-read, and hand the executor a closed set.** That converts the agent's worst step (search-and-over-fetch at execution time) into a lookup.

Concretely, in [`decompose-feature`](../skills/decompose-feature/SKILL.md):

- **Gold-context file fence** (operating principle 3.1). Every generated issue names the complete set of files in scope, marked edit vs read-only, with an explicit "these only — if you need another, stop and flag it, don't wander" boundary. This is a direct counter to finding #3 (over-fetching) and #2 (poor retrieval): the executor never has to find the surface, because the decomposition already did.
- **Scattered-edit smell.** An issue whose fence sprawls across many far-apart areas is flagged as a decomposition bug — tighten the slice or justify the spread. ContextBench selects *hard* tasks partly by edit dispersion; scattered edits are exactly what breaks retrieval, so the skill refuses to ship them unexamined.
- **Separate "find it" from "fix it."** The pipeline locates the seam (file:line) during decomposition, so the executor skips the consolidation step agents are worst at (finding #5).
- **Prefer the simple path.** The enrichment bar rewards a tight, transcribable issue over elaborate machinery — aligned with finding #1.

> Note: `2602.05892` is a recent preprint. Treat specific figures as of the cited version.
