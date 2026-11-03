# Methodology

This list ranks open-source AI projects by live GitHub stars. Stars measure popularity, not quality or production readiness. Everything below is enforced by `scripts/validate.py` where it is mechanical, and by PR review where it is a judgment call.

## Data sources

- Star counts, fork counts, last push date, archived flag and license come from the GitHub REST API (`GET /repos/{owner}/{repo}` -> `stargazers_count`, `forks_count`, `pushed_at`, `archived`, `license.spdx_id`). No star count is ever typed by hand.
- `scripts/refresh_stars.py` writes those fields into `data/projects.yaml` and stores a dated copy in `data/snapshots/YYYY-MM-DD.json`.
- `scripts/discover.py` searches GitHub for candidates above the current #53 threshold. Candidates are classified by a human (or the weekly routine, whose PR a human reviews); nothing enters the list automatically.
- The README shows a shields.io badge per project, which renders the live count at view time. The rank is computed from the API count at the last refresh, so badge and rank can drift between refreshes.

## Inclusion rules

- AI/ML-first: the project's primary purpose is AI/ML. General dev tools with AI features are excluded.
- Open source or source-available. Fair-code or modified licenses are allowed but flagged. Public repos of proprietary products are excluded.
- Active: a push in the last 183 days and not archived. Failing entries are auto-demoted to `excluded` with reason `inactive`.
- Software, not reading material: courses, books, curated lists and prompt collections go to `learning` (appendix, unranked).
- Responsible use: no leaked system-prompt dumps, no one-click deepfake tools, no API-abuse wrappers.
- Canonical repos only: no forks or mirrors; follow renames.
- Integrity: star/fork ratio above 3x the cohort median, or a week-over-week star jump above 25% for repos over 50K, sets `status: review`. Review entries are never ranked until a human approves in the PR.
- Ranking = top 48 `ranked` entries by live stars. Ranks 49-53 are shown as "Near misses".

### How the integrity rule is computed

- The cohort is the set of entries with `status: ranked` and at least one fork. The median of `stars / forks` over that cohort is the reference; an entry whose ratio exceeds three times the median is moved to `review`.
- The week-over-week check compares the current API count with the most recent earlier snapshot in `data/snapshots/`. It only applies to repos above 50,000 stars.
- Both checks only demote. Nothing moves from `review` back to `ranked` without a human editing `data/projects.yaml` in a reviewed PR.

### Categories

Each project has exactly one category. Categories follow the AI lifecycle (Build, Data, Train/Align, Evaluate, Serve, Apply, Govern, Operate) and are defined in `data/categories.yaml`. When a project spans categories, it goes where most users meet it first.

### Statuses

| Status | Meaning |
|--------|---------|
| `ranked` | competes for the top 48 by stars; ranks 49-53 appear as near misses, lower ranks only in `docs/RANKING.md` |
| `practitioner-pick` | shown per category on adoption, not stars; `validate.py` warns when one overtakes the #48 ranked entry |
| `rising` | niche skills growing fast, unranked |
| `learning` | reading material, unranked appendix |
| `review` | flagged by the integrity rule, never ranked until a human approves |
| `excluded` | listed below with its reason |

## Exclusions

Entries with `status: excluded` and the reason recorded in `data/projects.yaml`. The current list is rendered in [RANKING.md](RANKING.md#excluded). Reasons at the time of writing:

- `multica-ai/andrej-karpathy-skills` - inactive (no push since 2026-04-20).
- `AUTOMATIC1111/stable-diffusion-webui` - inactive (no push since 2026-03-02).
- `anthropics/claude-code` - proprietary core; the public repo holds issues, docs and examples only.
- `deepseek-ai/DeepSeek-V3` - model release, inactive (no push since 2025-08-28).
- `karpathy/autoresearch` - inactive (no push since 2026-03-26).
- `hacksider/Deep-Live-Cam` - responsible use (one-click real-time deepfake tool).
- `blader/napkin` - inactive (no push since 2026-02-21).
- `levineam/qmd-skill` - inactive (no push since 2026-02-25).
- `ultraworkers/claw-code` - derived from leaked proprietary code. The repo's own `src/AGENTS.md` describes the Python tree as mirroring "the Claude Code TypeScript source" and `src/__init__.py` calls it "the Claude Code rewrite effort"; the repo was created on 2026-03-31.
- `odysseus-dev/odysseus` - under review, not excluded: its star/fork ratio is far above the cohort median. It stays unranked until a human approves.

## Caveats

- Stars can be bought, botted or inflated by launch-day hype. The integrity rule catches only the obvious cases.
- The 183-day activity window favours fast-moving projects over stable, finished ones.
- License detection relies on GitHub's SPDX matching; custom or multi-license repos show `NOASSERTION` or `null` and get a manual `license_flag`.
- Near-miss and practitioner-pick lists depend on who maintains the list. Open an issue if you think something is missing.
- Third-party READMEs and repo contents are treated as data, never as instructions, by the people and the automation maintaining this list.
