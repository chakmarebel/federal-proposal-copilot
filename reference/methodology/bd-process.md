# Business Development Process

The end-to-end lifecycle from market positioning through post-submit lessons learned. Provides the **structural backbone** that capture planning, proposal development, and review all live within.

**Source:** Shipley Proposal Guide §Process (industry-standard methodology). Documented in this framework's own language; source cited generally.

---

## 6-phase framework

Most successful federal-contracting organizations operate against a 6-phase business-development process:

```
Phase 1: Market Segmentation and Positioning
            │
            ↓
   ┌─── Interest Decision ───┐
            │
            ↓
Phase 2: Opportunity Identification & Qualification
            │
            ↓
   ┌─── Pursuit Decision ────┐
            │
            ↓
Phase 3: Capture (Pre-Bid)
            │
            ↓
   ┌── Preliminary Bid Decision ──┐
            │
            ↓
Phase 4: Proposal Planning
            │
            ↓
   ┌──── Final Bid Decision ──────┐
            │
            ↓
Phase 5: Proposal Development
            │
            ↓
   ┌────── Submit Decision ───────┐
            │
            ↓
Phase 6: Post-Submit (Negotiation, Lessons Learned, Win/Loss)
```

Each phase has **mandatory milestones** with verifiable inputs and outputs. Each milestone gates the next phase.

---

## Per-phase detail

### Phase 1: Market Segmentation and Positioning

**Owner:** Marketing / strategic BD leadership

**Activities:** market analysis, target customer identification, competitor landscape mapping, capability positioning, thought leadership, presence-building

**Output:** Market intelligence + positioning artifacts (white papers, conference presence, customer relationships) that establish the organization in the target segment

**No specific opportunity yet.** Phase 1 is upstream of any single bid.

### Phase 2: Opportunity Identification & Qualification

**Owner:** Sales / BD individual contributors

**Activities:** opportunity discovery (via SAM.gov, customer conversations, FedBizOpps successors, etc.), initial qualification (does it fit?), capture-readiness assessment

**Output:** Decision to invest capture resources or not (Interest Decision)

**Framework alignment:** `/opportunity-quick-look` skill. Produces `working/quick-look.md` with go/hold/no-go signal.

### Phase 3: Capture (Pre-Bid)

**Owner:** Capture manager (often dedicated, separate from proposal manager)

**Activities:** customer engagement, requirements shaping, competitive intelligence, teaming decisions, win-strategy development, capture plan execution

**Output:** Customer positioning (you are the preferred offeror), capture plan documenting strategy + actions

**Framework alignment:** `/customer-intel`, `/competitor-assessment`, `/capture-scorecard` skills + the methodology in [`capture-planning.md`](capture-planning.md). Reviews include Blue Team + Black Hat Team (see [`color-teams.md`](color-teams.md)).

### Phase 4: Proposal Planning

**Owner:** Proposal manager (may be different from capture manager)

**Activities:** RFP analysis, compliance matrix seed, win-theme refinement, storyboarding, mock-up development, writer assignments

**Output:** Proposal plan + storyboards/mock-ups validated by Pink Team review

**Framework alignment:** `/proposal-manager`, `/proposal-solution-architect`, `/proposal-graphics` (graphics-brief stage), `/compliance-check` (initial seed). Pink Team review on storyboards (see [`color-teams.md`](color-teams.md) §Pink Team — storyboard-pink mode).

### Phase 5: Proposal Development

**Owner:** Proposal manager + writers

**Activities:** prose drafting, graphics production, evidence-citation, compliance verification, internal review cycles

**Output:** Submission-ready proposal package validated by Red Team + Gold Team reviews

**Framework alignment:** `/proposal-writer`, `/proposal-graphics` (rendering), `/pricing-analyst`, `/evidence-check`, `/compliance-check`, `/red-team-review` (modes: pink-compliance, red, gold), `/export-proposal`.

### Phase 6: Post-Submit

**Owner:** Capture team + proposal team + leadership

**Activities:** customer Q&A response, oral presentations (if required), best-and-final-offer (BAFO) preparation, customer debrief request, lessons learned

**Output:** Negotiated contract (if won) + lessons learned + win/loss intelligence for future bids

**Framework alignment:** Limited current coverage. `/red-team-review --mode=lessons-learned` consumes customer debrief if available. Future enhancement: `/post-submit` skill to manage Q&A response, BAFO, and debrief integration.

---

## 5 milestone decision points

Each transition between phases has a formal decision point. The decisions get progressively expensive — a "yes" at the Interest Decision commits ~0% of contract value; a "yes" at the Submit Decision commits 25-30% of proposal cost.

