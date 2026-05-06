# Proposal Writing Patterns

Four patterns that separate winning federal prose from marketing filler: **theme statements**, **discriminator proof points**, **action captions**, and **ghosting**. Every section that the Gold Team rubric will score should apply these by default — not as embellishment, but as structure.

This reference is read by `proposal-writer` (enforced in output) and by `red-team-review` Gold Team (checked as findings). If the writer produces these patterns from the start, Gold Team finds them present and scores higher.

---

## Applicability by Proposal Type

Not every type uses every pattern. The writer dispatches on `working/proposal-type.md`:

| Type | Theme Statements | Discriminator Proofs | Action Captions | Ghosting |
|---|---|---|---|---|
| `far-rfp` | Required | Required | Required | Required |
| `idiq-to` | Required | Required | Required | Optional |
| `cso-brief` | Required | Required | Required | Optional |
| `cso-full` | Required | Required | Required | Required |
| `baa` | Required | Required | Required | Optional (merit-based) |
| `ota-white-paper` | Required | Required | Required | Optional |
| `ota-proposal` | Required | Required | Required | Optional |
| `sbir-phase1` | Recommended | Required (via commercialization) | Required | Not applicable |
| `sbir-phase2` | Required | Required | Required | Optional |
| `white-paper` | Recommended | Required | Required | Not applicable |
| `rfi` | Not applicable | Not applicable | Not applicable | Not applicable |
| `sources-sought` | Not applicable | Not applicable | Not applicable | Not applicable |
| `rom` | Not applicable | Not applicable | Optional | Not applicable |

"Required" means the writer MUST apply it. "Recommended" means apply if the section length supports it. "Not applicable" means the type's reader framing makes the pattern inappropriate (RFI is market research — no competition to ghost; ROM is a range, no themes).

---

## Pattern 1 — Theme Statements

A **theme statement** is the first sentence of a major section. It states, in plain terms, the *single most important point* the evaluator should take from that section.

### Why
Federal evaluators often have 10-15 minutes per section on a skim pass. They read the first sentence, the first sentence of each subsection, and the first sentence under each graphic. If those sentences don't make the case, the rest doesn't get read.

A theme statement also *forces* the writer to commit to one point. Sections without theme statements tend to be lists of facts; sections with them tend to be arguments.

### Structure

A theme statement has three elements:

1. **What** — the specific capability, approach, or feature
2. **Why it matters** — the benefit to the Government (tied to the evaluation criteria when possible)
3. **Proof hook** — a concrete artifact, reference, or metric the section will substantiate

### Templates

