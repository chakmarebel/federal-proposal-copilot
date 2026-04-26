# Capture Planning Methodology

The discipline of positioning your organization to win a specific federal opportunity **before the proposal is even released**. Distinct from proposal drafting — capture planning happens upstream, during the period when customer relationships, requirements shaping, and competitive positioning determine ~40-80% of the outcome.

**Core insight:** The buying decision is made before the proposal is submitted. Industry data: 40-80% of buying decisions are substantially decided before any proposal arrives. Your goal in capture is to be the offeror the customer prefers when the proposal stage begins.

**Source:** Shipley Proposal Guide §Capture Planning (industry-standard methodology). This framework documents the methodology in its own language; the source is cited generally, never reproduced verbatim.

---

## When to use this methodology

- A federal opportunity has been identified, and the offeror is considering pursuit
- Customer relationships, requirements shaping, or competitive positioning could meaningfully change the outcome
- Bid stakes warrant the BD investment (typically $50K+ in BD spend or contract value $5M+)

**When NOT to use:**
- Reactive bids on commodity work (lowest-price-technically-acceptable services where positioning has minimal effect)
- Sole-source / sole-eligible vehicles where competition is procedural
- Bid-or-no-bid decisions that haven't reached the "pursue" stage yet (use `opportunity-quick-look` first)

---

## 5-phase structure

Capture planning has five phases, each with defined inputs and outputs:

| Phase | What happens | Output |
|---|---|---|
| **1. External Analysis** | Opportunity description, customer analysis, competitive analysis | Documented opportunity context |
| **2. Internal Analysis** | Probable solution definition, cost/pricing analysis, teaming partner selection | Internal capability assessment + solution outline |
| **3. Strategy Development** | Win strategy, positioning actions, value proposition | Capture plan with action list |
| **4. Execution** | Customer engagement, requirements shaping, teaming actions | Influence on the customer's preference |
| **5. Monitoring** | Track positioning, evaluate progress, adjust strategy | Adjusted plan + bid decision |

The phases overlap and iterate — capture planning is **dynamic and continuous**, not a sequential one-pass exercise.

---

## 10-point capture-planning discipline

Calibrated against the Shipley methodology:

1. **Implement a capture-planning discipline** to capture new business more efficiently — not as a one-off
2. **Use a defined structure** (the 5 phases above) for every capture plan; consistency lets reviewers and management compare across opportunities
3. **Keep the process dynamic, flexible, interactive, and current** — capture plans are living documents, not static deliverables
4. **Maintain a balance between planning and execution** — over-planning without action wastes time; over-action without planning loses focus
5. **Complete the Integrated Solution Worksheet and the Bidder Comparison Matrix**, even when time is short — these two artifacts are the highest-leverage capture tools
6. **Gain and maintain senior management approval and support** — capture planning costs money; executive sponsorship is essential
7. **Commit the right people to the capture team** — sales, technical, finance, and (often) a dedicated capture manager
8. **Assign specific measurable objectives, schedules, and completion dates** to department managers by name — accountability matters
9. **Establish regular reviews** to check progress, resolve conflicts, obtain feedback, make adjustments, and reevaluate pursuit and bid decisions
10. **Use the capture plan to jump-start the proposal planning process** — the capture plan IS the seed of the proposal-plan

---

## Key artifacts

### Integrated Solution Worksheet

The structural heart of a capture plan. A row-per-issue table with these columns:

| # | Prospect Issues | Prospect Requirement | Available Solution | Gap | Competitor Solution | Discriminator Strategy | Action Required |
|---|---|---|---|---|---|---|---|

**How to use it:**

- **Early in capture** (before requirements drafted): fill down the **Prospect Issues** column first. What are the customer's stated and unstated pains?
- **Once requirements exist:** fill down the **Prospect Requirement** column with the formal requirements as drafted.
- **Then complete each row horizontally:** for each issue/requirement, walk through Available Solution → Gap → Competitor Solution → Discriminator Strategy → Action Required.

The Integrated Solution Worksheet feeds directly into the proposal's win-themes work and the discriminator-with-proof-point pattern. When proposal-writer drafts later, this worksheet is the structured source for theme statements and discriminators.

### Bidder Comparison Matrix

A weighted competitor scoring grid:

