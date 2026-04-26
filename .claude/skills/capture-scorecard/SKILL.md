---
name: capture-scorecard
description: Use this skill to assess capture readiness across 9 dimensions before committing proposal resources. Produces a stoplight scorecard (Red/Yellow/Green), identifies the top risks, and gives a go/no-go recommendation. Reads from working/ files and writes to working/capture-scorecard.md.
---

# Capture Scorecard Skill

## Purpose
A fast, honest self-assessment of where you stand on a pursuit before committing B&P dollars to full proposal development. The scorecard takes 10–15 minutes, surfaces hidden risks, and either validates the go decision or forces a conversation about gaps that need fixing first.

A proposal written from a weak capture position loses. This skill tells you whether you're ready to write.

## When to Use
- After `/proposal-manager` completes (proposal plan exists)
- After `/competitor-assessment` completes (competitive picture exists)
- Before committing to full proposal effort (before `/proposal-writer` begins)
- On recompetes: run at 12+ months before recompete due date
- Any time capture leadership wants a status snapshot

## Inputs
Read before scoring:
1. `working/proposal-plan.md` — opportunity classification, prime/sub decision, evaluation criteria, win themes, bid/no-bid assessment
2. `working/competitor-assessment.md` — competitive landscape, teaming gaps
3. `working/customer-profile.md` — customer relationship status, hot buttons
4. `inputs/02_yourCompany/` — your company's capabilities and past performance
5. `inputs/06_notes/` — any meeting notes or relationship intel

For each dimension where information is missing, ask the user to fill it in before scoring. Do not score blindly — a missing answer is itself a yellow or red flag.

---

## The 9 Dimensions

### 1. Management (MGMT)
Is the capture organized and led?

| Score | Criteria |
|-------|---------|
| 🟢 Green | Capture manager assigned; capture plan documented; team roles defined; regular reviews scheduled |
| 🟡 Yellow | Capture manager assigned but plan incomplete or team not fully assembled |
| 🔴 Red | No capture manager; no plan; no organized team |

**Ask:** Who is leading this capture? Is a capture plan in place? Is the team assembled?

---

### 2. Shaping
Have we influenced the requirements before the solicitation drops?

| Score | Criteria |
|-------|---------|
| 🟢 Green | We have had substantive conversations with the customer about requirements; our solution approach is reflected in the draft/final solicitation; we have a champion inside the program |
| 🟡 Yellow | Some customer access; limited shaping; RFP language somewhat favorable |
| 🔴 Red | No customer access; requirements were written without our input; we are seeing this cold |

**Ask:** Have we briefed our solution to the customer? Have we seen draft requirements? Do we have a champion?

---

### 3. Technical / Solution
Do we have a credible, differentiated technical solution?

| Score | Criteria |
|-------|---------|
| 🟢 Green | Solution design is mature; capability matrix complete with no mandatory gaps; discriminators identified; solution aligns to evaluation criteria |
| 🟡 Yellow | Solution approach defined but gaps exist; some requirements not fully addressed; discriminators weak |
| 🔴 Red | No solution design; major capability gaps; cannot address key requirements without significant gaps or unproven assumptions |

**Ask:** Is the capability matrix complete? Are there mandatory requirements we cannot address? What are our discriminators?

---

### 4. Teaming
Is the team assembled to fill all capability gaps?

| Score | Criteria |
|-------|---------|
| 🟢 Green | All mandatory capability gaps filled by identified partners; teaming agreements in progress or signed; work share defined; no OCI risks |
| 🟡 Yellow | Key partners identified but not locked; teaming agreements not started; some gaps remain |
| 🔴 Red | Mandatory gaps with no partner identified; teaming strategy undefined; OCI risk unresolved |

**Ask:** What capability gaps exist? Have partners been identified and approached? Are teaming agreements in progress?

---

### 5. Competition
Do we understand the competitive landscape and have a strategy to win?

| Score | Criteria |
|-------|---------|
| 🟢 Green | Top competitors identified with profiles; Bidder Comparison Chart or competitive landscape complete; strategy statements developed; incumbent assessed |
| 🟡 Yellow | Key competitors known but limited intelligence; no formal competitive strategy |
| 🔴 Red | Competition unknown; incumbent not assessed; no competitive strategy |

**Ask:** Who are the top 2-3 competitors? Is there an incumbent? Do we have a competitive strategy?

---

### 6. Finance / Pricing
Do we have a pricing strategy and know the competitive price range?

| Score | Criteria |
|-------|---------|
| 🟢 Green | PTW estimate complete; customer budget known or estimated; pricing strategy defined (LPTA vs. best value); fee and margin approach set |
| 🟡 Yellow | ROM pricing only; customer budget unknown; limited PTW intelligence |
| 🔴 Red | No pricing strategy; no estimate; budget unknown; not prepared to price competitively |

**Ask:** Do we know the customer's budget? Do we have a PTW estimate? What is our pricing strategy?

---

### 7. Marketing / Positioning
Does the customer know who we are and associate us with this capability?

