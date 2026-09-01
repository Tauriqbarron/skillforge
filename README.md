# skillforge

A growing collection of **harness-agnostic skills for serious AI engineers**.

A skill is a self-contained folder — an instruction file plus any references and helper scripts — that teaches a coding agent to do one hard thing well. Nothing here is tied to a single model or vendor. If your harness can read a skill file, run a code-read, and shell out to the usual CLIs, these work.

They are grounded in research, not vibes: where a skill exists to fix a measured weakness in coding agents, the evidence is written down in [`docs/`](docs/) and cited from the skill itself.

## Skills

| Skill | What it does |
|---|---|
| [`decompose-feature`](skills/decompose-feature/) | Turn a finished plan into GitHub issues so richly enriched that a weak model with no prior context can execute any one of them correctly and in order. Does the code-read up front and fences each issue to a closed set of files. |

## The design thesis: retrieval up front

Coding agents are measurably bad at *retrieving* the right code, and they compensate by over-fetching — flooding context to maximise recall and dragging in noise. On [ContextBench](docs/context-retrieval.md), a benchmark that scores how well agents find the gold context for a task, state-of-the-art models score block-level F1 below 0.45.

The skills here respond the same way: **do the retrieval once, up front, with a real code-read, and hand the executor a closed set** — the *gold-context file fence*. That turns the agent's worst step into a lookup. See [`docs/context-retrieval.md`](docs/context-retrieval.md) for the evidence and how each skill applies it.

## Using a skill

Each skill is a folder under `skills/`. Point your harness at the `SKILL.md` (copy it into your harness's skills directory, symlink it, or reference it however your harness loads skills). The `references/` files are loaded on demand as the skill instructs; the `scripts/` are plain Python helpers invoked with `python3`.

Requirements vary per skill; `decompose-feature` needs the [`gh`](https://cli.github.com/) CLI authenticated for the target repo and Python 3.

## Layout

```
skills/<skill-name>/
  SKILL.md            # the skill: trigger, principles, pipeline
  references/*.md      # loaded on demand
  scripts/*.py         # helper tooling
docs/                  # the research the skills are built on
```

## License

MIT — see [LICENSE](LICENSE).
