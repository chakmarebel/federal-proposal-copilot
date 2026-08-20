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
# that should stay in sync between FPA and copilot, modulo the two mechanical
# transforms below. Things that need to diverge by hand (the company-neutral
# framing in CLAUDE.md, the LICENSE file, the QUICKSTART, etc.) are NOT in the
# sync list and stay copilot-specific.
#
# Overrides:
#   FPA_REPO   default chakmarebel/federal-proposal-assistant
#   FPA_REF    default main
#   FPA_LOCAL  path to a local FPA checkout. When set, the script copies from
#              that working tree instead of cloning. Use this to sync content
#              that has not been pushed to FPA's main yet; the commit message
#              should then record the local HEAD plus "+ uncommitted".
#
# Idempotent: re-running against the same source produces zero diff.
set -euo pipefail

FPA_REPO="${FPA_REPO:-chakmarebel/federal-proposal-assistant}"
FPA_REF="${FPA_REF:-main}"
FPA_LOCAL="${FPA_LOCAL:-}"

# Paths that should stay in sync between FPA and copilot.
# Add as the canonical-sync surface grows; remove anything that ought to
# diverge intentionally.
#
# Do NOT add a path whose divergence is EDITORIAL (a hand-written
# company-neutral rewording). Do add a path whose only divergence is
# MECHANICAL -- the neutralize/normalize transforms below handle it, and a
# mechanical transform keeps the file on the sync surface instead of freezing
# it. See docs/fpa-sync-model.md.
SYNC_PATHS=(
  # ---- Top-level reference docs ----
  "PROPOSAL-AGENT-DIAGNOSIS-2026-05-15.md"
  "PROPOSAL-AGENT-REDESIGN-2026-05-15.md"

  # ---- Skills ----
  # No editorial divergence from FPA. Do NOT add a skill that carries a
  # hand-written company-neutral hunk in copilot -- syncing overwrites it.
  # See docs/fpa-sync-model.md "Known divergence (intentional)".
  ".claude/skills/proposal-patcher"
  ".claude/skills/proposal-writer"
  ".claude/skills/proposal-manager"
  ".claude/skills/proposal-storyboard"
  ".claude/skills/red-team-review"
  ".claude/skills/adversarial-review"
  ".claude/skills/capture-demand-signals"

  # ---- Design / orientation docs ----
  "docs/AGENT-ORIENTATION.md"
  "docs/BD-CTO-DEMAND-SIGNAL-SYNC.md"

  # ---- Reference data consumed by the skills above ----
  "reference/adversarial-personas.md"
  "reference/preventable-gold-team-findings.md"
  "reference/pitch-demo-readiness-gate.md"
  "reference/capability-themes.md"
  "reference/customer-aliases.tsv"
  "reference/prose-lint-rules.json"

  # ---- Proposal types + their section patterns ----
  # A type and its section pattern must sync together, or the type declares a
  # pattern file that isn't there.
  "reference/proposal-types/README.md"
  "reference/proposal-types/baa-white-paper.md"
  "reference/proposal-types/marketplace-video-pitch.md"
  "reference/proposal-types/pitch-demo.md"
  "reference/proposal-types/unsolicited-proposal.md"
  "reference/proposal-types/white-paper.md"
  "reference/section-patterns/README.md"
  "reference/section-patterns/marketplace-video-pitch.md"
  "reference/section-patterns/pitch-demo.md"
  "reference/section-patterns/unsolicited-proposal.md"
  "reference/portal-formats/colosseum.md"

  # ---- Voice doctrine: profile + paired-example corpus ----
  # The before/after pairs are drawn from real drafts; the neutralize transform
  # rewrites the company and product names in them.
  "reference/voice-profiles/proposal.md"
  "reference/voice-pairs/proposal"
  "reference/voice-anchors"

  # ---- Feature scripts ----
  # A skill and its supporting scripts must sync together, or copilot ends up
  # with a skill that calls a script it doesn't have.
  "scripts/extract-evaluation-model.py"
  "scripts/compute-lift.py"
  "scripts/backfill-gold-snapshots.py"
  "scripts/prose-lint.py"
  "scripts/lint-document-structure.py"
  "scripts/lint-submission-file.py"
  "scripts/check-strengths.py"
  "scripts/render-matrix-to-xlsx.py"
  "scripts/render-md-to-docx.py"
  "scripts/calibration-status.py"
  "scripts/new-calibration-entry.sh"
  # Demand-signal loop: machinery only. The register (signals/) and the
  # adjudication decisions (reference/demand-signals/) are FPA-only data, and
  # scripts/backfill-demand-signals.py inlines real customer names and gap
  # admissions in its curation table -- none of the three are on this surface.
  "scripts/demand_signal_core.py"
  "scripts/extract-demand-signals.py"
  "scripts/ingest-crm-candidates.py"
  "scripts/promote-crm-candidates.py"
  "scripts/build-demand-signal-workbook.py"
  "scripts/build-demand-signal-brief.py"
  "scripts/customer-aliases.py"
  # Repo-hygiene tooling: the boundary guard that keeps company assets off a
  # public remote, and the backup that protects the gitignored my-company/.
  "scripts/check-git-boundary.sh"
  "scripts/install-hooks.sh"
  "scripts/backup-company-assets.py"

  # ---- Shared converters ----
  "tools/md_to_docx.py"
  "tools/polish_docx.py"

  # ---- JSON schemas ----
  # The only FPA/copilot difference is the $id namespace host, which the
  # namespace transform rewrites -- so they stay structurally in sync while
  # keeping copilot's own schema identity. Do not add host-namespaced files
  # here unless that transform covers them.
  "reference/schemas/evaluation-model.schema.json"
  "reference/schemas/gold-team-snapshot.schema.json"
  "reference/schemas/adversarial-round.schema.json"
  "reference/schemas/demand-signal.schema.json"
)

