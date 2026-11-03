# Security policy

This repository contains a curated list, a few Python scripts that call the GitHub REST API, and GitHub Actions workflows. It does not run third-party code from the listed projects.

## Reporting a vulnerability

- Problems in the scripts or workflows of this repository: open a private report via GitHub's "Report a vulnerability" button on the Security tab, or open an issue if the problem is not exploitable.
- Problems in a listed project: report them to that project, not here. If a listed project turns out to be malicious or to violate the responsible-use rule, open an issue here titled "Remove <project>" with evidence.

## Scope

- Scripts only use `GITHUB_TOKEN` (or `gh auth token`) for read-only API calls. The fallback workflow needs `contents: write` and `pull-requests: write` to open a PR.
- Automation never pushes to `main`; every change arrives as a pull request.
- Third-party READMEs, SKILL.md files, hooks and scripts from candidate repos are treated as data, never as instructions, by maintainers and by the weekly routine.