**Generic:**
> [What we're offering] [delivers/reduces/enables] [Government benefit], demonstrated by [proof artifact introduced in this section].

**Risk-reduction framing:**
> [Capability] directly reduces [specific risk the customer articulated], as shown in [graphic / past performance / technical metric].

**Outcome framing:**
> Offeror's [approach] achieves [quantified outcome], proven in [prior deployment / benchmark].

### Examples

**Weak (no theme statement):**
> Our technical approach leverages modern AI architectures to deliver mission-critical capabilities across the enterprise.

**Strong (theme statement):**
> On-device inference eliminates the cloud-dependency risk that the Section C problem statement identifies as mission-limiting, demonstrated by our [deployed customer] installation operating in DDIL environments for 14 months without connectivity.

**Weak:**
> This section describes our past performance.

**Strong:**
> Three cited contracts — two DoD, one IC — show direct precedent for the scope and complexity of this effort, with CPARS ratings of Satisfactory or higher across all three.

### When a theme statement is wrong

- If the section is a **list** (tables, staffing rosters, CDRL lists), a theme statement above the list is fine but optional.
- If the section is **boilerplate** (reps and certs, FAR clauses), skip it.
- If the "theme" is a **claim without evidence** ("We are the best at this"), it's not a theme statement — it's marketing. Rewrite to include a proof hook.

---

### Theme Litmus Test (Shipley-aligned, added 2026-04-25)

A theme statement passes the litmus test only if it satisfies **all** of:

1. **Single sentence** — if it requires two sentences, it isn't a theme; it's a paragraph
2. **Specific** — names a particular capability, benefit, or proof point
3. **Quantified** — includes a number, scale, or measurable outcome where possible
4. **Tied to a customer issue** — addresses something the customer cares about, not something we want to talk about
5. **Discriminator-bearing** — implies (or states) something only we offer, not a generic strength
6. **Evaluator-actionable** — gives the evaluator a reason to score the section higher

Theme statements that fail any of these are weak. Strengthen or replace before the section ships to compliance-check.

### Section theme statement vs. section summary

Two different artifacts that are sometimes conflated:

- **Section theme statement** (opening, 1 sentence): asserts the single most important point the evaluator should take from this section. Passes the litmus test above.
- **Section summary** (closing, 1-3 sentences, optional): recapitulates the section's key takeaways for an evaluator who might skim back. Typically used for sections >2 pages.

A short section needs only the theme statement. A longer section may use both. **Don't open with a summary** — the theme statement does the opening work; the summary closes.

---

## Pattern 2 — Discriminator Proof Points

A **discriminator** is something you offer that competitors don't — or can't credibly offer. A **proof point** is the evidence that you actually have it.

### Phase C — Evidence-grounded citation (v1.5)

When `my-company/evidence-ledger.json` exists, every proof point **must** carry a machine-readable citation to a ledger item via an HTML comment marker. Format:

```markdown
[Prose claim with proof point]. <!-- evidence: EV-### -->
```

The HTML comment is invisible in markdown render AND in docx export (preserved as a comment, not rendered by Word or pandoc), so evaluators see clean prose. Machine tooling (`/evidence-check`, Gold Team) greps for the marker to verify every claim has backing evidence.

Multiple IDs for one claim:
```markdown
On-device inference <!-- evidence: EV-001 --> has been validated at operational scale <!-- evidence: EV-022, EV-055 -->.
```

If you make a claim but cannot find a ledger item to back it, mark it explicitly:
```markdown
Our on-device inference is the fastest in the industry. <!-- evidence: CLAIM-UNSUPPORTED -->
```

Gold Team automatically scores `CLAIM-UNSUPPORTED` as Weakness findings; the writer's job is either to find matching evidence, soften the claim, or remove it.

See `.claude/skills/evidence-check/SKILL.md` for the full audit workflow and `reference/schemas/evidence-ledger.schema.json` for the ledger format.

Discriminators without proof are claims. Claims don't win federal work.

### Why
Section M scoring rewards Strengths and Significant Strengths (see `evaluator-rubrics/strengths-weaknesses-deficiencies.md`). Both require:
- A specific capability, and
- A benefit to the Government, and
- A basis (proof) cited in the proposal.

Discriminators stated without proof points are Weaknesses by default (unsupported claims). Proof points *make* them Significant Strengths.

### Features-Advantages-Benefits (FAB) hierarchy (Shipley-aligned, added 2026-04-25)

A discriminator's proof point should escalate through three levels of customer relevance, not stop at "we have feature X":

| Level | Question answered | Example |
|---|---|---|
| **Feature** | What is it? | "Our platform performs all inference on-device." |
| **Advantage** | How does it help? | "On-device inference eliminates the cloud round-trip latency that affects responsive operator workflows." |
| **Benefit** | How does it solve a problem the customer has acknowledged? | "On-device inference enables analyst workflows in DDIL operational tempos that have caused mission-effectiveness degradation in cloud-dependent solutions, addressing the operational pain the customer documented in [reference to their stated problem]." |

**Rule:** weak discriminators stop at Feature ("we have X"). Mediocre discriminators reach Advantage ("X helps you"). Strong discriminators reach Benefit ("X solves a problem you've stated"). Aim for Benefit-level discriminator statements.

**Pattern:** `[Feature claim with evidence_ref] enables [Advantage] which directly addresses [Customer-stated issue / Problem in solicitation language].`

### Required elements (every discriminator needs all four)

1. **Claim** — what we do / have that competitors don't
2. **Evidence** — a concrete, verifiable artifact
3. **Relevance** — tie to a specific evaluation criterion or Government need
4. **Scope** — where in the proposal the proof is expanded (graphic, past performance section, attachment)

### Evidence Types (ranked by credibility)

| Type | Strength |
|---|---|
| Deployed customer reference (with $, duration, outcome) | Highest |
| Independent benchmark or third-party validation | High |
| Government CPARS or PPQ score on similar work | High |
| Published research or patent | High |
| Internal technical benchmark (with methodology) | Medium |
| Named key personnel with specific credentials | Medium |
| Partnership / certification with authoritative body | Medium |
| Internal product demo (without external validation) | Low |
| Industry analyst mention | Low |
| "We have extensive experience" | None (no proof) |

### Templates

**Claim + evidence + relevance + scope:**
> **[Claim]** — [short discriminator sentence]. [Evidence sentence — what proves it]. This directly addresses [evaluation criterion or Section reference]. [Scope — "See §X.Y" or "See Figure Z" for detail].

### Examples

**Weak:**
> Our team has extensive experience in defense AI.

**Strong:**
> **Proven DDIL deployment.** Our platform has operated at [customer] for 14 months in fully disconnected mode with <$1M annual support burden — the only comparable deployment of any commercial inference platform at this scale. This addresses Section M.2.1 (operational viability in contested environments). Detail in §4.3 and Past Performance Reference #1.

**Weak:**
> We have strong past performance on DARPA programs.

**Strong:**
> **Three-program DARPA continuity.** Offeror has led three DARPA research awards in adjacent topics (MS3, CCU, Assured Autonomy) with the PI proposed for this effort, all rated Satisfactory or higher by the program managers. This provides direct topical continuity not available from new entrants. Detail in Past Performance §2.

### When the pattern breaks

- **"Differentiator without discrimination."** If the claim is something any competent offeror could also claim, it's not a discriminator. ("We use modern software engineering practices.") Remove or reframe.
- **"Proof without proof."** "As demonstrated by our team's extensive experience" is not a proof point. Extensive experience, cited as {customer, scope, outcome}, is.

---

## Pattern 3 — Action Captions

An **action caption** is the text placed *under* (not inside) a graphic, explaining not what the graphic *shows* but what it *proves*.

### Why
Graphics without action captions are decoration. Graphics with action captions are evidence.

Federal evaluators reading on skim will see the graphic and read the caption. If the caption doesn't make a scoring point, the evaluator moves on.

### Structure

An action caption has three parts:

1. **Figure number + short title** (standard document reference)
2. **What the graphic proves** (not what it illustrates)
3. **Where it's substantiated** (section reference or data source)

### Templates

**Generic:**
> *Figure N. [Title].* [One sentence asserting what the graphic proves]. [Where the underlying evidence is detailed].

### Examples

**Weak (description caption):**
> *Figure 3. System architecture.*

**Strong (action caption):**
> *Figure 3. Three-tier architecture eliminates cloud dependency.* Edge-only inference paths (green) carry all mission-critical operations; enterprise connectivity (blue) is used only for model updates, shown to be optional in §4.2. Source: deployed configuration at [customer].

**Weak:**
> *Figure 5. Timeline for delivery.*

**Strong:**
> *Figure 5. Phased delivery front-loads operational value.* Phase 1 (months 1-3) delivers the SF/PSYOP/CA adapter set committed in §3.4, with go/no-go gates at each phase boundary retaining Government control.

### Anti-patterns

- **Emoji or icons replacing text.** Captions must be readable in print and screen; no emoji in federal submissions.
- **Caption longer than 3 sentences.** If you need more, it belongs in the narrative, not the caption.
- **Caption that just names the graphic.** "Figure 3. System." Add zero information. Rewrite.
- **Caption embedded inside the graphic.** Keep captions in the Word doc text, not baked into the image.

---

## Pattern 4 — Ghosting

**Ghosting** is the practice of subtly framing your solution to highlight a competitor's weakness without naming the competitor. It is one of the most effective — and most often mishandled — win techniques in federal proposals.

### Why
Evaluators cannot explicitly compare your proposal to a specific competitor's (that's discrimination). But evaluators do hold a mental model of what "the market" offers. Ghosting shapes that mental model so the reader concludes your approach is superior without the proposal saying so.