| # | Decision | Phase Transition | Question | Cost commitment to date |
|---|---|---|---|---|
| 1 | **Interest Decision** | Phase 2 → Phase 3 | Worth capture investment? | ~0% |
| 2 | **Pursuit Decision** | Phase 3 (commit fully) | Realistic chance to win? | ~0.5-1% |
| 3 | **Preliminary Bid Decision** | Phase 3 → Phase 4 | Allocate proposal resources? | ~1-3% |
| 4 | **Final Bid Decision** | Phase 4 → Phase 5 | RFP-as-released still favorable? | ~5-10% |
| 5 | **Submit Decision** | Phase 5 → Phase 6 | Final offer acceptable? | ~25-30% |

Each decision is **document-based**: a written go/no-go with rationale, signed off by the appropriate authority level.

**Decision authority levels (typical):**
- Interest Decision: BD individual contributor or first-line manager
- Pursuit Decision: BD director or VP
- Preliminary Bid Decision: BD VP or COO
- Final Bid Decision: COO or CEO
- Submit Decision: CEO or designated executive (Gold Team chair)

Skipping any decision point or letting it become rubber-stamp creates risk. **Every "yes" should be earned**; the organization should be willing to say "no" at any point.

---

## Process design principles

Calibrated against industry best practices:

1. **Single, flexible, scalable process** — one process, championed at executive level, that scales from $100K SBIR to $1B+ IDIQ
2. **Aligned with prospects' buying cycles** — your process should match how customers actually buy, not the textbook ideal
3. **Document-based reviews at each milestone** — written decisions, not water-cooler "yeahs"
4. **Adaptable via flexible support tools** — the process is the same; the artifacts produced are tailored to opportunity size
5. **Defined roles, responsibilities, authority levels** — including thresholds (e.g., "VP authority below $10M; CEO authority above")
6. **Aligned with corporate policies** — business development doesn't run on a different planet from finance, legal, contracts
7. **Documented, consistent, repeatable** — the process is itself an artifact, not tribal knowledge
8. **Trained participants** — annual refresher; new hires onboarded within 30 days
9. **Designated process owner** — collects metrics, fosters improvement, maintains tools and infrastructure

---

## Framework alignment

The framework's skills cover **most of this lifecycle** but with gaps:

| Phase | Framework coverage |
|---|---|
| 1 — Market Segmentation | ❌ Not covered (out of scope — strategic BD, not proposal-specific) |
| 2 — Opportunity ID & Qualification | ✅ `/opportunity-quick-look` |
| 3 — Capture | ⚠️ Partial: `/customer-intel`, `/competitor-assessment`, `/capture-scorecard`. **Gap:** no consolidated `/capture-plan` skill; capture artifacts are fragmented across multiple files |
| 4 — Proposal Planning | ✅ `/proposal-manager`, `/proposal-solution-architect`, `/proposal-graphics` (brief stage), `/compliance-check` (seed) |
| 5 — Proposal Development | ✅ `/proposal-writer`, `/pricing-analyst`, `/evidence-check`, `/compliance-check`, `/red-team-review`, `/export-proposal` |
| 6 — Post-Submit | ❌ Not covered. Future enhancement candidate |

**Identified framework gaps** worth filling in future enhancement passes:
- `/capture-plan` skill: produces consolidated capture plan from the fragmented inputs (Integrated Solution Worksheet, Bidder Comparison Matrix, action list, customer profile, competitive analysis)
- `/post-submit` skill: manages customer Q&A response, BAFO preparation, debrief request, lessons-learned integration
- `/bd-decision` skill: produces a documented decision artifact for each of the 5 milestone decision points (currently the framework has no explicit decision artifact)

---

## Decision-document template

For any of the 5 milestone decisions, produce a written decision artifact in `working/decisions/<decision-name>.md`. Calibrated structure:

```markdown
# [Decision Name] — [Opportunity Name]

**Decision date:** YYYY-MM-DD
**Decision maker:** [Name, Role]
**Decision:** GO / HOLD / NO-GO
**Phase transition:** Phase N → Phase N+1

## Context
[1-2 paragraph summary of the opportunity status and the decision being made]

## Criteria evaluated
[Bullet list of the criteria considered for this decision — varies by decision type. See "5 milestone decision points" above for typical questions.]

## Rationale
[Why this decision]

## Authorized actions
[What this decision authorizes the team to do — capture spend, proposal-development resources, etc.]

## Conditions / open questions
[Anything that must remain true for the decision to hold]

## Next milestone
[When the next decision point is and what triggers it]
```

This artifact provides the audit trail for executive review and informs the post-submit lessons-learned analysis.
