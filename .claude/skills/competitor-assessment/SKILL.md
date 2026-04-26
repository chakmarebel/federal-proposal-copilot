---
name: competitor-assessment
description: Use this skill to identify likely competitors, profile each one, build a weighted Bidder Comparison Chart, identify teaming gaps, and generate win strategy statements. Uses open source web research plus inputs from the proposal workspace. Writes to working/competitor-assessment.md.
---

# Competitor Assessment Skill

## Purpose
Identify who you're competing against, understand their strengths and positions with the customer, score yourself against them on the factors that matter to the customer, find the gaps you need to fill through teaming, and generate strategy statements that drive every subsequent proposal decision.

This is the analytical engine of the entire capture — win strategy, teaming, pricing, and proposal themes all flow from this assessment.

## Capture Mode
**Read `working/proposal-brief.md` before proceeding.** Check two fields:
- `Capture Mode:` — Full Capture or Responsive
- `Proposal type:` — SBIR / CSO / OTA / BAA / RFP / IDIQ / etc.

Then go to the appropriate workflow section:
- **Full Capture** → run the complete workflow below (Steps 1–7)
- **Responsive** → skip to [Responsive Mode](#responsive-mode) at the bottom of this skill

If `proposal-brief.md` doesn't exist or the field is blank, ask the user before proceeding.

## When to Use
- Any competitive bid (RFP, RFQ, BAA, SBIR, OTA)
- Run after `/proposal-manager` (need proposal-plan.md for hot buttons and eval criteria)
- Run before or parallel to `/proposal-solution-architect`
- Skip for sole-source awards or white papers where competition is unknown

## Inputs
Read before starting:
1. `working/proposal-plan.md` — customer hot buttons, eval criteria, opportunity classification
2. `inputs/00_priority/` — solicitation for NAICS code, set-aside type, scope
3. `inputs/01_customer/` — customer context, agency, mission
4. `inputs/02_yourCompany/` — your company's capabilities and past performance for self-assessment

## Workflow

### Step 1: Research Likely Competitors
Use available web search tools to identify likely bidders. Search across:

**Award databases:**
- USASpending.gov: prior awards to this customer, same NAICS, similar scope — search "[customer agency] [capability area] contract awards"
- SAM.gov: active registrations, set-aside eligibility for this NAICS
- FPDS (Federal Procurement Data System): historical contract data

**Company intelligence:**
- LinkedIn: companies claiming this customer as a reference or this capability domain
- Company press releases: "[competitor name] [agency] contract award"
- GovWin / Deltek / Bloomberg Government (if accessible)
- Agency small business directories and 8(a) lists if set-aside

**Criteria for identifying likely competitors:**
- Currently working for this customer (incumbent advantage is real)
- Won similar contracts at similar size in the last 3 years
- Claims the same capability domain
- Same set-aside category (small business, 8(a), HUBZone, SDVOSB, etc.)
- Has a public relationship with the customer (press releases, conference presentations)

Identify 3–6 most likely competitors. If a competitor is unknown, use "Unknown Competitor" as a placeholder row and describe the archetype (e.g., "Large Prime with existing customer relationship").

---

### Step 2: Profile Each Competitor
For each identified competitor, research and document:

| Field | What to Find |
|-------|-------------|
| Market position | Prime or sub? LPTA player or best-value? |
| Products / services | What specifically do they offer for this scope? |
| Historical pricing | Past awards — contract value, vehicle, type |
| Customer relationship | Incumbent? How long? Key relationships? |
| Relevant experience | Past contracts similar to this scope |
| Past performance rating | Any public CPAR data or debrief intel |
| Probable approach | How will they likely propose? What's their pitch? |
| Strengths | What will they emphasize? |
| Weaknesses | Where are they vulnerable? |
| Key personnel | Named employees likely to appear on this bid |

Use web search for each. Prioritize: company website, LinkedIn, press releases, USASpending awards, GovWin profiles.

---

### Step 3: Self-Assessment
Apply the same profile to your company using `inputs/02_yourCompany/` files:
- What is our market position with this customer?
- What is our relevant experience for this specific scope?
- What is our past performance portfolio and its relevance?
- Where are we strong vs. the evaluation criteria?
- Where are we weak or uncovered?

---

### Step 4: Build the Bidder Comparison Chart
Using the customer hot buttons and evaluation criteria from `working/proposal-plan.md`:

**Structure:**
- Rows = Customer hot buttons / evaluation factors (from proposal plan)
- Columns = Your Company + each identified competitor
- Weight = 1–3 (1=important, 2=more important, 3=most important) — derived from eval factor weights or inferred from solicitation emphasis
- Score = 1–10 for each company on each factor (1–2=significant weakness, 5=neutral, 9–10=clear leader)
- Weighted Score = Weight × Score
- Total = sum of all weighted scores

| Hot Button / Factor | Weight | Your Company | Competitor A | Competitor B | Competitor C |
|---------------------|--------|-------------|-------------|-------------|-------------|
| [Factor 1] | | Score / WS | Score / WS | Score / WS | Score / WS |
| [Factor 2] | | | | | |
| **TOTAL** | | | | | |

**Scoring guidance:**
- 9–10: Clear leader — documented proof, customer acknowledgment
- 7–8: Strong position — good evidence, likely recognized by customer
- 5–6: Neutral — adequate but undifferentiated
- 3–4: Weakness — below average, no clear evidence
- 1–2: Significant gap — missing capability or poor past performance

---

### Step 5: Teaming Gap Analysis
Using the Bidder Comparison Chart and `working/capability-matrix.md` (if it exists from proposal-solution-architect):

**Identify gaps that require teaming:**
- Any evaluation factor where your company scores below 5
- Any requirement in the capability matrix with no coverage
- Any past performance category where you have no citable example

For each gap, assess:
- Can we address it with a teaming partner?
- What type of company fills this gap (systems integrator, cleared facility, specific domain expertise)?
- Known companies that could fill this role?

| Gap | Factor / Requirement | Type of Partner Needed | Candidate Partners | Priority |
|-----|---------------------|----------------------|-------------------|---------|
| | | | | High / Med / Low |

**Teaming decision rules:**
- If a gap is against a mandatory evaluation factor → teaming is required to bid
- If a gap is against a desired factor → teaming improves competitiveness
- If all gaps can be covered by partners → recommend BID with teaming
- If a mandatory gap cannot be covered → recommend reconsidering bid

---

### Step 6: Generate Strategy Statements
For the top 5–8 factors from the Bidder Comparison Chart, generate one or more strategy statements using the four Shipley types:

**Template:** "We will [TYPE] by [SPECIFIC ACTION]."

**Four types:**
1. **Leverage Our Strength:** "We will leverage [our discriminator] by [how we communicate it] to [customer outcome]."
2. **Mitigate Our Weakness:** "We will mitigate [our shortfall] by [teaming / solution design / framing] to [reduce evaluator concern]."
3. **Exploit Competitor Weakness:** "We will highlight [competitor's gap] by [emphasizing the contrast in our proposal] without naming them directly."
4. **Neutralize Competitor Strength:** "We will neutralize [competitor's advantage] by [repositioning the evaluation factor / ghosting / offering a superior alternative]."

Strategy statements feed directly into:
- Win themes in `working/proposal-plan.md` (update if needed)
- Solution design emphasis in `/proposal-solution-architect`
- Section framing in `/proposal-writer`
- Graphics selection in `/proposal-graphics`

---

### Step 7: Write Output File
Write all findings to `working/competitor-assessment.md`:

```markdown
# Competitor Assessment — [Proposal Name]

## Identified Competitors
[Summary table: company, set-aside category, incumbent status, overall threat level (High/Med/Low)]

## Competitor Profiles
[One section per competitor with all profiled fields]

## Self-Assessment
[Your company position on this specific opportunity]

## Bidder Comparison Chart
[Full weighted table]

## Teaming Gap Analysis
[Gap table with partner recommendations]

## Strategy Statements
[Organized by type, linked to Bidder Comparison Chart factors]

## Intelligence Gaps
[What we couldn't find and need to resolve before proposal kickoff]
```

**Always write to disk — do not just display in chat.**

---

---

## Responsive Mode

Use this workflow for SBIR, CSO, OTA, BAA, and white papers. The goal is a competitive picture — not a weighted matrix. Evaluators in these vehicles care more about your innovation and differentiation than about a head-to-head comparison.

### Responsive Step 1: Who's Playing in This Space
Web search for companies active in this capability area with this customer type. Focus on:
- Who has received awards from this agency or innovation office in the last 2 years?
- Who is presenting at relevant conferences (SOFIC, C4ISRNET, AUSA, DIU pitch days)?
- Who is publicly claiming this capability domain?
- For SBIR: who won Phase I/II topics in this technology area at this agency?

Produce a simple summary table (5–8 companies max):

| Company | Size | Relevant Work | Relationship With Customer | Threat Level |
|---------|------|--------------|---------------------------|-------------|
| [name] | Small/Mid/Large | [brief] | [known/unknown/incumbent] | High/Med/Low |

### Responsive Step 2: Your Top 3 Differentiators
Based on the competitive landscape and the customer's stated problem:
- What do you have that none of the players above can claim?
- What proof do you have for each (deployment, publication, benchmark)?

| Differentiator | Proof Point | Who Can't Match It |
|---------------|-------------|-------------------|
| | | |

### Responsive Step 3: Teaming Gap Check
Quick scan of the capability requirements from `working/proposal-plan.md` or `inputs/00_priority/`:
- Is there anything required that you can't cover?
- If yes: what type of partner fills it, and is teaming required to bid or just helpful?

Flag any mandatory gaps (must-have to bid) separately from helpful gaps.

### Responsive Step 4: Ghosting Language
For each of your top differentiators, draft 1–2 sentences of ghosting language — describing what you offer in a way that implicitly highlights competitors' weaknesses without naming them:

> *"Unlike cloud-dependent AI solutions, [Your Company] operates fully on-device with no network requirement — enabling consistent performance in disconnected, degraded, and air-gapped environments."*

These go directly into the proposal's technical approach and executive summary.

### Responsive Output
Write `working/competitor-assessment.md` with:
- Competitive landscape table
- Your top 3 differentiators with proof points
- Teaming gaps (mandatory vs. helpful)
- Ghosting language snippets (copy-paste ready)

**Always write to disk — do not just display in chat.**

---

## After Running This Skill
Tell the user:
1. Competitive threat summary — who is the top threat and why
2. Top 3 teaming gaps (mandatory vs. desired)
3. 3 recommended strategy statements to anchor the win strategy
4. Any intelligence gaps that need follow-up before the proposal team kicks off

## Rules
- Do not fabricate competitor capabilities — clearly label any inferred or unconfirmed data
- Flag when incumbent advantage is present — this is a major risk factor
- Score your company objectively — overconfident self-scoring produces losing proposals
- If web search returns limited results, document what was searched and what was found
- For set-aside competitions, flag any competitor that may not qualify for the set-aside

## Lessons Learned

### On Competitive Positioning
- A strong discriminator in military AI is the combination of on-device inference + military specialization + published benchmarks. Few competitors can claim all three.
- The most common competitor archetype in defense AI is a large prime (Booz, Leidos, SAIC, Palantir) with a cloud-dependent AI offering. Ghost their cloud dependency when positioning an edge-native approach.
- SBIR/STTR competitors are often university spinouts or small tech firms. Their weakness is typically operational experience and scale — operational deployments with real end users are a hard discriminator here.

### On Teaming
- For DOD programs over $10M, systems integration experience from a large prime or mid-tier is often needed to cover the "systems integration" or "program management at scale" evaluation factor.
- Cleared facilities (SCIF access, TS/SCI) are a frequent gap for early-stage defense AI companies. Identify this early — remedying it takes months.
- Teaming agreements need to be in place before proposal submission. Flag timing risks when teaming is required.

### On Strategy Statements
- The most effective strategy statements are customer-outcome-focused, not capability-focused. "We will reduce mission planning time from hours to minutes by deploying an on-device AI assistant" beats "We will leverage our advanced AI capabilities."
- Ghosting works: describe what you offer (on-device, air-gapped, no cloud dependency) without naming competitors. Evaluators who know the competitive landscape will make the comparison themselves.
