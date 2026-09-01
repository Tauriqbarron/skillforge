# Contributing to skillforge

Contributions are welcome — a new skill, an improvement to an existing one, a sharper research citation, or a plain bug fix. This is a curated collection, so a PR is a proposal, not an automatic merge. The bar below is what gets one accepted.

## The bar

Every skill in this repo has to clear four things. A PR that adds or changes a skill is reviewed against them.

1. **Harness-agnostic.** No dependency on a specific model, vendor, or proprietary harness. If it only works in one tool, it does not belong here. Assume the reader is an agent that can read a skill file, do a code-read, and shell out to common CLIs.
2. **No internal or private leakage.** No employer-internal process, no private hostnames, project keys, board IDs, credentials, tokens, or personal data. Read credentials from the environment or an OS keychain — never hardcode them. If a skill needs an integration, ship the *contract* and let the user wire their own (see `skills/decompose-feature/references/tracker-adapter.md` for the pattern).
3. **Grounded, not vibes.** If a skill exists to fix a known weakness in coding agents, cite the evidence in `docs/` and link it from the skill. A design choice that counters a measured failure mode is worth more than a clever-sounding heuristic. See `docs/context-retrieval.md`.
4. **Front-load the hard thinking.** The house philosophy: do the expensive work (the code-read, the retrieval, the decisions) up front so execution is mechanical. A skill should make a *weak* executor succeed, not assume a strong one.

## Skill anatomy

A skill is a folder under `skills/<skill-name>/`:

```
skills/<skill-name>/
  SKILL.md            # required — YAML frontmatter (name + description) then the instructions
  references/*.md      # optional — loaded on demand, keep SKILL.md lean
  scripts/*            # optional — helper tooling, dry-run by default for anything that writes
```

- `SKILL.md` frontmatter needs a `name` (kebab-case, matching the folder) and a `description` that says *when to use it* with concrete trigger phrases — that's what a harness matches on.
- Keep `SKILL.md` focused; push detail and examples into `references/` so they load only when needed.
- Any script that performs an outward-facing or destructive action **must dry-run by default** and require an explicit flag (e.g. `--apply` / `--create`) to write.

## How to contribute

1. **Open an issue first** for anything non-trivial (a new skill, a behavioural change). Use the templates. A quick issue avoids you building something that won't merge. Typo/wording fixes can skip straight to a PR.
2. **Fork and branch.** Branch name like `skill/<name>` or `fix/<short-desc>`.
3. **Build it against the bar above.** Run the leak check on your diff before pushing:
   ```bash
   git grep -niE 'token|secret|password|@[a-z0-9.-]+\.(com|net|io)|[a-z0-9-]+\.atlassian\.net' -- 'skills/**' 'docs/**'
   ```
   Anything that hit should be an example placeholder, not a real value.
4. **Open a PR** using the template. Describe what the skill does, which bar items it clears, and — if it's research-grounded — what it cites.

## Review

The maintainer reviews against the four bar items and the anatomy. Expect requests to genericise anything harness-specific or internal. Merges are squash by default. Be patient — this is curated, not automated.

## License

By contributing you agree your contribution is licensed under the repo's [MIT License](LICENSE).
