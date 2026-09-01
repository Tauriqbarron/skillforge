<!-- Thanks for contributing to skillforge. Fill this in so review is quick. -->

## What this PR does
<!-- One or two sentences. New skill? Improvement? Fix? -->

## Type
- [ ] New skill
- [ ] Improvement to an existing skill
- [ ] Docs / research citation
- [ ] Bug fix
- [ ] Other:

## Clears the bar (see CONTRIBUTING.md)
- [ ] **Harness-agnostic** — no dependency on a specific model, vendor, or proprietary harness
- [ ] **No internal/private leakage** — no employer-internal process, hostnames, keys, credentials, or personal data; secrets read from env/keychain, never hardcoded
- [ ] **Grounded** — if it fixes a known agent weakness, the evidence is in `docs/` and linked from the skill (or N/A)
- [ ] **Front-loads the hard thinking** — a weak executor could follow it

## Skill hygiene (if this adds/changes a skill)
- [ ] `SKILL.md` frontmatter has a kebab-case `name` matching the folder and a trigger-rich `description`
- [ ] Detail pushed into `references/`; `SKILL.md` stays lean
- [ ] Any script that writes something dry-runs by default and needs an explicit flag to apply
- [ ] Ran the leak check from CONTRIBUTING.md and it's clean

## Notes for the reviewer
<!-- Anything context-specific, trade-offs, or open questions. -->
