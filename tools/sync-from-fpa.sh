#!/usr/bin/env bash
# Sync canonical content from federal-proposal-assistant -> federal-proposal-copilot.
# Run from the root of federal-proposal-copilot.
#
# Per the FPA-canonical / copilot-stays-in-sync model:
# - federal-proposal-assistant is the working copy where new content lands first.
# - federal-proposal-copilot is the distributable mirror.
# - When meaningful changes accumulate on FPA, run this script in copilot,
#   review the diff, commit the synced result. Each sync is one PR.
#
# This script is intentionally narrow: SYNC_PATHS lists the files/directories
# that should stay byte-identical between FPA and copilot. Things that need
# to diverge intentionally (company-specific framing, the LICENSE file,
# the QUICKSTART, etc.) are NOT in the sync list and stay copilot-specific.
#
# Overrides:
#   FPA_REPO  default chakmarebel/federal-proposal-assistant
#   FPA_REF   default main
#
# Idempotent: re-running with the same FPA_REF produces zero diff.
set -euo pipefail

FPA_REPO="${FPA_REPO:-chakmarebel/federal-proposal-assistant}"
FPA_REF="${FPA_REF:-main}"

# Paths that should stay byte-identical between FPA and copilot.
# Add as the canonical-sync surface grows; remove anything that ought to
# diverge intentionally.
SYNC_PATHS=(
  # Top-level reference docs.
  "PROPOSAL-AGENT-DIAGNOSIS-2026-05-15.md"
  "PROPOSAL-AGENT-REDESIGN-2026-05-15.md"
  # Skills that have NO intentional divergence from FPA. Added in WP-N5
  # after a per-skill diff confirmed FPA and copilot are byte-identical
  # (modulo line endings). Future drift on these auto-flows via the sync.
  # Do NOT add any skill that has even one company-specific hunk in copilot
  # -- syncing will overwrite the company-neutral framing. See
  # docs/fpa-sync-model.md "Known divergence (intentional)" for skills
  # that intentionally stay out.
  ".claude/skills/proposal-patcher"
  ".claude/skills/proposal-writer"
  ".claude/skills/proposal-manager"
  ".claude/skills/proposal-storyboard"
  ".claude/skills/red-team-review"
)

tmp="$(mktemp -d)"
trap 'rm -rf "$tmp"' EXIT

# Shallow clone via ssh. GitHub does not support git-archive --remote, so a
# shallow clone is the working path. SSH means private repos work without a
# personal access token.
git clone --depth=1 --branch "$FPA_REF" "git@github.com:${FPA_REPO}.git" "$tmp/fpa" >/dev/null 2>&1

echo "Syncing from ${FPA_REPO}@${FPA_REF}:"
for path in "${SYNC_PATHS[@]}"; do
  src="$tmp/fpa/$path"
  if [[ ! -e "$src" ]]; then
    echo "  skip (not in FPA): $path"
    continue
  fi
  if [[ -d "$src" ]]; then
    # Sync directory: replace destination contents to match canonical.
    # Operators who hand-edit synced paths locally will lose those edits.
    mkdir -p "$path"
    rm -rf "$path"
    cp -R "$src" "$path"
  else
    dest_dir="$(dirname "$path")"
    [[ "$dest_dir" != "." ]] && mkdir -p "$dest_dir"
    cp "$src" "$path"
  fi
  echo "  synced: $path"
done

echo ""
echo "Synced from ${FPA_REPO}@${FPA_REF}"
echo "Commit the result to record the sync point."
