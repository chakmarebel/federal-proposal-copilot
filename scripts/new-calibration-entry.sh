#!/usr/bin/env bash
# new-calibration-entry.sh — scaffold a calibration corpus entry for a proposal.
#
# The calibration corpus (corpus/calibration/) is the framework's flagship
# learning loop, but it stays empty because feeding it is friction. This makes
# the pre-edit snapshot a ONE-COMMAND operation for a given proposal slug:
# it copies drafts/ -> auto-draft/, seeds manifest.json + edit-notes.md from the
# committed _template/, and leaves final-submitted/ for the post-submit phase.
#
# It implements the mechanical part of /capture-submission Phase 1 so the corpus
# can be fed without a full agent session. It does NOT fabricate data: auto-draft/
# is a byte copy of your real drafts, and edit-notes.md is left for you to fill.
#
# Usage:
#   bash scripts/new-calibration-entry.sh <proposal-slug>
#   bash scripts/new-calibration-entry.sh <proposal-slug> --from drafts   # source (default: drafts)
#   bash scripts/new-calibration-entry.sh --selftest
#
# Exit: 0 = entry scaffolded (or selftest passed), non-zero on error.
set -u

ROOT="$(cd "$(dirname "$0")/.." && pwd)"

utc_now() { date -u +"%Y-%m-%dT%H:%M:%SZ"; }

