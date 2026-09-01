#!/usr/bin/env python3
"""
create_issues.py — create an epic + enriched issues on GitHub from a manifest.

DRY-RUN BY DEFAULT. Pass --create to actually write to GitHub. Uses the `gh`
CLI (must be authenticated for the target org).

Manifest schema (JSON):
{
  "repo": "owner/repo",                     # default repo for all issues + the epic
  "epic": {
    "title": "Epic: <feature>",
    "body":  "<markdown overview of the whole feature>",
    "labels": ["epic", "..."]               # optional
  },
  "issues": [
    {
      "key":   "E1",                         # stable local id, used for depends_on
      "title": "<issue title>",
      "body":  "<full enriched markdown body>",
      "labels": ["frontend", "..."],         # optional
      "depends_on": ["E0"],                  # optional, keys of blockers
      "repo":  "owner/other-repo"            # optional per-issue override
    }
  ]
}

Behaviour:
  * Ensures every label exists in each target repo (idempotent).
  * Creates the epic first.
  * Creates issues in dependency (topological) order.
  * Appends "Part of <epic-ref>" and "Blocked by <refs>" to each issue body,
    resolving depends_on keys -> real issue numbers (cross-repo aware).
  * Updates the epic body with an ordered checklist of every created issue.
  * Prints a table of created URLs and the recommended execution order.

Usage:
  python3 create_issues.py manifest.json            # dry-run: show the plan
  python3 create_issues.py manifest.json --create    # actually create
"""
import argparse
import json
import subprocess
import sys
from collections import defaultdict, deque


def run(args, check=True, capture=True):
    return subprocess.run(
        args, check=check,
        stdout=subprocess.PIPE if capture else None,
        stderr=subprocess.PIPE if capture else None,
        text=True,
    )


def gh_repo_ok(repo):
    r = run(["gh", "repo", "view", repo], check=False)
    return r.returncode == 0


def ensure_label(repo, label, dry):
    if dry:
        print(f"    [dry] ensure label '{label}' in {repo}")
        return
    # idempotent: create, ignore "already exists"
    run(["gh", "label", "create", label, "--repo", repo, "--force"], check=False)


def topo_order(issues):
    by_key = {i["key"]: i for i in issues}
    indeg = {i["key"]: 0 for i in issues}
    adj = defaultdict(list)
    for i in issues:
        for dep in i.get("depends_on", []):
            if dep not in by_key:
                sys.exit(f"ERROR: issue {i['key']} depends_on unknown key '{dep}'")
            indeg[i["key"]] += 1
            adj[dep].append(i["key"])
    q = deque([k for k, d in indeg.items() if d == 0])
    order = []
    while q:
        k = q.popleft()
        order.append(k)
        for nxt in adj[k]:
            indeg[nxt] -= 1
            if indeg[nxt] == 0:
                q.append(nxt)
    if len(order) != len(issues):
        sys.exit("ERROR: dependency cycle detected — re-cut the seam.")
    return [by_key[k] for k in order]


def ref(repo, number, primary_repo):
    """Cross-repo aware issue reference."""
    return f"#{number}" if repo == primary_repo else f"{repo}#{number}"


def create_issue(repo, title, body, labels, dry, fake_n):
    if dry:
        print(f"    [dry] create in {repo}: {title}  (labels: {labels or '-'})")
        return fake_n, f"https://github.com/{repo}/issues/{fake_n}"
    args = ["gh", "issue", "create", "--repo", repo, "--title", title, "--body", body]
    for l in labels or []:
        args += ["--label", l]
    r = run(args)
    url = r.stdout.strip().splitlines()[-1]
    number = int(url.rstrip("/").split("/")[-1])
    return number, url


def update_issue_body(repo, number, body, dry):
    if dry:
        print(f"    [dry] update body of {repo}#{number}")
        return
    run(["gh", "issue", "edit", str(number), "--repo", repo, "--body", body])


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("manifest")
    ap.add_argument("--create", action="store_true", help="actually write to GitHub (default: dry-run)")
    args = ap.parse_args()
    dry = not args.create

    with open(args.manifest) as f:
        m = json.load(f)

    primary = m["repo"]
    issues = topo_order(m["issues"])
    repos = {primary} | {i.get("repo", primary) for i in issues}

    print(f"{'DRY-RUN' if dry else 'CREATE'} — primary repo {primary}, "
          f"{len(issues)} issues across {len(repos)} repo(s)\n")

    if not dry:
        for r in repos:
            if not gh_repo_ok(r):
                sys.exit(f"ERROR: gh cannot access {r}. Check auth/account for that org.")

    # labels
    all_labels = set(m.get("epic", {}).get("labels", []))
    for i in issues:
        all_labels |= set(i.get("labels", []))
    for r in repos:
        for l in sorted(all_labels):
            ensure_label(r, l, dry)

    # epic first (so issues can reference it)
    epic = m["epic"]
    fake = 1000
    epic_n, epic_url = create_issue(primary, epic["title"], epic["body"],
                                    epic.get("labels", []), dry, fake)
    epic_ref = ref(primary, epic_n, primary)
    print(f"  epic -> {epic_url}\n")

    # issues in dependency order
    created = {}  # key -> (repo, number, url)
    fake += 1
    for i in issues:
        repo = i.get("repo", primary)
        blockers = []
        for dep in i.get("depends_on", []):
            drepo, dnum, _ = created[dep]
            blockers.append(ref(drepo, dnum, repo))
        header = [f"_Part of {ref(primary, epic_n, repo)}_"]
        if blockers:
            header.append(f"_Blocked by {', '.join(blockers)}_")
        body = "\n".join(header) + "\n\n" + i["body"]
        num, url = create_issue(repo, i["title"], body, i.get("labels", []), dry, fake)
        created[i["key"]] = (repo, num, url)
        fake += 1

    # epic checklist
    lines = [epic["body"], "", "## Issues (execution order)", ""]
    for i in issues:
        repo, num, _ = created[i["key"]]
        blk = i.get("depends_on", [])
        blk_txt = ""
        if blk:
            refs = ", ".join(ref(created[b][0], created[b][1], primary) for b in blk)
            blk_txt = f" — after {refs}"
        lines.append(f"- [ ] {ref(repo, num, primary)} {i['title']}{blk_txt}")
    update_issue_body(primary, epic_n, "\n".join(lines), dry)

    # report
    print("\n=== Result ===")
    print(f"Epic: {epic_url}")
    print("Execution order:")
    for idx, i in enumerate(issues, 1):
        repo, num, url = created[i["key"]]
        print(f"  {idx:>2}. {i['key']:<4} {url}")
    if dry:
        print("\n(DRY-RUN — nothing was created. Re-run with --create to write.)")


if __name__ == "__main__":
    main()
