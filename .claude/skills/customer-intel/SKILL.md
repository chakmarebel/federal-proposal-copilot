---
name: customer-intel
description: Use this skill to research and profile the customer before writing begins. Searches open source for agency mission, key personnel, budget priorities, buying history, and hot buttons. Produces a structured customer profile combining AI-found intel with a user-fillable template for relationship knowledge. Writes to working/customer-profile.md and inputs/01_customer/.
---

# Customer Intelligence Skill

## Purpose
Build a complete picture of the customer before the architect designs anything. Understanding who the customer is, what they care about, what they've bought before, and what they're trying to achieve is what separates a generic proposal from one that feels written for them specifically.

AI can find the public record. You provide the relationship knowledge. This skill combines both.

## When to Use
- At the start of any pursuit, immediately after `/new-proposal` and before `/proposal-manager`
- When a new customer or program office is encountered for the first time
- To refresh customer knowledge on a recompete
- Any time you want to strengthen hot button alignment before drafting

## Inputs
Read before searching:
1. `working/proposal-brief.md` — customer name, agency, opportunity type
2. `inputs/01_customer/` — any existing customer materials the user has already dropped in
3. `inputs/02_yourCompany/` — your company's relationship status and prior customer interactions

## Workflow

### Step 1: Open Source Research
Using available web search tools, research the customer across these sources:

**Agency / Office:**
- Official agency website — mission statement, strategic priorities, current initiatives
- Agency news releases and press pages — what are they announcing and investing in?
- Agency leadership bios — who leads this office, what's their background and focus?
- Congressional testimony — what does leadership say under oath about priorities and gaps?

**Budget and Funding:**
- DoD Budget Justification Books (available at comptroller.defense.gov):
  - R-2 sheets (Research programs) — specific technology programs and funding levels
  - P-40 sheets (Procurement programs) — hardware/software programs and funding
  - O-1 sheets (Operations) — operational requirements driving procurement
- PPBE documents for the relevant service/agency
- Congressional Research Service reports on relevant programs
- News coverage of agency budget requests and congressional markups

**Acquisition History:**
- USASpending.gov — all awards to this agency's program office, by vendor, contract type, and value
- SAM.gov — prior Sources Sought, RFIs, solicitations from this contracting office
- FPDS — historical award patterns, preferred vehicles, vendor relationships
- SBIR.gov — prior SBIR/STTR awards from this agency in relevant technology areas

**Programs and Initiatives:**
- DoD program databases (DTIC, AcqNotes, defense.gov)
- Service-specific portals (army.mil, af.mil, navy.mil, socom.mil, etc.)
- CDAO, DIU, AFWERX, NavalX, ARL, DEVCOM program pages as relevant
- Defense news: Defense One, Breaking Defense, C4ISRNET, DVIDS

**Key Personnel:**
- Agency leadership directory and org chart
- LinkedIn profiles of program manager, SETA leads, technical directors
- Conference presentations (AUSA, ModernDayMarine, SOF Week, C4ISRNET, etc.)
- Published papers, articles, or interviews by agency technical staff

**Current Relationship Intelligence:**
- Check `inputs/02_yourCompany/` and `inputs/06_notes/` for any prior meeting notes, briefings, or contact history
- Check `inputs/06_notes/` for any call summaries or relationship intel the user has captured

---

### Step 2: Produce the Customer Profile Template
After searching, produce `working/customer-profile.md` pre-populated with everything found.

For every field AI cannot answer, leave a clearly marked placeholder: `[YOU KNOW THIS — PLEASE FILL IN]`

Use this structure:

