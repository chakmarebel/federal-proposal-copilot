# Compliance Matrix

**Proposal:** [proposal name]
**Type:** [type_id from working/proposal-type.md]
**Compliance sources:** [L, M, PWS, SOW, EvaluationCriteria, etc. from proposal-type.md]
**Last updated:** [timestamp — updated on each write by proposal-manager or proposal-writer]

---

## Purpose

Single source of truth for requirement → section → page → status traceability. Evaluators use a matrix like this to score proposals; yours should match theirs.

## How to read the Status column

| Status | Meaning |
|---|---|
| `Planned` | Requirement identified, section assigned, not yet drafted |
| `Drafted` | Section exists in `drafts/` and references this req |
| `Covered` | Section fully addresses the req, confirmed by writer |
| `Partial` | Section partly addresses — flagged for completion |
| `Exception` | Intentionally not meeting — requires rationale in narrative |
| `Gap` | Req has no section owner — must be resolved before submission |

## How to maintain

- **`proposal-manager`** seeds the table: one row per "shall" or scored requirement in the `compliance_sources` sections listed in `working/proposal-type.md`. Sets Status = `Planned` and assigns a tentative Section.
- **`proposal-writer`** updates Section, Page, Status, and Evidence when it drafts each section. Any req it does not touch must remain `Planned` or `Gap`.
- **`compliance-check`** re-reads `drafts/` and re-computes Status, flagging any row that remained `Planned` after drafts exist.
- **Humans** may flip rows to `Exception` and must add a one-line rationale in the Evidence column.

## Table

| Req ID | Source | Requirement (verbatim, trimmed ≤200 chars) | Section | Page | Status | Evidence |
|---|---|---|---|---|---|---|
| L.1 | L | [paste requirement text] | [vol/section ref] | [TBD] | Planned | |
| L.2 | L | ... | | | Planned | |
| M.1 | M | [evaluation factor] | | | Planned | |
| ... | | | | | | |

## Summary counters

Maintained by `compliance-check`. Regenerated on each run.

- **Total requirements:** 0
- **Covered:** 0
- **Drafted (not yet covered):** 0
- **Planned (no draft):** 0
- **Partial:** 0
- **Exception:** 0
- **Gap:** 0
- **Coverage %:** 0
