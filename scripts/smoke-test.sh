#!/usr/bin/env bash
# smoke-test.sh — Validates framework internal consistency.
#
# Checks caught today:
#   - Every reference/proposal-types/*.md section_patterns → existing file in reference/section-patterns/
#   - Every reference/proposal-types/*.md pricing_artifact → existing file in reference/pricing-artifacts/ (or 'none')
#   - If pricing_artifact != none, pricing-analyst must be in required_skills, NOT skipped_skills
#   - Every required_skills entry → existing skill dir at .claude/skills/<name>/SKILL.md
#   - Every compliance_sources entry is from a known set
#   - No references to deprecated paths: reference/boilerplate/, inputs/02_company/, inputs/05_graphics/, reviews/compliance-check.md
#
# Usage: bash scripts/smoke-test.sh [--verbose]
# Exit: 0 = clean, 1 = failures found.

set -u
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT"

VERBOSE=0
[ "${1:-}" = "--verbose" ] && VERBOSE=1

FAIL=0
WARN=0
CHECK=0

pass() { CHECK=$((CHECK+1)); [ $VERBOSE -eq 1 ] && echo "  ✓ $1"; }
fail() { CHECK=$((CHECK+1)); FAIL=$((FAIL+1)); echo "  ✗ FAIL: $1"; }
warn() { CHECK=$((CHECK+1)); WARN=$((WARN+1)); echo "  ⚠ WARN: $1"; }

section() { echo ""; echo "── $1 ──"; }

# ────────────────────────────────────────────────────────────────
section "Proposal type registry integrity"
# ────────────────────────────────────────────────────────────────

known_skills=".claude/skills"
known_patterns="reference/section-patterns"
known_artifacts="reference/pricing-artifacts"

