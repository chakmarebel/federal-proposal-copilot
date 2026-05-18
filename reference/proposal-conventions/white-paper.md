---
convention_id: white-paper
display_name: White Paper / Directed Brief / Unsolicited
section_patterns: white-paper
distilled_from: Senate PRC vs. Western Open-Source Models (Apr 2026), SOCPAC white paper
---

# White Paper Proposal Conventions

Calibrated conventions for white papers. These are distilled from actual submission-versus-draft diffs — they reflect what Senate staff, program offices, and senior DoD readers actually kept, not what looks complete to a proposal writer. Apply these when `section_patterns: white-paper`.

---

## Length

| Metric | Target | Hard cap |
|---|---|---|
| Total word count | 1,200 words | 2,000 words |
| Executive summary | 200 words | 250 words |
| Each numbered body section | 150–200 words | 250 words |
| Considerations / recommendations list | 200–300 words | 400 words |
| Company Position section | 75–150 words | 200 words |

**Enforce before shipping.** If the draft exceeds 2,000 words, compress before declaring complete. Do not rely on the reviewer to cut.

**Cut criterion.** Would deleting this section change a reader's takeaway from the executive summary? If no, delete it. The architecture-R&D detail section that is "on-topic but doesn't change the recommendation" gets cut.

---

## Register

Institutional, declarative. Senate staffers and program-office readers expect a dry policy register — not an op-ed.

**Avoid:**
- Rhetorical flourishes ("Anyone telling Congress X is selling.")
- Bold emphasis scattered through body paragraphs (bold is for table column headers only)
- Em-dash editorial asides (max 1 per paragraph)
- Italics for emphasis (italics for figure references / in-text citations only)

**Use:**
- Declarative sentences with no hedging on facts you know
- Parenthetical qualifiers `(per public reporting)` for claims that are inferred, not directly observed
- Plain prose — no punchy one-liners, no kicker sentences

---

## Structure and section order

```
1. [optional] Cover / header block
2. Executive Summary (4-finding pattern — see below)
3. [Primary framing section] — e.g., "The Right Frame: Closed vs. Open"
4. [Evidence sections] — model-level / agentic / supply chain / etc.
5. [Policy considerations] — numbered, imperative voice, 1 sentence each
6. Company Position — last, after the argument has landed
```

**Self-positioning goes last.** Company-specific content goes in the dedicated Position section at the end — after the policy argument has landed. Self-positioning early reads as a pitch; self-positioning after the argument reads as a natural conclusion.

---

## Executive Summary pattern (four-finding)

The Senate-PRC draft used a four-finding structure that was kept verbatim (words tightened, structure intact):

```
**[Theme statement — what we do, why it matters, proof hook].**

1. [Finding 1 — single declarative sentence with headline number]
2. [Finding 2 — same]
3. [Finding 3 — same]
4. [Finding 4 — same]

**Bottom line:** [One sentence — the policy takeaway]
```

The `1. claim → 2. claim → 3. claim → 4. claim → Bottom line:` pattern is the durable default for white-paper executive summaries. Use it unless the customer explicitly asked for a different structure.

---

## Headline numbers

Identify 3-5 numbers that load-bear the argument. Get them right — they will be the only things readers remember.

- State them in the executive summary
- Repeat them verbatim in the relevant body section
- Qualify any number that is estimated or inferred: "approximately," "per public reporting," "(as of [month/year])"

Examples from Senate-PRC: `19 of 20`, `$0 vs. ~$6,000/month for equivalent capability`, `3.5 trillion training tokens`, `~4% RLI`.

---

## Evidence tables

- Maximum: **5 rows × 4 columns** in a < 10-page brief
- Larger evidence sets are summarized in prose with the strongest 3-5 examples cited inline
- Evidence tables are evidentiary — **no company row inside a table meant to indict the field**. The company's position goes in the Position section.
- Column headers: short noun phrases, no verbs. Bold first row only.

---

## Heading depth

| Level | Markdown source | Word output |
|---|---|---|
| Document title | Paragraph text (no `#`) | Body / Title style |
| Section headings | `### 1. Title` (H3) | Heading 3 |
| Subsection headings | Avoid in < 10-page briefs | — |

The markdown-to-docx export tool handles this demotion automatically for `proposal_type: white-paper`. Do not manually use `## H2` for white-paper section headings — it produces Heading 2 in Word, which implies major-chapter weight the format doesn't support.

---

## Footnotes

**None.** Do not use `†`, `‡`, or `*` markers.

Replace with inline parenthetical qualifiers:
- `(per public reporting)` — industry/news-sourced claim
- `(indirectly)` — chain of custody is inferred, not direct
- `(multi-provider)` — averaged across vendors
- `([Your Company] internal benchmarking)` — first-party data

A single `Sources:` line at the end of the document is sufficient for citations. No footnote section, no numbered endnotes.

---

## Policy considerations / recommendations

When a section enumerates actions for the reader (Congress, program office, customer):

- **Imperative voice**, one sentence per item
- Optional: em-dash + one-clause rationale (`1. Mandate provenance disclosure — vendors receiving federal contracts should disclose training data provenance.`)
- Do NOT add rationale paragraphs under each item
- 6 items or fewer; if more are needed, group them

---

## Point of Contact

**Never invent a placeholder.** Read `my-company/contacts.md`. If no source exists, insert `[POC: name + email TBD]` so the export-proposal preflight checklist catches it.

Correct cover-page POC format: `[POC Name], [poc-email]`

---

## Company name

Use the configured company name from `my-company/` consistently throughout — one canonical spelling, not variant forms. Inside direct quotes from other sources, preserve the original text.

---

## Cost comparisons

Any side-by-side cost comparison requires "for equivalent capability" or "for comparable workload." Never publish a bare ratio.

Also state the volume assumption when relevant: "...at 2 billion tokens per month operator volume."

---

## What works — preserve these

From the Senate-PRC submission (patterns the user kept verbatim):

- **Four-finding executive summary** — skim anchor, lands the argument in 30 seconds
- **Two-tier framing** — reframes the customer's default question before they ask it
- **Headline numbers** — 3-5 concrete, memorable, citation-ready statistics
- **Provenance audit table** — indictment-shaped (only the rows that indict), not survey-shaped (everything)
- **Company Position closer** — one-paragraph, kept short, placed after the argument
