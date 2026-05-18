# Team Review Rubric

**For:** Internal reviewers (research engineers, BD owners, technical leads) reading a federal proposal draft before submission.
**Owner:** [Proposal POC] — sole experienced federal proposal POC at the company.
**Purpose:** Channel your expertise into the lanes that strengthen the proposal. Block edits that — though well-intentioned — make us *less likely* to win.

---

## Read this first (90 seconds)

A federal proposal is **not** a technical paper, sales deck, or product doc. It is **a document scored against a rubric by an evaluator who has 15 minutes per section, a red pen, and is looking for reasons to deduct points**. The voice, structure, and specifics all do work toward that scoring.

Federal evaluators reward:
- **Specific numbers** (95% statistical significance, 98.2% refusal-elimination, IL-6 ATO, $17.5M raised, 1st/7th/10th SFG)
- **Named programs and customers** (USSOCOM SOF AI Pilot, Navy ICOP/NIWC Atlantic, USSF TradeWinds CSO)
- **Doctrine and standards references** (AJP-01, FM 3-01, JP 3-13.1, MIL-STD-XXX, JDL framework)
- **Cited evidence** (peer-reviewed benchmarks, named deployments, contract IDs)
- **Scope discipline** (clearly stated boundaries — "we do X, not Y")

Federal evaluators *deduct points* for:
- Vague capability claims ("AI-enabled decision advantage," "robust solution")
- Unsupported superlatives ("industry-leading," "best-in-class")
- Marketing voice ("leverage," "synergy," "cutting-edge")
- Tone that *sounds polished* but says nothing scoreable
- Hedging that telegraphs lack of conviction ("approximately," "may include," "potentially")

**The single most common way internal reviewers hurt federal proposals: softening specific claims to "sound more professional." A specific claim is evidence; the smoothed version is marketing.**

---

## Your reviewer role

Pick **one**:

| Role | Your lane | Stay out of |
|---|---|---|
| **Research engineer / technical SME** | Verify technical claims, catch hallucinations, flag overstatement of capabilities you'd have to deliver | Tone, prose style, section structure, evaluator-facing strategic framing |
| **BD owner / customer lead** | Verify customer names, contract types, partnership characterizations, procurement vehicles | Technical claim assessment, tone, structure |
| **Reviewer with subject-matter context (e.g., military background)** | Validate doctrinal references, operator-role specificity, mission-thread realism | Tone, structure |
| **General reviewer** | Skip to "Things ANY reviewer can usefully do" at the bottom | Everything else — let role-specific reviewers handle their lanes |

---

## What each role should DO

### Research engineer / technical SME

