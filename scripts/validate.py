#!/usr/bin/env python3
"""Validate data/projects.yaml and apply the mechanical inclusion rules.

Checks (errors fail the run):
  - schema: required fields, types, enums, id/repo format, description house style (ASCII,
    lowercase first letter, max 80 chars, no trailing period)
  - dedupe: unique ids, unique repos (case-insensitive)
  - excluded and review entries carry a reason
  - ASCII-only typography in every text file of the repo
Rules applied in place (reported, not errors; use --check to only report):
  - activity: not archived and pushed within 183 days, else status -> excluded, reason `inactive`
  - integrity: star/fork ratio above 3x the cohort median (cohort = ranked entries), or a
    week-over-week star jump above 25% for repos over 50K (vs the previous snapshot),
    sets status -> review. Review entries are never ranked until a human changes the status.
Warnings:
  - a practitioner-pick whose stars exceed the current #48 ranked entry (consider promoting)
"""

from __future__ import annotations

import argparse
import datetime as dt
import json
import re
import statistics
import sys

from _common import (ACTIVE_DAYS, LICENSE_FLAGS, ROOT, SNAPSHOTS, STATUSES, TOP_N, as_date,
                     load_categories, load_projects, ranking_pool, save_projects, today)

REQUIRED = {
    "id": str, "name": str, "repo": str, "category": str, "description": str, "stars": int,
    "forks": int, "archived": bool, "status": str, "claude_tooling": bool,
}
NULLABLE = ("stars_checked", "license", "license_flag", "pushed_at", "exclusion_reason")
ID_RE = re.compile(r"^[a-z0-9][a-z0-9-]*$")
REPO_RE = re.compile(r"^[A-Za-z0-9][A-Za-z0-9-]*/[A-Za-z0-9._-]+$")
TEXT_EXT = {".md", ".yaml", ".yml", ".py", ".j2", ".json", ".toml", ".txt", ".sh", ""}
TEXT_SKIP_DIRS = {".git", ".venv", "node_modules", "__pycache__"}
# Proper nouns and acronyms keep their case; these common words must not be capitalized.
CAPITALIZED_COMMON_WORDS = {"A", "An", "The", "This", "Your", "Our", "Run", "Build", "Fast", "Simple", "Open", "Free",
                            "Best", "Powerful", "Easy", "Self-hosted", "Lightweight", "High-performance", "Modern",
                            "Ultimate", "Next-gen", "Next-generation", "Blazing", "Production-ready", "Official"}


def check_schema(projects, categories, errors):
    cat_ids = {c["id"] for c in categories}
    seen_ids, seen_repos = {}, {}
    for i, p in enumerate(projects):
        where = f"entry {i} ({p.get('id', '?')})"
        for key, typ in REQUIRED.items():
            if key not in p:
                errors.append(f"{where}: missing field '{key}'")
            elif not isinstance(p[key], typ) or (typ is int and isinstance(p[key], bool)):
                errors.append(f"{where}: field '{key}' must be {typ.__name__}")
        for key in NULLABLE:
            if key not in p:
                errors.append(f"{where}: missing field '{key}' (may be null)")
        if "added" not in p or as_date(p.get("added")) is None:
            errors.append(f"{where}: 'added' must be a date")
        if not isinstance(p.get("id"), str) or not ID_RE.match(p["id"]):
            errors.append(f"{where}: id must match {ID_RE.pattern}")
        if not isinstance(p.get("repo"), str) or not REPO_RE.match(p["repo"]):
            errors.append(f"{where}: repo must be owner/name")
        if p.get("category") not in cat_ids:
            errors.append(f"{where}: unknown category '{p.get('category')}'")
        if p.get("status") not in STATUSES:
            errors.append(f"{where}: status must be one of {STATUSES}")
        if p.get("license_flag") not in (None,) + LICENSE_FLAGS:
            errors.append(f"{where}: license_flag must be null or one of {LICENSE_FLAGS}")
        d = p.get("description")
        if isinstance(d, str):
            if not d.strip():
                errors.append(f"{where}: empty description")
            elif len(d) > 80:
                errors.append(f"{where}: description longer than 80 chars ({len(d)})")
            elif d.split(" ")[0] in CAPITALIZED_COMMON_WORDS:
                errors.append(f"{where}: description must start lowercase (house style): {d!r}")
            if d.endswith("."):
                errors.append(f"{where}: description must not end with a period")
            if any(ord(ch) > 127 for ch in d):
                errors.append(f"{where}: description must be ASCII")
        if p.get("status") in ("excluded", "review") and not p.get("exclusion_reason"):
            errors.append(f"{where}: status {p['status']} requires exclusion_reason")
        pid = p.get("id")
        if pid in seen_ids:
            errors.append(f"{where}: duplicate id (also entry {seen_ids[pid]})")
        seen_ids[pid] = i
        rk = str(p.get("repo", "")).lower()
        if rk in seen_repos:
            errors.append(f"{where}: duplicate repo (also entry {seen_repos[rk]})")
        seen_repos[rk] = i