# Scaffold one entry. Args: <repo_root> <slug> <source_subdir>
# Reads:  <root>/proposals/<slug>/{working/proposal-type.md, <source>/, working/customer-profile.md}
#         <root>/corpus/calibration/_template/
# Writes: <root>/corpus/calibration/<slug>/{auto-draft/, manifest.json, edit-notes.md}
scaffold_entry() {
  local root="$1" slug="$2" source_sub="$3"

  local prop_dir="$root/proposals/$slug"
  local tmpl_dir="$root/corpus/calibration/_template"
  local dest="$root/corpus/calibration/$slug"

  if [ ! -d "$prop_dir" ]; then
    echo "new-calibration-entry: proposal not found: proposals/$slug/" >&2
    return 2
  fi
  if [ ! -d "$tmpl_dir" ]; then
    echo "new-calibration-entry: template dir missing: corpus/calibration/_template/" >&2
    return 2
  fi

  # Never clobber an existing entry — re-snapshotting destroys the calibration signal.
  if [ -d "$dest/auto-draft" ]; then
    echo "new-calibration-entry: entry already has an auto-draft snapshot:" >&2
    echo "  corpus/calibration/$slug/auto-draft/" >&2
    echo "  Refusing to overwrite (that would destroy the calibration baseline)." >&2
    echo "  For the post-submit phase, run /capture-submission." >&2
    return 3
  fi

  local src_dir="$prop_dir/$source_sub"
  if [ ! -d "$src_dir" ]; then
    echo "new-calibration-entry: source dir missing: proposals/$slug/$source_sub/" >&2
    return 2
  fi

  # Count real draft files (exclude .gitkeep + empties).
  local ndrafts=0
  while IFS= read -r -d '' f; do
    [ -s "$f" ] && ndrafts=$((ndrafts+1))
  done < <(find "$src_dir" -maxdepth 1 -type f -name '*.md' ! -name '.gitkeep' -print0 2>/dev/null)

  if [ "$ndrafts" -eq 0 ]; then
    echo "new-calibration-entry: no non-empty *.md files in proposals/$slug/$source_sub/ — nothing to snapshot." >&2
    echo "  Run /proposal-writer first, or pass --from <dir> to point at the drafts." >&2
    return 4
  fi

  mkdir -p "$dest/auto-draft"

  # Copy drafts (top-level *.md, non-empty) into auto-draft/.
  local copied=0
  while IFS= read -r -d '' f; do
    [ -s "$f" ] || continue
    cp "$f" "$dest/auto-draft/$(basename "$f")"
    copied=$((copied+1))
  done < <(find "$src_dir" -maxdepth 1 -type f -name '*.md' ! -name '.gitkeep' -print0 2>/dev/null)

  # Copy context artifacts if present (prefixed with _ per capture-submission convention).
  [ -f "$prop_dir/working/compliance-matrix.md" ] && cp "$prop_dir/working/compliance-matrix.md" "$dest/auto-draft/_compliance-matrix.md"
  [ -f "$prop_dir/working/graphics-brief.md" ]     && cp "$prop_dir/working/graphics-brief.md" "$dest/auto-draft/_graphics-brief.md"

  # Derive proposal_type and customer from the proposal's working files.
  local ptype="unknown" customer="null"
  if [ -f "$prop_dir/working/proposal-type.md" ]; then
    local t
    t=$(grep -E "^type_id:" "$prop_dir/working/proposal-type.md" 2>/dev/null | head -1 | awk '{print $2}')
    [ -n "$t" ] && ptype="$t"
  fi
  if [ -f "$prop_dir/working/customer-profile.md" ]; then
    local c
    c=$(grep -iE "^(customer|agency)\s*[:|]" "$prop_dir/working/customer-profile.md" 2>/dev/null | head -1 | sed 's/^[^:|]*[:|]//; s/^ *//; s/ *$//; s/"/\\"/g')
    [ -n "$c" ] && customer="\"$c\""
  fi

  # Write manifest.json (mirrors capture-submission Phase 1 shape).
  local now; now="$(utc_now)"
  cat > "$dest/manifest.json" <<EOF
{
  "schema_version": "calibration-manifest.v1",
  "slug": "$slug",
  "proposal_type": "$ptype",
  "customer": $customer,
  "captured_pre": "$now",
  "captured_post": null,
  "submitted_date": null,
  "status": "pre-edit",
  "outcome": null,
  "edit_hours_estimate": null,
  "notes": "Scaffolded by scripts/new-calibration-entry.sh. Post-submit: run /capture-submission."
}
EOF

  # Seed edit-notes.md from the template, substituting the slug placeholder.
  if [ -f "$tmpl_dir/edit-notes.md.template" ]; then
    sed "s/\[Proposal Slug\]/$slug/g" "$tmpl_dir/edit-notes.md.template" > "$dest/edit-notes.md"
  fi

  echo "new-calibration-entry: scaffolded corpus/calibration/$slug/"
  echo "  auto-draft/       ($copied draft file(s) snapshotted from proposals/$slug/$source_sub/)"
  echo "  manifest.json     (status=pre-edit, type=$ptype)"
  echo "  edit-notes.md     (fill this out after you submit — 5 min)"
  echo ""
  echo "  Next: edit for submission, then after sending run /capture-submission"
  echo "  (Phase 2) to capture final-submitted/ and finalize the entry."
  return 0
}

