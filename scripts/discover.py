#!/usr/bin/env python3
"""Discover candidate repos via the GitHub search API and write data/candidates.json.

Two sweeps, both restricted to repos with more stars than the current #53 ranked entry
(or --min-stars):
  1. topic and keyword searches: ai, llm, agent, agents, mcp, claude-code, skills, rag,
     machine-learning, deep-learning, generative-ai, diffusion, inference
  2. repos created in the last 90 days with more than 20K stars (any topic)
Anything already present in data/projects.yaml (by repo, case-insensitive) is dropped.
The output is input for a human (or the weekly routine) to classify; nothing is added automatically.
"""

from __future__ import annotations

import argparse
import datetime as dt
import json
import sys

from _common import (API, CANDIDATES, NEAR_MISS_N, TOP_N, github_get, github_session,
                     load_projects, ranking_pool, today)

TERMS = ["ai", "llm", "agent", "agents", "mcp", "claude-code", "skills", "rag", "machine-learning",
         "deep-learning", "generative-ai", "diffusion", "inference"]
RECENT_DAYS = 90
RECENT_MIN_STARS = 20_000


def search(session, q: str, per_page: int = 50, pages: int = 2) -> list[dict]:
    out = []
    for page in range(1, pages + 1):
        resp = github_get(session, f"{API}/search/repositories",
                          params={"q": q, "sort": "stars", "order": "desc", "per_page": per_page, "page": page})
        if resp.status_code != 200:
            break
        items = resp.json().get("items", [])
        out.extend(items)
        if len(items) < per_page:
            break
    return out


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--min-stars", type=int, help="override the #53 threshold")
    ap.add_argument("--pages", type=int, default=2, help="search pages per query (50 results each)")
    args = ap.parse_args()

    projects = load_projects()
    known = {p["repo"].lower() for p in projects}
    pool = ranking_pool(projects)
    cutoff_index = TOP_N + NEAR_MISS_N - 1
    threshold = args.min_stars or (pool[cutoff_index]["stars"] if len(pool) > cutoff_index else pool[-1]["stars"])
    session = github_session()
    found: dict[str, dict] = {}

    def add(item: dict, source: str) -> None:
        name = item["full_name"]
        if name.lower() in known:
            return
        entry = found.setdefault(name, {
            "repo": name, "stars": item["stargazers_count"], "forks": item["forks_count"],
            "created_at": item["created_at"], "pushed_at": item["pushed_at"], "archived": item["archived"],
            "fork": item["fork"], "license": (item.get("license") or {}).get("spdx_id"),
            "description": (item.get("description") or "")[:200], "topics": item.get("topics", [])[:10],
            "url": item["html_url"], "sources": [],
        })
        if source not in entry["sources"]:
            entry["sources"].append(source)

    for term in TERMS:
        for q in (f"topic:{term} stars:>{threshold} fork:false archived:false",
                  f"{term} in:name,description stars:>{threshold} fork:false archived:false"):
            for item in search(session, q, pages=args.pages):
                add(item, q)
    since = (today() - dt.timedelta(days=RECENT_DAYS)).isoformat()
    for item in search(session, f"created:>{since} stars:>{RECENT_MIN_STARS} fork:false archived:false", pages=args.pages):
        add(item, f"created:>{since} stars:>{RECENT_MIN_STARS}")

    candidates = sorted(found.values(), key=lambda c: -c["stars"])
    CANDIDATES.write_text(json.dumps({
        "generated": today().isoformat(), "threshold_stars": threshold, "count": len(candidates),
        "candidates": candidates,
    }, indent=1) + "\n")
    print(f"threshold: {threshold} stars (current #{cutoff_index + 1}); {len(candidates)} candidates -> {CANDIDATES.name}")
    for c in candidates[:40]:
        print(f"{c['stars']:>8}  {c['repo']:<45} {c['description'][:70]}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