| Issue | Weight | Us (score) | Company A | Company B | Company C |
|---|---|---|---|---|---|
| Specific Experience | 30 | ... | ... | ... | ... |
| Low Price | 20 | ... | ... | ... | ... |
| Technical Approach | 25 | ... | ... | ... | ... |
| Past Performance | 15 | ... | ... | ... | ... |
| Customer Relationships | 10 | ... | ... | ... | ... |
| **Total** | **100** | ... | ... | ... | ... |

**How to use it:**
- Issues should mirror the customer's likely evaluation factors (informed by RFI/Sources Sought language, prior similar procurements, customer interactions)
- Weight column distributes 100 points across issues
- Score cells use a 1-10 or 1-25 scale per issue
- Compute weighted scores: `(score × weight)` per cell, sum per column
- The output is a **predicted relative position** vs. each named competitor

This matrix feeds into the framework's existing `competitor-assessment` skill and into the Black Hat Team review.

---

## Mapping capture planning to framework files

| Capture-planning artifact | Framework location |
|---|---|
| Integrated Solution Worksheet | `working/integrated-solution-worksheet.md` (or `.json` for structured form) — produced by `capture-scorecard` or a new `capture-plan` skill |
| Bidder Comparison Matrix | `working/competitor-assessment.md` (existing) — but extended to include explicit weighted scoring per Shipley methodology |
| Customer profile | `working/customer-profile.md` (existing — produced by `customer-intel`) |
| Win strategy | `working/proposal-plan.md` (existing — `win_themes` field in `working/proposal-plan.json`) |
| Action list / positioning actions | `working/capture-action-list.md` (gap — not currently produced by any skill) |

**Identified framework gap:** the framework currently has no explicit `capture-plan.md` artifact that consolidates all capture-planning outputs. The `capture-scorecard` skill is a 9-dimension stoplight, not a full capture plan. Future enhancement: a `/capture-plan` skill that produces the consolidated plan using this methodology.

---

## Bid decisions framework

Capture planning informs **multiple bid decisions** along the way, not a single yes/no. Shipley defines four distinct decision points:

| Decision | When | Question | Investment to date |
|---|---|---|---|
| **Interest Decision** | Opportunity identified | Does this fit our strategic goals + capabilities? Worth gathering more info? | ~0% (free) |
| **Pursuit Decision** | After initial customer engagement | Do we have a realistic chance of becoming the customer's preferred choice? | ~0.5-1% of contract value |
| **Preliminary Bid Decision** | After substantial capture work | Should we allocate proposal-development resources? | ~1-3% of contract value |
| **Final Bid Decision** | At RFP release | Do we still bid, given the actual RFP? | ~5-10% of contract value |
| **Submit Decision** | After Gold Team review | Do the final offer terms (price, risk) warrant submission? | ~25-30% of expected proposal-development cost |

Each decision point uses different criteria. The framework's existing `opportunity-quick-look` skill aligns roughly with the Interest Decision; `capture-scorecard` aligns with Pursuit + Preliminary Bid.

---

## Capture-planning rhythm

Calibrated norms:
- **Weekly capture-team meetings** during active capture
- **Monthly executive reviews** for opportunities >$10M expected value
- **Bid-Decision Review** at each formal decision point — documented, with go/no-go decision recorded
- **Capture plan refreshes**: full update at each decision point; quarterly even when no decision pending

---

## Pink-team integration

Capture planning culminates in a **Blue Team review** of the capture plan and win strategy (see `reference/methodology/color-teams.md` §Blue Team) before the formal Bid Decision. Black Hat Team review of competitor positioning may run in parallel.

These reviews are **independent** of the proposal team — capture and proposal are separate disciplines, even if some people contribute to both.

---

## Calibration notes

This methodology comes from Shipley as the canonical industry reference. The framework's existing skills cover **fragments** of capture planning (`capture-scorecard`, `opportunity-quick-look`, `competitor-assessment`, `customer-intel`) but **do not currently consolidate into a single capture plan**. This is a deliberate gap to be filled in a future enhancement (`/capture-plan` skill).

For now, this methodology doc serves as the reference standard. When running capture, use the existing skills + the methodology described here. The structured outputs (Integrated Solution Worksheet, Bidder Comparison Matrix, action list) can be hand-authored in `working/` files following the patterns above.
