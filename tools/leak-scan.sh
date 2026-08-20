#!/usr/bin/env bash
# Fail if any upstream company identity survives in the distributable tree.
#
# copilot is public. Its content is synced from single-company working repos
# (federal-proposal-assistant, proposal-workbench) and neutralized mechanically
# by tools/neutralize-company.sed. That table is only as complete as the last
# thing someone noticed -- this scan is the part that notices.
#
# Run it after any sync, and from the pre-commit hook. When it reports a
# survivor, add a rule to tools/neutralize-company.sed and re-run the sync.
# Do NOT hand-edit the synced file: the next sync would overwrite the fix.
#
# Usage:
#   ./tools/leak-scan.sh            # scan the tree, exit 1 on any survivor
#   ./tools/leak-scan.sh --list     # list the markers being scanned for
#
# Exit codes: 0 clean, 1 survivors found.
set -uo pipefail

# Markers that must never appear in published content. Extend alongside
# tools/neutralize-company.sed -- a marker here without a rule there means the
# scan blocks and nobody can fix it mechanically.
MARKERS=(
  "EdgeRunner"
  "edgerunner"
  "WarClaw"
  "Warclaw"
  "warclaw"
  "EVELYN"
  "9Z176"
  "SLZTJUA8DBD3"
  "wbal9"
  "Bellevue"
  "Saltsman"
  "Malkerson"
  "bd\.edgerunner-pipeline"
  "11011 NE 9th"
)

# Files that legitimately contain a marker and are not published content:
#  - the neutralize table and this scan define the markers;
#  - the sync-model doc and the WP-N* records describe the divergence itself,
#    which cannot be explained without naming it.
EXCLUDE_FILES=(
  "tools/neutralize-company.sed"
  "tools/leak-scan.sh"
  "docs/fpa-sync-model.md"
  "WP-N3-PROSE-QUALITY-PORT-2026-05-30.md"
  "WP-N5-SKILL-DRIFT-ALIGNMENT-2026-05-30.md"
  "CHANGELOG.md"
)

if [[ "${1:-}" == "--list" ]]; then
  printf '%s\n' "${MARKERS[@]}"
  exit 0
fi

pattern="$(IFS='|'; echo "${MARKERS[*]}")"

exclude_args=()
for f in "${EXCLUDE_FILES[@]}"; do
  exclude_args+=(":(exclude)$f")
done

# Scan tracked + untracked-but-not-ignored files only. Ignored paths
# (my-company/, signals/, proposals/) are by definition never published.
mapfile -t files < <(git ls-files --cached --others --exclude-standard -- . "${exclude_args[@]}")

hits=0
for f in "${files[@]}"; do
  [[ -f "$f" ]] || continue
  case "$f" in
    *.png|*.jpg|*.jpeg|*.gif|*.pdf|*.docx|*.xlsx|*.pptx|*.zip|*.ico) continue ;;
  esac
  if out="$(grep -nE "$pattern" "$f" 2>/dev/null)"; then
    while IFS= read -r line; do
      echo "LEAK  $f:$line"
      hits=$((hits + 1))
    done <<< "$out"
  fi
done

if (( hits > 0 )); then
  echo ""
  echo "$hits company-identity marker(s) survived neutralization."
  echo "Add a rule to tools/neutralize-company.sed and re-run the sync."
  echo "Do not hand-edit the synced file -- the next sync would overwrite it."
  exit 1
fi

echo "leak-scan: clean (${#files[@]} files, ${#MARKERS[@]} markers)"
exit 0
