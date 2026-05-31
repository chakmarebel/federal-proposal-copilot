#!/usr/bin/env bash
# Sync canonical prose-quality doctrine + voice anchors from the proposal-workbench repo.
# Run from the root of federal-proposal-assistant or federal-proposal-copilot.
#
# Overrides:
#   WORKBENCH_REPO  default chakmarebel/proposal-workbench
#   WORKBENCH_REF   default master
#   DEST_DOCTRINE   default reference/PROSE-QUALITY-DOCTRINE.md
#   DEST_ANCHORS    default reference/voice-anchors/
set -euo pipefail

WORKBENCH_REPO="${WORKBENCH_REPO:-chakmarebel/proposal-workbench}"
WORKBENCH_REF="${WORKBENCH_REF:-master}"
DEST_DOCTRINE="${DEST_DOCTRINE:-reference/PROSE-QUALITY-DOCTRINE.md}"
DEST_ANCHORS="${DEST_ANCHORS:-reference/voice-anchors}"

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

echo "Synced PROSE-QUALITY-DOCTRINE.md + voice anchors from"
echo "  ${WORKBENCH_REPO}@${WORKBENCH_REF}"
echo "  -> $DEST_DOCTRINE"
echo "  -> $DEST_ANCHORS/"
echo ""
echo "Commit the result to record the sync point."
