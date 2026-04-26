# Strengths, Weaknesses, and Deficiencies — Federal Source-Selection Definitions

Authority: FAR 15.305, DoD Source Selection Procedures. These are the precise terms evaluators use and how they determine them.

## Definitions

### Strength
An aspect of an offeror's proposal that has merit or exceeds specified performance or capability requirements in a way that will be advantageous to the Government during contract performance.

**Gold Team criteria:**
- Specific (names a feature, approach, credential, or commitment)
- Advantageous (describes the benefit to the Government)
- Proposal-based (cited to a draft paragraph, not inferred)

**Examples:**
- "Offeror's proposed use of SBOM generation at build time exceeds the PWS requirement for bill-of-materials at delivery and reduces supply-chain risk throughout the lifecycle."
- "Proposed PI holds an active TS/SCI and has led three prior DARPA awards in adjacent topics; low ramp-up risk."

### Significant Strength
A strength that appreciably increases the merit of the proposal or will have a significant, measurable benefit to the Government during contract performance.

**Gold Team criteria:**
- Meets all Strength criteria
- **Appreciable** — not just better, measurably better
- Ties to an evaluation-criterion element
- Typically rare — 1-3 per factor in a strong proposal

**How to know it's Significant vs. just a Strength:**
A Significant Strength is one the evaluator would cite in a source-selection decision document as a *reason* to select this offeror. A plain Strength is noted but not decisive.

**Examples:**
- "Offeror's on-device inference architecture eliminates the cloud-dependency risk identified in the Section C problem statement, a risk that every other approach introduces."
- "Demonstrated deployment at [prior customer] of the same capability being proposed reduces technical risk to near zero and is a direct proof point for Section M factor 1."

### Weakness
A flaw in the proposal that increases the risk of unsuccessful contract performance.

**Gold Team criteria:**
- Specific (names the problem — vagueness, omission, contradiction)
- Risk-based (describes what could go wrong)
- Proposal-based (cite the paragraph or the *absence* of one)

**Examples:**
- "Proposal states the team will 'provide sufficient senior engineers as needed' but does not commit to specific labor categories, hours, or named personnel — creating staffing risk."
- "Technical approach does not address the CUI handling requirement in PWS 3.2.4; no mention of FedRAMP or NIST 800-171 compliance."

### Significant Weakness
A flaw that appreciably increases the risk of unsuccessful contract performance.

**Gold Team criteria:**
- Meets Weakness criteria
- Risk is material — could cause schedule slip, cost overrun, or performance failure
- Not correctable by minor editing

### Deficiency
A material failure of a proposal to meet a Government requirement OR a combination of significant weaknesses in a proposal that increases the risk of unsuccessful contract performance to an unacceptable level.

**Gold Team criteria:**
- A requirement is not met at all (Gap in compliance matrix)
- OR a cluster of Significant Weaknesses accumulates to unacceptable risk
- Makes the proposal **Unacceptable** for that factor

**Examples:**
- "Proposal does not include the required Small Business Participation Plan (Section L.4) — Deficiency."
- "Proposal cannot demonstrate an approach to the ATO requirement in PWS 5.1; offeror does not appear to have the security assessment capability — Deficiency."

### Uncertainty
An ambiguity or missing information in a proposal that the evaluator cannot resolve without discussions with the offeror. Uncertainties cannot be the sole basis for a Deficiency but they contribute to risk.

**Examples:**
- "Proposal cites rate of $X/hr for Senior Engineer but the cost volume shows $Y/hr for the same category — evaluator cannot determine which is proposed."

## How evaluators write these up

A typical source-selection decision document uses this structure per Strength/Weakness:

```
Factor 1, Subfactor 1.2 — [Name]

Strength: [one-sentence assertion]
  Basis: [specific paragraph/section reference]
  Benefit to Government: [what the government gets]

Significant Weakness: [one-sentence assertion]
  Basis: [specific paragraph/section reference or absence]
  Risk to Government: [what could go wrong]
```

Gold Team output should mirror this structure — short, specific, attributable.

## Common Gold Team mistakes

- **"Claim without basis"** — writing "The proposal is strong in X" without citing a specific paragraph. Not an evaluator finding; more useful as marketing.
- **"Personal preference"** — "I wish they had included a diagram here" is not a Weakness. Weakness must tie to risk or non-compliance.
- **"Stacking trivial strengths"** — counting 5 minor strengths to imply a Significant Strength. Doesn't work in real source selection; don't do it in Gold Team.
- **"Everything is a Weakness"** — Gold Team is supposed to be balanced. If you can't find any Strengths, the proposal is Unacceptable and there's no point running Gold Team — go back to the writer.
- **"Matrix-stuffing the result"** — assigning a rating before doing the Strength/Weakness analysis, then back-filling. The rating must **emerge** from the S/W/D pattern.
