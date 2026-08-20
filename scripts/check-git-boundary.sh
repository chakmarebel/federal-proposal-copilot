#!/usr/bin/env bash
# check-git-boundary.sh — Fails if sensitive proposal data is staged in the git index.
#
# The crown-jewel risk in this repo: proposals/, my-company/, and the calibration
# corpus hold live solicitations, pricing, teaming, and customer intel. The ONLY
# thing keeping them out of the public GitHub remote is .gitignore. One bad
# `git add -f`, a gitignore edit, or a stray `git add -A` on an untracked path can
# leak them. This guard inspects the STAGED index (what `git commit` would write)
# and refuses to let sensitive paths through.
#
# It is wired as a pre-commit AND pre-push hook (see hooks/ + scripts/install-hooks.sh)
# and is also asserted by scripts/smoke-test.sh via --selftest.
#
# SCOPE LIMIT: this guard matches PATHS, not content. A tracked file under scripts/ or
# reference/ can carry protected material and pass. There is one reviewed, accepted
# exception today — scripts/backfill-demand-signals.py inlines customer names, program
# names, and gap admissions in its curation table, accepted 2026-08-01 on the condition
# that the remote stays private and single-user. See README "The guard is path-based, so
# it cannot see content" for the rationale and the trigger to revisit it. Do not read a
# passing guard as "this file contains nothing sensitive."
#
# Usage:
#   bash scripts/check-git-boundary.sh            # check the current index
#   bash scripts/check-git-boundary.sh --selftest # prove it catches a staged
#                                                 # proposal file and passes clean
# Exit: 0 = clean (or selftest passed), 1 = sensitive path staged (or selftest failed).

set -u

# ────────────────────────────────────────────────────────────────
# Sensitive path matcher
# ────────────────────────────────────────────────────────────────
# A staged path is BLOCKED if it matches any of these rules. Rules operate on
# repo-relative POSIX paths exactly as `git diff --cached --name-only` reports them.
#
#   proposals/**                    live solicitations, pricing, teaming, intel
#   my-company/**                   company IP: CAGE/UEI, capabilities, past perf
#   demos/**                        customer-targeted demo packets: named customer,
#                                   demo strategy, talk tracks, and the claim posture
#                                   we take into the room. Scenario data is synthetic;
#                                   the targeting and the pitch are not.
#   corpus/calibration/<slug>/**    real captured drafts/finals/edit-notes
#                                   (the _template/ dir and top-level README are OK)
#   drafts/**                       root-level authoring layer (customer content)
#   working/**                      root-level in-flight analysis (except .gitkeep)
#   scrubs/**                       HubSpot deal scrubs (deal IDs, $, customer intel)
#   signals/**                      demand signal register + briefs: verbatim customer
#                                   requirements and our own gap admissions, aggregated
#                                   across every pursuit (worse to leak than any single
#                                   proposal). The .gitkeep sentinel is OK.
#   reviews/**                      root-level review findings (except .gitkeep)
#   campaign_rollup.md              root-level pipeline rollup
#   watchlist_table.md              root-level deal watchlist
#
# Returns 0 (is-sensitive) or 1 (is-clean) for a single path.
is_sensitive_path() {
  local p="$1"

  case "$p" in
    proposals/*)   return 0 ;;
    my-company/*)  return 0 ;;
    demos/*)       return 0 ;;
    scrubs/*)      return 0 ;;
    campaign_rollup.md)  return 0 ;;
    watchlist_table.md)  return 0 ;;
  esac

  # drafts/, working/, reviews/ at ROOT only (not proposals/<slug>/drafts/ — those
  # are already covered by proposals/*). Allow the scaffold .gitkeep sentinels.
  case "$p" in
    drafts/.gitkeep|working/.gitkeep|reviews/.gitkeep|signals/.gitkeep) return 1 ;;
    drafts/*|working/*|reviews/*|signals/*) return 0 ;;
  esac

  # Calibration corpus: block real per-slug content, allow README + _template/.
  case "$p" in
    corpus/calibration/README.md) return 1 ;;
    corpus/calibration/_template/*) return 1 ;;
    corpus/calibration/*/*) return 0 ;;
  esac

  return 1
}