# Apply a sed program file over a file, or over every file under a directory.
_sed_over() {
  local target="$1" prog="$2"
  if [[ -d "$target" ]]; then
    find "$target" -type f -print0 | while IFS= read -r -d '' f; do
      sed -i -f "$prog" "$f"
    done
  elif [[ -f "$target" ]]; then
    sed -i -f "$prog" "$target"
  fi
}

# ---- Transform 1: schema $id namespace host ----
# Rewrite FPA's schema namespace host after each copy so schemas can live on the
# sync surface without importing FPA's identity.
NAMESPACE_SED="$(mktemp)"
cat > "$NAMESPACE_SED" <<'NS'
s#federal-proposal-assistant\.local#federal-proposal-copilot.local#g
NS

# ---- Transform 2: company neutralization ----
# The rule table lives in tools/neutralize-company.sed so this script and
# tools/sync-voice-anchors.sh strip identity the same way, and so
# tools/leak-scan.sh has one place to point at when a marker survives.
NEUTRALIZE_SED="tools/neutralize-company.sed"
[[ -f "$NEUTRALIZE_SED" ]] || { echo "missing $NEUTRALIZE_SED" >&2; exit 1; }


tmp="$(mktemp -d)"
trap 'rm -f "$NAMESPACE_SED"; rm -rf "$tmp"' EXIT

if [[ -n "$FPA_LOCAL" ]]; then
  [[ -d "$FPA_LOCAL/.claude/skills" ]] || {
    echo "FPA_LOCAL is not an FPA checkout: $FPA_LOCAL" >&2; exit 1; }
  src_root="$FPA_LOCAL"
  source_desc="$FPA_LOCAL (local tree @ $(git -C "$FPA_LOCAL" rev-parse --short HEAD))"
else
  # Shallow clone via ssh. GitHub does not support git-archive --remote, so a
  # shallow clone is the working path. SSH means private repos work without a
  # personal access token.
  git clone --depth=1 --branch "$FPA_REF" "git@github.com:${FPA_REPO}.git" "$tmp/fpa" >/dev/null 2>&1
  src_root="$tmp/fpa"
  source_desc="${FPA_REPO}@${FPA_REF}"
fi

echo "Syncing from ${source_desc}:"
for path in "${SYNC_PATHS[@]}"; do
  src="$src_root/$path"
  if [[ ! -e "$src" ]]; then
    echo "  skip (not in FPA): $path"
    continue
  fi
  if [[ -d "$src" ]]; then
    # Sync directory: replace destination contents to match canonical.
    # Operators who hand-edit synced paths locally will lose those edits.
    rm -rf "$path"
    mkdir -p "$(dirname "$path")"
    cp -R "$src" "$path"
  else
    dest_dir="$(dirname "$path")"
    [[ "$dest_dir" != "." ]] && mkdir -p "$dest_dir"
    cp "$src" "$path"
  fi
  _sed_over "$path" "$NAMESPACE_SED"
  _sed_over "$path" "$NEUTRALIZE_SED"
  echo "  synced: $path"
done

# Skills may have been added/changed/removed above; keep the generated index in
# step so SKILLS.md never drifts from the SKILL.md frontmatter.
if [[ -f scripts/build-skills-index.py ]]; then
  python scripts/build-skills-index.py >/dev/null 2>&1 && echo "  regenerated: SKILLS.md" || true
fi

echo ""
echo "Synced from ${source_desc}"
# Gate: nothing company-identifying may survive into the distributable tree.
if [[ -x tools/leak-scan.sh ]]; then
  echo ""
  bash tools/leak-scan.sh || {
    echo ""
    echo "Sync completed but the tree is NOT publishable. Fix the table above, re-run."
    exit 1
  }
fi

echo "Review the diff, then commit."
