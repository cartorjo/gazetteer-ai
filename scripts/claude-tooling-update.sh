#!/usr/bin/env bash
# Update the Claude Code tools installed per docs/CLAUDE-TOOLING.md, pinned-version aware.
# Shows what would change first; applies only after an explicit yes. ASCII only.
#
#   claude-tooling-update.sh            show diffs, then ask before applying
#   claude-tooling-update.sh --check    show diffs only
#   claude-tooling-update.sh --yes      apply without asking (for people who read the diff last time)
set -euo pipefail

CLAUDE_DIR="${CLAUDE_CONFIG_DIR:-$HOME/.claude}"
INSTALLED="$CLAUDE_DIR/plugins/installed_plugins.json"
MODE="ask"
case "${1:-}" in --check) MODE="check";; --yes) MODE="yes";; "") ;; *) echo "usage: $0 [--check|--yes]"; exit 2;; esac

# plugin id | marketplace | notes
PLUGINS=(
  "superpowers@claude-plugins-official|claude-plugins-official"
  "mattpocock-skills@claude-plugins-official|claude-plugins-official"
  "ecc@ecc|ecc"
  "ui-ux-pro-max@ui-ux-pro-max-skill|ui-ux-pro-max-skill"
)
# git-sourced copies: name | repo | pin file | subpaths copied
PONYTAIL_PIN="$CLAUDE_DIR/skills/ponytail/PINNED.txt"
AGENCY_PIN="$CLAUDE_DIR/agents/AGENCY-AGENTS-PINNED.txt"
AGENCY_DIVISIONS="engineering,design,testing,security"
SPECKIT_PIN_TAG="v1.2.6"

TMP="$(mktemp -d)"; trap 'rm -rf "$TMP"' EXIT
CHANGES=0

say() { printf '%s\n' "$*"; }
hr() { printf -- '---------------------------------------------------------------\n'; }

installed_field() {  # plugin-id field
  python3 - "$INSTALLED" "$1" "$2" <<'PY'
import json, sys
d = json.load(open(sys.argv[1])); e = (d.get("plugins", {}).get(sys.argv[2]) or [{}])[0]
print(e.get(sys.argv[3], ""))
PY
}

pin_value() { grep -E "^$2:" "$1" 2>/dev/null | sed 's/^[^:]*: *//' || true; }

hr; say "1. Marketplaces"
for m in $(for spec in "${PLUGINS[@]}"; do echo "${spec#*|}"; done | sort -u); do claude plugin marketplace update "$m" >/dev/null 2>&1 && say "  refreshed $m" || say "  warning: could not refresh $m"; done

hr; say "2. Plugins (installed -> available)"
PLUGIN_UPDATES=()
for spec in "${PLUGINS[@]}"; do
  id="${spec%%|*}"; m="${spec#*|}"; name="${id%@*}"
  cur_ver="$(installed_field "$id" version)"; cur_sha="$(installed_field "$id" gitCommitSha)"
  cache_root="$CLAUDE_DIR/plugins/marketplaces/$m"
  avail_ver="$(python3 - "$cache_root" "$name" <<'PY'
import json, os, sys
root, name = sys.argv[1], sys.argv[2]
mp = os.path.join(root, ".claude-plugin", "marketplace.json")
try:
    data = json.load(open(mp))
except Exception:
    print("?"); sys.exit()
for p in data.get("plugins", []):
    if p.get("name") == name:
        src = p.get("source")
        if isinstance(src, dict) and src.get("sha"):
            print("sha:" + src["sha"]); sys.exit()   # official marketplace pins by commit
        if isinstance(src, str) and src.startswith("."):
            pj = os.path.join(root, src, ".claude-plugin", "plugin.json")
            try:
                print(json.load(open(pj)).get("version", "?")); sys.exit()
            except Exception:
                pass
        print(p.get("version", "?")); sys.exit()
print("?")
PY
)"
  case "$avail_ver" in
    sha:*) avail_sha="${avail_ver#sha:}"
           if [ "$avail_sha" != "$cur_sha" ]; then say "  $id: $cur_ver ($cur_sha) -> commit $avail_sha   [UPDATE AVAILABLE]"; PLUGIN_UPDATES+=("$id"); CHANGES=$((CHANGES+1))
           else say "  $id: $cur_ver ($cur_sha) -> same commit (unchanged)"; fi ;;
    *)     if [ "$avail_ver" != "?" ] && [ "$avail_ver" != "$cur_ver" ]; then say "  $id: $cur_ver ($cur_sha) -> $avail_ver   [UPDATE AVAILABLE]"; PLUGIN_UPDATES+=("$id"); CHANGES=$((CHANGES+1))
           else say "  $id: $cur_ver ($cur_sha) -> ${avail_ver} (unchanged)"; fi ;;
  esac