# ────────────────────────────────────────────────────────────────
# Core check: scan the staged index
# ────────────────────────────────────────────────────────────────
# Uses an explicit index arg so --selftest can point at a throwaway repo.
run_check() {
  local git_dir_args="$1"  # extra args passed to git (e.g. "-C /tmp/xyz"), may be empty

  # Names of staged (added/copied/modified/renamed) files. -z for NUL-safety on
  # paths with spaces (this repo has "GenAI Afloat/" etc.).
  local offenders=()
  local path
  while IFS= read -r -d '' path; do
    if is_sensitive_path "$path"; then
      offenders+=("$path")
    fi
  done < <(git $git_dir_args diff --cached --name-only -z --diff-filter=ACMR 2>/dev/null)

  if [ ${#offenders[@]} -eq 0 ]; then
    return 0
  fi

  echo "" >&2
  echo "  ✗ GIT BOUNDARY GUARD — BLOCKED" >&2
  echo "" >&2
  echo "  The following STAGED path(s) hold sensitive proposal data that must" >&2
  echo "  NEVER reach the public remote (github.com/<you>/federal-proposal-copilot):" >&2
  echo "" >&2
  for path in "${offenders[@]}"; do
    echo "      $path" >&2
  done
  echo "" >&2
  echo "  Unstage them before committing:" >&2
  echo "" >&2
  for path in "${offenders[@]}"; do
    echo "      git restore --staged \"$path\"" >&2
  done
  echo "" >&2
  echo "  If this was intentional and you truly mean to publish it, you must edit" >&2
  echo "  scripts/check-git-boundary.sh (is_sensitive_path) — do NOT bypass the hook." >&2
  echo "" >&2
  return 1
}

# ────────────────────────────────────────────────────────────────
# Selftest: build a throwaway repo, prove catch + pass
# ────────────────────────────────────────────────────────────────
selftest() {
  echo "── check-git-boundary --selftest ──"
  local rc=0
  local tmp
  tmp="$(mktemp -d 2>/dev/null || mktemp -d -t cgb)"
  trap 'rm -rf "'"$tmp"'"' EXIT

  git -C "$tmp" init -q
  git -C "$tmp" config user.email "selftest@example.com"
  git -C "$tmp" config user.name "selftest"

  # --- Scenario A: clean index (an allowed file) should PASS ---
  mkdir -p "$tmp/corpus/calibration/_template" "$tmp/scripts"
  echo "template" > "$tmp/corpus/calibration/_template/README.md"
  echo "allowed"  > "$tmp/README.md"
  git -C "$tmp" add corpus/calibration/_template/README.md README.md
  if run_check "-C $tmp" >/dev/null 2>&1; then
    echo "  ✓ clean index (allowed files staged) passes"
  else
    echo "  ✗ FAIL: clean index was incorrectly blocked"
    rc=1
  fi

  # --- Scenario B: a staged proposal file should be CAUGHT ---
  mkdir -p "$tmp/proposals/secret-opportunity"
  echo "PRICING: \$4.2M ceiling; teaming with LM" > "$tmp/proposals/secret-opportunity/pricing.md"
  git -C "$tmp" add -f proposals/secret-opportunity/pricing.md
  if run_check "-C $tmp" >/dev/null 2>&1; then
    echo "  ✗ FAIL: staged proposal file was NOT caught"
    rc=1
  else
    echo "  ✓ staged proposals/ file is caught"
  fi

  # --- Scenario C: representative sensitive paths each caught ---
  local cases=(
    "my-company/capabilities.md"
    "scrubs/daily-2026-05-25.md"
    "campaign_rollup.md"
    "watchlist_table.md"
    "drafts/exec-summary.md"
    "working/plan.md"
    "reviews/gold-team.md"
    "corpus/calibration/real-slug/edit-notes.md"
    "signals/demand-signals.jsonl"
    "signals/briefs/2026-07-31-demand-signal-brief.md"
  )
  local c
  for c in "${cases[@]}"; do
    rm -rf "$tmp/.git/index.lock" 2>/dev/null
    git -C "$tmp" reset -q >/dev/null 2>&1
    mkdir -p "$tmp/$(dirname "$c")"
    echo "sensitive" > "$tmp/$c"
    git -C "$tmp" add -f "$c" >/dev/null 2>&1
    if run_check "-C $tmp" >/dev/null 2>&1; then
      echo "  ✗ FAIL: '$c' was NOT caught"
      rc=1
    else
      echo "  ✓ caught: $c"
    fi
  done

  # --- Scenario D: allowed sentinels must NOT be blocked ---
  local allow=(
    "drafts/.gitkeep"
    "working/.gitkeep"
    "reviews/.gitkeep"
    "signals/.gitkeep"
    "corpus/calibration/README.md"
    "corpus/calibration/_template/manifest.json.example"
  )
  for c in "${allow[@]}"; do
    git -C "$tmp" reset -q >/dev/null 2>&1
    mkdir -p "$tmp/$(dirname "$c")"
    echo "ok" > "$tmp/$c"
    git -C "$tmp" add -f "$c" >/dev/null 2>&1
    if run_check "-C $tmp" >/dev/null 2>&1; then
      echo "  ✓ allowed: $c"
    else
      echo "  ✗ FAIL: allowed sentinel '$c' was blocked"
      rc=1
    fi
  done

  echo ""
  if [ $rc -eq 0 ]; then
    echo "  ✓ SELFTEST PASSED"
  else
    echo "  ✗ SELFTEST FAILED"
  fi
  return $rc
}

# ────────────────────────────────────────────────────────────────
# Entry point
# ────────────────────────────────────────────────────────────────
main() {
  case "${1:-}" in
    --selftest) selftest ;;
    --help|-h)
      grep -E '^#( |$)' "$0" | sed 's/^# \{0,1\}//'
      ;;
    "")
      # Only meaningful inside a git work tree.
      if ! git rev-parse --is-inside-work-tree >/dev/null 2>&1; then
        echo "check-git-boundary: not inside a git work tree; nothing to check." >&2
        exit 0
      fi
      run_check ""
      ;;
    *)
      echo "check-git-boundary: unknown argument '$1' (use --selftest or --help)" >&2
      exit 2
      ;;
  esac
}

main "$@"
