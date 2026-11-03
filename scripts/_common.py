"""Shared helpers for the awesome-ai-stars scripts (YAML I/O, paths, GitHub session)."""

from __future__ import annotations

import datetime as dt
import os
import subprocess
import sys
import time
from pathlib import Path

import requests
import yaml

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "data"
PROJECTS = DATA / "projects.yaml"
CATEGORIES = DATA / "categories.yaml"
SNAPSHOTS = DATA / "snapshots"
CANDIDATES = DATA / "candidates.json"
DOCS = ROOT / "docs"
TEMPLATES = ROOT / "templates"
API = "https://api.github.com"
LIST_REPO = "cartorjo/awesome-ai-stars"  # this list's own repo, used for absolute doc links

STATUSES = ("ranked", "practitioner-pick", "rising", "learning", "excluded", "review")
LICENSE_FLAGS = ("fair-code", "modified-apache", "modified-bsd", "mixed")
ACTIVE_DAYS = 183
TOP_N = 48
NEAR_MISS_N = 5

PROJECTS_HEADER = (
    "# Single source of truth for awesome-ai-stars. Edit this file, never README.md.\n"
    "# Field reference: see CONTRIBUTING.md. stars/forks/pushed_at/license/archived/"
    "stars_checked are written by scripts/refresh_stars.py.\n"
)


class _Dumper(yaml.SafeDumper):
    def ignore_aliases(self, data):  # never emit &id anchors
        return True


def load_projects() -> list[dict]:
    with PROJECTS.open() as f:
        return yaml.safe_load(f) or []


def load_categories() -> list[dict]:
    with CATEGORIES.open() as f:
        cats = yaml.safe_load(f) or []
    return sorted(cats, key=lambda c: c["order"])


def save_projects(projects: list[dict]) -> None:
    with PROJECTS.open("w") as f:
        f.write(PROJECTS_HEADER)
        yaml.dump(projects, f, Dumper=_Dumper, sort_keys=False, allow_unicode=False, width=1000)


def today() -> dt.date:
    return dt.datetime.now(dt.timezone.utc).date()


def as_date(value) -> dt.date | None:
    if value is None:
        return None
    if isinstance(value, dt.datetime):
        return value.date()
    if isinstance(value, dt.date):
        return value
    return dt.date.fromisoformat(str(value)[:10])


def github_token() -> str | None:
    token = os.environ.get("GITHUB_TOKEN") or os.environ.get("GH_TOKEN")
    if token:
        return token
    try:
        return subprocess.check_output(["gh", "auth", "token"], text=True, stderr=subprocess.DEVNULL).strip() or None
    except (OSError, subprocess.CalledProcessError):
        return None


def github_session() -> requests.Session:
    s = requests.Session()
    s.headers.update({
        "Accept": "application/vnd.github+json",
        "X-GitHub-Api-Version": "2022-11-28",
        "User-Agent": "awesome-ai-stars",
    })
    token = github_token()
    if token:
        s.headers["Authorization"] = f"Bearer {token}"
    else:
        print("warning: no GitHub token found; unauthenticated rate limit is 60 requests/hour", file=sys.stderr)
    return s


def github_get(session: requests.Session, url: str, params: dict | None = None, retries: int = 6) -> requests.Response:
    """GET with rate-limit and transient-error handling. Returns the response (200 or 404); raises otherwise."""
    for attempt in range(retries):
        resp = session.get(url, params=params, timeout=30)
        if resp.status_code in (200, 404):
            return resp
        if resp.status_code in (403, 429):
            retry_after = resp.headers.get("Retry-After")
            remaining = resp.headers.get("X-RateLimit-Remaining")
            reset = resp.headers.get("X-RateLimit-Reset")
            if retry_after:
                wait = int(retry_after)
            elif remaining == "0" and reset:
                wait = max(0, int(reset) - int(time.time())) + 2
            elif resp.status_code == 403:
                # A 403 that is not a rate limit (e.g. a sandbox proxy that only allows some
                # repositories) is a real answer; let the caller decide.
                return resp
            else:
                wait = 5 * (2 ** attempt)
            print(f"rate limited ({resp.status_code}) on {url}; sleeping {wait}s", file=sys.stderr)
            time.sleep(min(wait, 3600))
            continue
        if resp.status_code >= 500:
            time.sleep(2 ** attempt)
            continue
        resp.raise_for_status()
    raise RuntimeError(f"gave up after {retries} attempts: {url}")


def search_repos(session: requests.Session, repos: list[str], max_query_chars: int = 240) -> dict[str, dict]:
    """Look repos up through GET /search/repositories (qualifiers repo:owner/name OR'd per query).

    Returns {full_name_lower: item}. The search API returns the same fields as /repos/{owner}/{repo}
    (stargazers_count, forks_count, pushed_at, archived, license, default_branch). It is the fallback
    for environments whose GitHub proxy blocks /repos/{owner}/{repo} for repositories other than the
    session's own, such as Claude Code cloud routines. Rate limit: 30 requests/minute when authenticated.
    """
    found: dict[str, dict] = {}
    chunks: list[list[str]] = [[]]
    for r in repos:  # GitHub caps a search query at 256 characters; "fork:true" keeps forks visible
        if chunks[-1] and len(" ".join(f"repo:{x}" for x in chunks[-1] + [r])) + len(" fork:true") > max_query_chars:
            chunks.append([])
        chunks[-1].append(r)
    for chunk in chunks:
        q = " ".join(f"repo:{r}" for r in chunk) + " fork:true"
        resp = github_get(session, f"{API}/search/repositories", params={"q": q, "per_page": 100})
        if resp.status_code != 200:
            print(f"warning: search lookup failed ({resp.status_code}) for {chunk}", file=sys.stderr)
            continue
        for item in resp.json().get("items", []):
            found[item["full_name"].lower()] = item
        time.sleep(2.1)  # stay under 30 search requests per minute
    return found


def fmt_stars(n: int) -> str:
    if n >= 1_000_000:
        return f"{n / 1_000_000:.2f}M"
    if n >= 1_000:
        return f"{n / 1_000:.1f}K"
    return str(n)


def ranking_pool(projects: list[dict]) -> list[dict]:
    """All `ranked` entries sorted by stars descending (ties broken by forks, then id)."""
    pool = [p for p in projects if p["status"] == "ranked"]
    return sorted(pool, key=lambda p: (-(p.get("stars") or 0), -(p.get("forks") or 0), p["id"]))