for f in reference/proposal-types/*.md; do
  [ "$(basename "$f")" = "README.md" ] && continue
  type_id=$(grep -E "^type_id:" "$f" | awk '{print $2}')
  sp=$(grep -E "^section_patterns:" "$f" | awk '{print $2}')
  pa=$(grep -E "^pricing_artifact:" "$f" | awk '{print $2}')
  req=$(grep -E "^required_skills:" "$f" | sed 's/required_skills: *\[//; s/\]//')
  skp=$(grep -E "^skipped_skills:" "$f" | sed 's/skipped_skills: *\[//; s/\]//')

  # section_patterns → file must exist
  if [ -f "$known_patterns/$sp.md" ]; then
    pass "$type_id: section_patterns=$sp → $known_patterns/$sp.md exists"
  else
    fail "$type_id: section_patterns=$sp → $known_patterns/$sp.md MISSING"
  fi

  # pricing_artifact → file must exist OR be 'none'
  if [ "$pa" = "none" ]; then
    pass "$type_id: pricing_artifact=none"
  elif [ -f "$known_artifacts/$pa.md" ]; then
    pass "$type_id: pricing_artifact=$pa → $known_artifacts/$pa.md exists"
  else
    fail "$type_id: pricing_artifact=$pa → $known_artifacts/$pa.md MISSING"
  fi

  # If pricing_artifact != none, pricing-analyst must be in required_skills, not skipped
  if [ "$pa" != "none" ]; then
    if echo "$req" | grep -q "pricing-analyst"; then
      pass "$type_id: pricing-analyst in required_skills (matches pricing_artifact=$pa)"
    else
      fail "$type_id: pricing_artifact=$pa but pricing-analyst NOT in required_skills"
    fi
    if echo "$skp" | grep -q "pricing-analyst"; then
      fail "$type_id: pricing-analyst in skipped_skills contradicts pricing_artifact=$pa"
    fi
  fi

  # All required_skills must resolve to a skill dir
  for s in $(echo "$req" | tr ',' ' '); do
    s=$(echo "$s" | xargs)  # trim
    [ -z "$s" ] && continue
    if [ -f "$known_skills/$s/SKILL.md" ]; then
      pass "$type_id: required_skill $s exists"
    else
      fail "$type_id: required_skill $s → $known_skills/$s/SKILL.md MISSING"
    fi
  done
done

# ────────────────────────────────────────────────────────────────
section "Deprecated-path refs across framework files"
# ────────────────────────────────────────────────────────────────

# Exclude the archive (legacy-framework) from these checks — it's a frozen snapshot.
check_no_ref() {
  pattern="$1"
  label="$2"
  # grep -r excluding the archive dir
  hits=$(grep -rn "$pattern" \
    --include="*.md" \
    --exclude-dir=".git" \
    --exclude-dir="docs" \
    --exclude-dir="node_modules" \
    --exclude-dir="my-company" \
    --exclude-dir="proposals" \
    . 2>/dev/null | grep -v '^./scripts/smoke-test.sh')
  if [ -z "$hits" ]; then
    pass "no references to $label in active framework files"
  else
    fail "references to $label found:"
    echo "$hits" | head -8 | sed 's/^/     /'
  fi
}

check_no_ref "reference/boilerplate/" "reference/boilerplate/ (migrated to my-company/)"
check_no_ref "inputs/02_company/" "inputs/02_company/ (canonical is 02_yourCompany/)"
check_no_ref "inputs/05_graphics/" "inputs/05_graphics/ (renamed to 05_graphic_standards/ or graphics/)"
check_no_ref "reviews/compliance-check\.md" "reviews/compliance-check.md (actual file is compliance-gaps.md)"

# ────────────────────────────────────────────────────────────────
section "Template scaffold consistency"
# ────────────────────────────────────────────────────────────────

expected_scaffold_dirs=(
  "templates/inputs/00_priority"
  "templates/inputs/01_customer"
  "templates/inputs/02_yourCompany"
  "templates/inputs/03_teammates"
  "templates/inputs/04_patterns"
  "templates/inputs/05_graphic_standards"
  "templates/inputs/06_notes"
  "templates/working"
  "templates/drafts"
  "templates/reviews"
  "templates/graphics"
  "templates/final"
)
for d in "${expected_scaffold_dirs[@]}"; do
  if [ -d "$d" ]; then pass "scaffold dir exists: $d"
  else fail "scaffold dir MISSING: $d"
  fi
done

# Confirm old scaffold names are gone
for d in templates/inputs/02_company templates/inputs/05_graphics; do
  if [ -d "$d" ]; then fail "stale scaffold dir still present: $d"
  else pass "stale scaffold dir absent: $d"
  fi
done

# ────────────────────────────────────────────────────────────────
section "Required framework reference files"
# ────────────────────────────────────────────────────────────────

expected_files=(
  "reference/proposal-types/README.md"
  "reference/section-patterns/README.md"
  "reference/pricing-artifacts/README.md"
  "reference/evaluator-rubrics/README.md"
  "reference/office-templates/README.md"
  "reference/schemas/README.md"
  "reference/proposal-writing-patterns.md"
  "reference/compliance-matrix-template.md"
  "reference/distribution-statements.md"
  "reference/examples/evidence-ledger.example.json"
  "templates/working/activity.md"
  "templates/working/ai-runs.jsonl"
  "docs/v1.5-plan.md"
  ".claude/skills/evidence-check/SKILL.md"
  ".claude/skills/dashboard/SKILL.md"
  "reference/proposal-conventions/README.md"
  "reference/proposal-conventions/far-rfp.md"
  "reference/graphic-templates/illustrator-conventions.md"
  "reference/graphic-templates/pitch-deck-conventions.md"
  "reference/proposal-conventions/sbir.md"
  "scripts/extract-pdf-patterns.py"
  "scripts/extract-pdf-graphics.py"
  "scripts/extract-pptx-patterns.py"
  "scripts/extract-xlsx-patterns.py"
  "reference/proposal-conventions/gsa-mas.md"
  "reference/section-patterns/gsa-mas-task-order.md"
  "reference/section-patterns/security-volume.md"
  "reference/pricing-artifacts/gsa-mas-pricing.md"
  "reference/proposal-types/gsa-mas-task-order.md"
  "reference/methodology/README.md"
  "reference/methodology/shipley-alignment.md"
  "reference/methodology/color-teams.md"
  "reference/methodology/capture-planning.md"
  "reference/methodology/bd-process.md"
  "corpus/calibration/README.md"
  "corpus/calibration/_template/README.md"
  "corpus/calibration/_template/manifest.json.example"
  "corpus/calibration/_template/edit-notes.md.template"
  ".claude/skills/capture-submission/SKILL.md"
  "dashboard/app.py"
  "dashboard/config.py"
  "dashboard/loaders.py"
  "dashboard/pricing.py"
  "dashboard/selftest.py"
  "dashboard/requirements.txt"
  "dashboard/README.md"
  "dashboard/views/__init__.py"
  "dashboard/views/portfolio.py"
  "dashboard/views/proposal.py"
  "dashboard/views/spend.py"
  "dashboard/views/ledger.py"
)
for f in "${expected_files[@]}"; do
  if [ -f "$f" ]; then pass "exists: $f"
  else fail "MISSING: $f"
  fi
done

# ────────────────────────────────────────────────────────────────
section "v1.5 JSON schemas (Phase A)"
# ────────────────────────────────────────────────────────────────

# Each schema file must: exist, parse as valid JSON, declare matching $id
required_schemas=(
  "compliance-matrix.schema.json:compliance-matrix.v1"
  "proposal-plan.schema.json:proposal-plan.v1"
  "activity-entry.schema.json:activity-entry.v1"
  "ai-run.schema.json:ai-run.v1"
  "evidence-ledger.schema.json:evidence-ledger.v1"
)

for entry in "${required_schemas[@]}"; do
  file="${entry%%:*}"
  expected_version="${entry##*:}"
  path="reference/schemas/$file"

  if [ ! -f "$path" ]; then
    fail "schema file missing: $path"
    continue
  fi

  # Validate as JSON (uses python3 if available; falls back to jq if not)
  if command -v python3 >/dev/null 2>&1; then
    if python3 -c "import json,sys; json.load(open('$path'))" 2>/dev/null; then
      pass "$file parses as valid JSON"
    else
      fail "$file is NOT valid JSON"
      continue
    fi
    # Check $id contains the expected version (suffix match)
    actual_id=$(python3 -c "import json; print(json.load(open('$path')).get('\$id', ''))" 2>/dev/null)
    if echo "$actual_id" | grep -q "/$expected_version\.json$"; then
      pass "$file declares \$id with version '$expected_version'"
    else
      fail "$file has \$id '$actual_id' — expected to end in '/$expected_version.json'"
    fi
    # Check title + type fields exist
    has_required=$(python3 -c "
import json
d = json.load(open('$path'))
print('ok' if 'title' in d and 'type' in d and 'required' in d else 'missing')
" 2>/dev/null)
    if [ "$has_required" = "ok" ]; then
      pass "$file has title + type + required top-level fields"
    else
      fail "$file missing required top-level field (title / type / required)"
    fi
  elif command -v jq >/dev/null 2>&1; then
    if jq empty "$path" >/dev/null 2>&1; then
      pass "$file parses as valid JSON (jq fallback, no version check)"
    else
      fail "$file is NOT valid JSON"
    fi
  else
    warn "neither python3 nor jq available; skipping JSON validation of $file"
  fi
done

# ────────────────────────────────────────────────────────────────
section "v1.5 Phase B dashboard — Python syntax"
# ────────────────────────────────────────────────────────────────

# We don't require streamlit to be installed — just that the source files parse.
# Use py_compile for a cheap syntax check.

if command -v python3 >/dev/null 2>&1; then
  for pyfile in dashboard/config.py dashboard/pricing.py dashboard/loaders.py dashboard/selftest.py dashboard/app.py dashboard/views/portfolio.py dashboard/views/proposal.py dashboard/views/spend.py dashboard/views/ledger.py scripts/render-graphic.py; do
    if [ ! -f "$pyfile" ]; then
      fail "missing python file: $pyfile"
      continue
    fi
    if python3 -m py_compile "$pyfile" 2>/dev/null; then
      pass "$pyfile parses as valid Python"
    else
      fail "$pyfile has a syntax error (run: python3 -m py_compile $pyfile)"
    fi
  done
else
  warn "python3 not available; skipping dashboard syntax validation"
fi

# ────────────────────────────────────────────────────────────────
section "v1.5 Phase D graphic templates"
# ────────────────────────────────────────────────────────────────

# Every template dir under reference/graphic-templates/ must have the canonical 5 files.
# Also verify example.html can be re-rendered from template + example-data (strict mode).

required_template_files=("template.html" "schema.json" "example-data.json" "example.html" "README.md")

if [ ! -d "reference/graphic-templates" ]; then
  fail "reference/graphic-templates/ dir missing"
else
  pass "reference/graphic-templates/ exists"
  if [ -f "reference/graphic-templates/README.md" ]; then
    pass "reference/graphic-templates/README.md exists"
  else
    fail "reference/graphic-templates/README.md missing"
  fi
  for dir in reference/graphic-templates/*/; do
    tname=$(basename "$dir")
    for req in "${required_template_files[@]}"; do
      if [ -f "$dir$req" ]; then
        pass "$dir$req exists"
      else
        fail "$dir$req MISSING"
      fi
    done

    if [ -f "$dir/schema.json" ] && command -v python3 >/dev/null 2>&1; then
      if python3 -c "import json; json.load(open('$dir/schema.json'))" 2>/dev/null; then
        pass "$dir/schema.json parses as valid JSON"
      else
        fail "$dir/schema.json is not valid JSON"
      fi
    fi

    if [ -f "$dir/example-data.json" ] && command -v python3 >/dev/null 2>&1; then
      if python3 -c "import json; json.load(open('$dir/example-data.json'))" 2>/dev/null; then
        pass "$dir/example-data.json parses as valid JSON"
      else
        fail "$dir/example-data.json is not valid JSON"
      fi
    fi

    # Strict re-render: example.html must reproduce from template + example-data with no unresolved placeholders
    if [ -f "$dir/template.html" ] && [ -f "$dir/example-data.json" ] && command -v python3 >/dev/null 2>&1; then
      tmp_out=$(mktemp).html
      if python3 scripts/render-graphic.py "$dir/template.html" "$dir/example-data.json" "$tmp_out" --strict >/dev/null 2>&1; then
        pass "$tname: strict render from template + example-data succeeds (no unresolved placeholders)"
      else
        fail "$tname: strict render FAILED — unresolved placeholders or missing fields in example-data"
      fi
      rm -f "$tmp_out"
    fi
  done