def check_ascii(errors):
    for path in ROOT.rglob("*"):
        if any(part in TEXT_SKIP_DIRS for part in path.parts) or not path.is_file():
            continue
        if path.suffix not in TEXT_EXT or path.name.endswith(".json") and "snapshots" in path.parts:
            continue
        try:
            text = path.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            errors.append(f"{path.relative_to(ROOT)}: not valid UTF-8")
            continue
        for ln, line in enumerate(text.splitlines(), 1):
            bad = [ch for ch in line if ord(ch) > 127]
            if bad:
                errors.append(f"{path.relative_to(ROOT)}:{ln}: non-ASCII character(s) {sorted(set(bad))}")
                break


def apply_activity(projects, day, changes):
    limit = day - dt.timedelta(days=ACTIVE_DAYS)
    for p in projects:
        if p["status"] == "excluded":
            continue
        pushed = as_date(p.get("pushed_at"))
        if p.get("archived"):
            reason = "inactive: repository is archived"
        elif pushed is not None and pushed < limit:
            reason = f"inactive: no push since {pushed.isoformat()} (limit {ACTIVE_DAYS} days)"
        else:
            continue
        changes.append(f"{p['id']}: {p['status']} -> excluded ({reason})")
        p["status"] = "excluded"
        p["exclusion_reason"] = reason


def previous_snapshot(day):
    files = sorted(SNAPSHOTS.glob("*.json")) if SNAPSHOTS.exists() else []
    files = [f for f in files if f.stem < day.isoformat()]
    if not files:
        return {}
    data = json.loads(files[-1].read_text())
    return {p["id"]: dict(p, date=data.get("date", files[-1].stem)) for p in data.get("projects", [])}


def apply_integrity(projects, day, changes, warnings):
    ranked = [p for p in projects if p["status"] == "ranked" and p["forks"] > 0 and p["stars"] > 0]
    if len(ranked) < 5:
        return
    median = statistics.median(p["stars"] / p["forks"] for p in ranked)
    limit = 3 * median
    prev = previous_snapshot(day)
    for p in projects:
        if p["status"] != "ranked":
            continue
        reasons = []
        if p["forks"] > 0 and p["stars"] / p["forks"] > limit:
            reasons.append(f"star/fork ratio {p['stars'] / p['forks']:.1f} above 3x cohort median ({median:.1f})")
        old = prev.get(p["id"])
        if old and old.get("stars") and p["stars"] > 50_000:
            jump = (p["stars"] - old["stars"]) / old["stars"]
            if jump > 0.25:
                reasons.append(f"star jump {jump:.0%} since {old.get('date', 'previous snapshot')}")
        if reasons:
            reason = "integrity: " + "; ".join(reasons) + ", pending human review"
            changes.append(f"{p['id']}: ranked -> review ({reason})")
            p["status"] = "review"
            p["exclusion_reason"] = reason
    pool = ranking_pool(projects)
    if len(pool) >= TOP_N:
        bar = pool[TOP_N - 1]["stars"]
        for p in projects:
            if p["status"] == "practitioner-pick" and p["stars"] > bar:
                warnings.append(f"{p['id']} (practitioner-pick, {p['stars']} stars) exceeds the #{TOP_N} ranked entry ({bar}); consider status: ranked")
    for p in projects:
        if p["status"] in ("ranked", "practitioner-pick", "rising") and not p.get("license"):
            warnings.append(f"{p['id']}: license is null (no detectable license file)")


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--check", action="store_true", help="report only; do not write projects.yaml")
    args = ap.parse_args()

    projects = load_projects()
    categories = load_categories()
    errors, warnings, changes = [], [], []
    day = today()

    check_schema(projects, categories, errors)
    check_ascii(errors)
    apply_activity(projects, day, changes)
    apply_integrity(projects, day, changes, warnings)

    if changes and not args.check:
        save_projects(projects)
    for c in changes:
        print(("would change: " if args.check else "changed: ") + c)
    for w in warnings:
        print("warning: " + w)
    for e in errors:
        print("error: " + e, file=sys.stderr)
    ranked = sum(1 for p in projects if p["status"] == "ranked")
    print(f"{len(projects)} entries, {ranked} ranked, {len(changes)} rule changes, {len(warnings)} warnings, {len(errors)} errors")
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
