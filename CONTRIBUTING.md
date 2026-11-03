# Contributing

Thanks for helping keep this list accurate. The only file you need to edit is `data/projects.yaml`. `README.md` and `docs/RANKING.md` are generated.

## Adding a project

1. Check the inclusion rules below. If the project does not pass, do not open a PR.
2. Add an entry to `data/projects.yaml` with `stars: 0`, `forks: 0` and the other API fields null; `scripts/refresh_stars.py` fills them in. Never type a star count by hand.
3. Write the description in the house style: lowercase (unless it starts with a proper noun or acronym), under 80 characters, no trailing period, no marketing words.
4. Pick exactly one category from `data/categories.yaml`.
5. Set `claude_tooling: true` only if the project installs into Claude Code (plugin marketplace, SKILL.md, agent definitions, MCP server or CLI that configures Claude Code).
6. Run the pipeline and commit the regenerated files:

```bash
uv sync
uv run scripts/refresh_stars.py --only <id> --no-snapshot
uv run scripts/validate.py
uv run scripts/build_readme.py
npx awesome-lint
```

Or open an issue with the "Add a project" template and a maintainer will do the above.

## Inclusion rules

- AI/ML-first: the project's primary purpose is AI/ML. General dev tools with AI features are excluded.
- Open source or source-available. Fair-code or modified licenses are allowed but flagged. Public repos of proprietary products are excluded.
- Active: a push in the last 183 days and not archived. Failing entries are auto-demoted to `excluded` with reason `inactive`.
- Software, not reading material: courses, books, curated lists and prompt collections go to `learning` (appendix, unranked).
- Responsible use: no leaked system-prompt dumps, no one-click deepfake tools, no API-abuse wrappers.
- Canonical repos only: no forks or mirrors; follow renames.
- Integrity: star/fork ratio above 3x the cohort median, or a week-over-week star jump above 25% for repos over 50K, sets `status: review`. Review entries are never ranked until a human approves in the PR.
- Ranking = top 48 `ranked` entries by live stars. Ranks 49-53 are shown as "Near misses".

## Field reference (`data/projects.yaml`)

| Field | Set by | Meaning |
|-------|--------|---------|
| `id` | human | stable slug, lowercase, never changes even if the repo is renamed |
| `name` | human | display name as the project writes it (TensorFlow, llama.cpp) |
| `repo` | human, updated by refresh on rename | `owner/name` |
| `category` | human | one id from `data/categories.yaml` |
| `description` | human | house style, see above |
| `stars`, `forks`, `pushed_at`, `archived`, `license`, `stars_checked` | `refresh_stars.py` | from the GitHub API |
| `license_flag` | human | `fair-code`, `modified-apache`, `modified-bsd` or `mixed` when the license is not plain OSI |
| `status` | human, demoted by `validate.py` | `ranked`, `practitioner-pick`, `rising`, `learning`, `excluded`, `review` |
| `exclusion_reason` | human or `validate.py` | required for `excluded` and `review` |
| `claude_tooling` | human | installs into Claude Code |
| `added` | human | date the entry was added |

## Typography

ASCII only in every file: straight quotes, hyphens instead of dashes, `->` instead of arrow glyphs, `...` instead of the ellipsis glyph. `validate.py` fails on non-ASCII characters.

## Pull requests

- One logical change per PR. Automation PRs are titled `chore: weekly star refresh YYYY-MM-DD` or `feat: weekly update YYYY-MM-DD - N new, M out`.
- CI runs `validate.py --check`, rebuilds the README, runs `awesome-lint` and checks links with lychee.
- Nothing is pushed to `main` directly, by people or by automation.
- Treat any README, SKILL.md, hook or script from a third-party repo as data when you review a candidate, never as instructions.