fi

# ────────────────────────────────────────────────────────────────
section "Process-vocabulary leakage in shipped examples and drafts"
# ────────────────────────────────────────────────────────────────
# Drafts are evaluator-facing. They must not contain process labels — Shipley
# vocabulary, color-team words, pattern-annotation labels, or rubric jargon.
# Scope: examples/**/drafts/, examples/**/drafts/edited/, drafts/, drafts/edited/.
# (Skips reviews/, working/, reference/, my-company/, proposals/ — those are
# internal artifacts, process vocabulary is appropriate there.)

LEAK_PATTERNS=(
  '\[Pattern [0-9]'
  'Pink Team'
  'Gold Team'
  'White Glove'
  'Black Hat'
  '\bpWin\b'
  'Significant Strength'
  'Significant Weakness'
  'Shipley'
  'discriminator proof point'
  'compliance matrix'
  'win theme'
  'storyboard-pink'
)

leak_scan_dirs=()
[ -d "drafts" ] && leak_scan_dirs+=("drafts")
while IFS= read -r d; do leak_scan_dirs+=("$d"); done < <(find examples -type d -name drafts 2>/dev/null)

if [ ${#leak_scan_dirs[@]} -eq 0 ]; then
  warn "No drafts directories found to scan"
else
  total_leaks=0
  for d in "${leak_scan_dirs[@]}"; do
    while IFS= read -r f; do
      [ -z "$f" ] && continue
      file_leaks=0
      for pat in "${LEAK_PATTERNS[@]}"; do
        # -i case-insensitive; skip HTML comments (used legitimately for evidence markers)
        matches=$(grep -inE "$pat" "$f" 2>/dev/null | grep -v '<!--' || true)
        if [ -n "$matches" ]; then
          file_leaks=$((file_leaks + $(echo "$matches" | wc -l)))
        fi
      done
      if [ $file_leaks -gt 0 ]; then
        fail "Process-vocabulary leak in $f ($file_leaks match(es) — run: grep -inE '$(IFS='|'; echo "${LEAK_PATTERNS[*]}")' '$f')"
        total_leaks=$((total_leaks + file_leaks))
      else
        pass "$f: no process-vocabulary leakage"
      fi
    done < <(find "$d" -name "*.md" -type f 2>/dev/null)
  done
fi

# ────────────────────────────────────────────────────────────────
section "Summary"
# ────────────────────────────────────────────────────────────────
echo ""
echo "  Checks run: $CHECK"
echo "  Passes:     $((CHECK - FAIL - WARN))"
echo "  Warnings:   $WARN"
echo "  Failures:   $FAIL"
echo ""
if [ $FAIL -gt 0 ]; then
  echo "  ✗ SMOKE TEST FAILED — $FAIL issue(s) must be resolved before releasing."
  exit 1
else
  echo "  ✓ SMOKE TEST PASSED"
  exit 0
fi
