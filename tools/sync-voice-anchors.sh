#!/usr/bin/env bash
# Sync canonical prose-quality doctrine + voice anchors + universal doctrine
# knowledge + the prose-lint rule set from the proposal-workbench repo.
# Run from the root of federal-proposal-assistant or federal-proposal-copilot.
#
# Overrides:
#   WORKBENCH_REPO   default chakmarebel/proposal-workbench
#   WORKBENCH_REF    default master
#   DEST_DOCTRINE    default reference/PROSE-QUALITY-DOCTRINE.md
#   DEST_ANCHORS     default reference/voice-anchors/
#   DEST_DOCTRINE_DIR default reference/doctrine/   (universal doctrine knowledge files)
#   DEST_LINT_RULES  default reference/prose-lint-rules.json  (shared prose-lint rule set)
set -euo pipefail

WORKBENCH_REPO="${WORKBENCH_REPO:-chakmarebel/proposal-workbench}"
WORKBENCH_REF="${WORKBENCH_REF:-master}"
DEST_DOCTRINE="${DEST_DOCTRINE:-reference/PROSE-QUALITY-DOCTRINE.md}"
DEST_ANCHORS="${DEST_ANCHORS:-reference/voice-anchors}"
DEST_DOCTRINE_DIR="${DEST_DOCTRINE_DIR:-reference/doctrine}"
DEST_LINT_RULES="${DEST_LINT_RULES:-reference/prose-lint-rules.json}"

tmp="$(mktemp -d)"
trap 'rm -rf "$tmp"' EXIT

if [[ -d "$WORKBENCH_REPO" ]]; then
  source_repo="$WORKBENCH_REPO"
else
  source_repo="git@github.com:${WORKBENCH_REPO}.git"
fi

# GitHub does not support git-archive over ssh, so use a shallow clone.
git clone --depth=1 --branch "$WORKBENCH_REF" "$source_repo" "$tmp/wb" >/dev/null

mkdir -p "$(dirname "$DEST_DOCTRINE")"
cp "$tmp/wb/proposal-workbench/PROSE-QUALITY-DOCTRINE.md" "$DEST_DOCTRINE"

mkdir -p "$DEST_ANCHORS"
# Replace the destination contents to match canonical. This is a sync, not a merge.
# Operators who hand-edit voice anchors locally will lose those edits on the next sync.
rm -f "$DEST_ANCHORS"/*.md
cp "$tmp"/wb/proposal-workbench/reference/voice-anchors/*.md "$DEST_ANCHORS"/

# Universal doctrine knowledge files (prohibited-claims, output-discipline, acronyms-federal).
# Canonical source: the workbench backend's bundled doctrine knowledge dir.
src_doctrine_dir="$tmp/wb/proposal-workbench/backend/app/knowledge/doctrine"
if [[ -d "$src_doctrine_dir" ]]; then
  mkdir -p "$DEST_DOCTRINE_DIR"
  rm -f "$DEST_DOCTRINE_DIR"/*.md
  cp "$src_doctrine_dir"/*.md "$DEST_DOCTRINE_DIR"/
fi

# Shared prose-lint rule set. Synced only once the workbench publishes it (see
# reference/prose-lint-rules.json header). Until then this is a no-op and the
# consumer-local rules file is authoritative.
src_lint_rules="$tmp/wb/proposal-workbench/backend/app/knowledge/prose-lint-rules.json"
if [[ -f "$src_lint_rules" ]]; then
  mkdir -p "$(dirname "$DEST_LINT_RULES")"
  cp "$src_lint_rules" "$DEST_LINT_RULES"
fi

echo "Synced from ${WORKBENCH_REPO}@${WORKBENCH_REF}:"
echo "  -> $DEST_DOCTRINE"
echo "  -> $DEST_ANCHORS/"
echo "  -> $DEST_DOCTRINE_DIR/ (universal doctrine knowledge)"
[[ -f "$src_lint_rules" ]] && echo "  -> $DEST_LINT_RULES (shared prose-lint rules)"
echo ""
echo "Commit the result to record the sync point."