```markdown
# Customer Profile — [Customer Name / Program Office]

**Last Updated:** [date]
**Proposal:** [short name from proposal-brief.md]

---

## 1. Organization Overview

### Mission and Strategic Priorities
[What this agency/office is chartered to do, and what they're prioritizing right now]
- Official mission statement: [found or TO BE PROVIDED]
- Current strategic priorities: [from budget docs, speeches, recent news]
- Known gaps or problems they're publicly trying to solve: [from congressional testimony, press]

### Relevant Programs and Initiatives
| Program | Description | Budget / Scale | Status |
|---------|-------------|---------------|--------|
| [program] | | | Active / Planning |

### Organization Structure (Relevant to This Pursuit)
| Role | Name | Notes |
|------|------|-------|
| Source Selection Authority (SSA) | [found or YOU KNOW THIS] | |
| Program Manager | [found or YOU KNOW THIS] | |
| Contracting Officer (CO) | [found or YOU KNOW THIS] | |
| Technical Lead / SETA | [found or YOU KNOW THIS] | |
| End Users / Operators | [YOU KNOW THIS — who uses the solution day-to-day?] | |
| Congressional Champion | [found or YOU KNOW THIS] | |
| Key Influencer | [YOU KNOW THIS — who else shapes this decision?] | |

---

## 2. Hot Buttons and Issues

### What Keeps Them Up At Night
[The problems they're trying to solve — from budget docs, testimony, speeches, news. Not requirements. Real problems.]

| Hot Button | Source | Priority (inferred) |
|------------|--------|---------------------|
| [issue 1] | [where found] | High / Med / Low |
| [issue 2] | | |

### What They've Said Publicly
[Direct quotes from leadership on this topic — from testimony, speeches, interviews]
- "[Quote]" — [Name, Title, Source, Date]
- "[Quote]" — [Name, Title, Source, Date]

### What AI Can't Know — Your Relationship Intel
**This section must be filled in by you. No AI can find this.**

- What has the customer told you directly about their priorities?
- What concerns have they raised about current solutions or vendors?
- What did they say at the last meeting / briefing / demo?
- What do they think of your company specifically?
- What objections have you heard from them?
- Who in the organization is a champion for this approach? Who is skeptical?

[YOU KNOW THIS — PLEASE FILL IN]

---

## 3. Buying History and Preferences

### Prior Awards in This Capability Area
[From USASpending / SAM.gov / FPDS research]

| Vendor | Program | Value | Year | Vehicle | Notes |
|--------|---------|-------|------|---------|-------|
| [vendor] | | | | FFP / OTA / etc. | Incumbent? |

### Acquisition Preferences
- Preferred vehicles: [OTA / FAR / SBIR / CSO — from award history]
- LPTA vs. best value tendency: [inferred from prior solicitations]
- Small business utilization: [% and set-aside history]
- Typical evaluation factors: [from prior solicitations for similar scope]
- Typical timelines: [draft to award, average from prior procurements]

### Incumbent Relationships
[Who is currently working for them? How entrenched? How long?]

---

## 4. Budget and Funding

### Known Budget Profile
- Annual budget for this program/office: [from budget justification books]
- Funding source: [RDT&E / O&M / Procurement / SBIR — matters for our pitch]
- Recent budget trends: [increasing / decreasing / new program]
- Congressional adds or cuts: [from markup documents]
- Estimated budget for this requirement: [from SAM, prior awards, or YOU KNOW THIS]

---

## 5. Buying Cycle Position
Where is this customer in their acquisition cycle right now?

- [ ] Recognition of Need — aware of the problem, no acquisition action yet
- [ ] Evaluation of Options — market research, RFIs, industry days
- [ ] Resolution of Concerns — draft solicitation, final requirements development
- [ ] Implementation — solicitation released, evaluating proposals

**Current position:** [AI assessment based on SAM.gov activity + YOU KNOW THIS]

**Upcoming events to watch:**
- [Industry day / bidders conference — date if known]
- [Draft solicitation expected — date if known]
- [Final solicitation expected — date if known]

---

## 6. Company Relationship Status

### Our Current Standing With This Customer
- Prior interactions: [from inputs/06_notes/ and your knowledge]
- Demonstrations or briefings given: [YOU KNOW THIS]
- Their perception of our company: [YOU KNOW THIS]
- Open questions or concerns from the customer: [YOU KNOW THIS]
- Our champion in the organization: [YOU KNOW THIS]

### What We Need to Do Before Proposal Submission
[Based on what AI found and relationship gaps — what customer contact should happen before we submit?]
- [Action 1: e.g., "Schedule technical demo with PM before solicitation drops"]
- [Action 2: e.g., "Clarify whether DDIL requirement is hard or soft in pre-submission Q&A"]

---

## 7. Hot Button Priority Ranking
After completing above sections, rank the top 5 hot buttons in order of importance to the customer:

1. [Hot button] — [why this ranks #1]
2.
3.
4.
5.

**This ranking feeds directly into `/proposal-manager` win themes and the Bidder Comparison Chart in `/competitor-assessment`.**

---

## Intelligence Gaps
[What we couldn't find and still need to resolve:]
- [ ] [Gap 1]
- [ ] [Gap 2]
```

