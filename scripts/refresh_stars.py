#!/usr/bin/env python3
"""Refresh stars, forks, pushed_at, license and archived for every entry in data/projects.yaml
from the GitHub REST API (GET /repos/{owner}/{repo}), then write data/snapshots/YYYY-MM-DD.json.

- Renamed repos (HTTP 301, followed automatically) update `repo` and keep `id`.
- Repos that 404 are demoted to `status: excluded` with reason `not-found`.
- Rate limits are honoured via Retry-After / X-RateLimit-Reset.
Never type a star count by hand; run this script instead.
"""

from __future__ import annotations

import argparse
import json
import sys

from _common import (API, SNAPSHOTS, github_get, github_session, load_projects, ranking_pool,
                     save_projects, today)


def fetch_repo(session, repo: str) -> dict | None:
    resp = github_get(session, f"{API}/repos/{repo}")
    if resp.status_code == 404:
        return None
    return resp.json()


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--only", nargs="*", help="refresh only these ids")
    ap.add_argument("--no-snapshot", action="store_true", help="do not write data/snapshots/<date>.json")
    args = ap.parse_args()

    projects = load_projects()
    session = github_session()
    day = today()
    renamed, missing, errors = [], [], []
    seen: dict[str, str] = {}

    for p in projects:
        if args.only and p["id"] not in args.only:
            continue
        try:
            data = fetch_repo(session, p["repo"])
        except Exception as exc:  # network or 5xx after retries: keep old values, report
            errors.append((p["id"], str(exc)))
            continue
        if data is None:
            missing.append(p["id"])
            if p["status"] != "excluded":
                p["status"] = "excluded"
                p["exclusion_reason"] = f"not-found: GitHub returned 404 on {day.isoformat()}"
            p["stars_checked"] = day
            continue
        full_name = data["full_name"]
        if full_name.lower() != p["repo"].lower():
            renamed.append((p["id"], p["repo"], full_name))
            p["repo"] = full_name
        if full_name.lower() in seen:
            errors.append((p["id"], f"resolves to the same repo as '{seen[full_name.lower()]}' ({full_name}); dedupe needed"))
        seen[full_name.lower()] = p["id"]
        p["stars"] = int(data.get("stargazers_count") or 0)
        p["forks"] = int(data.get("forks_count") or 0)
        p["pushed_at"] = data.get("pushed_at")
        p["archived"] = bool(data.get("archived"))
        lic = (data.get("license") or {}).get("spdx_id")
        p["license"] = lic if lic else None
        p["stars_checked"] = day

    save_projects(projects)

    if not args.no_snapshot:
        SNAPSHOTS.mkdir(parents=True, exist_ok=True)
        ranks = {p["id"]: i + 1 for i, p in enumerate(ranking_pool(projects))}
        snap = {
            "date": day.isoformat(),
            "source": "GET https://api.github.com/repos/{owner}/{repo}",
            "projects": [
                {
                    "id": p["id"], "repo": p["repo"], "category": p["category"], "status": p["status"],
                    "rank": ranks.get(p["id"]), "stars": p["stars"], "forks": p["forks"],
                    "pushed_at": p["pushed_at"], "archived": p["archived"], "license": p["license"],
                }
                for p in projects
            ],
        }
        path = SNAPSHOTS / f"{day.isoformat()}.json"
        path.write_text(json.dumps(snap, indent=1) + "\n")
        print(f"snapshot written: {path.relative_to(path.parents[2])}")

    print(f"refreshed {len(projects)} entries on {day.isoformat()}")
    for pid, old, new in renamed:
        print(f"renamed: {pid}: {old} -> {new}")
    for pid in missing:
        print(f"not found (404), demoted to excluded: {pid}")
    for pid, msg in errors:
        print(f"error: {pid}: {msg}", file=sys.stderr)
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
