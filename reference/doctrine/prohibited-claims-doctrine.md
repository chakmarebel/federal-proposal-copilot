# Prohibited Claims — Universal Doctrine

This is the universal Shipley discipline for federal proposal work. It applies
to every company persona the workbench operates on. Per-company additions
live in each company's own knowledge dir; deviations are recorded in the
company's `doctrine-overrides.md` and surface to reviewers as named
exceptions, not silent overrides.

## Never Claim Without Explicit Evidence

These are categorical no-go phrases unless the active proposal has a direct,
verifiable citation in the evidence ledger:

- FedRAMP authorization at any level
- SOC 2 certification
- ISO 27001 certification
- CMMC level
- NIST SP 800-171 / SPRS score
- Socioeconomic certifications (8(a), SDB, WOSB, SDVOSB, HUBZone, etc.)
- GSA MAS schedule status
- ATO transferability across customer commands or environments
- Blanket authorization for all customers or all environments
- Export-control determinations
- Classified deployment details
- Customer endorsements or testimonials
- Benchmark superiority for models other than the specific model evaluated
- Access to government data, systems, facilities, or networks not under
  current contract

## Forbidden Absolutes

These words carry implicit superiority claims federal evaluators are trained
to challenge. Use them only when the active evidence ledger contains a
quantitative benchmark with named comparison and methodology:

- "Best", "only", "first", "unmatched", "world-class"
- "Most secure", "military-grade", "battle-tested"
- "Guaranteed" applied to autonomy, targeting, lethal decision support,
  hallucination elimination, or refusal-rate elimination
- "Replacement for human judgment" applied to mission-critical functions

## Doctrine Boundaries For Operational Statements

- Do not assert the company has done work it has not delivered. Submitted
  proposals are not past performance. Down-selected bids are not past
  performance. Teaming arrangements proposed but not executed are not
  partnerships.
- Do not claim a teaming agreement, MOU, or distributor relationship that
  is not signed and active.
- Do not describe a TRL level above what is documented in the evidence
  ledger.
- Do not describe an ATO posture inherited from a parent product without
  citing the program of record that granted it.

## How To Treat An Unmet Doctrine Constraint

When the active task seems to require a phrase that violates this doctrine
but the operator has not recorded an override in `doctrine-overrides.md`,
mark the gap rather than inventing proof. Use a `Gaps and Follow-Ups`
section to surface the missing evidence or the missing override decision.
Do not weaken the surrounding prose to avoid the rule — that produces
non-answers that evaluators dock harder than honest gaps.

## When An Operator Override Exists

If the active company's `doctrine-overrides.md` records a named, dated
deviation from one of these rules with stated reasoning (e.g., "The DIU
Mystic Depot SOO requires vendors to describe 'best-in-class' capabilities
through 2026-08-15"), follow the override for the duration named in the
override file. Include a `Doctrine deviations cited` block in the drafted
section so reviewers see which override was relied on and why. The
override is the audit trail; do not silently weaken doctrine elsewhere
in the draft.