| Score | Criteria |
|-------|---------|
| 🟢 Green | We have previously briefed or demonstrated our solution to this customer; they associate [Your Company] with this capability area; our brand is established with this program office |
| 🟡 Yellow | Some customer awareness; one prior engagement; limited prior demonstrations |
| 🔴 Red | Customer does not know [Your Company]; no prior demonstrations or briefings; starting from zero |

**Ask:** Have we ever briefed this customer on our capabilities? Do they know our name?

---

### 8. Customer Engagement
What is the quality of our relationship with the decision-making chain?

| Score | Criteria |
|-------|---------|
| 🟢 Green | Regular access to the program manager, technical lead, or end users; champion identified inside the program; customer issues and hot buttons well understood from direct conversations |
| 🟡 Yellow | Occasional access; relationship is transactional; limited insight into internal priorities |
| 🔴 Red | No access to key decision makers; customer engagement not established; issues inferred, not validated |

**Ask:** Who do we know in the program office? When did we last engage? Do we have a champion?

---

### 9. Resources
Do we have the people and budget to write a competitive proposal?

| Score | Criteria |
|-------|---------|
| 🟢 Green | Proposal team identified and available during the proposal period; B&P budget allocated; subject matter experts committed; no competing proposal conflicts |
| 🟡 Yellow | Key personnel identified but availability uncertain; B&P budget not formally allocated; some schedule conflict risks |
| 🔴 Red | No proposal team; no B&P budget; key personnel unavailable; competing proposal conflicts |

**Ask:** Who will write this proposal? Are they available? Is B&P budget approved?

---

## Scoring and Recommendation

After assessing all 9 dimensions, produce the scorecard:

```markdown
# Capture Scorecard — [Proposal Name]
**Date:** [today]
**Capture Mode:** [Full Capture / Responsive]
**Prime vs. Sub:** [PRIME / SUB / CO-PRIME]

| # | Dimension | Status | Key Issue | Recommended Action |
|---|-----------|--------|-----------|-------------------|
| 1 | Management | 🟢/🟡/🔴 | | |
| 2 | Shaping | 🟢/🟡/🔴 | | |
| 3 | Technical / Solution | 🟢/🟡/🔴 | | |
| 4 | Teaming | 🟢/🟡/🔴 | | |
| 5 | Competition | 🟢/🟡/🔴 | | |
| 6 | Finance / Pricing | 🟢/🟡/🔴 | | |
| 7 | Marketing / Positioning | 🟢/🟡/🔴 | | |
| 8 | Customer Engagement | 🟢/🟡/🔴 | | |
| 9 | Resources | 🟢/🟡/🔴 | | |

**Score:** X Green / X Yellow / X Red

## Overall Readiness Assessment
[One paragraph: what's strong, what's at risk, what must be resolved before proposal kickoff]

## Go / No-Go Recommendation
**[GO / NO-GO / GO WITH CONDITIONS]**

[Rationale — 2-3 sentences]

## Conditions (if conditional go)
1. [Condition that must be resolved before proposal kickoff]
2.
3.

## Top 3 Actions Before Proposal Kickoff
1. [Most urgent — owner and deadline]
2.
3.
```

**Threshold guidance:**
- 7–9 Green → GO
- 5–6 Green, remainder Yellow → GO WITH CONDITIONS (state them)
- Any Red in dimensions 3, 4, or 9 (Technical, Teaming, Resources) → NO-GO until resolved — these are execution risks, not just competitive risks
- Any Red in dimensions 2 or 8 (Shaping, Customer Engagement) on a competitive RFP → serious concern; flag prominently

---

## Output File
**Always write to `working/capture-scorecard.md` — do not just display in chat.**

---

## After Running This Skill
Tell the user:
1. Overall score (X Green / X Yellow / X Red)
2. Go / No-Go recommendation with one-sentence rationale
3. Top 3 actions to take before proposal kickoff
4. Any dimension scored Red that represents a bid-blocking risk

---

## Rules
- Score based on what is known, not what is planned — a plan to do something is not the same as having done it
- If the user cannot answer a question, that dimension defaults to Yellow (unknown = risk)
- Do not let an overall strong capture position mask a single Red in a blocking dimension
- Re-run this scorecard after major capture events (customer meeting, solicitation release, teaming agreement signed) to update the picture

---

## Lessons Learned

### On Shaping
The biggest recurring gap for small companies is Shaping. Most bids are reactive — solicitation drops, we respond. Proactive shaping (briefing before the RFP, influencing requirements language) dramatically increases win probability. Even a single pre-solicitation meeting that results in favorable language is worth more than weeks of proposal writing. Target Shaping as a consistent Yellow-to-Green improvement area.

### On Customer Engagement
For SOCOM and SOF-adjacent customers, end-user operator relationships are more valuable than program office relationships. An operator who has used your solution and will say so to the PM is a stronger signal than a formal meeting with the contracting officer. Track operator relationships as part of Customer Engagement.

### On Resources for Responsive Bids
For SBIR/CSO/OTA, the "Resources" bar is lower — a 1-2 person writing effort for a 10-page white paper is sufficient. Don't penalize a responsive bid for lacking a full proposal team. Scale the resource standard to the proposal complexity.
