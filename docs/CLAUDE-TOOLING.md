# Claude Code tooling guide

The top 8 projects in this list with `claude_tooling: true`, recomputed from `data/projects.yaml` on 2026-11-03, installed into Claude Code at user scope and smoke-tested. Everything below was reviewed before install: every hook, install script and MCP config was read as data, never executed from the repo. Claude Code version at install time: 2.1.316.

Rank order on 2026-11-03 (from data/snapshots/2026-11-03.json): superpowers (#2), mattpocock/skills (#3), ECC (#4), anthropics/skills (#12), ponytail (#14), agency-agents (#16), spec-kit (#22), ui-ux-pro-max-skill (#24). graphify (#25) and gstack (#26) were in the original shortlist and dropped to positions 9 and 10 among Claude tooling when mattpocock/skills and anthropics/skills entered; they are not installed.

A copy of this guide lives at `~/.claude/TOOLING.md`. The update script is `scripts/claude-tooling-update.sh` (copy at `~/.claude/claude-tooling-update.sh`).

## Summary

| Tool | Method | Pinned | Always-on context | Hooks | Risk notes |
|------|--------|--------|------------------:|-------|------------|
| superpowers | plugin `superpowers@claude-plugins-official` | 7.0.0, `bb92a777` | ~850 tok + ~3.4 KB injected per session start | 1 SessionStart (on) | none found |
| mattpocock/skills | plugin `mattpocock-skills@claude-plugins-official` | 1.3.1, `49dd158d` | ~1,650 tok | none | setup skill edits project CLAUDE.md |
| ECC | plugin `ecc@ecc` (marketplace affaan-m/ECC) | 2.2.3, `b38be6a7` | ~48,000 tok | 27 hooks, all OFF | observer logs tool I/O, Stop hook runs prettier, spawns `claude -p` (all off) |
| anthropics/skills | already present as synced plugin `anthropic-skills` | claude.ai-managed | per enabled skill | none | skill scripts spawn LibreOffice, Playwright, `claude -p` on invoke |
| ponytail | skills only, copied to `~/.claude/skills/ponytail*` | v5.3.3, `96608e07` | 6 skill descriptions | none installed (plugin has 3 + band mod) | plugin hooks run per prompt and per turn; not installed |
| agency-agents | 97 agent files in `~/.claude/agents/` | `b37b5bb3` | 97 agent descriptions | none | 16 personas declare WebFetch/WebSearch tools |
| spec-kit | `uv tool install specify-cli` from git tag | v1.2.6 | 10 project skills after `specify init` | none by default | `specify self upgrade` reaches the network |
| ui-ux-pro-max-skill | plugin `ui-ux-pro-max@ui-ux-pro-max-skill` | 2.15.0, `713eef51` | ~1,070 tok | none | design sub-skills read API keys from `~/.claude/.env` and call image APIs on invoke |

Total always-on context added by the installed set: roughly 52,000 tokens per session, of which ECC is about 48,000. If that is too much, `claude plugin disable ecc@ecc` and re-enable it for sessions where you want its agents.

## 1. superpowers (obra/superpowers)

**What and when.** Jesse Vincent's workflow skills: brainstorm before building, write a plan, red/green TDD, subagent-driven execution, systematic debugging, verification before claiming done. Use it for any non-trivial feature or bug where you want Claude to follow a disciplined process.

**Install.** `claude plugin install superpowers@claude-plugins-official --scope user`. Pinned 7.0.0 at commit `bb92a777` (upstream release is 7.0.1; the official marketplace lags by one patch). The security review read upstream `2ce8aa15` (7.0.1); the three hook files in the installed 7.0.0 copy were diffed against it and are identical. Files added: `~/.claude/plugins/cache/claude-plugins-official/superpowers/7.0.0/`, entry in `~/.claude/plugins/installed_plugins.json`, `enabledPlugins` in `~/.claude/settings.json`.

**Invoke.** No slash commands. Skills trigger on intent, or by name via the Skill tool: `superpowers:brainstorming`, `superpowers:writing-plans`, `superpowers:executing-plans`, `superpowers:test-driven-development`, `superpowers:systematic-debugging`, `superpowers:subagent-driven-development`, `superpowers:verification-before-completion`, `superpowers:using-git-worktrees`, `superpowers:requesting-code-review`, `superpowers:receiving-code-review`, `superpowers:finishing-a-development-branch`, `superpowers:writing-skills`, `superpowers:diagnosing-superpowers`. Example: start a fresh session and say "Let's build a CSV export for the orders page"; the brainstorming skill asks clarifying questions before any code.

**Hooks.** One SessionStart hook (`hooks/session-start`, matcher startup, clear, compact) that injects `skills/using-superpowers/SKILL.md` (about 3.4 KB) as context. No network, no credentials, no writes. To turn it off without losing the skills, disable the plugin for a session with `claude plugin disable superpowers@claude-plugins-official` (there is no per-hook switch).

**Update / uninstall.** `claude plugin marketplace update claude-plugins-official && claude plugin update superpowers@claude-plugins-official`. Uninstall: `claude plugin uninstall superpowers@claude-plugins-official`.

**Conflicts.** Same job, different names: its `test-driven-development` overlaps mattpocock `tdd` and ECC `tdd-workflow`; its `brainstorming` and `writing-plans` overlap ECC `/ecc:plan` and spec-kit `/speckit-plan`; its code-review skills overlap mattpocock `code-review`, ECC `/ecc:code-review` and `ponytail-review`. Its SessionStart text tells Claude to use a skill whenever one might apply, which makes it the loudest of the three workflow packs. Pick one process per project (see cheat sheet).

## 2. mattpocock/skills (Skills For Real Engineers)

**What and when.** Matt Pocock's small, composable engineering skills: spec writing, ticket splitting, grilling requirements, domain modelling, bug diagnosis, PR writing, retros. Use it when you want lightweight structure without a full methodology.

**Install.** `claude plugin install mattpocock-skills@claude-plugins-official --scope user`. Pinned 1.3.1 at `49dd158d` (upstream release is 1.3.2). The security review read upstream HEAD `4ae2317d` (1.3.2); the installed 1.3.1 commit was not diffed against it. The plugin ships no hooks or scripts that run automatically, so the exposure is limited to skill text. Files: `~/.claude/plugins/cache/claude-plugins-official/mattpocock-skills/1.3.1/`. The plugin ships 27 of the repo's 39 skills; 16 are user-invoked only (their descriptions do not load), 11 are model-invoked.

**Invoke.** Slash form of any skill, for example `/mattpocock-skills:ask-matt`, `/mattpocock-skills:grill-me`, `/mattpocock-skills:to-spec`, `/mattpocock-skills:to-tickets`, `/mattpocock-skills:diagnosing-bugs`, `/mattpocock-skills:pr`, `/mattpocock-skills:retro`, `/mattpocock-skills:wait-what`. Example: paste a vague feature request and run `/mattpocock-skills:grill-me`; it interrogates the requirements until they are unambiguous, then `/mattpocock-skills:to-tickets` splits them.

**Hooks.** None. The optional `git-guardrails-claude-code` skill (not in the plugin) would add a PreToolUse hook if you invoke it; nothing here does.

**Update / uninstall.** `claude plugin update mattpocock-skills@claude-plugins-official`; `claude plugin uninstall mattpocock-skills@claude-plugins-official`.

**Conflicts.** `tdd` vs superpowers `test-driven-development` and ECC `tdd-workflow`; `code-review` vs the built-in `/code-review`, superpowers review skills and ECC `/ecc:code-review`; `pr` vs ECC `/ecc:pr`. The `setup-matt-pocock-skills` skill appends an "Agent skills" block to the project CLAUDE.md; run it only in repos where you want that.

## 3. ECC (affaan-m/ECC)

**What and when.** A very large harness: 412 skills (as counted by Claude Code), 98 commands, 71 agents, language-specific reviewers and build resolvers, learning loops, and 27 hooks. Use it for its specialist agents (`ecc:security-reviewer`, `ecc:python-reviewer`, `ecc:build-error-resolver`, `ecc:architect`) and commands when you need breadth. It costs about 48,000 always-on tokens per session.

**Install.** `claude plugin marketplace add affaan-m/ECC && claude plugin install ecc@ecc --scope user --config hooks_enabled=false`. Pinned 2.2.3 at `b38be6a7`. Files: `~/.claude/plugins/cache/ecc/ecc/2.2.3/`, `pluginConfigs["ecc@ecc"].options.hooks_enabled = false` in `~/.claude/settings.json`. The bundled `.mcp.json` (which starts `npx -y chrome-devtools-mcp@1.10.1` every session) was renamed to `.mcp.json.disabled-by-user` in the cache copy so no MCP server auto-starts; a plugin update restores it and the update script re-applies the rename.

**Invoke.** Commands are namespaced: `/ecc:ecc-guide` (read-only overview), `/ecc:plan "add OAuth login"`, `/ecc:code-review`, `/ecc:security-scan`, `/ecc:test-coverage`, `/ecc:refactor-clean`, `/ecc:build-fix`. Agents via the Agent tool, for example `ecc:security-reviewer`. Example: `/ecc:plan "migrate the orders table to UUID keys"` produces a phased plan with risks.

**Hooks (all OFF until you opt in).** With hooks on, node runs on every tool call (observe runner, hookify), every prompt (hookify), every response (8 Stop hooks including prettier/biome/tsc on edited files, a console.log check, session summary, cost tracker, desktop notify), plus SessionStart, PreCompact and SessionEnd. Side effects when on: tool I/O logged to `~/.local/share/ecc-homunculus/`, state in `~/.gateguard`, sessions and metrics under `~/.claude/`, automatic `claude -p` calls for summaries (API spend), HTTP probes to your own MCP URLs. Opt in: `claude plugin configure ecc@ecc` and set `hooks_enabled=true` (or `/plugin configure ecc@ecc`); choose `hook_profile=minimal` first. Env overrides: `ECC_HOOKS_ENABLED=false`, `ECC_HOOK_PROFILE=minimal`, `ECC_DISABLED_HOOKS=id,id`, `ECC_SKIP_LLM_SUMMARY=1`.

**Update / uninstall.** `claude plugin marketplace update ecc && claude plugin update ecc@ecc`, then re-run the update script step that renames `.mcp.json`. Uninstall: `claude plugin uninstall ecc@ecc` and `claude plugin marketplace remove ecc`. ECC's own `npx ecc-universal@2.2.3 setup` wizard runs remote code and edits settings.json; it was not used.

**Conflicts.** Commands `plan`, `code-review` and skill `security-review` share names with Claude Code built-ins (ECC's are reachable only with the `ecc:` prefix, so nothing breaks). Skill `design-system` exists in both ECC and ui-ux-pro-max (the harness disambiguates by plugin prefix). Workflow overlap with superpowers and mattpocock as listed above. Its README asks you to copy `rules/` into `~/.claude/rules/ecc/`; not done.

## 4. anthropics/skills

**What and when.** Anthropic's reference skills: docx, pdf, pptx, xlsx document skills, plus examples (mcp-builder, skill-creator, canvas-design, web-artifacts-builder, brand-guidelines and others). Use them for document production and as templates when writing your own skills.

**Install.** Nothing new was installed. The same skills are already on this machine as the claude.ai-synced plugin `anthropic-skills` (`~/.claude/skills/synced/<id>/`), which is the supported distribution for this account. Installing `document-skills@anthropic-agent-skills` or `example-skills@anthropic-agent-skills` from the marketplace would load duplicate skill names. The repo's two non-duplicate plugins (`academy-guide`, `discernment-nudge`) were judged marginal and skipped.

**Invoke.** Enable individual synced skills in `~/.claude/settings.json` under `skillOverrides` (several are currently `"off"`, for example `anthropic-skills:pptx`, `anthropic-skills:docx`, `anthropic-skills:pdf`). Then invoke by name, for example `/anthropic-skills:xlsx` or "use the PDF skill to extract the form fields from invoice.pdf".

**Hooks.** None. On invoke, some skill scripts spawn LibreOffice (docx, pptx), Playwright (webapp-testing) or `claude -p` (skill-creator evals).

**Update / uninstall.** Managed by claude.ai sync; toggle in `skillOverrides`. To use the GitHub marketplace instead: `claude plugin marketplace add anthropics/skills` then `claude plugin install <plugin>@anthropic-agent-skills`.

**Conflicts.** Duplicate names with the synced plugin if installed from the marketplace; otherwise none.

## 5. ponytail (DietrichGebert/ponytail)

**What and when.** "Lazy senior dev mode": the smallest change that fully solves the task, YAGNI, and a reply a busy human reads once. Use it when Claude is over-engineering, or before accepting a design with many moving parts.

**Install.** Skills only. The six `skills/*` folders from commit `96608e07` (release v5.3.3) were copied to `~/.claude/skills/ponytail`, `ponytail-review`, `ponytail-audit`, `ponytail-debt`, `ponytail-gain`, `ponytail-help`; pin recorded in `~/.claude/skills/ponytail/PINNED.txt`. The full plugin (`/plugin marketplace add DietrichGebert/ponytail`, `/plugin install ponytail@ponytail`) was deliberately not installed: it adds a UserPromptSubmit hook on every prompt, a SessionStart hook that reads `~/.claude/settings.json`, runs `git ls-files` and bulk-reads sources, injects about 500 words into every session and subagent, nudges Claude to edit your statusline settings, and a band mod that greps the transcript and repo on every tool call and writes `~/.config/ponytail/band/*.csv` and `board.html` every turn.

**Invoke.** `/ponytail` (level report; "ponytail", "be lazy", "yagni" also trigger it), `/ponytail-review` (review a change for logic, safety, load, tests, and every unnecessary line), `/ponytail-audit` (whole-repo audit, changes nothing), `/ponytail-debt` (lists `shortcut:` comments), `/ponytail-help`. Example: after Claude proposes a plugin architecture for a one-off script, say "ponytail: is this over-engineered?".

**Hooks.** None installed. Without the plugin's mode tracker, level switching (`/ponytail lite|full|ultra`) is prompt-only and does not persist between sessions.

**Update / uninstall.** The update script diffs `skills/` between the pinned commit and upstream HEAD and re-copies on approval. Uninstall: `rm -rf ~/.claude/skills/ponytail*`.

**Conflicts.** `ponytail-review` overlaps the other review skills; `ponytail` overlaps ECC `refactor-clean` and `code-simplifier`. The skill asks Claude to leave `shortcut:` comments in code; superpowers' and ECC's review flows do not expect them.

## 6. agency-agents (msitarzewski/agency-agents)

**What and when.** A roster of expert subagent personas (Backend Architect, Frontend Developer, Security Architect, QA Automation Engineer, UX Researcher and so on). Use them for a specialist second opinion or to delegate a well-scoped task.

**Install.** From commit `b37b5bb3`: `scripts/install.sh --tool claude-code --division engineering,design,testing,security` copied 97 agent files into `~/.claude/agents/` (66 engineering, 10 design, 9 testing, 12 security). Pin in `~/.claude/agents/AGENCY-AGENTS-PINNED.txt`. The installer is plain bash, offline, and writes only to that directory. The other 14 divisions (marketing, sales, finance, gis, healthcare and more; 171 agents) were skipped to limit startup context; add one with `--division <name>`.

**Invoke.** Agents register under their display names from the file frontmatter, for example "Backend Architect", "Security Architect", "AI-Generated Code Security Auditor". Ask in plain language ("Activate Frontend Developer and help me build a React component") or pick them in the Agent tool. Example: "Have the Security Architect review the auth middleware in src/auth/ and report findings only".

**Hooks.** None. 16 personas declare WebFetch/WebSearch in their `tools:` and 7 of those also Bash; they can browse when delegated to.

**Update / uninstall.** The update script diffs the four division folders against upstream HEAD and re-copies on approval. Uninstall: delete `~/.claude/agents/{engineering,design,testing,security}-*.md` and the pin file.

**Conflicts.** Overlaps ECC's 71 agents by role (code-reviewer, security-reviewer, architect, tdd-guide). No name collisions because ECC agents carry the `ecc:` prefix.

## 7. spec-kit (github/spec-kit)

**What and when.** GitHub's spec-driven development: constitution, specify, clarify, plan, tasks, analyze, checklist, implement, converge. Use it for a new feature in a repo that benefits from a written spec and task list before code.

**Install.** `uv tool install --force "specify-cli @ git+https://github.com/github/spec-kit.git@v1.2.6"`. Pinned to tag v1.2.6. Files: `~/.local/share/uv/tools/specify-cli/`, `~/.local/bin/specify`. Nothing under `~/.claude`. Per project, `specify init --here --integration claude` (or `specify init <name> --integration claude`) writes `.claude/skills/speckit-*/SKILL.md` (10 skills) and `.specify/` (templates, bash scripts, memory/constitution.md). Smoke test done in a scratch project.

**Invoke.** In an initialised project: `/speckit-constitution`, `/speckit-specify "export orders as CSV with date filters"`, `/speckit-clarify`, `/speckit-plan`, `/speckit-tasks`, `/speckit-analyze`, `/speckit-checklist`, `/speckit-implement`, `/speckit-converge`, `/speckit-taskstoissues`. `specify check` verifies the CLIs it can see.

**Hooks.** None by default. Only an installed spec-kit extension that declares events writes hooks into the project `.claude/settings.json`; pass `--integration-options="--events false"` to prevent it.

**Update / uninstall.** `uv tool install --force "specify-cli @ git+https://github.com/github/spec-kit.git@vX.Y.Z"` with the new tag (the update script shows the latest release first); `specify integration upgrade claude` per project. Avoid `specify self upgrade` if you want the pin kept. Uninstall: `uv tool uninstall specify-cli`; per project `specify integration uninstall claude` or delete `.claude/skills/speckit-*` and `.specify/`.

**Conflicts.** `/speckit-plan` and `/speckit-specify` cover the same ground as superpowers brainstorming and writing-plans, mattpocock `to-spec`, and ECC `/ecc:plan` and `/ecc:plan-prd`.

## 8. ui-ux-pro-max-skill (nextlevelbuilder/ui-ux-pro-max-skill)

**What and when.** UI/UX design intelligence: a local BM25 search over curated style, palette, typography and component data, plus sub-skills for design systems, branding, banners, slides and shadcn/tailwind styling. Use it for landing pages, dashboards, design tokens and anything where "generic AI UI" is the risk.

**Install.** `claude plugin marketplace add nextlevelbuilder/ui-ux-pro-max-skill && claude plugin install ui-ux-pro-max@ui-ux-pro-max-skill --scope user`. Pinned 2.15.0 at `713eef51` (marketplace installs HEAD; the release tag v2.15.0 is older). Files: `~/.claude/plugins/cache/ui-ux-pro-max-skill/ui-ux-pro-max/2.15.0/`.

**Invoke.** Auto-activates on design phrasing ("Build a landing page for my SaaS product"), or by skill name: `ui-ux-pro-max:ui-ux-pro-max`, `:design`, `:design-system`, `:ui-styling`, `:brand`, `:banner-design`, `:slides`. Direct search: `python3 ~/.claude/plugins/cache/ui-ux-pro-max-skill/ui-ux-pro-max/2.15.0/.claude/skills/ui-ux-pro-max/scripts/search.py "glassmorphism" --domain style`. Example: "Design a dark analytics dashboard, fintech, no purple gradients; give me tokens and a component list".

**Hooks.** None. On invoke only: the `design` sub-skill's `generate.py` scripts read `~/.claude/.env` and `~/.claude/skills/.env` for `GEMINI_API_KEY`, `MUAPI_API_KEY`, `ATLASCLOUD_API_KEY` and call those image APIs (and ask for `pip install google-genai pillow`); `ui-styling` runs `npx shadcn` and `npm install`; `--persist` writes `design-system/<slug>/MASTER.md` into the project. Do not set those keys unless you want image generation.

**Update / uninstall.** `claude plugin marketplace update ui-ux-pro-max-skill && claude plugin update ui-ux-pro-max@ui-ux-pro-max-skill`; `claude plugin uninstall ui-ux-pro-max@ui-ux-pro-max-skill`.

**Conflicts.** `design-system` skill name also exists in ECC; agency-agents has UI Designer and UX Researcher personas that do design work without this data.

## Which one when

- New feature in a repo with a spec culture -> `specify init` then `/speckit-specify`, `/speckit-plan`, `/speckit-tasks`.
- New feature, lighter process -> superpowers brainstorming (just describe the feature in a fresh session), then `superpowers:writing-plans`.
- Vague request, unclear requirements -> `/mattpocock-skills:grill-me`, then `/mattpocock-skills:to-tickets`.
- Bug you cannot reproduce -> `superpowers:systematic-debugging` or `/mattpocock-skills:diagnosing-bugs`.
- "Am I over-engineering?" -> `/ponytail` or say "ponytail".
- Review before merge -> `/ponytail-review` for the honest short version; `superpowers:requesting-code-review` for the process version; `ecc:security-reviewer` for security.
- Specialist second opinion -> an agency agent by name ("Security Architect", "Backend Architect", "QA Automation Engineer").
- UI work -> ui-ux-pro-max (describe the page) or `/ui-ux-pro-max:design-system` for tokens.
- Language-specific build failure -> `ecc:build-error-resolver` or `/ecc:build-fix`.
- Documents (docx, pdf, pptx, xlsx) -> the synced anthropic-skills document skills.
- Unfamiliar codebase -> not covered by this set; graphify (rank 9 among Claude tooling) is the candidate if you add one.

## Updating all of it

Run `scripts/claude-tooling-update.sh` (or `~/.claude/claude-tooling-update.sh`). It refreshes the marketplaces, shows version and commit diffs for every pinned tool, and applies nothing until you answer yes. `--check` only shows the diff. After applying it re-asserts the two safety settings: ECC `hooks_enabled=false` and the renamed ECC `.mcp.json`.