done

git_diff_report() {  # name repo pin_sha subpath...
  local name="$1" repo="$2" pin="$3"; shift 3
  local dir="$TMP/$name"
  git clone -q --filter=blob:none "https://github.com/$repo.git" "$dir" 2>/dev/null || { say "  $name: clone failed"; return 1; }
  local head; head="$(git -C "$dir" rev-parse HEAD)"
  if [ "$head" = "$pin" ]; then say "  $name: $pin (unchanged)"; return 1; fi
  say "  $name: $pin -> $head   [UPDATE AVAILABLE]"
  git -C "$dir" diff --stat "$pin" "$head" -- "$@" 2>/dev/null | tail -15 | sed 's/^/      /' || say "      (pinned commit not reachable from HEAD; history rewritten?)"
  printf '%s' "$head" > "$TMP/$name.head"; CHANGES=$((CHANGES+1))
}

hr; say "3. Git-sourced copies"
PONY_PIN_SHA="$(pin_value "$PONYTAIL_PIN" commit)"; AG_PIN_SHA="$(pin_value "$AGENCY_PIN" commit)"
[ -n "$PONY_PIN_SHA" ] && git_diff_report ponytail DietrichGebert/ponytail "$PONY_PIN_SHA" skills/ || true
[ -n "$AG_PIN_SHA" ] && git_diff_report agency-agents msitarzewski/agency-agents "$AG_PIN_SHA" ${AGENCY_DIVISIONS//,/ } scripts/install.sh scripts/lib.sh || true

hr; say "4. spec-kit"
SPEC_LATEST="$(gh api repos/github/spec-kit/releases/latest --jq .tag_name 2>/dev/null || curl -fsSL https://api.github.com/repos/github/spec-kit/releases/latest | python3 -c 'import json,sys; print(json.load(sys.stdin)["tag_name"])' 2>/dev/null || echo '?')"
SPEC_CUR="$(specify --version 2>/dev/null | tr -dc '0-9.' || echo '?')"
if [ "$SPEC_LATEST" != "?" ] && [ "v$SPEC_CUR" != "$SPEC_LATEST" ]; then say "  specify-cli: v$SPEC_CUR -> $SPEC_LATEST   [UPDATE AVAILABLE]"; CHANGES=$((CHANGES+1)); else say "  specify-cli: v$SPEC_CUR -> $SPEC_LATEST (unchanged)"; fi

hr; say "5. graphify (PyPI graphifyy)"
GRAPHIFY_CUR="$(graphify --version 2>/dev/null | tr -dc '0-9.' || echo '?')"
GRAPHIFY_LATEST="$(curl -fsSL https://pypi.org/pypi/graphifyy/json 2>/dev/null | python3 -c 'import json,sys; print(json.load(sys.stdin)["info"]["version"])' 2>/dev/null || echo '?')"
if [ "$GRAPHIFY_LATEST" != "?" ] && [ "$GRAPHIFY_CUR" != "$GRAPHIFY_LATEST" ]; then say "  graphifyy: $GRAPHIFY_CUR -> $GRAPHIFY_LATEST   [UPDATE AVAILABLE]"; CHANGES=$((CHANGES+1)); else say "  graphifyy: $GRAPHIFY_CUR -> $GRAPHIFY_LATEST (unchanged)"; fi

hr; say "6. rtk (Homebrew)"
RTK_CUR="$(rtk --version 2>/dev/null | tr -dc '0-9.' || echo '?')"
RTK_OUTDATED="$(brew outdated --quiet rtk 2>/dev/null || true)"
if [ -n "$RTK_OUTDATED" ]; then say "  rtk: $RTK_CUR -> $(brew info --json=v2 rtk 2>/dev/null | python3 -c 'import json,sys; print(json.load(sys.stdin)["formulae"][0]["versions"]["stable"])' 2>/dev/null || echo newer)   [UPDATE AVAILABLE]"; CHANGES=$((CHANGES+1)); else say "  rtk: $RTK_CUR (unchanged)"; fi

hr
if [ "$CHANGES" -eq 0 ]; then say "Nothing to update."; exit 0; fi
[ "$MODE" = "check" ] && { say "$CHANGES update(s) available. Re-run without --check to apply."; exit 0; }
if [ "$MODE" = "ask" ]; then
  read -r -p "Apply the $CHANGES update(s) above? [y/N] " ans
  [ "$ans" = "y" ] || [ "$ans" = "Y" ] || { say "Not applied."; exit 0; }
fi

hr; say "Applying"
for id in "${PLUGIN_UPDATES[@]:-}"; do [ -n "$id" ] && { claude plugin update "$id" && say "  updated $id -> $(installed_field "$id" version) ($(installed_field "$id" gitCommitSha))"; }; done
if [ -f "$TMP/ponytail.head" ]; then
  head="$(cat "$TMP/ponytail.head")"
  for s in ponytail ponytail-review ponytail-audit ponytail-debt ponytail-gain ponytail-help; do rm -rf "$CLAUDE_DIR/skills/$s"; cp -R "$TMP/ponytail/skills/$s" "$CLAUDE_DIR/skills/$s"; done
  printf 'source: https://github.com/DietrichGebert/ponytail\ncommit: %s\ninstalled: %s\nmethod: skills only (skills/* copied); hooks, band mod and statusline deliberately not installed\n' "$head" "$(date +%F)" > "$PONYTAIL_PIN"
  say "  ponytail skills re-copied at $head"
fi
if [ -f "$TMP/agency-agents.head" ]; then
  head="$(cat "$TMP/agency-agents.head")"
  (cd "$TMP/agency-agents" && bash scripts/install.sh --tool claude-code --division "$AGENCY_DIVISIONS" >/dev/null)
  printf 'source: https://github.com/msitarzewski/agency-agents\ncommit: %s\ninstalled: %s\nmethod: scripts/install.sh --tool claude-code --division %s\n' "$head" "$(date +%F)" "$AGENCY_DIVISIONS" > "$AGENCY_PIN"
  say "  agency-agents re-installed at $head"
fi
if [ "$SPEC_LATEST" != "?" ] && [ "v$SPEC_CUR" != "$SPEC_LATEST" ]; then
  uv tool install --force "specify-cli @ git+https://github.com/github/spec-kit.git@$SPEC_LATEST" >/dev/null && say "  specify-cli -> $SPEC_LATEST"
fi

if [ "$GRAPHIFY_LATEST" != "?" ] && [ "$GRAPHIFY_CUR" != "$GRAPHIFY_LATEST" ]; then
  uv tool install --force "graphifyy==$GRAPHIFY_LATEST" >/dev/null && graphify install >/dev/null 2>&1 && say "  graphifyy -> $GRAPHIFY_LATEST (skill re-installed)"
fi
if [ -n "$RTK_OUTDATED" ]; then
  brew upgrade rtk >/dev/null 2>&1 && printf 'n\nn\nn\n' | RTK_ONRAMP_DISABLED=1 rtk init -g --auto-patch >/dev/null 2>&1 && say "  rtk upgraded, hook re-registered"
fi

hr; say "Re-asserting safety settings"
python3 - "$CLAUDE_DIR/settings.json" <<'PY'
import json, sys
p = sys.argv[1]; s = json.load(open(p))
opts = s.setdefault("pluginConfigs", {}).setdefault("ecc@ecc", {}).setdefault("options", {})
if opts.get("hooks_enabled") is not False:
    opts["hooks_enabled"] = False
    json.dump(s, open(p, "w"), indent=2); print("  ecc hooks_enabled set back to false")
else:
    print("  ecc hooks_enabled is false")
PY
for f in "$CLAUDE_DIR"/plugins/cache/ecc/ecc/*/.mcp.json; do [ -f "$f" ] && mv "$f" "$f.disabled-by-user" && say "  renamed $(basename "$(dirname "$f")")/.mcp.json (chrome-devtools MCP stays off)"; done
command -v rtk >/dev/null 2>&1 && { rtk telemetry disable >/dev/null 2>&1 && say "  rtk telemetry off"; }
python3 - "$CLAUDE_DIR/settings.json" <<'PY'
import json, sys
p = sys.argv[1]; s = json.load(open(p))
if s.setdefault("env", {}).get("RTK_RECALL") != "0":
    s["env"]["RTK_RECALL"] = "0"; json.dump(s, open(p, "w"), indent=2); print("  RTK_RECALL=0 restored")
else:
    print("  RTK_RECALL=0 is set")
PY
say "Done. Restart Claude Code sessions to pick up plugin updates."
