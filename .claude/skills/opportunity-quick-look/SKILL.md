---
name: opportunity-quick-look
description: Use this skill to rapidly vet a new opportunity before committing to full proposal analysis. Produces a one-page triage report covering opportunity fit, funded/unfunded status, size/scope, customer alignment, and go/no-go signal. Reads from inputs/00_priority/ and inputs/01_customer/. Writes to working/quick-look.md.
---

# Opportunity Quick Look Skill

## Purpose
A 5–10 minute triage that tells you whether an opportunity is worth pursuing before investing in full capture analysis. This is not a technical review. It is a business-sense filter — does the shape of this opportunity fit your company's profile, capacity, and priorities?

Run this first. Kill bad opportunities fast. Save full analysis for the ones that pass.

## When to Use
- A new solicitation, BAA, CSO, or white paper task drops
- You need a rapid fit assessment before briefing leadership on a new opportunity
- You are evaluating multiple opportunities in parallel and need to prioritize
- You are unsure whether to invest in `/proposal-manager` and downstream analysis

## What This Skill Does NOT Do
- Build a capability matrix (that's `/proposal-solution-architect`)
- Analyze evaluation criteria in depth (that's `/proposal-manager`)
- Assess capture readiness (that's `/capture-scorecard`)
- Research the customer in depth (that's `/customer-intel`)

---

## Inputs

Read only what exists. Do not ask for files that aren't there yet — work with what's available.

1. `inputs/00_priority/` — solicitation, BAA, CSO, white paper task, RFI (any available)
2. `inputs/01_customer/` — customer context, mission notes, any prior intel

If neither folder has content, ask the user to paste or describe the opportunity before proceeding. A URL, email, or paragraph description is sufficient to run this skill.

---

## The 7 Quick Look Factors

Assess each factor on a **GREEN / YELLOW / RED** basis. Keep each assessment to 1–2 sentences. This is judgment, not deep research.

### 1. Mission Fit
Does the stated requirement align with what your company actually does?

| Signal | Assessment |
|--------|-----------|
| 🟢 | Core to your mission: edge AI, on-device inference, DDIL environments, mission-specific LLMs, military/IC analytics |
| 🟡 | Adjacent — you could address it but it's not a natural strength (cloud AI, enterprise integrations, non-AI software) |
| 🔴 | Outside your lane: hardware-only, facilities, logistics, non-AI services, capabilities you don't have and can't build for this effort |

### 2. Customer Fit
Is this a customer segment your company can credibly serve?

| Signal | Assessment |
|--------|-----------|
| 🟢 | SOF, SOCOM, Army, USAF, USMC, defense IC, program offices with clear operational AI need |
| 🟡 | Civilian agency, unfamiliar program office, or customer with no known AI appetite — possible but needs more intel |
| 🔴 | Customer has stated preference for incumbent, has OCI concerns with your company, or is a segment you have zero relationship or credibility in |

### 3. Funding Status
Is there money behind this, and is it real?

| Signal | Assessment |
|--------|-----------|
| 🟢 | Funded: contract type specified, CLIN structure present, ceiling value stated, award expected within 12 months |
| 🟡 | Partially funded or TBD: BAA with flexible ceilings, OTA with task order structure, funding subject to congressional action |
| 🔴 | Unfunded: white paper only (no follow-on stated), exploratory RFI with no solicitation planned, budget not identified |

**Note:** Unfunded (RED) is not automatically a no-go — some white papers and BAAs are strategic positioning plays. Flag it and let the user decide.

### 4. Size and Scope Fit
Is the contract size and work scope a match for a small company?

| Signal | Assessment |
|--------|-----------|
| 🟢 | $500K–$10M, clear set-aside (SBIR, 8(a), small business), or explicitly structured for small business participation |
| 🟡 | $10M–$50M — possible as sub or in a strong team; limited set-aside language; scope may exceed current capacity without partners |
| 🔴 | $50M+ unrestricted, large integrator territory, or requires facilities/clearances/capacity your company does not have and cannot acquire for this effort |

### 5. Schedule Fit
Can we respond in time and execute if we win?

| Signal | Assessment |
|--------|-----------|
| 🟢 | Response deadline 3+ weeks out; performance period aligns to current bandwidth; no unusual mobilization requirements |
| 🟡 | Response deadline 1–3 weeks out (tight but possible); performance start is immediate with unclear ramp time |
| 🔴 | Response deadline under 1 week; requires personnel or resources you cannot staff by award; OR no deadline stated and unclear when solicitation will formalize |

### 6. Competitive Position
Do we have a credible reason to win this?

| Signal | Assessment |
|--------|-----------|
| 🟢 | You have prior relationship, relevant past performance, or a discriminating technical capability that fits the requirement; OR it's a set-aside with limited competition |
| 🟡 | You are competitive but the field is unknown; no relationship with this customer; capability match is reasonable but not differentiated |
| 🔴 | Strong incumbent with years of performance history; clear large-prime opportunity you'd enter as unknown sub; no distinguishable advantage over likely competitors |

### 7. Common Sense Barriers
Are there any immediate disqualifiers — legal, ethical, logistical, or strategic?

Examples to check:
- Clearance requirements you cannot meet by award
- Organizational conflict of interest (OCI) with existing work
- Work scope that conflicts with your ethics or customer commitments
- Geographic or facility requirements (SCIF, specific installation)
- Teaming restrictions that exclude you
- Explicitly prohibited from small business participation

| Signal | Assessment |
|--------|-----------|
| 🟢 | No significant barriers identified |
| 🟡 | One barrier exists but is resolvable (e.g., clearance can be sponsored, facility can be leased) |
| 🔴 | Hard barrier that cannot be resolved in time — disqualifying |

---

## Output Format

Write the following to `working/quick-look.md`. Always write to disk — do not just display in chat.

```markdown
# Opportunity Quick Look — [Opportunity Name]
**Date:** [today]
**Source:** [BAA / CSO / RFP / RFI / White Paper Task / Other]
**Program:** [Program name or "Unknown"]
**Customer:** [Agency / Command / Program Office]
**Ceiling Value:** [$ if known, or "Not stated"]
**Response Deadline:** [Date or "Not stated"]
**Contract Type:** [SBIR / OTA / IDIQ / FFP / Cost / Unknown]

---

## Quick Look Scorecard

| # | Factor | Status | Assessment |
|---|--------|--------|------------|
| 1 | Mission Fit | 🟢/🟡/🔴 | [1–2 sentences] |
| 2 | Customer Fit | 🟢/🟡/🔴 | [1–2 sentences] |
| 3 | Funding Status | 🟢/🟡/🔴 | [1–2 sentences] |
| 4 | Size and Scope Fit | 🟢/🟡/🔴 | [1–2 sentences] |
| 5 | Schedule Fit | 🟢/🟡/🔴 | [1–2 sentences] |
| 6 | Competitive Position | 🟢/🟡/🔴 | [1–2 sentences] |
| 7 | Common Sense Barriers | 🟢/🟡/🔴 | [1–2 sentences] |

**Score:** X Green / X Yellow / X Red

---

## Bottom Line
[2–3 sentences: what kind of opportunity is this, why it does or doesn't fit, and what the single biggest risk or opportunity is]

## Recommendation
**[PURSUE / PASS / HOLD]**

- **PURSUE** — Fits well enough to invest in `/proposal-manager` and downstream analysis. At least 5 Green, no Red in Mission Fit, Customer Fit, or Common Sense Barriers.
- **PASS** — Does not fit. Do not invest further unless circumstances change.
- **HOLD** — Interesting but missing information or a resolvable barrier. Identify what needs to happen before re-evaluating.

[1–2 sentence rationale]

## If PURSUE: Recommended Next Steps
1. [First action — e.g., run `/proposal-manager` to extract eval criteria and page limits]
2. [Second action — e.g., check clearance requirement with security officer before proceeding]
3. [Third action — e.g., identify teaming partner for [specific gap] before kickoff]

## If HOLD: What Would Change This
- [Condition 1 — e.g., "Confirm funding is in FY26 POM before investing"]
- [Condition 2 — e.g., "Wait for draft RFP to confirm small business set-aside"]
```

---

## Rules
- Do not invent funding, clearance, or customer details — state "not stated" if unknown
- An unfunded opportunity is not automatically a PASS — some are worth strategic positioning
- A single RED in Mission Fit, Customer Fit, or Common Sense Barriers is normally a PASS unless there is an explicit strategic reason to override
- Keep all factor assessments to 1–2 sentences — this is a triage, not an analysis
- If key information is absent, default to YELLOW with a note on what's missing
- Do not run this skill and then immediately pivot to full analysis in the same session — let the user confirm PURSUE before proceeding

---

## After Running This Skill
Tell the user:
1. Score (X Green / X Yellow / X Red)
2. Recommendation (PURSUE / PASS / HOLD) with one-sentence rationale
3. If PURSUE: confirm they want to proceed to `/proposal-manager` before starting

---

## Lessons Learned

### On Unfunded Opportunities
DARPA BAAs, DIU CSOs, and SOCOM white paper tasks are often "unfunded" at the quick-look stage but represent genuine pipeline. Do not reflexively score these RED on funding — look for language about follow-on contracts, transition pathways, or OTA authority. Flag it YELLOW with a note.

### On Schedule
The highest-risk response failures come from underestimating proposal burden on a compressed timeline, not from capability gaps. If the deadline is under 2 weeks and the proposal requires more than 10 pages, flag schedule RED regardless of other factors.

### On Scope Creep in Requirements
Watch for requirements that look like your lane but contain embedded scope that isn't — e.g., "AI analytics with full system integration and facility build-out." The AI portion may fit; the rest may not. Flag this in Common Sense Barriers rather than failing Mission Fit entirely.