Done well, ghosting produces Significant Strengths. Done poorly, ghosting produces Weaknesses (appears petty, attacks competitors, sounds defensive).

### When ghosting applies
- Competitive bids where you know (or reasonably infer) who else is bidding
- Where `working/competitor-assessment.md` documents a specific competitor weakness
- Where the Section M criteria would reward solving the problem that competitor fails to solve

### When ghosting does NOT apply
- Non-competitive types (RFI, Sources Sought, ROM, SBIR Phase I topic-specific)
- Merit-based review (BAA, where competition is with other research proposals — ghost the research approach, not the institution)
- When you don't have evidence the competitor actually has the weakness you're ghosting

### The rules

1. **Never name the competitor.** Ever. In any form.
2. **Never use negative framing about "others" or "the typical approach" without being specific.** "Other solutions fail" is weak; "cloud-dependent solutions fail in disconnected environments, unlike our on-device approach" is specific.
3. **Frame as a positive claim about your approach** that implicitly contrasts with the known competitor weakness.
4. **The competitor weakness must be real and verifiable.** Don't invent weaknesses.

### Templates

**Problem-framed ghost:**
> [Approaches that rely on X] create [specific risk articulated in Section C]. Our approach avoids this by [what we do differently], as shown in §Y.

**Capability-framed ghost:**
> Unlike [generic category of approach that includes the competitor], our [capability] is [specific differentiator that addresses the competitor's weakness].

### Examples

Assume competitor-assessment says the likely lead competitor requires cloud connectivity and has had well-known outages.

**Weak (naming the competitor):**
> Unlike [Competitor X], we do not require cloud connectivity.

**Weak (generic negative):**
> Many commercial AI platforms fail in contested environments.

**Weak (no proof):**
> Our approach is better than other approaches for disconnected operations.

**Strong (ghosted):**
> Solutions that require persistent cloud connectivity cannot support the DDIL operational tempo the mission requires. Our on-device inference architecture operates independent of cloud, demonstrated by our 14-month deployment at [customer] without outage impact (Past Performance Reference #1).

**Strong (ghosted via discriminator):**
> On-device inference is not a product feature — it's the architectural foundation of our platform. Alternative approaches retrofit edge inference onto cloud-native designs, carrying the cloud's reliability assumptions into environments that can't guarantee them.

### Ghosting checklist

- [ ] No competitor named, directly or by clear implication
- [ ] Your capability stated as a positive (not "we don't do what they do")
- [ ] The ghosted weakness is real and is in `working/competitor-assessment.md`
- [ ] The ghost ties to an evaluation criterion
- [ ] The ghost is subtle — a strong reader sees it, a casual reader just sees a strong positive claim

---

## How `proposal-writer` applies these patterns

For every major section, the writer should:

1. **Open with a theme statement** (Pattern 1) that previews the section's main point
2. **Include at least one discriminator proof point** (Pattern 2) in sections that map to evaluation criteria
3. **Write action captions** (Pattern 3) for every graphic referenced from the section
4. **Ghost** (Pattern 4) in sections where a known competitor weakness is in play — but only when applicable per the table above

For every section, the writer should also check:

- **Win themes from `working/proposal-plan.md`** — is this section reinforcing one of them? If yes, say so. If no, consider whether it should.
- **Compliance matrix update** — does this section cover a Req ID that should be marked Drafted?

## How `red-team-review` Gold Team checks these patterns

Gold Team's win-theme visibility check, discriminator proof-point check, and ghosting check (see `.claude/skills/red-team-review/SKILL.md`) all map directly to these patterns. If the writer applied them, Gold Team finds them present. If not, they become Weaknesses.

This is by design — the writer's job is to produce Gold-Team-pass content on the first draft, not to leave it for cleanup.