**Score each technical claim** (rate each one yes / no / can't tell):

- [ ] **Factually accurate** — does this match what we actually do, or is it overstated?
- [ ] **Deliverable** — if we're awarded and someone asks us to demonstrate this, can we?
- [ ] **Methodology specified** — for benchmark claims, is the eval set / methodology / comparison model named? (If not, flag — but don't soften the claim; the fix is to *add* methodology, not remove the claim.)
- [ ] **Compatible with adjacent claims** — does claim X in §3 contradict claim Y in §6?
- [ ] **Honest about what's roadmap vs. fielded** — are "live today" and "planned" distinguished?

**Useful technical feedback looks like:**

> ✅ "§3 says 'matches GPT-5 on military tasks at 95% statistical significance' — I confirm this is from the company-model paper; the test set was mil-bench-5k + 3 others. Suggest adding 'on the mil-bench-5k benchmark suite' to make the methodology explicit."

> ✅ "§6 second bullet says we 'achieved IL-6 ATO via Navy ICOP' — confirm yes, granted [date]. Could add the date for evaluator-checkable specificity."

> ✅ "§5 claim 'continues full inference under GPS denial' is accurate today, but our SATCOM-loss test is from a controlled environment. If asked, we can defend the architectural claim but not a full DDIL field test. Flag."

> ❌ NOT: "§3 'matches GPT-5 at 95%' is too aggressive — recommend rephrasing to 'demonstrates strong performance on military tasks'" — this strips the specific number that's the entire reason the claim is scoreable. *If the number is defensible, keep it; if it isn't, fix the data, not the prose.*

### BD owner / customer lead

**Score each customer / partnership / procurement claim**:

- [ ] **Customer name correct** — exact program office, command, and unit numbers as we'd cite them in a sources-sought response
- [ ] **Cleared for public/CUI citation** — has the customer cleared us to name them in unclassified proposals?
- [ ] **Contract type accurate** — CSO Direct Award vs. OTA prototype vs. SBIR Phase II vs. CRADA — pick the right one
- [ ] **Procurement vehicle name precise** — "CDAO Tradewinds Marketplace Awardable status" and "TradeWinds CSO Direct Award" are different things; don't merge them
- [ ] **Partnership characterization honest** — formal teaming agreement signed? LOI? OEM partnership? Handshake from a conference? These rate differently

**Useful BD feedback looks like:**

> ✅ "§6 bullet says 'U.S. Space Force production contract via TradeWinds CSO Direct Award' — confirm. Note the draft also mentions 'concurrent Tradewinds Marketplace Awardable status' — these are two different credentials and the evaluator may want both called out distinctly."

> ✅ "Partnership list includes General Radar — confirm this is a defense integrator partnership with active engagement, not a one-time intro call. If the latter, recommend dropping or qualifying."

> ❌ NOT: "The customer list is too detailed — recommend consolidating into a 'multiple DoD programs' summary." — Specific customer names ARE the credibility. Generic summaries read as inability to name customers.

### Reviewer with subject-matter context

**Score each operator-role / doctrine / mission-thread claim**:

- [ ] **MOS / AFSC / rate codes correct** — FA14 = ADA officer, 14E = Patriot Fire Control, etc. — verify the codes match the role described
- [ ] **Schoolhouse / center of excellence names correct** — Fort Sill (Fires CoE), Fort Eisenhower (Cyber CoE)
- [ ] **Doctrine document references real and current** — FM 3-01 family, ATP 3-01.7, JP 3-13.1 — verify these are current pubs
- [ ] **Mission thread realistic** — does the operator workflow described match how operators actually work?
- [ ] **TTPs cited correctly** — Iranian proxy TTPs, sUAS profiles, etc. — match current threat picture?

**This kind of reviewer is rare and high-leverage.** When you have one, their specific knowledge is the strongest signal in the review.

### Things ANY reviewer can usefully do

- [ ] **Spelling, grammar, typos** — fix directly
- [ ] **Internal consistency** — does the abstract say one thing and §6 say a different version? Does the whitepaper say UNCLASSIFIED // CUI and the quad chart say UNCLASSIFIED only? Flag.
- [ ] **Missing acronym definitions on first use** — CENTCOM, DIANA, DDIL, COA, MOS, AJP, etc.
- [ ] **Broken cross-references** — "See Figure 1" but no Figure 1 exists; "(§4)" but no §4 — flag.
- [ ] **Numbered list integrity** — duplicate numbers, skipped numbers, mismatched figure counts
- [ ] **Things you don't recognize** — if a customer name, program name, partnership, certification, or benchmark sounds unfamiliar to you, flag it. Don't assume; ask.

---

## What NOT to do (and why)

These are real edit patterns that have hurt past proposals. **If you find yourself reaching for one of these, stop.**

### ❌ DON'T soften specific claims to "sound more professional"

| Specific claim (evaluator gold) | Softened version (evaluator discount) |
|---|---|
| "matches GPT-5 at 95% statistical significance on military tasks" | "demonstrates strong performance on military-domain evaluation sets" |
| "eliminates 98.2% of unjustified refusals" | "addresses common refusal limitations of commercial models" |
| "deployed with 1st, 7th, and 10th Special Forces Groups" | "deployed across multiple SOF units" |
| "FA14 anchor at D+30; 14E/14G/14H/14P + 17E at D+60/D+90/D+120" | "phased delivery of role-specific adapters" |

**The softened versions are *what we said internally before we had the evidence*. The specific versions are *what we say externally because we have the evidence*. Reverting to the internal voice strips our advantage.**

### ❌ DON'T strip named partners / customers / programs

If a section names HP, Panasonic, AMD, Intel, Akamai, Lockheed Martin, BigBear.ai — those names are doing work. They demonstrate hardware-ecosystem reach. Collapsing them to "multiple OEM partners" is a 50% credibility cut.

If a section names USSOCOM 1st/7th/10th SFGs — those unit numbers prove operational fielding. "U.S. Special Operations Forces" is a generic wave-of-the-hand.

### ❌ DON'T restructure the document

Section structure was chosen against the evaluation criteria (each section maps to a scored factor). Inserting a new section, renaming a section, or merging sections changes how the evaluator's scoring rubric maps to the document. **If a section feels redundant, that's likely intentional reinforcement of a win theme. Flag the duplication for the [Proposal POC] to assess; don't restructure.**

### ❌ DON'T add internal-audience clarity

A federal evaluator is not your colleague. They have a rubric and 15 minutes. Adding sentences like "To clarify, this means…" or "In other words…" doesn't help them — it adds words they have to skim. **The proposal should read dense; that's evidence of substance.** Density is good; vagueness is bad.

### ❌ DON'T add hedging language to make claims "safer"

"Approximately," "may include," "potentially," "could be configured to" — every hedge subtracts from the claim's scoring weight. If a claim is not defensible, **fix the data; don't hedge the prose**. If a claim *is* defensible, leave it confident.

### ❌ DON'T cut quantified claims because "we can't prove the exact number"

If we have a peer-reviewed number, cite it. If we have an internal-benchmark number, cite it with methodology. **The wrong fix is to remove the number; the right fix is to add the methodology that makes it defensible.** A specific number with methodology beats a vague claim every time.

---

## How to flag instead of edit

When you're uncertain about a claim, use this structure in your comment (or in a separate doc):

```
SECTION: §X.Y
CONCERN TYPE: [factual / consistency / defensibility / unfamiliar]
CLAIM: "[exact text of concern]"
WHAT I KNOW: "[what you can verify or know to be true]"
WHAT I DON'T KNOW: "[what's outside your context]"
RECOMMEND: [keep as-is | verify with [Proposal POC / SME] | revise to specifics if available | discuss]
```

**Examples:**

> SECTION: §6 paragraph 2
> CONCERN TYPE: defensibility
> CLAIM: "Acme Defense 20B matches GPT-5 on military tasks at 95%+ statistical significance"
> WHAT I KNOW: We have the mil-bench-5k results showing parity at 95% CI.
> WHAT I DON'T KNOW: Whether "95%+ statistical significance" is the right framing vs. "95% confidence interval" — these mean different things statistically.
> RECOMMEND: Verify language with [Research Engineer]; if 95% CI is what we mean, change "statistical significance" to "confidence interval."

> SECTION: §1 third bullet
> CONCERN TYPE: factual
> CLAIM: "Five production MOS adapters shipped (Logistics, Combat Medic, Combat Arms, Acquisitions, Cyber)"
> WHAT I KNOW: We have Logistics, Combat Arms, Cyber.
> WHAT I DON'T KNOW: Whether Combat Medic and Acquisitions adapters are shipped or in flight.
> RECOMMEND: Verify with the [Proposal POC] before submission.

This format gives the [Proposal POC] a triage queue. They can resolve, defer, or push back — but they can see exactly what you're flagging and why, without having to reverse-engineer your edits.

---

## Scoring summary (use this as your reviewer output)

Fill this in once for the whole proposal (or per section if scope is large):

| Item | Score | Notes |
|---|---|---|
| Number of factual errors found | | |
| Number of unfamiliar claims flagged for verification | | |
| Number of internal-consistency issues | | |
| Number of broken cross-references / numbering issues | | |
| Number of acronyms undefined on first use | | |
| Spelling/grammar fixes (made directly) | | |
| Concerns I'm flagging but not editing | | (use the structure above) |

**Reviewer time budget:** 30–60 min for first read; another 30 min to write up the findings table. Don't spend more time than this on stylistic concerns — that's actively counterproductive.

---

## Why this rubric works this way (for the curious)

If you want to understand the reasoning beyond "the POC said so":

1. **Federal evaluators are scoring, not reading.** A typical Section M evaluation has 4–8 factors, each with rubric language like "Significantly increases the Government's confidence…" Evaluators map proposal text to rubric language. Specifics map; vagueness doesn't.

2. **The evaluator's incentive is to deduct.** Federal evaluators write source-selection decision documents that justify their ratings. A finding of "applicant claims X but did not substantiate" is the language they're trained to write. Every vague claim is an invitation to write that finding.

3. **Marketing voice gets discounted; technical voice gets scored.** A research paper voice ("we demonstrated X with Y methodology yielding Z result") scores higher than a product-marketing voice ("our cutting-edge solution leverages…"). Your research-engineer instincts are actually *closer* to federal proposal voice than your BD instincts.

4. **Specificity is risk transfer.** When we name a customer, a number, a partner, a date — we're transferring verification risk from the evaluator to ourselves. Evaluators reward this because it makes their job easier. Vagueness keeps the verification burden on the evaluator, who responds by deducting points.

5. **The proposal is a contract, not a brochure.** Specific commitments ("FA14 anchor at D+30") become commitments we have to deliver. Vague aspirations ("phased adapter delivery") don't. Reviewers' instinct to soften claims often comes from a sensible desire not to over-commit — but the right fix is to ensure we *can* deliver, not to hedge the commitment.

---

## What to do with this rubric

1. **First time:** read it before reading the proposal. ~10 min.
2. **Each proposal:** the [Proposal POC] provides a 1-page proposal-specific briefing (the per-proposal companion to this rubric) naming the specific discriminators, named Significant Strengths from Gold Team review, and quantified claims that ARE evidenced. **Treat that briefing as the answer key for what NOT to soften.**
3. **As you read:** use the role-specific checklist for your lane. Skip lanes outside your expertise.
4. **When done:** submit the scoring summary table + flagged concerns using the structure above. Don't submit a tracked-changes document with stylistic edits.
5. **If you disagree with this rubric:** that's a conversation for the [Proposal POC], not a reason to override it in your review. Federal proposal conventions aren't a matter of taste — they're a scoring system we don't control.

---

## Glossary (one-line each, for non-federal-proposal context)

- **Section M** — the part of a federal solicitation that lists the evaluation factors and how they'll be scored.
- **Gold Team review** — internal mock evaluation against the rubric. Names the proposal's **Significant Strengths** — these are the load-bearing claims you should not soften.
- **Red Team review** — internal narrative-quality review. Names risks an evaluator might use to deduct points.
- **White Glove review** — final editorial pass before submission.
- **Discriminator** — a specific capability/credential a competitor cannot match. Discriminators are *what win proposals*; they should NOT be smoothed away.
- **CDR/PDR/CDR voice** — formal technical-document voice with quantified claims, named tests, defensible methodology. *This is the voice federal proposals use.* (You probably already write this way in your domain.)
