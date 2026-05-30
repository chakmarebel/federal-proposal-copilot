# Proposal Style Guide

## Voice & Tone

### The six principles (apply to every proposal and white paper)

1. **Clinical, not clever.** Engineer briefing a commander, not founder pitching a VC. No hype words. No fluff — every sentence maps to a requirement or evaluation factor.
2. **Assertive, but provable.** "We deliver X" — good. "We are the leading provider of X" — useless unless directly substantiated.
3. **Structured for scoring, not reading.** Mirror the RFP/CFT section names and language. Make it easy for the evaluator to give points.
4. **Risk-reducing, not idea-generating.** Make the evaluator feel safe picking us. Emphasize execution over concepts. Show prior similar-environment use. Highlight integration over invention.
5. **Specific over broad.** Numbers, protocols, identifiers, dates, MOS codes, doctrine references. Examples that land: "Supports IL5/IL6 deployment with ATO inheritance pathways"; "Integrates with existing CDS via Kafka/REST without modifying guard policy."
6. **Measured and restrained.** The best federal proposals feel almost understated. Let facts do the talking. If a passage reads like a press release, rewrite it.

### Failure modes to avoid

- **Marketing tone:** "cutting-edge," "world-class," "innovative," "best-in-class," "next-generation," "revolutionary," "game-changing"
- **Consultant vagueness:** "leveraging best practices," "synergies," "holistic," "end-to-end solution"
- **Academic tone:** long theory blocks with no execution detail
- **Overpromising:** evaluators assume vendors under-deliver against promises; write only what is provable

### Operating defaults

- Direct, technically grounded, no filler
- Write as if the evaluator has 15 minutes and a red pen
- Lead with what's broken (problem-first), then present the solution
- Frame [Your Company] as the operational layer that connects enterprise to edge — not a replacement for anything
- Cut rhetorical lead sentences, em-dash asides in body paragraphs, bold emphasis inside body paragraphs (white paper register), and superlatives that aren't immediately substantiated
- Select the narrative operating mode from `reference/narrative-operating-modes.md` before drafting; length and vehicle determine how much explanation the prose can afford.
- Use transitions that carry meaning (consequence, selection, proof, decision), not structural announcements.
- Voice doctrine lives in `reference/PROSE-QUALITY-DOCTRINE.md`; operative drafting guidance is in `reference/editorial-voice-guide.md`.

## Register by Proposal Type

The register (formality + rhetorical style) varies by audience. Match the register to the type before drafting:

| Proposal type | Register | Key constraints |
|---|---|---|
| `white-paper` | Institutional, declarative. No rhetorical flourishes. No bold emphasis in body paragraphs. No em-dash asides (max 1 per paragraph). No italics for emphasis (italics for figure references only). | Dry, flat — Senate staff / program office framing |
| `far-rfp` / `ota-proposal` / `cso-full` | Assertive, plain. Specific and technical. Evaluation-criterion-aware. | Standard default register |
| `sbir-phase1` / `sbir-phase2` | Technical, merit-oriented. Minimize marketing language. | PI voice, not sales voice |
| `rfi` / `sources-sought` | Informational, measured. Answer the question; don't pitch. | No win-theme framing |

**White paper anti-patterns** (cut on sight):
- "Anyone telling Congress X is selling." — op-ed register, not institutional
- Bold emphasis scattered through body paragraphs
- Rhetorical em-dash asides mid-sentence
- Exclamation marks, rhetorical questions

## Word Choice
| Don't Write | Write Instead |
|-------------|---------------|
| Govt | Government |
| an inconsistent company name | the configured company name from `my-company/` (unless inside a direct quote) |
| an [Company] engineer | One [Company] engineer (article + numeral when introducing a single-source anecdote) |
| ours or Govt-provided | [Your Company] or Government-provided |
| robust, innovative, cutting-edge | [describe what it actually does] |
| leverage (as verb) | use, apply, extend |
| utilize | use |
| in order to | to |
| at this point in time | now |
| the fact that | [cut entirely] |
| $X vs. $Y (bare cost ratio) | $X vs. $Y for equivalent capability (always add hedge — see Cost Comparisons below) |
| § or §§ (the section-sign glyph) | "Section 3.2" / "Sections 3–4" — spell it out in prose. Better still, refer to the section by name ("as described in the technical approach"). Never use the § glyph in proposal narrative. |