selftest() {
  echo "── new-calibration-entry --selftest ──"
  local rc=0 tmp
  tmp="$(mktemp -d 2>/dev/null || mktemp -d -t nce)"
  trap 'rm -rf "'"$tmp"'"' EXIT

  # Build a minimal fake repo: _template/ + a proposal with drafts.
  mkdir -p "$tmp/corpus/calibration/_template"
  echo '{"schema_version":"calibration-manifest.v1"}' > "$tmp/corpus/calibration/_template/manifest.json.example"
  printf '# Edit Notes — [Proposal Slug]\n\n## 1. Time spent\n' > "$tmp/corpus/calibration/_template/edit-notes.md.template"
  mkdir -p "$tmp/proposals/demo-slug/drafts" "$tmp/proposals/demo-slug/working"
  printf 'type_id: white-paper\n' > "$tmp/proposals/demo-slug/working/proposal-type.md"
  printf 'Customer: Example Agency\n' > "$tmp/proposals/demo-slug/working/customer-profile.md"
  printf '# Exec Summary\nbody\n' > "$tmp/proposals/demo-slug/drafts/exec-summary.md"
  printf '# Approach\nbody\n' > "$tmp/proposals/demo-slug/drafts/approach.md"
  : > "$tmp/proposals/demo-slug/drafts/.gitkeep"

  # --- A: scaffolds successfully ---
  if scaffold_entry "$tmp" "demo-slug" "drafts" >/dev/null 2>&1; then
    echo "  ✓ scaffolds an entry"
  else
    echo "  ✗ FAIL: scaffolding errored"; rc=1
  fi

  # --- B: auto-draft has the 2 real drafts, not .gitkeep ---
  local n; n=$(find "$tmp/corpus/calibration/demo-slug/auto-draft" -maxdepth 1 -name '*.md' 2>/dev/null | wc -l | tr -d ' ')
  if [ "$n" = "2" ]; then echo "  ✓ auto-draft/ holds 2 draft files (.gitkeep excluded)"; else echo "  ✗ FAIL: expected 2 drafts, got $n"; rc=1; fi

  # --- C: manifest is valid JSON with the right slug + type ---
  # Translate the MSYS/Cygwin temp path to a native path when python is the
  # Windows interpreter (Git Bash), so json.load can find the file.
  local manifest_path="$tmp/corpus/calibration/demo-slug/manifest.json"
  local py_path="$manifest_path"
  command -v cygpath >/dev/null 2>&1 && py_path="$(cygpath -w "$manifest_path")"
  if command -v python3 >/dev/null 2>&1; then
    if MANIFEST="$py_path" python3 -c "import json,os,sys; d=json.load(open(os.environ['MANIFEST'])); sys.exit(0 if d['slug']=='demo-slug' and d['proposal_type']=='white-paper' and d['status']=='pre-edit' else 1)" 2>/dev/null; then
      echo "  ✓ manifest.json is valid JSON with slug/type/status"
    else
      echo "  ✗ FAIL: manifest.json invalid or wrong fields"; rc=1
    fi
  fi

  # --- D: edit-notes has slug substituted ---
  if grep -q "demo-slug" "$tmp/corpus/calibration/demo-slug/edit-notes.md" 2>/dev/null; then
    echo "  ✓ edit-notes.md seeded with slug"
  else
    echo "  ✗ FAIL: edit-notes.md not seeded"; rc=1
  fi

  # --- E: refuses to clobber an existing entry ---
  if scaffold_entry "$tmp" "demo-slug" "drafts" >/dev/null 2>&1; then
    echo "  ✗ FAIL: re-scaffolding was allowed (would destroy baseline)"; rc=1
  else
    echo "  ✓ refuses to overwrite an existing auto-draft"
  fi

  # --- F: errors on unknown proposal ---
  if scaffold_entry "$tmp" "no-such-slug" "drafts" >/dev/null 2>&1; then
    echo "  ✗ FAIL: accepted a nonexistent proposal"; rc=1
  else
    echo "  ✓ errors on nonexistent proposal"
  fi

  echo ""
  [ $rc -eq 0 ] && echo "  ✓ SELFTEST PASSED" || echo "  ✗ SELFTEST FAILED"
  return $rc
}

main() {
  case "${1:-}" in
    --selftest) selftest; exit $? ;;
    --help|-h) grep -E '^#( |$)' "$0" | sed 's/^# \{0,1\}//'; exit 0 ;;
    "") echo "Usage: bash scripts/new-calibration-entry.sh <proposal-slug> [--from <dir>]" >&2; exit 2 ;;
  esac

  local slug="$1"; shift
  local source_sub="drafts"
  while [ $# -gt 0 ]; do
    case "$1" in
      --from) source_sub="${2:-drafts}"; shift 2 ;;
      *) echo "new-calibration-entry: unknown argument '$1'" >&2; exit 2 ;;
    esac
  done

  scaffold_entry "$ROOT" "$slug" "$source_sub"
  exit $?
}

main "$@"