---

### Step 3: Summarize Findings for the User
After writing the file, present:
1. Top 3 hot buttons found in open source — ranked by inferred importance
2. Key personnel identified
3. Most relevant prior awards / incumbent relationships to be aware of
4. What fields are blank and need the user's relationship knowledge
5. Suggested customer contact actions before proposal submission

---

## Output Files
**Always write to disk — do not just display in chat.**

- `working/customer-profile.md` — the complete profile (AI-found + user placeholders)
- `inputs/01_customer/` — if the user drops in additional materials (briefing decks, meeting notes), reference them but do not duplicate

---

## Rules
- Label every AI-sourced fact with its source
- Never fabricate quotes, budget figures, or personnel information
- Clearly mark every field that requires the user's relationship knowledge
- Budget figures from unofficial sources must be flagged as estimates
- Personnel in sensitive roles (source selection) — note that direct contact rules apply (route through CO)

---

## Defense Customer Quick Reference

### Key Budget Document Sources
- **comptroller.defense.gov** — all DoD budget justification books by year and service
- **R-2 sheets** — line-item RDT&E (research) funding; search by program name or PE number
- **Congressional Budget Justification** — direct from agency websites
- **govinfo.gov** — archived Congressional testimony and appropriations markup

### Key Acquisition Activity Sources
- **sam.gov/opp** — solicitations, sources sought, contract awards
- **usaspending.gov** — all federal awards; filter by agency + NAICS + date
- **sbir.gov** — SBIR/STTR awards by agency and topic

### SOF / SOCOM-Specific
- **socom.mil/procurement** — SOCOM acquisition office
- **sofwerx.org** — SOFWERX events and tech engagement opportunities
- **[Customer A]**: budgets under Army RDTE; search "[Customer A]" or "ARSOF" in budget exhibits
- **TSOC budget lines**: typically under respective geographic combatant command

### CDAO / DIU / AFWERX / Navy / Army
- **cdao.mil** — CDAO programs and initiatives; AI strategy documents
- **diu.mil** — DIU project pages and commercial solution openings
- **afwerx.af.mil** — AFWERX challenges and SBIR opportunities
- **devcom.army.mil** — Army research lab and DEVCOM programs

---

## Lessons Learned

### On SOF Customers
- SOCOM and subordinate commands rarely post detailed requirements publicly — relationship intel is essential. What they publish is sanitized.
- [Customer A] budget lines are buried in Army RDT&E exhibits — search for "ARSOF" or "SOF AI" in the Army budget justification books.
- SOF evaluators care about operator adoption above all else. Published requirement compliance is secondary. Frame deployments around operator behavior change, not feature lists.

### On CDAO / DIU
- CDAO's [Procurement Vehicle] is iterative — new topics drop regularly. Monitor cdao.mil and tradewindssolutions.com for upcoming topics.
- DIU evaluators are former industry; they evaluate like investors, not acquisition officials. Hot buttons: commercial viability, speed to fielding, team credibility.
- The DIU relationship is different from the contracting relationship — engage DIU program leads directly and early; they shape requirements before solicitations drop.

### On What AI Can and Cannot Find
- AI can find: budget numbers, program names, prior awards, published statements, org charts, acquisition history
- AI cannot find: what the PM said in a closed industry day, relationship dynamics, informal customer feedback, unwritten evaluation biases, internal budget battles
- The fields marked [YOU KNOW THIS] are often more valuable than everything AI finds. Fill them in.