## Cost Comparisons

Any side-by-side cost comparison **must** include "for equivalent capability" or "for comparable workload." Never publish a bare ratio.

**Wrong:** "$0/month vs. $6,000/month"
**Right:** "$0/month vs. approximately $6,000/month for equivalent capability on a commercially hosted model"

When a cost comparison relies on volume assumptions (token count, request rate, etc.), state the assumption inline: "...at 2 billion tokens per month operator volume."

## Footnotes in White Papers

Do NOT use `†` / `‡` / `*` footnote markers in white papers. Footnote apparatus signals academic format; a 3-page brief can't support it.

**Instead:** Use inline parenthetical qualifiers:
- `(per public reporting)` — for claims sourced from news/industry
- `(indirectly)` — for claims where the chain of custody isn't direct observation
- `(multi-provider)` — for claims that average across vendors
- `([Your Company] internal benchmarking)` — for first-party claims

A single `Sources:` line at the end of the document is sufficient for citation. No footnote section.

## Formatting Rules
| Rule | Standard |
|------|----------|
| Spaces after periods | Single (never double) |
| Section numbering | "5." not "5.0" |
| Acronyms | Define on first use: "subject matter expert (SME)" |
| Heading styles (FAR/OTA/SBIR) | Heading1 for sections, Heading2 for sub-sections (never manual bold on Normal) |
| Heading styles (white paper) | Title at Body/paragraph style (not Heading 1); sections at Heading 3; no subsection headings |
| Font (Word docs) | Times New Roman 12pt throughout — body, headers, footers |
| Line spacing | 1.15 or multiple at 276 (Word default) |
| Margins | 1 inch all sides |
| Page size | US Letter (8.5 x 11) |

## Document Structure
| Element | Standard |
|---------|----------|
| Header | Right-aligned: "[Your Company] — [Document Title]", centered above: "UNCLASSIFIED" |
| Footer | Left: "[Your Company] \| [Document Title]", Right: "Page X" |
| Classification | UNCLASSIFIED (or as specified) — in header and footer |
| Distribution | Statement D (DoD & DoD contractors) is the default for program submissions |
| Cover page | Standalone docx — classification, company, title, subtitle, prepared-for, date, POC, distribution |
| Figure captions | In the document text below each image, not embedded in the graphic |

## Point of Contact (POC) Fields

**Never invent a placeholder POC name.** Read `my-company/contacts.md` (or equivalent) for a real name and email. If no authoritative source exists, insert the literal marker `[POC: name + email TBD]` so the export-proposal preflight catches it.

Wrong: `Bill (contact details on request)`
Right: `[POC Name], [poc-email]` — or — `[POC: name + email TBD]`

## Section Writing Patterns

### Executive Summary (~3 paragraphs)
1. Context + strategy alignment + theater-specific hook
2. What's needed + what this paper describes
3. What [Your Company] is + how it complements existing investments

### Problem Statement / Execution Gap
- Lead with the three challenges (as bullets with bold labels)
- Each bullet: problem-first framing — what's broken, not what needs to happen
- Close with a pivot to the solution: "These challenges are interconnected. Solving all three as a unified system produces a continuously improving one."

### Capability Overview (~200 words max)
- "[Your Company] is the operational layer that connects..." — one sentence
- Three core functions as bullets
- Past performance paragraph
- Transition: "The following section describes how these capabilities address each challenge."

### Detail Sections (one per challenge)
- Each maps 1:1 to a challenge from the problem statement
- No content repeated from the overview section
- Pattern: problem context → how [Your Company] solves it → specific commitment/deliverable → closing takeaway

### Path Forward / Pilot Plan
- Pilot scope paragraph
- Delivery timeline reference (with graphic)
- Technical + operational objectives (as graphic or structured list)
- Success metric: adaptation velocity

### Conclusion (~2 paragraphs)
- Restate the opportunity (not the problem)
- Close with what the customer gains by adopting this framework

## Submission Email Pattern
- Subject: "White Paper: [Capability] for [Customer] [Use Case]"
- 60-second read maximum
- Three bullets: (1) operational now, (2) delivery commitment, (3) low barrier to pilot
- Clear ask: "Welcome the opportunity to discuss" + offer to brief
- Respectfully, [signature]
